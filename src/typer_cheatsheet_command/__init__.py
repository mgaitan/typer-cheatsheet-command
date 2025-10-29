
from typing import Annotated

from rich.console import Console
from rich.tree import Tree
import typer


app = typer.Typer(help="demo")

users_app = typer.Typer(help="Manage users in the system.")

@users_app.command("add")
def add_user(username: str):
    """Adds a new user."""
    print(f"Adding user: {username}")

@users_app.command("delete")
def delete_user(username: str):
    """Deletes an existing user."""
    print(f"Deleting user: {username}")

app.add_typer(users_app, name="users")

@app.command()
def generate_report(month: str):
    """
    Generates a monthly report.
    """
    print(f"Generating report for {month}...")

@app.command()
def configure():
    """
    Configure application settings.
    """
    print("Configuring application...")

@app.command()
def cheatsheet(show_all: Annotated[bool, typer.Option("--show-all", help="Include hidden commands")] = False):
    """
    Show the command tree structure.
    """
    console = Console()
    tree = Tree("[bold]typer-cheatsheet-command[/bold]", guide_style="bright_green")

    def add_subcommands(typer_app, tree_node):
        for command in typer_app.registered_commands:
            if command.hidden and not show_all:
                continue
            command_name = command.name or command.callback.__name__.replace("_", "-")
            command_help = command.short_help or (command.callback.__doc__ or "").strip().split("\n")[0]
            tree_node.add(f"[green]{command_name}[/green]: {command_help}")

        for sub_typer in typer_app.registered_groups:
            if isinstance(sub_typer.name, typer.models.DefaultPlaceholder):
                add_subcommands(sub_typer.typer_instance, tree_node)
            else:
                sub_node = tree_node.add(f"[bold cyan]{sub_typer.name}[/bold cyan]")
                add_subcommands(sub_typer.typer_instance, sub_node)

    add_subcommands(app, tree)
    console.print(tree)
