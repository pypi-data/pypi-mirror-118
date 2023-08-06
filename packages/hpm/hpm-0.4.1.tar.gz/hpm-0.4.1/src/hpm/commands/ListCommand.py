from argparse import Namespace
from rich import print
from rich.columns import Columns
from rich.console import Console, Group, group
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from .. import api
from .._typing import Command
from .._printing import (
    clr_scr,
    print_command_header
)
from ..namespaces import create_namespace_tree


class ListCommand(Command):
    """List all user's projects"""

    def _generate_project_tree(self, namespace: dict, tree: Tree = None) -> None:
        """Print the project list

        Args:
            namespace (dict): Current namespace
            tree (Tree): Tree to build
        """
        if tree is None:
            tree = Tree(
                f'[link {namespace["url"]}][bold cyan]{namespace["name"]}[/bold cyan][/link {namespace["url"]}]'
            )
        else:
            tree = tree.add(
                f'[link {namespace["url"]}][bold cyan]{namespace["name"]}[/bold cyan][/link {namespace["url"]}]'
            )

        # Recursivly print the children
        for c in namespace["children"]:
            self._generate_project_tree(c, tree=tree)

        # Print the projects list
        for i, p in enumerate(namespace["projects"]):
            tree.add(
                f"{p.name} :glowing_star:{p.star_count} :name_badge:{p.open_issues_count}"
            )

        return tree

    def execute(self, args: Namespace) -> None:
        """List all the project

        Args:
            args (Namespace): Not used
        """
        page = 1
        prev_page = 0
        co = ""
        console = Console()

        # Emulate a `do {...} while()`
        while True:
            clr_scr()
            print_command_header("list")

            # Only call the api if the pages have changed
            if prev_page != page:
                groups = api.get_owned_groups()
                owned_projects = api.get_owned_projects(page)

                if groups is None or owned_projects is None:
                    return

                groups = sorted(groups, key=lambda k: k.full_path)
                headers = owned_projects["headers"]
                group_projects = owned_projects["list"]

            prev_page = "<" if (headers["X-Prev-Page"] != "") else ""
            next_page = ">" if (headers["X-Next-Page"] != "") else ""

            roots = []
            for root in create_namespace_tree(groups, group_projects):
                roots.append(Panel(self._generate_project_tree(root)))

            # Format navigation menu
            navigation = Group(
                Panel(
                    Group(
                        Text.assemble(
                            ("Page", "bright_white"),
                            f": {prev_page} ",
                            (str(page), "bright_white"),
                            "/",
                            (headers["X-Total-Pages"], "bright_white"),
                            f"{next_page}",
                            justify="center",
                        ),
                        Text.assemble(
                            ("Navigation", "bright_white"),
                            ": Previous (",
                            ("p", "green"),
                            ") | Next (",
                            ("n", "green"),
                            ") | Close (",
                            ("c", "red1"),
                            ") | ",
                            justify="center",
                        ),
                    )
                )
            )

            # Print
            print(Columns(roots))
            print(navigation)

            co = console.input("[bold magenta]Action: [/bold magenta]")

            # List commands
            if co == "c":
                break
            elif co == "p":
                if headers["X-Prev-Page"] != "":
                    prev_page = page
                    page = headers["X-Prev-Page"]
            elif co == "n":
                if headers["X-Next-Page"] != "":
                    prev_page = page
                    page = headers["X-Next-Page"]
            else:
                prev_page = page
                continue

            # `do {...} while()` condition
            if co == "c":
                break
