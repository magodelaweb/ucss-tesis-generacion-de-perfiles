# Generated by Django 3.0 on 2019-12-09 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0004_auto_20191209_0324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='discoteca',
            field=models.CharField(choices=[('mia', 'Mia'), ('hula', 'Hula'), ('ccb', 'CCB')], default='mia', max_length=10),
        ),
        migrations.AlterField(
            model_name='evento',
            name='distrito',
            field=models.CharField(choices=[('surco', 'Surco'), ('barranco', 'Barranco')], default='mia', max_length=10),
        ),
    ]