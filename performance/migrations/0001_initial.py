# Generated by Django 3.0.2 on 2020-02-20 02:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerformanceRequisicao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora_requisicao', models.DateTimeField(verbose_name='Data/hora da requisição')),
                ('data_hora_resposta', models.DateTimeField(verbose_name='Data/hora da resposta')),
                ('url', models.CharField(max_length=255, verbose_name='URL')),
                ('metodo', models.CharField(max_length=8, verbose_name='Metodo')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
