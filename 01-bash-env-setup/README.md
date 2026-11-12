# Bash script exercise (Slide 18)

Bash script (`env_install.sh`) to set up a Python environment on macOS.

## What the script does

- Checks if the OS is macOS (exits if unsupported)
- Checks if `python3` is installed, and installs it with `brew` (macOS) if missing
- Creates a `venv` folder if it doesn't exist yet and activates it
- Upgrades `pip` and installs packages from `requirements.txt` (or `pytest` if no `requirements.txt` is found)
- Runs `brew doctor` on macOS to verify the setup

## How to run it

```bash
chmod +x env_install.sh
source env_install.sh
```
