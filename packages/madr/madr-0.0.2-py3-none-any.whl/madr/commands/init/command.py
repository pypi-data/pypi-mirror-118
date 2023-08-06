from os import remove
from glob import iglob
from argparse import ArgumentParser, Namespace
from pathlib import Path
from shutil import copytree

from madr.cli import command


def init(args: Namespace) -> None:
    init_template_path = Path(__file__).parent / "template"
    copytree(init_template_path, args.path, dirs_exist_ok=True)
    for placeholder in iglob(str(args.path / "**/.empty"), recursive=True):
        remove(placeholder)


@command
def init_parser(subparsers):
    init_parser: ArgumentParser = subparsers.add_parser(
        "init",
        description="Create a new MADR project",
    )
    init_parser.add_argument(
        "path",
        help="Filesystem path to create the MADR project in",
        type=Path,
    )

    init_parser.set_defaults(func=init)
