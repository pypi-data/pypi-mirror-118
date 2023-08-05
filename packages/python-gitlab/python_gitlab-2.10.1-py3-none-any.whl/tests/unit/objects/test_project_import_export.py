"""
GitLab API: https://docs.gitlab.com/ce/api/project_import_export.html
"""
import pytest
import responses


@pytest.fixture
def resp_import_project():
    content = {
        "id": 1,
        "description": None,
        "name": "api-project",
        "name_with_namespace": "Administrator / api-project",
        "path": "api-project",
        "path_with_namespace": "root/api-project",
        "created_at": "2018-02-13T09:05:58.023Z",
        "import_status": "scheduled",
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/import",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_import_status():
    content = {
        "id": 1,
        "description": "Itaque perspiciatis minima aspernatur corporis consequatur.",
        "name": "Gitlab Test",
        "name_with_namespace": "Gitlab Org / Gitlab Test",
        "path": "gitlab-test",
        "path_with_namespace": "gitlab-org/gitlab-test",
        "created_at": "2017-08-29T04:36:44.383Z",
        "import_status": "finished",
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/import",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_import_github():
    content = {
        "id": 27,
        "name": "my-repo",
        "full_path": "/root/my-repo",
        "full_name": "Administrator / my-repo",
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/import/github",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_import_project(gl, resp_import_project):
    project_import = gl.projects.import_project("file", "api-project")
    assert project_import["import_status"] == "scheduled"


def test_refresh_project_import_status(project, resp_import_status):
    project_import = project.imports.get()
    project_import.refresh()
    assert project_import.import_status == "finished"


def test_import_github(gl, resp_import_github):
    base_path = "/root"
    name = "my-repo"
    ret = gl.projects.import_github("githubkey", 1234, base_path, name)
    assert isinstance(ret, dict)
    assert ret["name"] == name
    assert ret["full_path"] == "/".join((base_path, name))
    assert ret["full_name"].endswith(name)


def test_create_project_export(project, resp_export):
    export = project.exports.create()
    assert export.message == "202 Accepted"


def test_refresh_project_export_status(project, resp_export):
    export = project.exports.create()
    export.refresh()
    assert export.export_status == "finished"


def test_download_project_export(project, resp_export, binary_content):
    export = project.exports.create()
    download = export.download()
    assert isinstance(download, bytes)
    assert download == binary_content
