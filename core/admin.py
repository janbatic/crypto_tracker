from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from core.models import User


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
    )

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',
            )
        }),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'email',
            )
        })
    )
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name'
    ]


admin.site.register(User, CustomUserAdmin)
