# Generated by Django 3.0 on 2019-12-09 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('tipoLista', models.CharField(choices=[('general', 'General'), ('vip', 'VIP')], default='general', max_length=10)),
                ('discoteca', models.CharField(max_length=150)),
                ('distrito', models.CharField(max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('abierto', 'Abierto'), ('cerrado', 'Cerrado'), ('borrado', 'Borrado')], default='abierto', max_length=10)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
