"""Registration and login for the prototype.

IMPORTANT: passwords are temporarily stored as plaintext in this first draft.
Do not use real passwords. Replace this with password hashing before real use.
"""

from getpass import getpass

from storage import load_users, save_users, user_documents_dir


def register():
    """Create a new user account and persist it in users.json."""
    users = load_users()

    print("\n--- Register ---")
    username = input("Choose a username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return
    if any(char in username for char in "/\\") or username in {".", ".."}:
        print("Username cannot contain path separators.")
        return
    if username in users:
        print("That username is already registered.")
        return

    password = getpass("Choose a password: ")
    if not password:
        print("Password cannot be empty.")
        return

    # Prototype only: replace with a password hash in the next iteration.
    users[username] = {
        "password": password,
        "documents": [],
    }
    save_users(users)
    user_documents_dir(username).mkdir(parents=True, exist_ok=True)

    print(f"Account '{username}' created successfully.")


def login():
    """Authenticate a user against the prototype's JSON database."""
    users = load_users()

    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = getpass("Password: ")

    account = users.get(username)
    if account is None or account.get("password") != password:
        print("Incorrect username or password.")
        return None

    print(f"Welcome, {username}!")
    return username
