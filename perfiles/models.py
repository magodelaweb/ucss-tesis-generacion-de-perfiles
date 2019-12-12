from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Cliente(models.Model):
    STATUS_CHOICES = (
        ('habilitado', 'Habilitado'),
        ('borrado', 'Borrado'),
    )
    SEXO = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    nombre = models.CharField(max_length=150)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=10,
                              choices=SEXO,
                              default='M')
    created = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='habilitado')
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return self.nombre

class Evento(models.Model):
    STATUS_CHOICES = (
        ('abierto', 'Abierto'),
        ('cerrado', 'Cerrado'),
        ('borrado', 'Borrado'),
    )
    TIPO_LISTA = (
        ('general', 'General'),
        ('vip', 'VIP'),
    )
    DISCOTECA = (
        ('mia', 'Mia'),
        ('hula', 'Hula'),
        ('ccb', 'CCB'),
    )
    DISTRITO = (
        ('surco', 'Surco'),
        ('barranco', 'Barranco'),
    )
    nombre = models.CharField(max_length=150)
    tipoLista = models.CharField(max_length=10,
                              choices=TIPO_LISTA,
                              default='general')
    discoteca = models.CharField(max_length=10,
                              choices=DISCOTECA,
                              default='mia')
    distrito = models.CharField(max_length=10,
                              choices=DISTRITO,
                              default='surco')
    created = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='abierto')
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return self.nombre

class Operacion(models.Model):
    cliente = models.ForeignKey(
    Cliente,
    on_delete=models.CASCADE,
    verbose_name="el cliente que realiza la operación",
    )
    evento = models.ForeignKey(
    Evento,
    on_delete=models.CASCADE,
    verbose_name="el evento al que asiste el cliente",
    )
    created = models.DateTimeField(auto_now_add=True)    
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return str(self.created)

class Perfil(models.Model):
    nombre = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return str(self.nombre)
class PerfilCliente(models.Model):
    perfil = models.ForeignKey(
    Perfil,
    on_delete=models.CASCADE,
    verbose_name="el perfil asociado",
    )
    cliente = models.ForeignKey(
    Cliente,
    on_delete=models.CASCADE,
    verbose_name="el cliente que pertenece a este perfil",
    )
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return str(self.id)
