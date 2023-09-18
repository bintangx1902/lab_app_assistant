from .models import User


def check_nim(nim_list: list, target: str):
    if target in nim_list:
        return f"{target} sudah terdaftar di sistem", True
    return "", False


def total_average(models, Avg):
    return models.aggregate(Avg('score'))


def check_request(models, user):
    """ models must be request password models """
    find = models.objects.filter(user=user, is_done=False)
    return True if find else False


def check_nullable(instance):
    user = User.objects.get(pk=instance)
    nim = user.user.nim
    if not nim or nim.isspace():
        return True
    return False
