"""Registration and login"""

import os
import base64

from getpass import getpass

from storage import load_users, save_users, user_documents_dir

from UserSession import UserSession

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def register():
    """Create a new user account and generate password hash, salts, and keys, persisting them in users.json."""
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

    # generate 2 different salts 
    password_salt = os.urandom(16)
    KEK_salt = os.urandom(16)

    # use PBKDF2 to mix the password with the salt and hash it
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=password_salt,
        iterations=1_200_000
    )
    password_hash = kdf.derive(password.encode("utf-8"))

    # derive the 32 byte KEK using PBKDF2 with 2nd salt  
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=KEK_salt,
        iterations=1_200_000
    )
    KEK = kdf.derive(password.encode("utf-8"))

    # generate 32 byte AES-256 data key
    data_key = os.urandom(32)

    # generate nonce
    nonce = os.urandom(12)

    # encrypt the data key using aes with KEK and nonce
    aesgcm = AESGCM(KEK)
    wrapped_data_key = aesgcm.encrypt(nonce, data_key, None)

    users[username] = {
        "password_hash": base64.b64encode(password_hash).decode("ascii"),
        "password_salt": base64.b64encode(password_salt).decode("ascii"),
        "KEK_salt": base64.b64encode(KEK_salt).decode("ascii"),
        "wrapped_data_key": base64.b64encode(wrapped_data_key).decode("ascii"),
        "data_key_nonce": base64.b64encode(nonce).decode("ascii"),
        "documents": [],
    }
    save_users(users)
    user_documents_dir(username).mkdir(parents=True, exist_ok=True)

    print(f"Account '{username}' created successfully.")


def login():
    """Authenticate a user against the password_hash in users.json and unlock and return the keys in a UserSession object"""
    users = load_users()

    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = getpass("Password: ")

    account = users.get(username)
    if account is None:
 
        # run a dummy PBKDF2 computation  when the user isnt found, so both paths take the same amount of time and attacker 
        # cant discover which usernames exist or not based off time
        kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=os.urandom(16),
                iterations=1_200_000
            )
        password_hash = kdf.derive(password.encode("utf-8"))

        
        print("\nIncorrect username or password.")
        return None

         
    # get and decode salts
    password_salt = base64.b64decode(account["password_salt"])
    KEK_salt = base64.b64decode(account["KEK_salt"])

    # use PBKDF2 to mix the entered password with the stored salt and hash it
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=password_salt,
        iterations=1_200_000
    )
    password_hash = kdf.derive(password.encode("utf-8"))

    # compare generated hash to stored one to see if they match
    stored_password_hash = base64.b64decode(account["password_hash"])
    if password_hash != stored_password_hash:
        print("\nIncorrect username or password.")
        return None
    
    # re-derive KEK from password  
    kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=KEK_salt,
                iterations=1_200_000,
            )
    KEK = kdf.derive(password.encode("utf-8"))

    # unwrap keys 
    wrapped_data_key = base64.b64decode(account["wrapped_data_key"])
    nonce = base64.b64decode(account["data_key_nonce"])
    aesgcm = AESGCM(KEK)
    data_key = aesgcm.decrypt(nonce, wrapped_data_key, None)

    # fill usersession with keys
    print(f"Welcome, {username}!")
    return UserSession(username, data_key=data_key, private_key=None, certificate=None)
