from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class InfoPerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def my_handler(sender, instance, created, **kwargs):
    if created:
        InfoPerfilUsuario.objects.create(user=instance)


class Negocio(models.Model):
    FORMAS_ENTREGA_CHOICES = [
        (1, 'Delivery'), (2, 'Take Out'), (3, 'Delivery e Take Out')
    ]

    nome = models.CharField('Nome', max_length=50)
    formas_entrega = models.SmallIntegerField('Formas de entrega', default=0,
                                              choices=FORMAS_ENTREGA_CHOICES)
    valor_minimo = models.PositiveSmallIntegerField(
        'Valor mínimo para entrega', default=0)
    formas_pagamento = models.CharField(
        'Formas de pagamento', max_length=100, default='')
    endereco = models.CharField(
        'Endereço', max_length=120, null=True, blank=True)
    taxa_padrao_entrega = models.PositiveSmallIntegerField(
        'Taxa padrão de entrega', default=0)
    instagram = models.CharField(
        'Instagram', max_length=30, default='')

    def __str__(self):
        return self.nome

    @property
    def responsaveis(self):
        return NegocioUsuario.objects.filter(negocio=self) \
            .values_list('usuario', flat=True)

    @property
    def categorias(self):
        return Produto.objects.filter(negocio=self) \
            .values('categoria').distinct()


class Contato(models.Model):
    nome = models.CharField('Nome', max_length=50, default='')
    telefone = models.CharField('Telefone', max_length=12)
    negocio = models.ForeignKey(
        'Negocio', on_delete=models.CASCADE, related_name='contatos')
    instagram = models.CharField(
        'Instagram', max_length=30, null=True, blank=True)
    possui_whatsapp = models.BooleanField(
        'Atendimento por Whatsapp?', default=False)

    def __str__(self):
        return self.nome


class NegocioUsuario(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    negocio = models.ForeignKey('Negocio', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'negocio')


class Produto(models.Model):
    nome = models.CharField('Nome', max_length=50)
    negocio = models.ForeignKey('Negocio', on_delete=models.CASCADE)
    preco = models.PositiveSmallIntegerField('Preço', default=0)
    categoria = models.ForeignKey(
        'Categoria', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=30)

    def __str__(self):
        return self.nome


class RegiaoEntrega(models.Model):
    nome = models.CharField('Nome', max_length=30)

    def __str__(self):
        return self.nome


class NegocioRegiaoEntrega(models.Model):
    regiao = models.ForeignKey('RegiaoEntrega', on_delete=models.CASCADE)
    negocio = models.ForeignKey(
        'Negocio', on_delete=models.CASCADE, related_name="regioes_entrega")
    taxa_entrega = models.PositiveSmallIntegerField(
        'Taxa de entrega', default=0)

    class Meta:
        unique_together = ('regiao', 'negocio')


class NegocioHorarioEntrega(models.Model):
    descricao = models.CharField('Descrição', max_length=100)
    negocio = models.ForeignKey('Negocio', on_delete=models.CASCADE)
