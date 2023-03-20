from django.contrib import admin
from .models import *

admin.site.register(TokenToResetPassword)
admin.site.register(StudentScore)
admin.site.register(ResetPasswordRequest)
