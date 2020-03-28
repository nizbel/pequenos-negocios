from django.contrib.auth.models import User
from rest_framework import serializers
from apn.negocios.models import Negocio, Contato


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username']


class ContatoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contato
        fields = ['url', 'negocio', 'nome', 'telefone',
                  'possui_whatsapp']


class NegocioSerializer(serializers.ModelSerializer):
    contatos = ContatoSerializer(many=True, required=False)

    class Meta:
        model = Negocio
        fields = ['url', 'id', 'nome', 'formas_entrega', 'valor_minimo',
                  'formas_pagamento', 'endereco', 'taxa_padrao_entrega',
                  'instagram', 'contatos']
