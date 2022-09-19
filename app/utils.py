from string import ascii_letters, digits
from random import choice


def create_user_id() -> str:
    letters = ascii_letters + digits
    result = ''.join([choice(letters) for _ in range(0, 11)])
    return result
