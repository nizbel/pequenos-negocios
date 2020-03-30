from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from apn.negocios.models import InfoPerfilUsuario, Negocio, \
    NegocioUsuario, Produto

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


class NegocioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor_minimo', 'formas_pagamento',
                    'endereco', 'taxa_padrao_entrega', 'instagram')
    search_fields = ['user__username', 'url']

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.register(Negocio, NegocioAdmin)

admin.site.register(NegocioUsuario)

admin.site.register(Produto)
