from argparse import Namespace
import pathlib
from .._typing import Command, Parameter
import yaml
from yaml.loader import SafeLoader


class SetupCommand(Command):
    """Setup command"""

    def __init__(self, name: str, help: str) -> None:
        """Create a new setup command

        Args:
            name (str): Name in argparse
            help (str): Help in argparse
        """
        super(SetupCommand, self).__init__(
            name,
            help,
            params=[
                Parameter(name="--token", help="Store API token"),
                Parameter(
                    name="--target",
                    help="Target uri for the chooseng gitlab instance. E.g. : https://gitlab.example.com/api/v4",
                ),
            ],
        )

    def execute(self, args: Namespace, location: str = "../config.yaml") -> None:
        """Setup the user API token

        Args:
            args (Namespace): Must contains `token`

        Raises:
            Exception: No token provided
        """
        if not args.token and not args.target:
            print(
                "Command `setup` require one of those arguments `--token` and `--target`."
            )
            raise Exception("No token or target provided")

        try:
            with open(pathlib.Path(__file__).resolve().parent.absolute() / location, "r") as f:
                current_conf = yaml.load(f, Loader=SafeLoader)

            state = current_conf
        except FileNotFoundError:
            state = None

        with open(
            pathlib.Path(__file__).resolve().parent.absolute() / location, "w+"
        ) as f:
            token = args.token
            target = args.target

            # Only when config file isn't created yet
            if not state:
                if not target:
                    target = "https://gitedu.hesge.ch/api/v4"
                state = {}

            if token is not None:
                state["token"] = token
            if target is not None:
                state["target"] = target

            f.write(yaml.dump(state))
