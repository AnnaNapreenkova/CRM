from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from django.contrib.auth.models import Group

admin.site.unregister(Group)
#admin.site.register(Account)

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('id', 'email','phone','surname','name','patronim', 'role', 'date_joined', 'last_login')
    search_fields = ('id', 'email','phone','surname','name','patronim', 'role')
    read_only = ('date_joined', 'last_login')

    exclude = ('username',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()
    
