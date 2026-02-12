"""
WallCTL - time-based dynamic wallpaper manager.

This script can manage wallpapers which switch
automatically based on current system time.

Dependencies:
    - crontab
    - python3

Notes:
    - Running globally requires root privileges.
    - User-level installs modify the user's crontab only.
"""

import argparse
import sys
import getpass
import os
import json

from pathlib import Path
from typing import Dict
from datetime import datetime

SCHEMA="org.cinnamon.desktop.background"
CRON_TAG="WALLCTL_WALLPAPER_TOOL"

USER_CONFIG = Path.home() / ".config" / "wallctl" / "schedule.json"
SYSTEM_CONFIG = Path("/etc/wallctl/schedule.json")

ScheduleDict = Dict[str, Dict[str, str]]


def setup_parser() -> argparse.ArgumentParser:
    """
    Sets up an `ArgumentParser` object for the program
    
    :return: The parser object
    :rtype: ArgumentParser
    """

    parser = argparse.ArgumentParser(description="Wallpaper management tool")
    subparsers = parser.add_subparsers(dest="COMMAND", required=True, help="Action to perform")
    
    # Global system option
    parser.add_argument("--system", action="store_true", help="Operate on the system-wide cron (requires root)")

    # Install command
    install_parser = subparsers.add_parser("install", help="Install a wallpaper")
    install_parser.add_argument("IMAGE", help="Path to the image to use")
    install_parser.add_argument("-t", "--time", required=True, help="The time on which the wallpaper will be set [HH:MM]")
    install_parser.add_argument("-i", "--id", help="ID to use for the image")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a wallpaper")
    remove_parser.add_argument("-i", "--id", required=True, help="ID of the wallpaper to remove")
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show the current configuration")


    return parser


def prepare_config(user) -> Path:
    path_to_use = SYSTEM_CONFIG if user == "SYSTEM" else USER_CONFIG
    if not path_to_use.exists():
            path_to_use.parent.mkdir(parents=True, exist_ok=True)
            path_to_use.write_text("{}")

    return path_to_use


def get_next_id(schedule: Dict[str, Dict[str, str]]) -> int:
    pass


def validate_time(time_str: str) -> bool:
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


def handle_install(schedule: ScheduleDict, config_path: Path, args: argparse.Namespace) -> None:
    id = args.id if args.id else get_next_id(schedule)
    image_path = Path(args.IMAGE)
    time = args.time

    if not validate_time(time):
        print("TIME must be a valid time in the format: HH:MM!")
        return

    if not image_path.is_file():
        print("IMAGE must be a valid file (did you have a typo or use a directory?)")
        return
    
    schedule[time] = {"image": str(image_path), "id": id}
    with config_path.open("w") as f:
        json.dump(schedule, f, indent=4)

    print(f"Successfully installed entry! [{image_path}@{time}] [id={id}]")


def handle_remove(schedule: ScheduleDict, config_path: Path, args: argparse.Namespace) -> None:
    id = args.id if args.id else get_next_id(schedule)
    found = False

    for time, entry in list(schedule.items()):
        if entry.get("id") == id:
            del schedule[time]
            found = True
            break

    if not found:
        print(f"Found no entry with corresponding id='{id}'!")
        return

    with config_path.open("w") as f:
        json.dump(schedule, f, indent=4)
    
    print(f"Successfully removed wallpaper with id='{id}'!")


def main() -> None:
    
    parser = setup_parser()
    args = parser.parse_args()

    # Get current user
    user = getpass.getuser()
    if args.system:
        if os.getuid() != 0:
            print("Cannot use system option without root!")
            return
        user = "SYSTEM"

    # Validate config structure
    config_path = prepare_config(user)
    schedule: ScheduleDict = {}

    # Load config
    with config_path.open('r') as f:
        try:
            schedule = json.load(f)
        except json.JSONDecodeError as json_err:
            print(f"Config file contains Illegal JSON! ({json_err})")
            return

    # Handle commands
    match args.COMMAND:
        case "install":
            handle_install(schedule, config_path, args)

        case "remove":
            handle_remove(schedule, config_path, args)

        case "show":
            pass

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
