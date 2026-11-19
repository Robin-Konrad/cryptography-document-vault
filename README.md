# Secure Document Vault — first draft

A menu-based terminal prototype for a cryptography course project.

## Features in this draft

- Register and log in through a terminal menu.
- Persist registered users in `data/users.json`.
- Create a per-user document folder under `data/documents/`.
- Show placeholder menu options for encryption, decryption, signing, and signature verification.

## Requirements

- Python 3.9 or newer recommended.
- Install dependencies:

  ```bash
  python -m pip install -r requirements.txt
  ```

## Run

From this folder, run:

```bash
python main.py
```

The `python_text_menu` package adds an `Exit` option automatically to each menu.

## Important prototype limitation

Passwords are temporarily stored in plaintext in `data/users.json`. This is only for a classroom UI prototype; do not use real passwords or real sensitive documents. Before real use, replace this with password hashing, implement safe key management, and add the cryptographic operations.

## Planned next steps

1. Hash passwords and improve account handling.
2. Implement file encryption/decryption with authenticated encryption (for example AES-GCM).
3. Implement digital signatures and verification (for example RSA-PSS with SHA-256).
4. Add certificate handling if required by the assignment.
5. Add tests and document the design decisions.
