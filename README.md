# Git Repo Manager

This is a command-line tool for managing a set of git repositories. It can clone repositories, generate a list of repositories, add missing repositories to the list, show the list of repositories, and push changes to the repositories.

## Requirements

To use this tool, you need to have the following dependencies installed:

- Python 3
- `typer`
- `PyGithub`
- `ansible` (optional)

### Installation

First clone this repository:
```
git clone git clone https://github.com/theintegrative/git-repo-manager.git
```

To install using setup.py, clone the repository and run:
```
python setup.py install
```

### Usage
To use the tool, you first need to create a repoconfig.json file that lists the repositories you want to manage. You can do this using the generate command:

- generate: Generate a repoconfig.json file that lists the repositories you want to manage.

Once you have created the repoconfig.json file, you can use the other commands to manage your repositories.

- clone: Clone all the repositories listed in the repoconfig.json file.
- show: Show the list of repositories listed in the repoconfig.json file.
- push: Push changes to all the repositories listed in the repoconfig.json file.
- export: Export the list of repositories to a file.
- import: Import a list of repositories from a file.
- ansible: Create an Ansible playbook to deploy the repositories.
