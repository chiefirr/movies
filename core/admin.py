from django.contrib import admin
from .models.user import ExtendedUser

admin.site.register(ExtendedUser)
