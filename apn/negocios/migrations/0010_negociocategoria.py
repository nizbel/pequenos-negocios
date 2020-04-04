# Generated by Django 3.0.4 on 2020-04-03 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('negocios', '0009_auto_20200328_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='NegocioCategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='negocios.Categoria')),
                ('negocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorias', to='negocios.Negocio')),
            ],
        ),
    ]
