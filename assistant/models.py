from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from presence.models import ClassName


class TokenToResetPassword(models.Model):
    token = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        now = timezone.now()
        return f"{self.token} is {'expired' if now > self.valid_until else 'available'}"

    def val_stamp(self):
        return self.valid_until.strftime('%a %H:%M  %d/%m/%y')


class StudentScore(models.Model):
    name = models.CharField(max_length=255)
    score = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='score', related_query_name='score')
    classification = models.CharField(max_length=255)
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE, related_name='user_score',
                                   related_query_name='user_score')

    def __str__(self):
        return f"{self.user.username} - {self.name} : {self.score}"


class ResetPasswordRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    token = models.ForeignKey(TokenToResetPassword, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} is requested" if not self.is_done else f"{self.user} has changed password"
