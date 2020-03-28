from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from apn.negocios.models import InfoPerfilUsuario, NegocioUsuario, Produto

# Define an inline admin descriptor for InfoPerfilUsuario model
# which acts a bit like a singleton


class InfoPerfilUsuarioInline(admin.StackedInline):
    model = InfoPerfilUsuario
    can_delete = False
    verbose_name_plural = 'Outras informações'

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = (InfoPerfilUsuarioInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(InfoPerfilUsuario)

admin.site.register(NegocioUsuario)

admin.site.register(Produto)
