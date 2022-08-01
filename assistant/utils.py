import string, random


def slug_generator(n):
    letter = string.ascii_letters
    num = '1234567890'
    raw = num + letter
    return ''.join(random.sample(raw, n))


def check_slug(link: str, link_list: list, n):
    while True:
        if link in link_list:
            link = slug_generator(n)
        else:
            return link
