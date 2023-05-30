import os
import glob
import json
from pprint import pprint
from prompt_toolkit import prompt
from git import Repo

REPO_CONFIG_FILE = "repoconfig.json"
REPO_CONFIG_PATH = "/home/theintegrative/git-repo-manager/test/git-repo/"
SEARCH_PATH = os.path.expanduser('~')

def read_file_contents(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def write_data_to_file(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def create_path(extension):
    base_path = os.getcwd()
    extended_path = os.path.join(base_path, extension)
    os.makedirs(extended_path, exist_ok=True)
    return extended_path

## REPO CONFIG
def create_repoconfig(directory, repoconfig=REPO_CONFIG_FILE):
    directory_links = get_repository_links(directory)
    write_data_to_file(repoconfig, {"links": directory_links})
    print(f"Created {repoconfig}")

def update_repoconfig(directory, repoconfig=REPO_CONFIG_FILE):
    directory_links = get_repository_links(directory)
    repoconfig_links = read_file_contents(repoconfig)["links"]
    write_data_to_file(repoconfig, {"links": get_unique_links(directory_links, repoconfig_links)})

def init_repoconfig(directory, repoconfig=REPO_CONFIG_FILE):
    if not os.path.exists(repoconfig):
        create_repoconfig(directory, repoconfig)
    repoconfig_setup(repoconfig)

## STRIPPING
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
    directories = parts[:-1]
    return repository, directories

def get_alias(platform, repoconfig=REPO_CONFIG_FILE):
    return read_file_contents(repoconfig)["platforms"][platform]["alias"]

## SETUP
def repoconfig_setup(repoconfig=REPO_CONFIG_FILE):
    repoconfig_file = read_file_contents(repoconfig)
    if repoconfig_file["links"] == []:
        update_repoconfig(SEARCH_PATH)
        sort_repositories()
        set_aliases()
    elif repoconfig_file.get("platforms") == None:
        sort_repositories()
        set_aliases()
    elif repoconfig_file["platforms"] == []:
        set_aliases()
        for link in repoconfig["platforms"].keys():
            if not get_alias(strip_platform(link), repoconfig):
                set_aliases()

def clone_repos(repoconfig=REPO_CONFIG_FILE):
    init_repoconfig(SEARCH_PATH)
    repoconfig_file = read_file_contents(repoconfig)
    for link in repoconfig_file["links"]:
        current_path = create_path(get_alias(strip_platform(link)))
        repository, directories = split_repository_directory(link)
        for subdir in directories:
            current_path = os.path.join(current_path, subdir)
            os.makedirs(current_path, exist_ok=True)
        repo_path = os.path.join(current_path, repository)
        Repo.clone_from(link, repo_path)
        print(f"Repository '{repository}' cloned successfully.")
    print("Folders and repositories created successfully.")

#clone_repos("repoconfig.json")
def get_repository_links(directory):
    remote_urls = []
    for repo_path in glob.iglob(os.path.join(directory, '**', '.git'), recursive=True):
        repo = Repo(os.path.dirname(repo_path))
        remote_urls.extend([remote.url for remote in repo.remotes])
    return get_unique_links(remote_urls)

def get_unique_links(source, target=[]):
    for url in source:
        if url not in target:
            target.append(url)
    return target

def sort_repositories(repoconfig=REPO_CONFIG_FILE):
    repoconfig_file = read_file_contents(repoconfig)
    repoconfig_file["platforms"] = {}
    repoconfig_platforms = list(set([strip_platform(link) for link in repoconfig_file["links"]]))
    for platform in repoconfig_platforms:
        repoconfig_file["platforms"][platform] = {"alias": "", "repos": []}
        for link in repoconfig_file["links"]:
            if platform == strip_platform(link):
                repoconfig_file["platforms"][platform]["repos"].append(link)
    write_data_to_file(repoconfig, repoconfig_file)

def set_aliases(repoconfig=REPO_CONFIG_FILE):
    repoconfig_file = read_file_contents(repoconfig)
    for platform in repoconfig_file["platforms"]:
        answer = prompt(f'Set alias for {platform}: ')
        repoconfig_file["platforms"][platform]["alias"] = answer
        print(f'Alias for {platform} set to: {repoconfig_file["platforms"][platform]["alias"]}')
    write_data_to_file(repoconfig, repoconfig_file)

#sort_repositories()
#set_aliases()
#update_repo_config("/home/theintegrative/", "test2.json")
clone_repos()
