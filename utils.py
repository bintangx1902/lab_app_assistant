import random
import string


def link_generator(n):
    num = '0123456789'
    letters = string.ascii_letters
    raw = num + letters
    return ''.join(random.sample(raw, n))
