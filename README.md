# Git Repo Manager

This is a command-line tool for managing a set of git repositories. It can clone repositories, generate a list of repositories, add missing repositories to the list, show the list of repositories, and push changes to the repositories.

## Requirements

To use this tool, you need to have the following dependencies installed:

- `Python3`
- `typer`
- `PyGithub`
- `ansible` (optional)

### Installation

First clone this repository:
```
git clone https://github.com/theintegrative/git-repo-manager.git
```

To install using setup.py, run:
```
pip install .
```

### Usage

Once you have created the repoconfig.json file, you can use the other commands to manage your repositories.
- `clone`: 		Clone repositories.
- `create`:         	Create necessary directories.
- `create-playbook`:    Create a ansible playbook with all the repositories.
- `export`:         	Export configuration to a JSON file.
- `generate`:       	Generate repo lists based on config files.
- `import-file`:    	Import configuration from a JSON file.
- `init`:           	Intitialize directory structure and clone repo confituration
- `list-repos`:     	List all git repositories recursively starting from this path.
- `push`:           	Push changes to remote repositories.
- `show`:           	Show repositories.
