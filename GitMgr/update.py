import typer
from GitMgr.manager import *

app = typer.Typer()

@app.command()
def all(path=CONFIG_FILE):
    """
    Update config
    """
    config = update_repoconfig(get_config(), directory=SEARCH_PATH)
    write_data_to_file(path, config)

if __name__ == "__main__":
    app()
