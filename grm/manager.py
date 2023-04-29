import os
import re
import json
import typer
import git
import concurrent.futures


CONFIG_PATH = "./git/repoconfig.json"
directories = [f"./git/{org}/{loc}" for org in ["hub", "lab"] for loc in ["int", "ext"]]

def create_dirs():
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def generate_repolists():
    repos = {}
    for directory in directories:
        repos[directory] = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == 'config':
                    path = os.path.join(root, file)
                    with open(path, 'r') as f:
                        content = f.read()
                        match = re.search(r'git@[^@]*\.com:[^:]+/[^/]+', content)
                        if match:
                            url = match.group(0)
                            url = re.sub(r'\s+fetch\s*=.*', '', url)
                            repos[directory].append(url)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(repos, f, indent=4)

def clone_repositories():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        with open(CONFIG_PATH, 'r') as f:
            repos = json.load(f)
            for directory, urls in repos.items():
                for url in urls:
                    executor.submit(clone_repository, directory, url)

def clone_repository(directory, url):
    os.system(f"cd {directory} && git clone --quiet {url}")

def check_repoconfig_file(func):
    def wrapper(*args, **kwargs):
        if not os.path.isfile(CONFIG_PATH):
            typer.echo("The repoconfig.json file does not exist. Please run the 'create' command to generate it.")
            return
        with open(CONFIG_PATH, 'r') as f:
            repos = json.load(f)
            if not repos:
                typer.echo("The repoconfig.json file is empty.")
                return
        for directory in repos:
            for url in repos[directory]:
                repo_dirname = os.path.basename(url)
                if not os.path.exists(repo_dirname):
                    continue
                repo = git.Repo(repo_dirname)
                for remote in repo.remotes:
                    for remote_url in remote.urls:
                        if remote_url.endswith('.git'):
                            remote_url = remote_url[:-4]
                        if url not in remote_url:
                            typer.echo(f"Repository {url} in {directory} is not listed in the repoconfig file.")
        return func(*args, **kwargs)
    return wrapper

def add_missing_repositories():
    with open(CONFIG_PATH, 'r') as f:
        repos = json.load(f)
    for directory in directories:
        if not os.path.exists(directory):
            continue
        repo = git.Repo(directory)
        for remote in repo.remotes:
            for url in remote.urls:
                if url.endswith('.git'):
                    url = url[:-4]
                if url not in repos.get(directory, []):
                    typer.echo(f"Adding repository {url} in {directory} to the repoconfig file.")
                    repos.setdefault(directory, []).append(url)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(repos, f, indent=4)

@check_repoconfig_file
def show_repositories():
    if not os.path.isfile(CONFIG_PATH):
        typer.echo("The repoconfig.json file does not exist. Please run the 'create' command to generate it.")
        return
    with open(CONFIG_PATH, 'r') as f:
        repos = json.load(f)
        if not repos:
            typer.echo("The repoconfig.json file is empty.")
            add_missing_repositories()
            typer.echo("Repositories added to repoconfig.json file.")
            return
        for directory, urls in repos.items():
            typer.echo(f"\n{directory}:")
            for url in urls:
                typer.echo(f" - {url}")

def push_changes():
    repo = git.Repo(os.getcwd())
    if repo.is_dirty(untracked_files=True):
        repo.git.add(".")
        repo.index.commit("Automatic commit")
        origin = repo.remote(name="origin")
        origin.push()
        typer.echo("Changes pushed to remote repository.")
    else:
        typer.echo("No changes to push.")

def export_config(file_path: str):
    data = {}
    for directory in directories:
        data[directory] = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == 'config':
                    path = os.path.join(root, file)
                    with open(path, 'r') as f:
                        content = f.read()
                        match = re.search(r'git@[^@]*\.com:[^:]+/[^/]+', content)
                        if match:
                            url = match.group(0)
                            url = re.sub(r'\s+fetch\s*=.*', '', url)
                            data[directory].append(url)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

@check_repoconfig_file
def import_config(file_path: str):
    with open(file_path, 'r') as f:
        data = json.load(f)
        for directory, urls in data.items():
            for url in urls:
                clone_repository(directory, url)
    typer.echo("Repositories imported successfully.")
