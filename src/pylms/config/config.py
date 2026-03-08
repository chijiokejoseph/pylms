import secrets
from base64 import urlsafe_b64encode
from typing import Self

from cryptography.fernet import Fernet

from .facilitator import Facilitator


class Config:
    """Manage application configuration including course settings and state.

    Attributes:
        data_dir (str): Directory path for data storage.
        course_name (str): Course name.
        open (list[bool]): History of open/closed states.
        facilitators (list[Facilitator]): List of facilitators.
        admin (str): Admin username.
        encrypted_password (str): Encrypted password.
        encryption_key (str): Encryption key for password.
    """

    def __init__(self) -> None:
        self.data_dir: str = ""
        self.course_name: str = ""
        self.open: list[bool] = []
        self.facilitators: list[Facilitator] = []
        self.admin: str = ""
        self.encrypted_password: str = ""
        self.encryption_key: str = ""

    def set_password(self, password: str) -> None:
        """Encrypt password and store it with encryption key.

        Args:
            password: Plain text password to encrypt.
        """
        # Generate random 32-byte key and encode as base64
        key = urlsafe_b64encode(secrets.token_bytes(32))
        # Create Fernet cipher
        cipher = Fernet(key)
        # Encrypt password
        encrypted = cipher.encrypt(password.encode())
        # Store encrypted password and key
        self.encrypted_password = encrypted.decode()
        self.encryption_key = key.decode()

    def get_password(self) -> str:
        """Decrypt and return the plain text password.

        Returns:
            str: Decrypted plain text password, or empty string if not set.
        """
        if not self.encrypted_password or not self.encryption_key:
            return ""

        # Create Fernet cipher with stored key
        cipher = Fernet(self.encryption_key.encode())
        # Decrypt password
        decrypted = cipher.decrypt(self.encrypted_password.encode())
        return decrypted.decode()

    def verify_password(self, password: str) -> bool:
        """Verify password against stored encrypted password.

        Args:
            password: Plain text password to verify.

        Returns:
            bool: True if password matches, False otherwise.
        """
        return self.get_password() == password

    def copy_from(self, other: Self):

        attributes = vars(other)
        for key, value in attributes.items():
            setattr(self, key, value)
