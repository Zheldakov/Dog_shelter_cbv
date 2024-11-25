import string
import random


def slug_generation():
    # генерирует slug с использованием маленьких букв латинского алфавита, цифр и больших букв
    return ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))
