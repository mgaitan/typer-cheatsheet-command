# Typer Cheatsheet Command

A pluggable `cheatsheet` command for Typer applications to visualize their command tree structure.

This library provides a `cheatsheet` subcommand that you can easily integrate into any existing Typer application. It automatically inspects your Typer application and its subcommands/groups to generate a clear, tree-like representation, making it easier for users to understand available commands.

## Installation

You can install this command directly from GitHub using `uv` (or `pip`):

```bash
uv pip install git+https://github.com/mgaitan/typer-cheatsheet-command.git
```

## Usage

### As a standalone application (Demo)

You can run the demo application included in this repository to see the `cheatsheet` command in action:

```bash
uv run --from=git+https://github.com/mgaitan/typer-cheatsheet-command.git -m typer_cheatsheet_command -- cheatsheet
```

This will output a tree structure of the demo application's commands:

```
typer-cheatsheet-command
├── users: Manage users in the system.
│   ├── add: Adds a new user.
│   └── delete: Deletes an existing user.
├── generate-report: Generates a monthly report.
├── configure: Configure application settings.
└── cheatsheet: Show the command tree structure of the application.
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
python main.py cheatsheet
```

This would produce an output similar to:

```
MyCoolApp
├── hello: Say hello to someone.
├── users: Manage users.
│   └── create: Creates a new user.
└── cheatsheet: Show the command tree structure of the application.
```

### Customizing the subcommand name

By default, the command is registered as `cheatsheet`. If you want to use a different name for the subcommand, you can modify the `register_cheatsheet_command` function or use `app.add_command` manually.

However, the provided `register_cheatsheet_command` function is designed to register the command directly. If you need a different name, you would typically define your own function based on the `cheatsheet_command` logic or directly use `app.command(name="my-custom-name")` with the `cheatsheet` command's callback.

For advanced customization, you could copy the `cheatsheet` command's internal logic and register it with `app.command(name="your-custom-name")`.

```python
# main.py
import typer
from typer_cheatsheet_command.cheatsheet_command import cheatsheet_command_callback # assuming we expose the internal callback

app = typer.Typer(name="MyCoolApp", help="A cool command-line application.")

# ... your other commands ...

# Registering with a custom name
@app.command(name="map")
def custom_cheatsheet_command(show_all: bool = typer.Option(False, "--show-all", help="Include hidden commands")):
    """Show the command tree structure with a custom name."""
    # The cheatsheet_command_callback would need to be adapted to accept the app instance
    # For now, stick to `register_cheatsheet_command` which takes the app instance.
    # To rename it, you'd generally copy the logic or modify the library.

    # A simpler approach for renaming if the library only exposed the function:
    # app.command(name="map")(cheatsheet_command_callback)
    # This example requires exposing the internal `cheatsheet` function and passing `app`
    # However, the current `register_cheatsheet_command` is the intended way.
    pass # This section is illustrative, the current API uses register_cheatsheet_command(app)
```

The `register_cheatsheet_command(app)` function currently registers the command as `cheatsheet`. To truly customize the name without modifying the library, you would need to either:

1.  Modify the `cheatsheet_command.py` to allow passing the `name` argument to `app.command()`.
2.  Manually copy the `cheatsheet` function's logic into your app and decorate it with `@app.command(name="your-desired-name")`.

For now, the intended way is to use `register_cheatsheet_command(app)`, which adds it as `cheatsheet`. If a strong need for renaming arises without touching the source, a future version could expose a parameter for it in `register_cheatsheet_command`.