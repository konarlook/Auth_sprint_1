import hashlib
import random
import string


def get_random_string(length: int = 12) -> str:
    """Generate a random string for salt."""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None) -> str:
    """Hash a password with salt."""
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode(),
        salt=salt.encode(),
        iterations=100000
    )
    return enc.hex()


def validate_password(
        password: str,
        hashed_password: str = None
) -> bool:
    """Check matching of a hashed password with a threshold in database."""
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed
