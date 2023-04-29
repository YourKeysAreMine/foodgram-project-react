from django.contrib import admin
from .models import User, Subscription


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email', 'username']
    list_filter = ['email', 'username']


admin.site.register(User, UserAdmin)
admin.site.register(Subscription)
