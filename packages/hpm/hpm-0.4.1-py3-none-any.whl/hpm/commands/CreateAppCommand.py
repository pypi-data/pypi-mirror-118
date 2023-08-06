import subprocess
import os
from argparse import Namespace
from rich import print
from rich.box import DOUBLE_EDGE
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from .._typing import Command
from ..questions.project import QUESTIONS
from .. import api
from ..errors import APIError
from .._printing import print_command_header, del_last_line, print_ssh_key_warning_message


class CreateAppCommand(Command):
    """Create app command"""

    def execute(self, args: Namespace) -> None:
        """Create a new project

        Args:
            args (Namespace): Not used
        """
        console = Console()

        # @see: https://github.com/kefranabg/readme-md-generator for good cli use guidance
        print_command_header("create-app")
        print_ssh_key_warning_message()

        for question in QUESTIONS:
            tmp_res = None
            prompt = (
                f"[green]?[/green] [bright_white]{question.message}[/bright_white] "
            )
            default_indication = f"[dim italic]({question.default})[/dim italic] "

            if question.default != "":
                prompt += default_indication

            # Prompt the question
            tmp_res = console.input(prompt)

            # Set the default value as current value when not provided
            if question.default != "" and tmp_res == "":
                prompt = prompt.replace(default_indication, "")
                tmp_res = question.default

            # Validate the user input
            question.set_response(tmp_res)
            while not question.validate(question.response):
                del_last_line()
                tmp_res = console.input(f"{prompt}[red1]({question.help})[/red1] ")
                question.set_response(tmp_res)

            # Remove default indication prompt when entered a valid input
            if tmp_res != "":
                prompt = prompt.replace(default_indication, "")

            del_last_line()
            print(f"{prompt}[cyan]{question.response}[/cyan]")

            # Transform the response if needed for the api
            if question.transform != None:
                question.transform(tmp_res)

        # Create the api params list
        api_params = []
        for q in QUESTIONS:
            api_params.append({"key": q.name, "value": q.response, "non_api": q.non_api})

        try:
            new_project = api.create_project(api_params)

            if new_project is None:
                return

            with console.status("[bold green]🦊 Making local project..."):
                # Create local directory (at location where command as been ran)
                os.mkdir(new_project.path)
                os.chdir(new_project.path)
                subprocess.call(["git", "init"], stdout=open(os.devnull, 'wb'))

                # Get user input for remote type
                remote_type = next((item for item in api_params if item["key"] == "remote_type"), None)
                if remote_type is not None:
                    remote_type = remote_type["value"]

                # Setup remote
                subprocess.call(["git", "remote", "add", "origin", new_project.ssh_url_to_repo], stdout=open(os.devnull, 'wb')) # Default remote as ssh

                # Pull existing readme
                readme = next((item for item in api_params if item["key"] == "initialize_with_readme"), None)
                if readme is not None:
                    subprocess.call(["git", "pull", "--quiet", "origin", "main"], stdout=open(os.devnull, 'wb'))

            print("✅ Project created")
            print()
            print(
                f"👀 View the created project on [link {new_project.web_url}]{new_project.web_url} !"
            )
            print()
            print(
                Panel(
                    Text(
                        "Project was successfully created.\nThanks for using hpm !",
                        justify="center",
                    ),
                    box=DOUBLE_EDGE,
                    border_style="bright_cyan",
                    padding=(1, 2),
                    expand=False,
                )
            )
            print()
        except APIError as e:
            print(e.message)
