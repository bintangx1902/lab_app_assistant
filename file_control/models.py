from os import path, remove

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from presence.models import ClassName
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.
class Files(models.Model):
    file = models.FileField(upload_to='files')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    class_name = models.ForeignKey(ClassName, default='', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} has {path.basename(self.file.name)}"

    def delete(self, using=None, *args, **kwargs):
        try:
            file_path = path.join(settings.MEDIA_ROOT, self.file.name)
            if path.isfile(file_path):
                remove(file_path)
        except ObjectDoesNotExist as e:
            print("File Does Not Exists")
        return super().delete(using=None, *args, **kwargs)

    def name(self):
        return str(path.basename(self.file.name))

    def date(self):
        return self.time_stamp.strftime('%d - %m - %y')
