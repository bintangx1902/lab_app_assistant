from io import BytesIO
from os import path, remove

import qrcode
from PIL import Image, ImageDraw
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.db import models


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', related_query_name='user')
    is_controller = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    nim = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class ClassName(models.Model):
    name = models.CharField(max_length=255)
    link = models.SlugField(max_length=255, unique=True)
    unique_code = models.CharField(max_length=255, unique=True)
    pr = models.ManyToManyField(User, blank=True, related_name='assist', related_query_name='assist')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='class_creator',
                                related_query_name='class_creator')
    students = models.ManyToManyField(User, related_name='stud', related_query_name='stud', null=True, blank=True)
    lecture_name = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='Nama Dosen : ')

    def __str__(self):
        return f"{str(self.name)}"


class GenerateQRCode(models.Model):
    qr_code = models.SlugField(unique=True)
    valid_until = models.DateTimeField(blank=True)
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE, related_name='from_class',
                                   related_query_name='from_class')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    qr_img = models.FileField(blank=True, upload_to='qr/')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        file_path = path.join(settings.MEDIA_ROOT, self.qr_img.name)
        img_code = qrcode.make(self.qr_code)
        canvas = Image.new('RGB', (330, 330), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(img_code)
        f_name = f"qr_generated_{self.qr_code}.png"
        buffer = BytesIO()

        if not path.isfile(file_path):
            canvas.save(buffer, 'PNG')
            self.qr_img.save(f_name, File(buffer), save=False)
            canvas.close()
        return super().save(*args, **kwargs)

    def delete(self, using=None, *args, **kwargs):
        try:
            file_path = path.join(settings.MEDIA_ROOT, self.qr_img.name)
            if path.isfile(file_path):
                remove(file_path)
        except ObjectDoesNotExist as e:
            print(e)

        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"class : {self.class_name.name} - {self.qr_code}"

    def qr_name(self):
        return str(path.basename(self.qr_img.name))

    def stamp(self):
        return self.created.strftime('%a %H:%M  %d/%m/%y')


class Recap(models.Model):
    qr = models.ForeignKey(GenerateQRCode, on_delete=models.CASCADE, related_name='qr_c', related_query_name='qr_c')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recap', related_query_name='user_recap')
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} presence @ {self.time_stamp.strftime('%a %H:%M  %d/%m/%y')}"

    def stamp(self):
        return self.time_stamp.strftime('%a %H:%M  %d/%m/%y')
