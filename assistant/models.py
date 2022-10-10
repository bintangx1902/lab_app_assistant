from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class TokenToResetPassword(models.Model):
    token = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, related_name='user_pass', related_query_name='user_pass', blank=True, null=True)

    def __str__(self):
        now = timezone.now()
        return f"{self.token} is {'expired' if now > self.valid_until else 'available'}"

    def val_stamp(self):
        return self.valid_until.strftime('%a %H:%M  %d/%m/%y')


class StudentScore(models.Model):
    name = models.CharField(max_length=255)
    score = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classification = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.name} : {self.score}"
