#!/bin/bash

USER_PREFIX="$HOME/.local"
SYSTEM_PREFIX="/usr/local"
TEMP_FILE="/tmp/wall_ctl_script.py.tmp"

# Ask the user for global or user install
read -rp "Install globally for the entire system? [y/N] " IS_SYSTEM

case "$IS_SYSTEM" in
    [yY]|[yY][eE][sS])
        INSTALL_MODE="global"
        ;;
    *)
        INSTALL_MODE="user"
        ;;
esac

# Download the Python script
echo -n "Retrieving code... "
curl -fsSL \
    "https://raw.githubusercontent.com/Delta7Actual/wall-ctl/refs/heads/main/wall_ctl.py" \
    -o "$TEMP_FILE"
echo "DONE"

if [ "$INSTALL_MODE" = "global" ]; then
    if [ "$EUID" -ne 0 ]; then
        echo "You need root privileges for system-wide install!"
        exit 1
    fi

    echo -n "Installing system-wide... "

    # Copy Python script
    mkdir -p "$SYSTEM_PREFIX/lib/wallctl"
    mv "$TEMP_FILE" "$SYSTEM_PREFIX/lib/wallctl/wall_ctl.py"

    # Create launcher
    cat > "$SYSTEM_PREFIX/bin/wallctl" <<'EOF'
#!/bin/bash
exec python3 /usr/local/lib/wallctl/wall_ctl.py "$@"
EOF

    chmod +x "$SYSTEM_PREFIX/bin/wallctl"

    # Schedule wallpaper change
    CRON_JOB="* * * * * /usr/local/bin/wallctl show"
    (crontab -l 2>/dev/null | grep -v "wallctl"; echo "$CRON_JOB") | crontab -

    echo "DONE"

else
    echo -n "Installing for user $(whoami)... "

    # Copy Python script
    mkdir -p "$USER_PREFIX/lib/wallctl"
    mv "$TEMP_FILE" "$USER_PREFIX/lib/wallctl/wall_ctl.py"

    # Make sure user bin exists
    mkdir -p "$USER_PREFIX/bin"

    # Create launcher
    cat > "$USER_PREFIX/bin/wallctl" <<'EOF'
#!/bin/bash
exec python3 "$HOME/.local/lib/wallctl/wall_ctl.py" "$@"
EOF

    chmod +x "$USER_PREFIX/bin/wallctl"

    # Schedule wallpaper change
    CRON_JOB="* * * * * $HOME/.local/bin/wallctl show"
    (crontab -l 2>/dev/null | grep -v "wallctl"; echo "$CRON_JOB") | crontab -

    echo "DONE"
fi

# Clean up temp file if it still exists
rm -f "$TEMP_FILE"

echo "Installation complete! Make sure $USER_PREFIX/bin (or /usr/local/bin) is in your PATH."
