from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apn.negocios.models import Negocio


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class NegocioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Negocio
        fields = ['url', 'nome', 'formas_entrega', 'valor_minimo',
                  'formas_pagamento', 'endereco', 'taxa_padrao_entrega']
