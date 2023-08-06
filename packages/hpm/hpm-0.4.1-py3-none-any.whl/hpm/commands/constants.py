from typing import List
from .._typing import Command
from .SetupCommand import SetupCommand
from .ListCommand import ListCommand
from .CreateAppCommand import CreateAppCommand
from .CloneCommand import CloneCommand

COMMANDS: List[Command] = [
    CreateAppCommand("create-app", "Create a new project."),
    ListCommand("list", "List all your projects."),
    SetupCommand("setup", "Save API token."),
    CloneCommand("clone", "Clone all group's projects"),
]