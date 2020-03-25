from django.contrib.auth.models import User
from django.db import models


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Negocio(models.Model):
    nome = models.CharField('Nome', max_length=50)
    formas_entrega = models.SmallIntegerField('Formas de entrega', default=0)
    valor_minimo = models.PositiveSmallIntegerField(
        'Valor mínimo para entrega', default=0)
    formas_pagamento = models.CharField(
        'Formas de pagamento', max_length=100, default='')
    endereco = models.CharField(
        'Endereço', max_length=120, null=True, blank=True)
    taxa_padrao_entrega = models.PositiveSmallIntegerField(
        'Taxa padrão de entrega', default=0)


class Contato(models.Model):
    nome = models.CharField('Nome', max_length=50)
    telefone = models.CharField('Telefone', max_length=12)
    negocio = models.ForeignKey('Negocio', on_delete=models.CASCADE)
    instagram = models.CharField(
        'Instagram', max_length=30, null=True, blank=True)
    possui_whatsapp = models.BooleanField(
        'Atendimento por Whatsapp?', default=False)


class NegocioUsuario(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    negocio = models.ForeignKey('Negocio', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'negocio')


class Produto(models.Model):
    nome = models.CharField('Nome', max_length=30)
    negocio = models.ForeignKey('Negocio', on_delete=models.CASCADE)
    preco = models.PositiveSmallIntegerField('Preço')
    categoria = models.ForeignKey(
        'Categoria', on_delete=models.SET_NULL, blank=True, null=True)


class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=30)


class RegiaoEntrega(models.Model):
    nome = models.CharField('Nome', max_length=30)


class NegocioRegiaoEntrega(models.Model):
    regiao = models.ForeignKey('RegiaoEntrega', on_delete=models.CASCADE)
    negocio = models.ForeignKey('Negocio', on_delete=models.CASCADE)
    taxa_entrega = models.PositiveSmallIntegerField('Taxa de entrega')

    class Meta:
        unique_together = ('regiao', 'negocio')


class NegocioHorarioEntrega(models.Model):
    descricao = models.CharField('Descrição', max_length=100)
    negocio = models.ForeignKey('Negocio', on_delete=models.CASCADE)
