# Git Repo Manager

This is a simple command line tool for managing Git repositories.

## Installation

1. Clone the repository:
```shell
git clone https://github.com/theintegrative/git-repo-manager.git
```
2. Install the required packages by running `pip install -r requirements.txt`

## Usage

The following commands are available:

- `create`: Creates the required directories for cloning repositories
- `generate`: Generates repolists for all directories
- `clone`: Clones all repositories in parallel
- `show`: Shows all repositories in each repolist
- `export`: Export directory structure and repolist information as JSON
- `import_file`: Import directory structure and repolist information from JSON
- `push`: Pushes changes to git repo manager repository

Example usage:

```bash
# Create directories
python git_repo_manager.py create

# Generate repolists
python git_repo_manager.py generate

# Clone repositories
python git_repo_manager.py clone

# Show repositories
python git_repo_manager.py show

# Export config to file
python git_repo_manager.py export config.json

# Import config from file
python git_repo_manager.py import_file config.json

# Push changes
python git_repo_manager.py push
```
