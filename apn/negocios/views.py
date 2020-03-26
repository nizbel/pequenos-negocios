from apn.negocios.serializers import UserSerializer, \
    NegocioSerializer, ContatoSerializer
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from apn.negocios.models import Negocio, NegocioUsuario, Contato
from apn.negocios.permissions import ResponsavelOuReadOnly, ProprioUsuario, \
    ResponsavelNegocioOuReadOnly, ReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ProprioUsuario]


class NegocioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para Negocio.
    """
    queryset = Negocio.objects.all().order_by('nome')
    serializer_class = NegocioSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, ResponsavelOuReadOnly]

    def create(self, request):
        try:
            with transaction.atomic():
                result = super().create(request)
                NegocioUsuario.objects.create(
                    negocio=Negocio.objects.get(id=result.data['id']),
                    usuario=request.user)
        except:
            raise
        return result

    @action(detail=False)
    def meus(self, request, *args, **kwargs):
        negocios = NegocioUsuario.objects.filter(usuario=request.user)
        negocios = self.queryset.filter(id__in=negocios)
        serializer = self.get_serializer(negocios, many=True)
        return Response(serializer.data)


class ContatoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para Contato.
    """
    queryset = Contato.objects.all().order_by('nome')
    serializer_class = ContatoSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, ResponsavelNegocioOuReadOnly]

    def get_queryset(self):
        negocio_id = self.kwargs.get('negocio_id')
        print(negocio_id)
        if negocio_id:
            return self.queryset.filter(negocio__id=negocio_id)
        else:
            return self.queryset

    def create(self, request):
        try:
            with transaction.atomic():
                result = super().create(request)
                if request.user.id not in Negocio.objects.get(id=result.data['negocio']) \
                        .responsaveis:
                    raise ValueError(
                        'Contato deve ser vinculado a um negócio do usuário')
        except:
            raise
        return result
