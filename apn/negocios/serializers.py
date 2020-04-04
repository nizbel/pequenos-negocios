from django.contrib.auth.models import User
from rest_framework import serializers
from apn.negocios.models import Negocio, Contato, Categoria, Produto, \
    RegiaoEntrega, NegocioRegiaoEntrega, NegocioCategoria


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ContatoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contato
        fields = ['id', 'negocio', 'nome', 'telefone',
                  'possui_whatsapp']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'negocio', 'preco', 'categoria']


class RegiaoEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegiaoEntrega
        fields = ['id', 'nome']


class NegocioRegiaoEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NegocioRegiaoEntrega
        fields = ['id', 'negocio', 'regiao', 'taxa_entrega']


class NegocioCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NegocioCategoria
        fields = ['id', 'negocio', 'categoria']


# class NegocioCategoriaInNegocioSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(source='categoria_id')

#     class Meta:
#         model = NegocioCategoria
#         fields = ['id']


class NegocioSerializer(serializers.ModelSerializer):
    contatos = ContatoSerializer(many=True, required=False)
    regioes_entrega = NegocioRegiaoEntregaSerializer(
        many=True, required=False)
    categorias = NegocioCategoriaSerializer(
        many=True, required=False)

    class Meta:
        model = Negocio
        fields = ['id', 'nome', 'formas_entrega', 'valor_minimo',
                  'formas_pagamento', 'endereco', 'taxa_padrao_entrega',
                  'instagram', 'contatos', 'regioes_entrega', 'categorias']
