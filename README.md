# Github README

## Introduction

This project provides a command-line tool for managing multiple GitHub repositories. The `grm` tool can create directories, generate repository lists, clone repositories, show repositories, push changes to remote repositories, export configurations to a JSON file, and import configurations from a JSON file. Additionally, the tool provides the option to create an Ansible playbook.

## Requirements

To use this tool, you need to have the following dependencies installed:

- Python 3
- `typer`
- `PyGithub`
- `ansible` (optional)

## Installation

You can install this tool using pip:

```
pip install git+https://github.com/<username>/<repository>.git
```

## Usage

To use the `grm` tool, run the following commands:

- `grm create`: Creates necessary directories.
- `grm generate`: Generates repo lists based on config files.
- `grm clone`: Clones repositories.
- `grm show`: Shows repositories.
- `grm push`: Pushes changes to remote repositories.
- `grm export`: Exports configuration to a JSON file.
- `grm import`: Imports configuration from a JSON file.
- `grm create_playbook`: Creates an Ansible playbook.

## Examples

To create necessary directories:

```
grm create
```

To generate repository lists based on config files:

```
grm generate
```

To clone repositories:

```
grm clone
```

To show repositories:

```
grm show
```

To push changes to remote repositories:

```
grm push
```

To export configuration to a JSON file:

```
grm export /path/to/config.json
```

To import configuration from a JSON file:

```
grm import /path/to/config.json
```

To create an Ansible playbook:

```
grm create_playbook
```
