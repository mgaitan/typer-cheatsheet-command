import typer

from .cheatsheet_command import register_cheatsheet_command


app = typer.Typer(name="typer-cheatsheet-demo", help="demo")

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

# Register the cheatsheet command
register_cheatsheet_command(app)

if __name__ == "__main__":
    app()
