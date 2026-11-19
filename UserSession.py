class UserSession:
    def __init__(self, username, data_key, private_key, certificate):
        """Unlocked keys and details for a currently logged in user. Lives in memory only, never on disk."""
        self.username = username
        self.data_key = data_key # 32-byte AES symmetric key for encrypting/decrypting
        self.private_key = private_key # RSA private key for signatures
        self.certificate = certificate # users X.509 public certificate
