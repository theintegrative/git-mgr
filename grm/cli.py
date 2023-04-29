import typer

from grm.manager import *

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
    create_ansible_playbook()

def main():
    app()
