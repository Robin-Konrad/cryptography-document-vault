"""Terminal menus and navigation for the Secure Document Vault."""

from auth import login, register
from crypto import decrypt_document, encrypt_document, sign_document, verify_signature
from storage import list_documents

def print_menu(options, title="Menu", input_text="Select an option: "):
    """Print a menu with options and return the choice as a string."""
    print(f"\n{title}")
    for i, option in enumerate(options, start=1):
        print(f"[{i}] {option}")
    print(f"[{len(options) + 1}] Exit")
    return input(input_text).strip()

def user_menu(username):
    """Display the actions available to a logged-in user."""
    options = [
        "Upload and encrypt a document",
        "List my documents",
        "Download and decrypt a document",
        "Sign a document",
        "Verify a document signature",
        "Logout",
    ]

    while True:
        choice = print_menu(
            options,
            title=f"SECURE DOCUMENT VAULT — Logged in as {username}",
            input_text="Choose an option: ",
        )

        if choice == "1":
            encrypt_document(username)
        elif choice == "2":
            list_documents(username)
        elif choice == "3":
            decrypt_document(username)
        elif choice == "4":
            sign_document(username)
        elif choice == "5":
            verify_signature(username)
        elif choice == "6":
            print("Logged out.")
            return
        elif choice == str(len(options) + 1):
            # python-text-menu adds an Exit option after the listed options.
            print("Returning to the main menu.")
            return
        else:
            print("Please choose a valid option.")


def main_menu():
    """Display the application's main menu."""
    options = ["Register", "Login"]

    while True:
        choice = print_menu(
            options,
            title="SECURE DOCUMENT VAULT",
            input_text="Choose an option: ",
        )

        if choice == "1":
            register()
        elif choice == "2":
            username = login()
            if username is not None:
                user_menu(username)
        elif choice == str(len(options) + 1):
            print("Goodbye!")
            return
        else:
            print("Please choose a valid option.")
