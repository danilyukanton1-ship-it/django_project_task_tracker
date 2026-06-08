from django.contrib import admin
from account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("user_permissions",)
