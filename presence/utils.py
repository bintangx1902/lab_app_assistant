from .models import User
from .models import Recap, ClassName

from .models import Recap, ClassName, GenerateQRCode

def get_total_presence(user):
    total_recaps = Recap.objects.filter(user=user).count()
    total_qr = GenerateQRCode.objects.filter(class_name__in=user.stud.all()).count()  # Hitung total QR Code 
    
    if total_qr == 0:
      return "0/0"

    return f"{total_recaps}/{total_qr}"

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
