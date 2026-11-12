#!/usr/bin/env bash

# Feature 1: Pretty printing function
print_title() {
    printf "\n--- %s ---\n" "$1"
}

# Feature 2: Operating system detection
print_title "Checking OS"
if [[ "$OSTYPE" == "darwin"* ]]; then
    TARGET_OS="macos"
    echo "OS detected: macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    TARGET_OS="linux"
    echo "OS detected: Linux"
else
    echo "Unsupported OS"
    exit 1
fi

# Feature 3: Python check and installation
print_title "Checking Python 3"
if command -v python3 &> /dev/null; then
    echo "Python 3 is installed: $(python3 --version)"
else
    echo "Python 3 is missing, installing..."
    if [[ "$TARGET_OS" == "macos" ]]; then
        brew install python3
    elif [[ "$TARGET_OS" == "linux" ]]; then
        sudo apt update && sudo apt install -y python3
    fi
fi

# Feature 4: Virtual environment setup
print_title "Setting up virtual environment"
MY_VENV="venv"
if [[ ! -d "$MY_VENV" ]]; then
    echo "Creating venv..."
    python3 -m venv "$MY_VENV"
else
    echo "venv directory already exists."
fi
source "$MY_VENV/bin/activate"
echo "Virtual environment activated."

# Feature 5: Package and dependency management
print_title "Installing packages"
pip install --upgrade pip

REQ_FILE="requirements.txt"
if [[ -f "$REQ_FILE" ]]; then
    echo "Installing dependencies from $REQ_FILE..."
    pip install -r "$REQ_FILE"
else
    echo "No $REQ_FILE found, installing pytest..."
    pip install pytest
fi

# Feature 6: macOS-specific health check
if [[ "$TARGET_OS" == "macos" ]]; then
    print_title "Running Homebrew check"
    brew doctor
fi

echo "Setup completed successfully."
