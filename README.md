# Typer Cheatsheet Command

A pluggable `cheatsheet` command for your Typer applications to visualize their command tree structure.

This library provides a `cheatsheet` subcommand that you can easily integrate into any existing Typer application. It automatically inspects your Typer application and its subcommands/groups to generate a clear, tree-like representation, making it easier for users to understand available commands.

## Installation

You can install this command directly from GitHub using `uv`

```bash
uv add git+https://github.com/mgaitan/typer-cheatsheet-command.git
```

### As a standalone application (Demo)

You can run the demo application included in this repository to see the `cheatsheet` command in action:

```bash
uv run --from=git+https://github.com/mgaitan/typer-cheatsheet-command.git -m typer_cheatsheet_command -- cheatsheet
```

This will output a tree structure of the demo (dummy) application's commands:

```
╭─ Cheatsheet ───────────────────────────────────────────────────────────────╮
│ typer-cheatsheet-demo                                                      │
│ ├── generate-report: Generates a monthly report.                           │
│ ├── configure: Configure application settings.                             │
│ ├── cheatsheet: Show the command tree structure for typer-cheatsheet-demo  │
│ └── users                                                                  │
│     ├── add: Adds a new user.                                              │
│     └── delete: Deletes an existing user.                                  │
╰────────────────────────────────────────────────────────────────────────────╯
```

You can also include hidden commands with the `--show-all` option:

```bash
uv run --from=git+https://github.com/mgaitan/typer-cheatsheet-command.git -m typer_cheatsheet_command -- cheatsheet --show-all
```

### Integrating into your Typer application

To add the `cheatsheet` command to your own Typer application, simply import the `register_cheatsheet_command` function and call it with your `typer.Typer` instance.

First, ensure `typer-cheatsheet-command` is installed in your project's environment.

Then, in your main application file (e.g., `main.py`):

```python
# main.py
import typer
from typer_cheatsheet_command.cheatsheet_command import register_cheatsheet_command

app = typer.Typer(name="MyCoolApp", help="A cool command-line application.")

@app.command()
def hello(name: str = "World"):
    """Say hello to someone."""
    print(f"Hello {name}!")

users_app = typer.Typer(help="Manage users.")
@users_app.command("create")
def create_user(username: str):
    """Creates a new user."""
    print(f"Creating user {username}")

app.add_typer(users_app, name="users")

# Register the cheatsheet command
register_cheatsheet_command(app)

if __name__ == "__main__":
    app()
```

Now, when you run your application, the `cheatsheet` command will be available:

```bash
uv run main.py cheatsheet
```

This would produce an output similar to:

```
╭─ Cheatsheet ───────────────────────────────────────────────────────────────╮
│ MyCoolApp                                                                  │
│ ├── hello: Say hello to someone.                                           │
│ ├── cheatsheet: Show the command tree structure of the application.        │
│ └── users: Manage users.                                                   │
│     └── create: Creates a new user.                                        │
╰────────────────────────────────────────────────────────────────────────────╯
```

By default, the command is registered as `cheatsheet`. If you want to use a different name for the subcommand, you can set it explicitly

```python
register_cheatsheet_command(app, command_name="cheat")
```
