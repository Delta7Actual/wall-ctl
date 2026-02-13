#!/bin/bash

USER_PREFIX="$HOME/.local"
SYSTEM_PREFIX="/usr/local"

# Ask the user for global or user uninstall
read -rp "Uninstall globally from the entire system? [y/N] " IS_SYSTEM

case "$IS_SYSTEM" in
    [yY]|[yY][eE][sS])
        UNINSTALL_MODE="global"
        ;;
    *)
        UNINSTALL_MODE="user"
        ;;
esac

if [ "$UNINSTALL_MODE" = "global" ]; then
    if [ "$EUID" -ne 0 ]; then
        echo "You need root privileges for system-wide uninstall!"
        exit 1
    fi

    echo -n "Removing system-wide installation... "

    rm -f "$SYSTEM_PREFIX/bin/wallctl"
    rm -rf "$SYSTEM_PREFIX/lib/wallctl"

    # Optionally, remove system cron jobs
    if command -v crontab >/dev/null 2>&1; then
        crontab -l | grep -v "wallctl" | crontab -
    fi

    echo "DONE"

else
    echo -n "Removing user installation... "

    rm -f "$USER_PREFIX/bin/wallctl"
    rm -rf "$USER_PREFIX/lib/wallctl"

    # Remove user cron jobs containing wallctl
    if command -v crontab >/dev/null 2>&1; then
        crontab -l | grep -v "wallctl" | crontab -
    fi

    echo "DONE"
fi

echo "wallctl was successfully uninstalled!"
