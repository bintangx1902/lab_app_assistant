import random
import re
import string

class_list = [f"Kelas {char}" for char in string.ascii_uppercase]
course_list = ['PBO', 'Struktur Data', 'Dasar Pemrograman', 'Pemrograman Deklaratif']
conditions = ['Izin', 'Sakit']


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


def set_class_name(start, end, class_, gen, course):
    punc = r'[' + string.punctuation + ']'
    name = f"{gen} {class_} {course} Jam"
    name = re.sub(punc, '', name)
    class_name = f"{name} {start}-{end}"

    start = re.sub(punc, '', start)
    end = re.sub(punc, '', end)
    class_link = f"{name} {start}-{end}".replace(' ', '-')

    return class_name, class_link
