# -*- coding: utf-8 -*-
from django.db import models


class PerformanceRequisicao(models.Model):
    data_hora_requisicao = models.DateTimeField('Data/hora da requisição')
    data_hora_resposta = models.DateTimeField('Data/hora da resposta')
    url = models.CharField('URL', max_length=255)
    user = models.ForeignKey('auth.User', blank=True,
                             null=True, on_delete=models.SET_NULL)
    metodo = models.CharField('Metodo', max_length=8)
