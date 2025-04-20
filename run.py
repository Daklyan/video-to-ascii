import os
import platform
import subprocess

from pathlib import Path


def launch_in_cli(script_to_launch_path: str, width: int = 100, height: int = 30):
    """Start a new terminal and launch passed script

    Args:
        width (int): width of the terminal to start (defaults to 100)
        height (int): height of the terminal to start (defaults to 30)
        script_to_launch_path (str): path to script to launch in terminal
    """
    system = platform.system()

    if system == "Linux":
        terminal = find_linux_terminal()
        if not terminal:
            print("No terminal found")  # replace by LOGGER.error
            exit(1)

        if "konsole" in terminal:
            subprocess.Popen(
                [
                    terminal,
                    "--new-tab",
                    "--geometry",
                    f"{width}x{height}",
                    "-e",
                    "python3",
                    str(script_to_launch_path),
                ]
            )
        elif "gnome-terminal" in terminal:
            subprocess.Popen(
                [
                    terminal,
                    "--geometry",
                    f"{width}x{height}",
                    "--",
                    "bash",
                    "-c",
                    f"python3 {script_to_launch_path}; exec bash",
                ]
            )
        elif "xterm" in terminal:
            subprocess.Popen(
                [
                    terminal,
                    "-geometry",
                    f"{width}x{height}",
                    "-e",
                    f"python3 {script_to_launch_path}",
                ]
            )
        elif "alacritty" in terminal:
            subprocess.Popen(
                [
                    terminal,
                    "-o",
                    f"window.dimensions.columns={width}",
                    "-o",
                    f"window.dimensions.lines={height}",
                    "-e",
                    "python3",
                    str(script_to_launch_path),
                ]
            )
        elif (
            "tilix" in terminal
            or "xfce4-terminal" in terminal
            or "mate-terminal" in terminal
        ):
            subprocess.Popen([terminal, "-e", f"python3 {script_to_launch_path}"])
        else:
            subprocess.Popen([terminal, "-e", f"python3 {script_to_launch_path}"])
    elif system == "Windows":
        subprocess.Popen(["cmd.exe", "/k", f"python {script_to_launch_path}"])
    else:
        print(f"{system} is not supported")  # replace by LOGGER.error
        exit(1)


def find_linux_terminal():
    """Tries to find linux terminal

    Returns: The name of default terminal if found, None otherwise
    """
    terminal = os.environ.get("TERMINAL")
    if terminal:
        return terminal

    try:
        output = subprocess.check_output(
            ["update-alternatives", "--query", "x-terminal-emulator"],
            stderr=subprocess.DEVNULL,
        ).decode()

        for line in output.splitlines():
            if line.startswith("Value:"):
                return line.split(":", 1)[1].strip()
    except Exception as error:
        print(
            f"Error while using update-alternatives: {error}"
        )  # TO CHANGE by LOGGER.debug

    # Trying well known terminals
    known_terminals = [
        "konsole",
        "gnome-terminal",
        "xterm",
        "alacritty",
        "tilix",
        "xfce4-terminal",
    ]
    for terminal in known_terminalss:
        if (
            subprocess.call(
                ["which", terminal],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            == 0
        ):
            return terminal

    return None
