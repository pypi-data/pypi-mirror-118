from django.urls import reverse
from rest_framework.test import APIClient

from ..domain.activitypub import ActivityPub
from ..domain.fedeproxy import Fedeproxy
from ..domain.identity import IdentityPrivate, IdentityPublic


def test_user(tmpdir, settings, make_user, make_project, password, forge_factory):
    (settings.FEDEPROXY_FORGE_FACTORY, settings.FEDEPROXY_FORGE_URL) = forge_factory
    settings.FEDEPROXY_FORGE_DIRECTORY = str(tmpdir)
    f = Fedeproxy(
        forge_factory=settings.FEDEPROXY_FORGE_FACTORY,
        url=settings.FEDEPROXY_FORGE_URL,
        base_directory=settings.FEDEPROXY_FORGE_DIRECTORY,
    )

    u = make_user(f.own, f.own.owner)
    f.own.authenticate(username=f.own.owner, password=password)
    make_project(f.own, f.own.namespace, "fedeproxy")

    f.init()

    i = IdentityPublic(url=u.url)
    i.create_key()
    f.own.identities.identities.append(i)

    f.save()

    username = f.own.owner
    url = reverse("user", args=[username])
    client = APIClient()
    response = client.get(url)
    assert response.status_code == 200
    user = response.json()
    owner = user["publicKey"]["owner"]
    assert owner.endswith(username)
    assert user["publicKey"]["publicKeyPem"].startswith("-----BEGIN PUBLIC KEY-----")


def wiptest_commit(mocker, tmpdir, settings, make_user, make_project, password, forge_factory):
    mocker.patch("fedeproxy.views.activitypub.verified_signature_active", return_value=False)
    (settings.FEDEPROXY_FORGE_FACTORY, settings.FEDEPROXY_FORGE_URL) = forge_factory
    settings.FEDEPROXY_FORGE_DIRECTORY = str(tmpdir)
    f = Fedeproxy(
        forge_factory=settings.FEDEPROXY_FORGE_FACTORY,
        url=settings.FEDEPROXY_FORGE_URL,
        base_directory=settings.FEDEPROXY_FORGE_DIRECTORY,
    )

    o = make_user(f.own, f.own.owner)
    f.own.authenticate(username=f.own.owner, password=password)
    o_token = f.own.get_token()
    make_project(f.own, f.own.namespace, "fedeproxy")

    f.init()

    i = IdentityPrivate(
        url=o.url,
        token=o_token,
    )
    i.create_key()
    f.own.identities.identities.append(i)

    username1 = "testuser1"
    username2 = "testuser2"
    for username in (username1, username2):
        u = make_user(f.own, username)
        f.own.authenticate(username=username, password=password)
        i = IdentityPrivate(
            url=u.url,
            token=f.own.get_token(),
        )
        i.create_key()
        f.own.identities.identities.append(i)
        make_project(f.own, username, "fedeproxy")

    f.save()

    client = APIClient()
    #
    # Get username1 last activity as a Commit
    #
    f.forge.authenticate(username=username1, password=password)
    dvcs1 = f.forge.project_create(username1, "fedeproxy").dvcs()
    assert dvcs1.clone("master") is True
    activity = ActivityPub().commit_get(dvcs1.directory)
    print(activity.to_dict())
    #
    # Let username2 know about username1 last activity
    #
    f.forge.authenticate(username=username2, password=password)
    dvcs2 = f.forge.project_create(username2, "fedeproxy").dvcs()
    assert dvcs2.clone("master") is True
    url = reverse("inbox", args=[username2])
    response = client.post(url, data=activity.to_dict(), format="json")
    assert response.content == "abc"
    assert response.status_code == 200
    assert dvcs2.clone(dvcs1.url_hashed)
    assert dvcs1.hash == dvcs2.hash
