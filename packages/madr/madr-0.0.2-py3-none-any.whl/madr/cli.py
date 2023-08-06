from argparse import ArgumentParser
from pkgutil import walk_packages
from typing import Callable

from . import commands


COMMANDS: list[Callable] = []


def command(func: Callable):
    COMMANDS.append(func)
    return func


def register_commands():
    commands_path = commands.__path__
    mod_infos = walk_packages(commands_path, f"{commands.__name__}.")
    for __, name, __ in mod_infos:
        __import__(name, fromlist=["_trash"])


def load_commands(cli: ArgumentParser):
    subparsers = cli.add_subparsers()
    for command in COMMANDS:
        command(subparsers)


def run():
    cli = ArgumentParser(
        "madr",
        description="A command line interface for managing your MADR repo",
    )
    register_commands()
    load_commands(cli)
    args = cli.parse_args()
    args.func(args)
