from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
import binascii

def get_fernet():
    # Ensure key exists and is bytes
    key = settings.ENCRYPTION_KEY
    if not key:
        raise ValueError("No ENCRYPTION_KEY found in settings.")
    return Fernet(key.encode() if isinstance(key, str) else key)

def encrypt_password(password):
    f = get_fernet()
    return f.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    f = get_fernet()
    try:
        # Attempt to decrypt
        return f.decrypt(encrypted_password.encode()).decode()
    except (InvalidToken, binascii.Error):
        # Return None if the key is wrong or data is corrupted
        return None