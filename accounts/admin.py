from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
UserAdmin.fieldsets[2][1]['fields']= ('is_active', 'is_staff', 'special_user','is_author','is_superuser', 'groups', 'user_permissions')

UserAdmin.list_display += ('is_author','is_special_user')
admin.site.register(User,UserAdmin)