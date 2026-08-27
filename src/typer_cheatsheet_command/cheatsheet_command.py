from __future__ import annotations

import json
from inspect import cleandoc
from dataclasses import asdict, dataclass, field
from typing import Annotated, Any, Literal

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from typer.core import TyperGroup, TyperOption
from typer.main import get_command


@dataclass(frozen=True)
class ParameterInfo:
    name: str
    kind: Literal["argument", "option"]
    required: bool
    type: str
    help: str | None = None
    options: list[str] = field(default_factory=list)
    default: Any = None
    multiple: bool = False


@dataclass(frozen=True)
class CommandInfo:
    name: str
    help: str
    hidden: bool
    parameters: list[ParameterInfo] = field(default_factory=list)
    commands: list["CommandInfo"] = field(default_factory=list)


def _json_default(value: Any) -> Any:
    try:
        json.dumps(value)
    except TypeError:
        return repr(value)
    return value


def _parameter_info(parameter) -> ParameterInfo:
    is_option = isinstance(parameter, TyperOption)
    return ParameterInfo(
        name=parameter.name or "",
        kind="option" if is_option else "argument",
        required=parameter.required,
        type=parameter.type.name,
        help=getattr(parameter, "help", None),
        options=list(parameter.opts + parameter.secondary_opts) if is_option else [],
        default=_json_default(parameter.default),
        multiple=parameter.multiple or parameter.nargs != 1,
    )


def _command_info(
    command,
    *,
    name: str,
    parent_context: typer.Context | None,
    show_all: bool,
) -> CommandInfo:
    context = typer.Context(command, info_name=name, parent=parent_context)
    children = []
    if isinstance(command, TyperGroup):
        for child_name in command.list_commands(context):
            child = command.get_command(context, child_name)
            if child is None or (child.hidden and not show_all):
                continue
            children.append(
                _command_info(
                    child,
                    name=child_name,
                    parent_context=context,
                    show_all=show_all,
                )
            )

    return CommandInfo(
        name=name,
        help=cleandoc(command.help or ""),
        hidden=command.hidden,
        parameters=[_parameter_info(parameter) for parameter in command.params],
        commands=children,
    )


def get_command_tree(app: typer.Typer, *, show_all: bool = False) -> CommandInfo:
    """Return the Typer application's command tree as serializable data."""
    command = get_command(app)
    name = app.info.name or command.name or "cli"
    return _command_info(command, name=name, parent_context=None, show_all=show_all)


def _rich_tree(command: CommandInfo, *, root: bool = False) -> Tree:
    style = "bold" if root else "bold cyan" if command.commands else "green"
    label = Text(command.name, style=style)
    if command.help and not root:
        label.append(f": {command.help}")
    tree = Tree(label, guide_style="bright_green")
    for child in command.commands:
        tree.add(_rich_tree(child))
    return tree


def register_cheatsheet_command(
    app: typer.Typer,
    command_name: str = "cheatsheet",
    description: str = "Show the command tree structure of the application.",
) -> None:
    """Register a command that displays the application's command tree."""

    @app.command(name=command_name, help=cleandoc(description))
    def cheatsheet(
        show_all: Annotated[
            bool, typer.Option("--show-all", help="Include hidden commands.")
        ] = False,
        output: Annotated[
            Literal["tree", "json"],
            typer.Option("--output", "-o", help="Output format."),
        ] = "tree",
    ) -> None:
        command_tree = get_command_tree(app, show_all=show_all)
        if output == "json":
            typer.echo(
                json.dumps(
                    {"schema_version": "1", "command": asdict(command_tree)},
                    ensure_ascii=False,
                )
            )
            return

        Console().print(
            Panel(
                _rich_tree(command_tree, root=True),
                title="Cheatsheet",
                title_align="left",
            )
        )
