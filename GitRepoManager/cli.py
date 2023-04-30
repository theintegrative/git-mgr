import typer

from GitRepoManager.manager import *

app = typer.Typer()

@app.command()
def create():
    """
    Create necessary directories.
    """
    create_dirs()

@app.command()
def generate():
    """
    Generate repo lists based on config files.
    """
    generate_repolists()

@app.command()
def clone():
    """
    Clone repositories.
    """
    clone_repositories()

@app.command()
def show():
    """
    Show repositories.
    """
    show_repositories()

@app.command()
def push():
    """
    Push changes to remote repositories.
    """
    push_changes()

@app.command()
def export(file_path: str):
    """
    Export configuration to a JSON file.
    """
    export_config(file_path)

@app.command()
def import_file(file_path: str):
    """
    Import configuration from a JSON file.
    """
    import_config(file_path)

@app.command()
def create_playbook():
    """
    Create a ansible playbook with all the repositories.
    """
    create_ansible_playbook()

@app.command()
def list_repos(path: str):
    """
    List all git repositories recursively starting from this path
    """
    for repo in list_all_repositories(path):
        typer.echo(repo)
        
@app.command()
def init():
    """ 
    Intitialize directory structure and clone repo confituration
    """
    create()
    show()
    clone()


def main():
    app()
