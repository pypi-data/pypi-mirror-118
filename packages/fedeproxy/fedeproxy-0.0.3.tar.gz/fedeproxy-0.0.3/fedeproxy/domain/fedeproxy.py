import hashlib
import os

from fedeproxy.interfaces import forge

from .identity import IdentitiesPrivate


class Fedeproxy(object):
    def __init__(self, forge_factory, url, base_directory):
        self._forge_factory = forge_factory
        self._url = url
        self._base_directory = base_directory
        self.own_forge_create()
        self.forge_create()

    def init(self):
        self.own.init()

    @property
    def url(self):
        return self._url

    @property
    def base_directory(self):
        return self._base_directory

    @property
    def forge_factory(self):
        return self._forge_factory

    @property
    def own(self):
        return self._own

    def own_forge_create(self):
        class F(FedeproxyOwnForge, self.forge_factory):
            pass

        self._own = F(self.url, self.base_directory)

    @property
    def forge(self):
        return self._forge

    def forge_create(self):
        class F(FedeproxyForge, self.forge_factory):
            pass

        self._forge = F(self.url, self.base_directory)

    def project_export(self, namespace, project):
        p = self.forge.project_create(namespace, project)
        d = self.own.own_project_create().dvcs()
        d.clone(p.name)
        p.save(d.directory)
        d.commit("exported project", "issues.json")
        d.push(p.name)
        return f"{d.directory}/issues.json"

    def save(self):
        self.own.identities.save()

        d = self.own.own_project_create().dvcs()
        d.clone(self.own.namespace)
        self.own.save(d.directory)
        d.commit("exported fedeproxy", "users.json")
        d.push(self.own.namespace)
        return d.directory

    def inbox(self, username, activity):
        u = self.own.users.get(username)
        token = None
        for i in self.own.identities.identities:
            if i.url == u.url:
                token = i.token
                break
        assert token is not None, f"No token found for {username}"
        self.forge.authenticate(token=token)
        if activity.type == "Commit":
            self.inbox_commit(username, activity)

    def inbox_commit(self, username, commit):
        d = self.forge.project_create(username, "fedeproxy").dvcs()
        branch = d.url_hashed(commit.context)
        d.clone(branch)
        d.fetch(commit.context, commit.hash)
        d.reset(branch, commit.hash)
        d.push(branch)


class FedeproxyBaseForge(forge.Forge):
    def __init__(self, url, base_directory, **kwargs):
        super().__init__(url, **kwargs)
        self._base_directory = base_directory

    @property
    def base_directory(self):
        return self._base_directory


class FedeproxyOwnForge(FedeproxyBaseForge):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._namespace = "fedeproxy"
        self._owner = "fedeproxy"

    def init(self):
        self.identities = IdentitiesPrivate(self)
        self.identities.init()

    @property
    def owner(self):
        return self._owner

    @property
    def namespace(self):
        return self._namespace

    def own_project_delete(self):
        return super().project_delete(self.namespace, "fedeproxy")

    def project_factory(self):
        class F(FedeproxyOwnProject, super().project_factory()):
            pass

        return F

    def users_factory(self):
        class F(FedeproxyOwnUsers, super().users_factory()):
            pass

        return F

    def own_project_create(self):
        return super().project_create(self.namespace, "fedeproxy")


class FedeproxyOwnUsers(forge.Users):
    def get(self, username):
        return super().get(username)

    def create(self, username, password, email):
        return super().create(username, password, email)


class FedeproxyOwnProject(forge.Project):
    def dvcs(self):
        return super().dvcs(f"{self.forge.base_directory}/fedeproxy")


class FedeproxyForge(FedeproxyBaseForge):
    def project_factory(self):
        class F(FedeproxyProject, super().project_factory()):
            pass

        return F


class FedeproxyProject(forge.Project):
    @property
    def name(self):
        return hashlib.sha256(self.http_url_to_repo.encode("ascii")).hexdigest()

    def dvcs(self):
        namespace_directory = f"{self.forge.base_directory}/{self.namespace}"
        if not os.path.exists(namespace_directory):
            os.makedirs(namespace_directory)
        return super().dvcs(f"{namespace_directory}/{self.project}")
