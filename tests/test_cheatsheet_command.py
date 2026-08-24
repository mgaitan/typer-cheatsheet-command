import json

import typer
from typer.testing import CliRunner

from typer_cheatsheet_command import get_command_tree, register_cheatsheet_command


def make_app():
    app = typer.Typer(name="example")
    users = typer.Typer(help="Manage users.")

    @app.command()
    def hello(name: str, formal: bool = False):
        """Say hello."""

    @app.command(hidden=True)
    def secret():
        """A hidden command."""

    @users.command("create")
    def create_user(username: str):
        """Create a user."""

    app.add_typer(users, name="users")
    register_cheatsheet_command(app)
    return app


def test_get_command_tree_uses_click_command_structure():
    tree = get_command_tree(make_app())

    assert tree.name == "example"
    commands = {command.name: command for command in tree.commands}
    assert list(commands) == ["hello", "cheatsheet", "users"]
    assert commands["hello"].help == "Say hello."
    assert [parameter.name for parameter in commands["hello"].parameters] == [
        "name",
        "formal",
    ]
    assert commands["users"].commands[0].name == "create"


def test_hidden_commands_are_opt_in():
    app = make_app()

    assert "secret" not in [command.name for command in get_command_tree(app).commands]
    assert "secret" in [
        command.name for command in get_command_tree(app, show_all=True).commands
    ]


def test_cheatsheet_renders_tree():
    result = CliRunner().invoke(make_app(), ["cheatsheet"])

    assert result.exit_code == 0
    assert "example" in result.stdout
    assert "users" in result.stdout
    assert "create: Create a user." in result.stdout


def test_cheatsheet_outputs_versioned_json():
    result = CliRunner().invoke(make_app(), ["cheatsheet", "--output", "json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "1"
    assert payload["command"]["name"] == "example"
    commands = {command["name"]: command for command in payload["command"]["commands"]}
    assert commands["hello"]["parameters"][0] == {
        "name": "name",
        "kind": "argument",
        "required": True,
        "type": "str",
        "help": None,
        "options": [],
        "default": None,
        "multiple": False,
    }


def test_custom_command_name():
    app = typer.Typer(name="example")

    @app.command()
    def hello():
        """Say hello."""

    register_cheatsheet_command(app, command_name="commands")

    result = CliRunner().invoke(app, ["commands"])

    assert result.exit_code == 0
