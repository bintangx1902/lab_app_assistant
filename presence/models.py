from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from os import path, remove
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', related_query_name='user')
    is_controller = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    nim = models.CharField(max_length=255)
    cname = models.ForeignKey('ClassName', on_delete=models.CASCADE, related_name='user_data', related_query_name='user_data')

    def __str__(self):
        return self.user.name


class ClassName(models.Model):
    name = models.CharField(max_length=255)
    link = models.SlugField(max_length=255, unique=True)
    unique_code = models.CharField(max_length=255, unique=True)
    pr = models.ManyToManyField(User, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='class_creator', related_query_name='class_creator')

    def __str__(self):
        return f"{str(self.name)}"


class GenerateQRCode(models.Model):
    qr_code = models.SlugField(unique=True)
    valid_until = models.DateTimeField(blank=True)
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    qr_img = models.FileField(blank=True, upload_to='qr/')

    def save(self, *args, **kwargs):
        img_code = qrcode.make(self.qr_code)
        canvas = Image.new('RGB', (600, 600), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(img_code)
        f_name = f"qr_generated_{self.qr_code}.png"
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_img.save(f_name, File(buffer), save=False)
        canvas.close()
        return super().save(*args, **kwargs)

    def delete(self, using=None, *args, **kwargs):
        remove(path.join(settings.MEDIA_ROOT, self.qr_img.name))
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"class : {self.class_name.name} - {self.qr_code}"


class Recap(models.Model):
    qr = models.ForeignKey(GenerateQRCode, on_delete=models.CASCADE, related_name='qr_c', related_query_name='qr_c')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} presence @ {self.time_stamp.srtftime('%a %H:%M  %d/%m/%y')}"


