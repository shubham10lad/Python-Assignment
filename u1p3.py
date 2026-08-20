import os
import sys
import venv
import subprocess
from pathlib import Path
import importlib.metadata
from dotenv import load_dotenv

# Define base paths and project structure
PROJECT_DIR = Path("ai_project")
DIRECTORIES = ["data", "logs", "config", "src"]
VENV_DIR = PROJECT_DIR / "venv"
ENV_FILE = PROJECT_DIR / ".env"
REQ_FILE = PROJECT_DIR / "requirements.txt"
MAIN_FILE = PROJECT_DIR / "main.py"

REQUIRED_PACKAGES = ["requests", "pandas", "python-dotenv"]


def setup_project_structure():
    """Creates the ai_project directory and required subdirectories."""
    PROJECT_DIR.mkdir(exist_ok=True)
    for folder in DIRECTORIES:
        (PROJECT_DIR / folder).mkdir(exist_ok=True)
    if not MAIN_FILE.exists():
        MAIN_FILE.write_text("# Main project entry point\nprint('AI Project Initialized')\n")


def create_virtual_environment():
    """Generates a Python virtual environment inside the project directory."""
    if not VENV_DIR.exists():
        venv.create(VENV_DIR, with_pip=True)


def get_venv_executables():
    """Helper to retrieve OS-specific venv Python and Pip paths."""
    if sys.platform == "win32":
        python_bin = VENV_DIR / "Scripts" / "python.exe"
        pip_bin = VENV_DIR / "Scripts" / "pip.exe"
    else:
        python_bin = VENV_DIR / "bin" / "python"
        pip_bin = VENV_DIR / "bin" / "pip"
    return str(python_bin), str(pip_bin)


def install_and_export_requirements():
    """Installs dependencies and exports freezing to requirements.txt."""
    _, pip_bin = get_venv_executables()
    
    # Install required packages
    subprocess.run([pip_bin, "install", *REQUIRED_PACKAGES], check=True)
    
    # Generate requirements.txt
    result = subprocess.run([pip_bin, "freeze"], capture_output=True, text=True, check=True)
    REQ_FILE.write_text(result.stdout)


def create_env_file():
    """Creates .env file containing environment variables."""
    if not ENV_FILE.exists():
        content = (
            "API_KEY=sk-proj-9876543210abcdef\n"
            "API_URL=https://api.openai.com/v1\n"
        )
        ENV_FILE.write_text(content)


def validate_and_display_config():
    """Loads, validates, and prints masked configuration from .env."""
    load_dotenv(ENV_FILE)

    api_key = os.getenv("API_KEY")
    api_url = os.getenv("API_URL")

    # Validation step
    missing = []
    if not api_key:
        missing.append("API_KEY")
    if not api_url:
        missing.append("API_URL")

    if missing:
        print(f"Error: Missing environment variable(s): {', '.join(missing)}")
        return

    # Mask API key (show only last 4 characters)
    masked_key = "*" * max(0, len(api_key) - 4) + api_key[-4:]

    print("\n--- Project Configuration ---")
    print(f"API URL: {api_url}")
    print(f"API Key: {masked_key}")


def display_installed_versions():
    """Displays installed versions of required dependencies."""
    print("\n--- Installed Dependency Versions ---")
    for package in REQUIRED_PACKAGES:
        try:
            version = importlib.metadata.version(package)
            print(f"{package}: {version}")
        except importlib.metadata.PackageNotFoundError:
            print(f"{package}: Not installed")


if __name__ == "__main__":
    setup_project_structure()
    create_virtual_environment()
    install_and_export_requirements()
    create_env_file()
    validate_and_display_config()
    display_installed_versions()