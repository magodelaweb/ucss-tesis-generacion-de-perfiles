# Generated by Django 3.0 on 2019-12-09 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0003_operacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='sexo',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='M', max_length=10),
        ),
    ]
