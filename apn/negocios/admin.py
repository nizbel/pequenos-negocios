from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from apn.negocios.models import Usuario

# Define an inline admin descriptor for Usuario model
# which acts a bit like a singleton


class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'Usuario'

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
