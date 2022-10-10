from django.contrib import admin
from .models import TokenToResetPassword, StudentScore

admin.site.register(TokenToResetPassword)
admin.site.register(StudentScore)
