from typing import Annotated

from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel
import typer
import typer.models


def register_cheatsheet_command(app: typer.Typer, command_name: str = "cheatsheet"):
    """
    Registers the 'cheatsheet' command to the provided Typer application.
    """

    @app.command(
        name=command_name,
        help="Show the command tree structure of the application."
    )
    def cheatsheet(
        show_all: Annotated[
            bool,
            typer.Option("--show-all", help="Include hidden commands")
        ] = False
    ):
        """
        Show the command tree structure for the current Typer application.
        """
        console = Console()
        # Dynamically get the app's name. Use "Typer Application" as a fallback.
        app_name = app.info.name if app.info and app.info.name else "Typer Application"
        tree = Tree(f"[bold]{app_name}[/bold]", guide_style="bright_green")

        def add_subcommands(typer_app: typer.Typer, tree_node: Tree):
            # Add commands
            for command in typer_app.registered_commands:
                if command.hidden and not show_all:
                    continue
                command_name = command.name or command.callback.__name__.replace("_", "-")
                command_help = command.short_help   or (command.callback.__doc__ or "").strip().split("\n")[0]
                tree_node.add(f"[green]{command_name}[/green]: {command_help}")

            # Add sub-applications (groups)
            for sub_group in typer_app.registered_groups:
                # sub_group is of type typer.models.TyperGroup
                group_name = sub_group.name
                group_typer_instance = sub_group.typer_instance

                if group_name:
                    sub_node = tree_node.add(f"[bold cyan]{group_name}[/bold cyan]")
                    add_subcommands(group_typer_instance, sub_node)
                else:
                    # This case should ideally not happen if groups are explicitly named,
                    # but if an unnamed group is encountered, we'll just add its commands
                    # directly to the current tree_node.
                    add_subcommands(group_typer_instance, tree_node)


        add_subcommands(app, tree) # Start recursion with the main app
        console.print(Panel(tree, title="Cheatsheet", title_align="left"))
