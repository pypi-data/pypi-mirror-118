import os

import pytest

from .activitypub import ActivityPub
from .fedeproxy import Fedeproxy
from .identity import IdentityPrivate


def test_fedeproxy_init(tmpdir, make_user, make_project, password, forge_factory):
    (Forge, url) = forge_factory
    f = Fedeproxy(Forge, url, tmpdir)

    make_user(f.own, f.own.owner)
    f.own.authenticate(username=f.own.owner, password=password)
    make_project(f.own, f.own.namespace, "fedeproxy")

    f.init()

    assert isinstance(f.own, Forge)
    assert isinstance(f.forge, Forge)


@pytest.mark.forges(["GitLab"])
def test_fedeproxy_export(fedeproxy):
    pathname = fedeproxy.project_export(fedeproxy.forge.username, "testproject")
    assert os.path.exists(pathname)


def test_fedeproxy_save(fedeproxy):
    pathname = fedeproxy.save()
    for what in ("users", "identities"):
        assert os.path.exists(f"{pathname}/{what}.json")


def test_fedeproxy_inbox(fedeproxy, testuser, password, make_user, make_project, dvcs_factory):
    if not fedeproxy.own.is_dvcs_supported(dvcs_factory[0]):
        pytest.skip(f"{dvcs_factory[0].__name__} is not supported by {fedeproxy.forge_factory.__name__}")
    from fedeproxy.architecture.dvcs.hg import Hg

    if dvcs_factory[0] == Hg:
        pytest.skip("hg not supported just yet")
    (DVCS, repository) = dvcs_factory
    #
    # fedeproxy project of testuser
    #
    fedeproxy.forge.authenticate(username=testuser, password=password)
    make_project(fedeproxy.forge, testuser, "fedeproxy")
    testuser_project = fedeproxy.forge.project_create(testuser, "fedeproxy")
    testuser_dvcs = testuser_project.dvcs()
    assert testuser_dvcs.clone("testbranch") is True
    repository(testuser_dvcs.directory).populate().commit()
    testuser_dvcs.push("testbranch")
    #
    # create otheruser
    #
    otheruser = "otheruser"
    make_user(fedeproxy.forge, otheruser)
    fedeproxy.forge.authenticate(username=otheruser, password=password)
    make_project(fedeproxy.forge, otheruser, "fedeproxy")
    #
    # dump the fedeproxy state
    #
    for username in (testuser, otheruser):
        u = fedeproxy.own.users.get(username)
        fedeproxy.own.authenticate(username=username, password=password)
        i = IdentityPrivate(
            url=u.url,
            token=fedeproxy.own.get_token(),
        )
        i.create_key()
        fedeproxy.own.identities.identities.append(i)
    fedeproxy.save()
    #
    # notify otheruser the latest activity from testuser
    #
    activity = ActivityPub().commit_get(testuser_dvcs.directory)
    fedeproxy.inbox(otheruser, activity)
    #
    # check that otheruser now knows about the activity of testuser
    #
    otheruser_dvcs = fedeproxy.forge.project_create(otheruser, "fedeproxy").dvcs()
    otheruser_dvcs.clone(testuser_dvcs.url_hashed(activity.context))
    assert otheruser_dvcs.hash == testuser_dvcs.hash
