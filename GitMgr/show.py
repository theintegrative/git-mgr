import typer
from GitMgr.manager import *
from pprint import pprint

app = typer.Typer()

@app.command()
def platforms():
    """
    Show platforms
    """
    for platform in get_platform_names(get_config()):
        print(platform)

@app.command()
def all():
    """
    Show all repos
    """
    for repo in get_repos(get_config()):
        print(repo)

@app.command()
def subrepos(platform):
    """
    Show sub repos
    """
    for repo in get_subrepos(get_config(), platform):
        print(repo)

@app.command()
def settings():
    """
    Show settings
    """
    pprint(get_settings())

@app.command()
def config():
    """
    Show config    
    """
    pprint(get_config())

if __name__ == "__main__":
    app()
