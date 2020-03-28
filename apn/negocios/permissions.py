from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    """
    Permissão para apenas leitura
    """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class AdminOuReadOnly(permissions.BasePermission):
    """
    Apenas admins podem alterar
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser


class ResponsavelOuReadOnly(permissions.BasePermission):
    """
    Apenas responsáveis por um negócio podem editá-lo
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.id in obj.responsaveis \
            or request.user.is_superuser


class ResponsavelNegocioOuReadOnly(permissions.BasePermission):
    """
    Apenas responsáveis por um negócio podem editá-lo
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.id in obj.negocio.responsaveis \
            or request.user.is_superuser


class ProprioUsuario(permissions.BasePermission):
    """
    Apenas próprio usuário ou admin pode alterar
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.id == obj.id \
            or request.user.is_superuser
