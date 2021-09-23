from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser, Address


# Register your models here.

# # Now register the new UserAdmin...
admin.site.register(CustomUser, UserAdmin)
# # ... and, since we're not using Django's built-in permissions,
# # unregister the Group model from admin.
admin.site.unregister(Group)
admin.site.register(Address)
