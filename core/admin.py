from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class AdminCustomUser(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username", "password1", "password2", "email", 
                    "first_name", "last_name", 
                ),
            },
        ),
    )
