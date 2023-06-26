import click

from dashboard.themes.themes import (
    DARK_THEMES,
    darkly_theme,
    flatly_theme,
    pulse_theme,
    sandstone_theme,
    slate_theme,
    solar_theme,
    spacelab_theme,
)

from .app import setup

@click.command()
@click.option(
    "--ui-theme",
    help="Activate UI theme",
    required=False,
    default="flatly",
    show_default=True,
    type=click.Choice(
        [
            darkly_theme.name,
            flatly_theme.name,
            pulse_theme.name,
            sandstone_theme.name,
            slate_theme.name,
            solar_theme.name,
            spacelab_theme.name,
        ]
    ),
)
@click.option("--debug", "-d", is_flag=True, help="Activate Dash debug tools")
def main(ui_theme: str, debug: bool):

    app = setup(ui_theme=ui_theme, debug=debug)
    # this import is placed here because dash is dealing with
    # cyclic dependencies and we want the setup to be complete, before importing the layout
    from .index import main_layout

    app.layout = main_layout
    app.run_server(debug=debug)

if __name__ == "__main__":
    main()