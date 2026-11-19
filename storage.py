"""Local JSON and document-folder helpers."""

import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
USERS_FILE = DATA_DIR / "users.json"
DOCUMENTS_DIR = DATA_DIR / "documents"


def ensure_data_directories():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)


def load_users():
    """Load user records from JSON, returning an empty dict if none exist."""
    ensure_data_directories()
    if not USERS_FILE.exists():
        return {}

    try:
        with USERS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not read users.json: {error}")
        return {}


def save_users(users):
    """Persist user records to JSON."""
    ensure_data_directories()
    with USERS_FILE.open("w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)


def user_documents_dir(username):
    """Return the document directory for a username."""
    # Usernames are validated during registration; reject separators defensively.
    if not username or "/" in username or "\\" in username or username in {".", ".."}:
        raise ValueError("Invalid username")
    return DOCUMENTS_DIR / username


def list_documents(username):
    """Display document metadata currently recorded for a user."""
    users = load_users()
    account = users.get(username)
    if account is None:
        print("User account could not be found.")
        return

    documents = account.get("documents", [])
    print("\n--- My documents ---")
    if not documents:
        print("No documents registered yet.")
        return

    for index, document in enumerate(documents, start=1):
        if isinstance(document, dict):
            print(f"{index}. {document.get('name', 'Unnamed document')}")
        else:
            print(f"{index}. {document}")
