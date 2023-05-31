import typer
import GitMgr.repos as repos
from GitMgr.manager import *

app = typer.Typer()

app.add_typer(repos.app, name="repos", help="Manage repositories")

@app.command()
def show(path=os.getcwd()):
    """
    Show all repositories recursively on path
    """
    for link in get_repository_links(path):
        print(link)

@app.command()
def init():
    """ 
    Intitialize git manager
    """
    config = append_subrepos(set_aliases(set_platforms_repos(create_config())))
    write_data_to_file(CONFIG_FILE, config)
    clone_repos(get_config())
    
def main():
    app()
