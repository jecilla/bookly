from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from app.admin_soft_deletion import SoftDeletionAdmin
from app.models.user import User

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin, SoftDeletionAdmin):
    add_form_template = 'admin/add_form.html'
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions', 'is_deleted'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',
         'deleted_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_filter = ()
    list_display = ('id', 'first_name', 'last_name', 'email', 'role',
                    'is_deleted')