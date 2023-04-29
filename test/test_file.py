import os
import json
import git
import pytest
from unittest import mock
from io import StringIO

from grm import create_dirs, generate_repolists, clone_repositories, clone_repository, check_repoconfig_file, add_missing_repositories, show_repositories, push_changes, export_config, import_config

@pytest.fixture
def mocked_config_path(tmp_path):
    config_path = tmp_path / "git" / "repoconfig.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    return str(config_path)


def test_create_dirs(tmp_path):
    directories = [f"{tmp_path}/git/{org}/{loc}" for org in ["hub", "lab"] for loc in ["int", "ext"]]
    create_dirs()
    for directory in directories:
        assert os.path.exists(directory)


def test_generate_repolists(tmp_path, mocked_config_path):
    with mock.patch('builtins.open', mock.mock_open(read_data='git@github.com:myorg/myrepo.git\n')) as mock_file:
        generate_repolists()
    with open(mocked_config_path, 'r') as f:
        repos = json.load(f)
        assert repos == {f"{tmp_path}/git/hub/int": ["git@github.com:myorg/myrepo"], f"{tmp_path}/git/hub/ext": [], f"{tmp_path}/git/lab/int": [], f"{tmp_path}/git/lab/ext": []}


def test_clone_repositories(tmp_path, mocked_config_path):
    os.makedirs(f"{tmp_path}/git/hub/int", exist_ok=True)
    with open(mocked_config_path, 'w') as f:
        json.dump({f"{tmp_path}/git/hub/int": ["git@github.com:myorg/myrepo"]}, f)
    clone_repositories()
    assert os.path.exists(f"{tmp_path}/git/hub/int/myrepo")


def test_clone_repository(tmp_path):
    os.makedirs(f"{tmp_path}/git/hub/int", exist_ok=True)
    url = "git@github.com:myorg/myrepo.git"
    clone_repository(f"{tmp_path}/git/hub/int", url)
    assert os.path.exists(f"{tmp_path}/git/hub/int/myrepo")


def test_check_repoconfig_file(tmp_path, mocked_config_path):
    with open(mocked_config_path, 'w') as f:
        json.dump({f"{tmp_path}/git/hub/int": ["git@github.com:myorg/myrepo"]}, f)
    with mock.patch('sys.stdout', new=StringIO()) as mock_stdout:
        show_repositories()
        assert mock_stdout.getvalue() == "\n./git/hub/int:\n - git@github.com:myorg/myrepo\n"
    with mock.patch('builtins.input', side_effect=["yes"]):
        with mock.patch('sys.stdout', new=StringIO()) as mock_stdout:
            check_repoconfig_file(lambda x: None)()
            assert mock_stdout.getvalue() == "Changes pushed to remote repository.\n"
    with mock.patch('builtins.input', side_effect=["no"]):
        with mock.patch('sys.stdout', new=StringIO()) as mock_stdout:
            check_repoconfig_file(lambda x: None)()
            assert mock_stdout.getvalue() == ""

def test_add_missing_repositories(tmp_path, mocked_config_path):
    with open(mocked_config_path, 'r') as f:
        repos = json.load(f)
    assert repos == {f"{tmp_path}/git/hub/int": ["git@github.com:myorg/myrepo"], f"{tmp_path}/git/hub/ext": [], f"{tmp_path}/git/lab/int": [], f"{tmp_path}/git/lab/ext": []}

def test_show_repositories(tmp_path, mocked_config_path):
    with open(mocked_config_path, 'w') as f:
        json.dump({f"{tmp_path}/git/hub/int": ["git@github.com:myorg/myrepo"]}, f)
    with mock.patch('sys.stdout', new=StringIO()) as mock_stdout:
        show_repositories()
    assert mock_stdout.getvalue() == "\n./git/hub/int:\n - git@github.com:myorg/myrepo\n"

def test_push_changes(tmp_path, mocked_config_path):
    os.makedirs(f"{tmp_path}/git/hub/int", exist_ok=True)
    with open(mocked_config_path, 'w') as f:
        json.dump({f"{tmp_path}/git/hub/int": ["git@github.com:myorg/myrepo"]}, f)
    with git.Repo.init(f"{tmp_path}/git/hub/int/myrepo") as repo:
        with open(f"{tmp_path}/git/hub/int/myrepo/test.txt", 'w') as f:
            f.write("test")
        repo.index.add(["test.txt"])
        repo.index.commit("Added test file")
    push_changes()
    with open(mocked_config_path, 'r') as f:
        repos = json.load(f)
    assert repos == {f"{tmp_path}/git/hub/int": ["git@github.com:myorg/myrepo"]}

def test_export_config(tmp_path, mocked_config_path):
    os.makedirs(f"{tmp_path}/git/hub/int", exist_ok=True)
    with open(mocked_config_path, 'w') as f:
        json.dump({f"{tmp_path}/git/hub/int": ["git@github.com:myorg/myrepo"]}, f)
    export_config(f"{tmp_path}/config.json")
    with open(f"{tmp_path}/config.json", 'r') as f:
        config = json.load(f)
    assert config == {f"{tmp_path}/git/hub/int": ["git@github.com:myorg/myrepo"]}

def test_import_config(tmp_path, mocked_config_path):
    os.makedirs(f"{tmp_path}/git/hub/int", exist_ok=True)
    with open(f"{tmp_path}/config.json", 'w') as f:
        json.dump({f"{tmp_path}/git/hub/int": ["git@github.com:myorg/myrepo"]}, f)
    import_config(f"{tmp_path}/config.json")
    with open(mocked_config_path, 'r') as f:
        repos = json.load(f)
    assert repos == {f"{tmp_path}/git/hub/int": ["git@github.com:myorg/myrepo"]}
