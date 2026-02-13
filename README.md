# wallctl

`wallctl` is a small command-line tool for managing **time-based, auto-changing wallpapers** using cron jobs.  

It is designed to be simple, transparent, and dependency-light.

---

## Requirements

- Python 3.10+
- `crontab`
- A desktop environment that supports `gsettings`  

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Delta7Actual/wall-ctl.git
cd wall-ctl
```

### 2. Installation (and un-installation)

You can simply use the included scripts:
```bash
[sudo] ./install.sh
[sudo] ./uninstall.sh
```

> Be aware, using wallctl *system-wide* requires root privileges

#### *But my mother told me to not run random scripts off the internet!

Your mother is very right, here is what the installer actually does:

- Downloads wall_ctl.py into /usr/local/lib/wallctl (system) or ~/.local/lib/wallctl (user)
- Creates a launcher in /usr/local/bin/wallctl (system) or ~/.local/bin/wallctl (user)
- Sets up a cron job that runs wallctl install every minute

And of course, feel free to look at [install.sh](https://github.com/Delta7Actual/wall-ctl/blob/main/install.sh) and [uninstall.sh](https://github.com/Delta7Actual/wall-ctl/blob/main/uninstall.sh)

## Usage

> You can get more info with the -h or --help flag
```bash
wallctl install [image] [-t HH:MM] [-d DIRECTORY]
wallctl remove <id>
wallctl show
```

- install – Install a wallpaper
- remove – Remove a scheduled wallpaper
- show – Show the current configuration and update the wallpaper

> The cronjob periodically calls `wallctl show` to update the wallpaper
