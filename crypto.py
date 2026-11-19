"""Cryptography feature placeholders.

The functions in this file are intentionally stubs for the first draft.
Implement and test the cryptographic operations here, not in the menu code.
"""


def encrypt_document(username):
    print("\n--- Upload and encrypt a document ---")
    file_path = input("Path to the document: ").strip()
    if not file_path:
        print("No file selected.")
        return

    # TODO: Read the input file.
    # TODO: Encrypt its contents with AES-GCM.
    # TODO: Store the encrypted output under data/documents/<username>/.
    # TODO: Record document metadata in users.json.
    print("Encryption is not implemented yet.")
    print(f"Selected file: {file_path}")


def decrypt_document(username):
    print("\n--- Download and decrypt a document ---")
    # TODO: Let the user select an encrypted document.
    # TODO: Load its key safely and decrypt/authenticate with AES-GCM.
    # TODO: Save the recovered file to a user-selected location.
    print("Decryption is not implemented yet.")


def sign_document(username):
    print("\n--- Sign a document ---")
    # TODO: Load the user's private key safely.
    # TODO: Sign the document bytes using RSA-PSS and SHA-256.
    print("Digital signing is not implemented yet.")


def verify_signature(username):
    print("\n--- Verify a document signature ---")
    # TODO: Load the document, signature, and trusted public key/certificate.
    # TODO: Verify the signature and report success/failure clearly.
    print("Signature verification is not implemented yet.")
