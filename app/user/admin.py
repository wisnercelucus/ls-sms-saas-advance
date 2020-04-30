from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from user.models import User, Follow

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email','username', 'name', 'first_name', 'last_name', 'last_login']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'username', 'first_name', 'last_name', 'image',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)