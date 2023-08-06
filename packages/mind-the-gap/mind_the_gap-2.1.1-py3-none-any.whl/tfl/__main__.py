try:
    import typer
except ImportError as import_error:
    raise ImportError(
        "You don't have Typer installed, "
        "install this package with the [cli] extra:\n"
        "pip install mind-the-gap[cli]"
    ) from import_error

from tfl.cli import cycles, tube

app = typer.Typer()
app.add_typer(cycles.app, name="cycles")
app.add_typer(tube.app, name="tube")

if __name__ == "__main__":
    app()
