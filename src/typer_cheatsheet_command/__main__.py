"""Demo application for the Typer Cheatsheet Command package."""

import typer

from .cheatsheet_command import register_cheatsheet_command

app = typer.Typer(name="typer-cheatsheet-demo", help="demo")

users_app = typer.Typer(help="Manage users in the system.")


@users_app.command("add")
def add_user(username: str) -> None:
    """Add a new user."""
    print(f"Adding user: {username}")


@users_app.command("delete")
def delete_user(username: str) -> None:
    """Delete an existing user."""
    print(f"Deleting user: {username}")


app.add_typer(users_app, name="users")


@app.command()
def generate_report(month: str) -> None:
    """Generate a monthly report."""
    print(f"Generating report for {month}...")


@app.command()
def configure() -> None:
    """Configure application settings."""
    print("Configuring application...")


register_cheatsheet_command(app)


def main() -> None:
    """Run the demo application."""
    app()


if __name__ == "__main__":
    main()
