import os

import pytest
import requests

#
# forge.Forge
#


def test_authenticate(forge):
    (Forge, url) = (type(forge), forge.url)
    forgeA = Forge(url)
    forgeA.authenticate(username="root", password="Wrobyak4")
    assert forgeA.users.get("root") is not None
    forgeB = Forge(url)
    forgeB.authenticate(token=forgeA.get_token())
    assert forgeB.users.get("root") is not None


@pytest.mark.forges(["Gitea"])
def test_gitea_is_dvcs_supported_true(forge):
    from ..dvcs.git import Git

    assert forge.is_dvcs_supported(Git) is True


@pytest.mark.forges(["GitLab"])
def test_gitlab_is_dvcs_supported_true(forge):
    from ..dvcs.git import Git
    from ..dvcs.hg import Hg

    assert forge.is_dvcs_supported(Git) is True
    assert forge.is_dvcs_supported(Hg) is True


def test_is_dvcs_supported_false(forge):
    assert forge.is_dvcs_supported("unknown") is False


#
# forge.Project
#


def test_project_create(forge, make_user, password):
    username = "testuser1"
    make_user(forge, username)
    forge.authenticate(username=username, password=password)

    forge.project_delete(username, "testproject")
    assert forge.project_get(username, "testproject") is None
    p = forge.project_create(username, "testproject")
    assert p.project == "testproject"
    assert p.id == forge.project_create(username, "testproject").id
    assert forge.project_delete(username, "testproject") is True
    assert forge.project_delete(username, "testproject") is False


@pytest.mark.forges(["GitLab"])
def test_project_save(tmpdir, forge, make_user, password, make_project):
    username = "testuser1"
    make_user(forge, username)

    forge.authenticate(username=username, password=password)
    p = make_project(forge, username, "testproject")
    p.issues.create("ISSUE ONE")
    p.issues.create("ISSUE TWO")
    p.save(tmpdir)
    assert p.load(tmpdir) == 2


@pytest.mark.forges(["GitLab"])
def test_project_dvcs(tmpdir, forge, make_user, password, make_project):
    username = "testuser1"
    make_user(forge, username)

    forge.authenticate(username=username, password=password)
    p = make_project(forge, username, "testproject")

    directory = f"{tmpdir}/somewhere"
    d = p.dvcs(directory)
    assert not os.path.exists(d.directory)
    assert d.clone("master") is True
    assert os.path.exists(d.directory)


#
# forge.Users & forge.User
#


def test_users_save(tmpdir, forge, make_user):
    username = "testuser1"
    make_user(forge, username)

    assert forge.save(tmpdir) == len(list(forge.users.list()))
    assert forge.load(tmpdir) == len(list(forge.users.list()))


def test_user_create(forge):
    forge.authenticate(username="root", password="Wrobyak4")
    username = "testuser1"
    email = "testuser1@example.com"
    password = "Wrobyak4"
    forge.users.delete(username)
    u = forge.users.create(username, password, email)
    assert u.url == forge.users.create(username, password, email).url
    assert any([x.username == username for x in forge.users.list()])
    forge.authenticate(username=username, password=password)
    forge.authenticate(username="root", password="Wrobyak4")
    assert forge.users.delete(username) is True
    assert forge.users.get(username) is None
    assert forge.users.delete(username) is False


def test_user_get(forge):
    forge.authenticate(username="root", password="Wrobyak4")

    password = "Wrobyak4"

    username1 = "testuser1"
    email1 = "testuser1@example.com"
    forge.users.delete(username1)
    forge.users.create(username1, password, email1)

    username2 = "testuser2"
    email2 = "testuser2@example.com"
    forge.users.delete(username2)
    forge.users.create(username2, password, email2)

    #
    # As an admin, the email of all users is exposed
    #
    u = forge.users.get(username1)
    assert u.emails == [email1]

    #
    # When authenticated as a user, its email is exposed
    #
    forge.authenticate(username=username1, password=password)
    u = forge.users.get(username1)
    assert u.emails == [email1]

    #
    # When authenticated as an unprivileged user, its email is unknown
    # and is either not returned at all or replaced by a placeholder
    # that is different from the real email
    #
    forge.authenticate(username=username2, password=password)
    u = forge.users.get(username1)
    assert u.emails == [] or u.emails[0] != email1

    forge.authenticate(username="root", password="Wrobyak4")
    assert forge.users.delete(username1) is True
    assert forge.users.delete(username2) is True


def test_user_url(forge):
    forge.authenticate(username="root", password="Wrobyak4")
    username = "testuser1"
    email = "testuser1@example.com"
    password = "Wrobyak4"
    forge.users.delete(username)
    u = forge.users.create(username, password, email)
    assert u.username == username
    r = requests.get(u.url)
    r.raise_for_status()


#
# forge.Milestones & forge.Milestone
#


def test_milestone_create(forge, make_user, password, make_project):
    from ...interfaces.forge import Milestone

    username = "testuser1"
    make_user(forge, username)

    forge.authenticate(username=username, password=password)
    p = make_project(forge, username, "testproject")

    milestones = list(p.milestones.list())
    assert not milestones and len(milestones) == 0

    title = "THE TITLE"
    i = p.milestones.create(title)
    assert i.id == p.milestones.get(i.id).id
    milestones = list(p.milestones.list())
    assert milestones and len(milestones) == 1 and milestones[0].id == i.id
    assert isinstance(milestones[0], Milestone)
    assert p.milestones.delete(i.id) is True
    assert not list(p.milestones.list())
    assert p.milestones.get(i.id) is None
    assert p.milestones.delete(i.id) is False


#
# forge.Issues & forge.Issue
#


@pytest.mark.forges(["GitLab"])
def test_issue_create(forge, make_user, password, make_project):
    username = "testuser1"
    make_user(forge, username)

    forge.authenticate(username=username, password=password)
    p = make_project(forge, username, "testproject")

    title = "THE TITLE"
    i = p.issues.create(title)
    assert i.id == p.issues.get(i.id).id
    for x in p.issues.list():
        assert x.id == i.id
    assert p.issues.delete(i.id) is True
    assert p.issues.get(i.id) is None
    assert p.issues.delete(i.id) is False


@pytest.mark.forges(["GitLab"])
def test_issue_save(tmpdir, forge, make_user, password, make_project):
    username = "testuser1"
    make_user(forge, username)

    forge.authenticate(username=username, password=password)
    p = make_project(forge, username, "testproject")

    title = "THE TITLE"
    p.issues.create(title)
    save_path = f"{tmpdir}/issue.json"
    p.issues.save(save_path)
    assert p.issues.load(save_path) == 1
