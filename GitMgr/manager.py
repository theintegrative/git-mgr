import os
import glob
import json
from pprint import pprint
from prompt_toolkit import prompt
from git import Repo

# VARIABLES
HOME_PATH = os.path.expanduser('~')
SEARCH_PATH = HOME_PATH
MGR_PATH = f"{HOME_PATH}/git_mgr"
REPOS_PATH = f"{MGR_PATH}/repos"
CONFIG_PATH = f"{MGR_PATH}/.git_mgr"
CONFIG_FILE = f"{MGR_PATH}/config.json"
SETTINGS_FILE = f"{CONFIG_PATH}/settings.json"

## CONFIGURATION SETTINGS
def settings_json(config_path: str, search_path: str):
    return {"config_path": config_path, "search_path": search_path}

def config_json(repos=[], platforms={}):
    return {"repos": repos, "platforms": platforms}

def platform_json(alias="", sub_repos=[]):
    return {"alias": alias, "subrepos": sub_repos}

## FILE and DIRECTORY
def read_file_contents(path):
    with open(path, 'r') as f:
        return json.load(f)

def write_data_to_file(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def extend_path(base, extension):
    new_path = os.path.join(base, extension)
    os.makedirs(new_path, exist_ok=True)
    return new_path

def extend_paths(base, directory: list):
    for extension in directory:
        base = extend_path(base, extension)
    return base

def create_git_mgr_paths():
    # Ask for normal install, configfile or custom
    for path in [CONFIG_PATH, REPOS_PATH]:
        os.makedirs(path, exist_ok=True)

def create_platform_paths(config):
    # Note: Check if platforms not empty
    for platform in get_platform_names(config):
        extend_path(REPOS_PATH, platform)

def create_repository_path(link):
    platform_path = get_platform_path(link)
    repository, directory = split_repository_directory(link)
    directory_path = extend_paths(platform_path, directory)
    repository_path = os.path.join(directory_path, repository)
    return repository_path, repository

## REPO CONFIG
def create_config():
    create_git_mgr_paths()
    return config_json(get_repository_links())

def update_repoconfig(config, directory=SEARCH_PATH):
    # give feedback if updated or not
    unique_links = get_unique_links(get_repository_links(directory), config["repos"])
    return set_repos(config, unique_links)

## TEXT MANIPULATION
def rstrip_ssh(link):
    return link.rstrip("git").rstrip(".")

def lstrip_ssh(link):
    return link.lstrip("git").lstrip("@")

def strip_directory(link):
    return link.split(":")[1].split("/")

def strip_platform(link):
    return lstrip_ssh(link.split(":")[0])

def split_repository_directory(link):
    # .rstrip(".git") strips to much characters
    parts = strip_directory(rstrip_ssh(link))
    repository = parts[-1]
    directory = parts[:-1]
    return repository, directory

def get_platform_path(link):
    return os.path.join(REPOS_PATH, get_alias(strip_platform(link)))

## SETTINGS CONFIGURATION
def get_settings():
    return read_file_contents(SETTINGS_FILE)

## CONFIG CONFIGURATION
def get_config():
    return read_file_contents(CONFIG_FILE)
 
def set_repos(config, repos):
    config["repos"] = repos
    return config

def get_platforms_repos(config):
    return list(set([strip_platform(link) for link in config["repos"]]))

def get_platform_names(config):
    return config["platforms"].keys()

def set_platform(config, platform):
    # Check if platform already exist
    config["platforms"][platform] = platform_json()
    return config

def set_platforms_repos(config):
    for platform in get_platforms_repos(config):
        new_config = set_platform(config, platform)
    return new_config

def append_subrepos(config):
    for link in config["repos"]:
        platform = strip_platform(link)
        subrepos = config["platforms"][platform].setdefault("subrepos", [])
        subrepos.append(link)
        config["platforms"][platform]["subrepos"] = sorted(subrepos)
    return config

def get_alias(platform, config=get_config()):
    return config["platforms"][platform]["alias"]

def set_alias(config, platform, alias):
    config["platforms"][platform]["alias"] = alias 
    return config

def set_aliases(config):
    new_config = config
    for platform in config["platforms"]:
        alias = prompt(f'Set alias for {platform}: ')
        config["platforms"][platform]["alias"] = alias 
    return new_config

def get_subrepos(config, platform):
    return config["platforms"][platform]["subrepos"]

def get_repos(config):
    return config["repos"]

def clone_repo(link):
    repository_path, repository = create_repository_path(link)
    Repo.clone_from(link, repository_path)
    return repository

def clone_repos(config):
    for link in get_repos(config):
        print(f"Cloned repository: {clone_repo(link)}")

def get_repository_links(path=SEARCH_PATH):
    remote_urls = []
    for repo_path in glob.iglob(os.path.join(path, '**', '.git'), recursive=True):
        repo = Repo(os.path.dirname(repo_path))
        remote_urls.extend([remote.url for remote in repo.remotes])
    return get_unique_links(remote_urls)

def get_unique_links(source, target=[]):
    for url in source:
        if url not in target:
            target.append(url)
    return target

def sort_repositories(config):
    return append_subrepos(set_platforms(config))
