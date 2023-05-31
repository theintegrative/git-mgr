import typer
import GitMgr.show as show
import GitMgr.update as update
from GitMgr.manager import *

app = typer.Typer()

@app.command()
def clone():
    """
    Clone repositories from configuration
    """
    clone_repos(get_config())

app.add_typer(update.app, name="update", help="Update configurations")
app.add_typer(show.app, name="show", help="Show configurations")

if __name__ == "__main__":
    app()
