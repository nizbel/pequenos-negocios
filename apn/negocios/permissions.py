from rest_framework import permissions


class ResponsavelOuReadOnly(permissions.BasePermission):
    """
    Apenas responsáveis por um negócio podem editá-lo
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.id in obj.responsaveis() \
            or request.user.is_superuser
