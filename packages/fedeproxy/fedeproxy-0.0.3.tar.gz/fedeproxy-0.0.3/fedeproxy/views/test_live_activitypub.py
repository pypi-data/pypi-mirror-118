import os
import tempfile
from unittest.mock import patch

import requests
from django.conf import settings
from django.test import override_settings
from rest_framework.test import APILiveServerTestCase

from fedeproxy.architecture.forge.gitea import Gitea

from ..activitypub import Follow
from ..activitypub.client import Post
from ..domain.fedeproxy import Fedeproxy
from ..domain.identity import IdentityPrivate


class ActivityPubTests(APILiveServerTestCase):
    project = "fedeproxy"
    password = "Wrobyak4"

    def setUp(self):
        self.f = Fedeproxy(
            forge_factory=settings.FEDEPROXY_FORGE_FACTORY,
            url=settings.FEDEPROXY_FORGE_URL,
            base_directory=settings.FEDEPROXY_FORGE_DIRECTORY,
        )

        forge = self.f.own
        self.username = forge.owner
        self.cleanup()
        email = f"{self.username}@example.com"
        u = forge.users.create(self.username, self.password, email)
        forge.authenticate(username=forge.owner, password=self.password)
        forge.project_create(self.username, self.project)

        self.f.init()

        self.i = IdentityPrivate(url=u.url)
        self.i.create_key()
        self.f.own.identities.identities.append(self.i)

        self.f.save()

    def tearDown(self):
        self.cleanup()

    def cleanup(self):
        forge = self.f.own
        forge.authenticate(username="root", password="Wrobyak4")
        forge.project_delete(self.username, self.project)
        forge.users.delete(self.username)


tmpdir_user = tempfile.TemporaryDirectory()


@override_settings(
    FEDEPROXY_FORGE_FACTORY=Gitea,
    FEDEPROXY_FORGE_URL=f"http://{os.environ.get('MY_IP', '0.0.0.0')}:8781",
    FEDEPROXY_FORGE_DIRECTORY=tmpdir_user.name,
    DEBUG=True,
)
class UserTests(ActivityPubTests):
    def test_user(self):
        id = f"{self.live_server_url}/user/{self.username}"
        response = requests.get(id)
        response.raise_for_status()
        assert response.json()["type"] == "Person"
        assert response.json()["id"] == id


tmpdir_inbox = tempfile.TemporaryDirectory()


@override_settings(
    FEDEPROXY_FORGE_FACTORY=Gitea,
    FEDEPROXY_FORGE_URL=f"http://{os.environ.get('MY_IP', '0.0.0.0')}:8781",
    FEDEPROXY_FORGE_DIRECTORY=tmpdir_inbox.name,
    DEBUG=True,
)
@patch("fedeproxy.domain.fedeproxy.Fedeproxy.inbox")
class InboxTests(ActivityPubTests):
    def test_inbox(self, inbox):
        f = Follow(
            id="https://test.com/user/follow/id",
            actor="follower_id",
            object="followee_id",
        )
        url = f"{self.live_server_url}/user/{self.username}/inbox"

        response = requests.post(url, json=f.to_dict())
        assert "No Signature header found" in response.text
        assert response.status_code == 400

        client = Post(key_username=self.username, key_private=self.i.private, key_url=self.live_server_url)
        response = client.post(url, json=f.to_dict())
        assert response.status_code == 200
