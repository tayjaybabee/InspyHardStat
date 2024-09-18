import shelve
from pathlib import Path
from inspy_hard_stat.ihs_lib.libre_hw_monitor.config import CONFIG
from inspy_hard_stat.crypt import encrypt_data, decrypt_data


DEFAULT_CREDENTIALS_DIRECTORY = Path(CONFIG.config_dir_path).joinpath('credentials')
DEFAULT_CREDENTIALS_FILE = DEFAULT_CREDENTIALS_DIRECTORY.joinpath('credentials.shelve')



class Credentials:

    def __init__(self, file_path=DEFAULT_CREDENTIALS_FILE):
        self.file_path = file_path
        self.__username = None
        self.__password = None
        self.__db = None
        self.__plaintext_mode = False  # To indicate whether decryption mode is active

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def __enter__(self):
        """Context manager entry, enabling decryption mode."""
        self.__plaintext_mode = True
        self.__db = shelve.open(str(self.file_path))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit, disabling decryption mode and closing shelve."""
        self.__plaintext_mode = False
        if self.__db is not None:
            self.__db.close()

    @property
    def username(self):
        if self.__plaintext_mode:
            return self.__username
        return "****"  # Masked when not in plaintext mode

    @username.setter
    def username(self, new):
        self.__username = new
        self.__db['username'] = encrypt_data(new)

    @property
    def password(self):
        if self.__plaintext_mode:
            return self.__password
        return "****"  # Masked when not in plaintext mode

    @password.setter
    def password(self, new):
        self.__password = new
        self.__db['password'] = encrypt_data(new)

    def load_credentials(self):
        """Load credentials from shelve, decrypting them if in plaintext mode."""
        with shelve.open(str(self.file_path)) as db:
            self.__username = decrypt_data(db.get('username', '')) if self.__plaintext_mode else db.get('username', '')
            self.__password = decrypt_data(db.get('password', '')) if self.__plaintext_mode else db.get('password', '')

    def save_credentials(self):
        """Save encrypted credentials to shelve."""
        with shelve.open(str(self.file_path)) as db:
            db['username'] = encrypt_data(self.__username)
            db['password'] = encrypt_data(self.__password)
