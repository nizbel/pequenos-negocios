from apn.negocios.serializers import UserSerializer, \
    NegocioSerializer, ContatoSerializer, CategoriaSerializer, \
    ProdutoSerializer, RegiaoEntregaSerializer, NegocioRegiaoEntregaSerializer
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from apn import settings
from apn.negocios.models import Negocio, NegocioUsuario, Contato, \
    Categoria, Produto, RegiaoEntrega, NegocioRegiaoEntrega
from apn.negocios.permissions import ResponsavelOuReadOnly, ProprioUsuario, \
    ResponsavelNegocioOuReadOnly


def home(request):
    return render(request, 'index.html', {'PROD': (not settings.DEBUG)})


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

    def list(self, request):
        result = super().list(request)

        # Percorrer todos os ids para adicionar categorias
        ids = []
        for negocio_data in result.data:
            ids.append(negocio_data['id'])

        # Listar produtos para trazer pares (categoria, negócio)
        categorias_negocios = Produto.objects.filter(
            negocio__id__in=ids).values('categoria', 'negocio').order_by('negocio').distinct()

        for negocio_data in result.data:
            negocio_data['categorias'] = []
            for categoria_negocio in categorias_negocios:
                if negocio_data['id'] == categoria_negocio['negocio']:
                    negocio_data['categorias'].append(
                        {'id': categoria_negocio['categoria']})

        return result

    @action(detail=True)
    def categorias(self, request, *args, **kwargs):
        negocio_id = self.kwargs.get('pk')
        if not negocio_id:
            return Response([])

        negocio = Negocio.objects.get(id=negocio_id)
        categorias = Categoria.objects.filter(id__in=negocio.categorias)
        serializer = CategoriaSerializer(
            categorias, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def meus(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response([])

        negocios = NegocioUsuario.objects.filter(usuario=request.user) \
            .values_list('negocio', flat=True)
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
        if negocio_id:
            return self.queryset.filter(negocio__id=negocio_id)
        else:
            return self.queryset

    def create(self, request, negocio_id=None):
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


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para Categoria.
    """
    queryset = Categoria.objects.all().order_by('nome')
    serializer_class = CategoriaSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]


class ProdutoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para Produto.
    """
    queryset = Produto.objects.all().order_by('nome')
    serializer_class = ProdutoSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, ResponsavelNegocioOuReadOnly]

    def get_queryset(self):
        negocio_id = self.kwargs.get('negocio_id')
        if negocio_id:
            return self.queryset.filter(negocio__id=negocio_id)
        else:
            return self.queryset

    def create(self, request, negocio_id=None):
        try:
            with transaction.atomic():
                result = super().create(request)
                if request.user.id not in Negocio.objects.get(id=result.data['negocio']) \
                        .responsaveis:
                    raise ValueError(
                        'Produto deve ser vinculado a um negócio do usuário')
        except:
            raise
        return result


class RegiaoEntregaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para RegiaoEntrega.
    """
    queryset = RegiaoEntrega.objects.all().order_by('nome')
    serializer_class = RegiaoEntregaSerializer
    permission_classes = [
        AdminOuReadOnly]


class NegocioRegiaoEntregaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para RegiaoEntrega.
    """
    queryset = NegocioRegiaoEntrega.objects.all().order_by('nome')
    serializer_class = NegocioRegiaoEntregaSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]
