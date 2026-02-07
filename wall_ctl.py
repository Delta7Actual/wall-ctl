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

from os import system


def setup_parser() -> argparse.ArgumentParser:
    """
    Sets up an `ArgumentParser` object for the program
    
    :return: The parser object
    :rtype: ArgumentParser
    """

    parser = argparse.ArgumentParser(description="Wallpaper management tool")
    subparsers = parser.add_subparsers(dest="command", help="Action to perform")
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install a wallpaper")
    install_parser.add_argument("image", help="Path to the image to use")
    install_parser.add_argument("-t", "--time", help="The time on which the wallpaper will be set [HH:MM]")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a wallpaper")
    remove_parser.add_argument("id", help="ID of the wallpaper to remove")
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show the current configuration")

    return parser


def main() -> None:
    
    parser = setup_parser()
    args = parser.parse_args()

    # TODO: Finish actual logic
    match args.command:
        case "install":
            print(f"Installing wallpaper: {args.image}")
            if args.time:
                print(f"Scheduled for: {args.time}")
            
        case "remove":
            print(f"Removing wallpaper with ID: {args.id}")
        
        case "show":
            print(f"Showing wallpaper: {args.image}")

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()