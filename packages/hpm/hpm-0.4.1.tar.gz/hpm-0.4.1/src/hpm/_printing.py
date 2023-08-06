import os
import platform
import sys
from datetime import datetime
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text

CURSOR_UP_ONE = "\x1b[1A"
ERASE_LINE = "\x1b[2K"


def print_command_header(command: str):
    """Global header

    Args:
        command (str): Executed command
    """
    print(
        Panel(
            Columns(
                [
                    Text("Made By Tanguy Cavagna with 💖", style="italic"),
                    Text(
                        datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
                        justify="right",
                        style="italic",
                    ),
                ],
                expand=True,
                title="[bold bright_white]HES-SO[/bold bright_white] - [bold red1]HEPIA[/bold red1]",
            ),
            border_style="bright_white",
            title=f"Command: [orange_red1]{command}[/orange_red1]",
            title_align="left",
        )
    )


def print_ssh_key_warning_message():
    """Warning message for user regarding ssh key"""
    have_ssh = None
    console = Console()
    prompt = "⚠️ [bright_white]Do you have an ssh key setup[/bright_white] [dim italic](y, n)[/dim italic] "

    while have_ssh not in ["y", "n"]:
        have_ssh = console.input(prompt)
        del_last_line()

    print(f"{prompt}[cyan]{have_ssh}[/cyan]")

    have_ssh = True if have_ssh == "y" else False

    # Exit execution if no setup
    if not have_ssh:
        print()
        print("Please setup an ssh key before using the `create-app` command.")
        help_link = "[italic bold cyan][link=https://docs.gitlab.com/ee/ssh/#generate-an-ssh-key-pair]generate ssh key[/link][/italic bold cyan]"
        print(f"> Refer to {help_link} to correctly setup one.")
        print()
        exit()


def clr_scr():
    """Clear screen on all os"""
    if platform.system().lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")


def del_last_line():
    """Delete the last console line"""
    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)
