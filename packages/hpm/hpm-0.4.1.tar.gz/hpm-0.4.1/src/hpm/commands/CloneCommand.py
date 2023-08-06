import os
import subprocess
from argparse import Namespace
from typing import List
from rich import print
from rich.box import DOUBLE_EDGE
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from .. import api
from ..api import get_subgroups, get_group_projects
from ..namespaces import get_namespace_id
from .._typing import Command, Parameter, Group
from .._printing import print_command_header


def generate_group_list(root: Group, recursive=True) -> dict:
    """Generate group project dict

    Args:
        group (Group): Root group

    Returns:
        dict: Group projects dict
    """
    return {
        "id": root.id,
        "name": root.name,
        "projects": get_group_projects(root),
        "subgroups": generate_subgroup_list(root) if recursive else [],
    }


def generate_subgroup_list(parent: Group) -> List[Group]:
    """Generate a list with all subgroup of a provided group with projects included

    Args:
        parent (Group): Parent group

    Returns:
        List[Group]: Subgroup list
    """
    res = []
    subs = get_subgroups(parent)

    if subs is None or len(subs) == 0:
        return res

    for s in subs:
        res.append(
            {
                "id": s.id,
                "name": s.name,
                "projects": get_group_projects(s),
                "subgroups": generate_subgroup_list(s),
            }
        )

    return res


class CloneCommand(Command):
    """Clone command fro groups"""

    def __init__(self, name: str, help: str) -> None:
        """Create a new clone command

        Args:
            name (str): Name in argparse
            help (str): Help in argparse
        """
        super(CloneCommand, self).__init__(
            name,
            help,
            params=[
                Parameter(
                    name="group_name",
                    help="Group name to clone project from",
                ),
                Parameter(
                    name="--recursive",
                    help="Includes all subgroup recursively",
                    action="store_true",
                ),
            ],
        )

    def execute(self, args: Namespace) -> None:
        """Clone recursively all the projects located in the provided group

        Args:
            args (Namespace): Must contains `group_name`
        """
        console = Console()

        if not args.group_name:
            print("Group name not provided")
            return

        print_command_header("clone")

        group_id = get_namespace_id(args.group_name)

        if group_id == -1:
            print("Group not found")
            return

        root_group = api.get_group(group_id)

        if root_group is None:
            return

        all_projects = generate_group_list(root_group, recursive=args.recursive)

        def clone_recursive_group_projects(parent):
            for p in parent["projects"]:
                os.mkdir(p.path_with_namespace)
                subprocess.run(["git", "clone", "-q", p.ssh_url_to_repo])

            for s in parent["subgroups"]:
                clone_recursive_group_projects(s)

        with console.status("[bold green]🧬 Cloning projects...") as status:
            clone_recursive_group_projects(all_projects)

        print(
            Panel(
                Text(
                    "Projects was successfully clonned.\nThanks for using hpm !",
                    justify="center",
                ),
                box=DOUBLE_EDGE,
                border_style="bright_cyan",
                padding=(1, 2),
                expand=False,
            )
        )
