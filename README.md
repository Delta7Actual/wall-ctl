# wallctl

`wallctl` is a small command-line tool for managing **time-based, auto-changing wallpapers**
using cron jobs.

It is designed to be simple, transparent, and dependency-light.

---

## Features

- Install scheduled wallpaper changes
- Remove existing wallpaper schedules
- Inspect current configuration
- Uses standard system tools (cron + gsettings)
- Works per-user or system-wide

---

## Requirements

- Python 3.10+
- `crontab`
- A desktop environment that supports `gsettings`
  - Tested with **Linux Mint 22.2 (Cinnamon)**

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Delta7Actual/wall-ctl.git
cd wall-ctl
```

2. Run the script:
```bash
[sudo] python wall_ctl.py
[sudo] python3 wall_ctl.py
```

## Usage

```bash
wallctl install IMAGE [-t HH:MM]
wallctl remove ID
wallctl show
```
