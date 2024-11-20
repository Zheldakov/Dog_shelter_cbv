import string
import random


def slug_generation():
    return ''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))
