from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as CustomUserAdmin

from .models import User

class UserAdmin(CustomUserAdmin):
    fieldsets = tuple(
        (fieldset[0], {
            **{key: value for (key, value) in fieldset[1].items()
                if key != 'fields'},
            'fields': fieldset[1]['fields'] + ('bio', 'role')
        })
        if fieldset[0] == 'Personal info'
        else fieldset
        for fieldset in CustomUserAdmin.fieldsets
    )
    list_display = ['email', 'username', 'role', 'is_active']
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)