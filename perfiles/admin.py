from django.contrib import admin

# Register your models here.
from .models import Cliente
from .models import Evento
from .models import Operacion
from .models import Perfil
from .models import PerfilCliente
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'edad', 'sexo')
admin.site.register(Cliente,ClienteAdmin)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_tipoLista', 'discoteca', 'distrito')
    def get_tipoLista(self, obj):
        return obj.tipoLista
    get_tipoLista.short_description = 'Tipo de Lista'
admin.site.register(Evento,EventoAdmin)
class OperacionAdmin(admin.ModelAdmin):
    list_display = ('created', 'get_cliente', 'get_evento')
    def get_cliente(self, obj):
        return obj.cliente.nombre
    #get_cliente.admin_order_field  = 'cliente'
    get_cliente.short_description = 'Cliente'
    def get_evento(self, obj):
        return obj.evento.nombre
    #get_evento.admin_order_field  = 'evento'
    get_evento.short_description = 'Evento'
admin.site.register(Operacion, OperacionAdmin)
admin.site.register(Perfil)
admin.site.register(PerfilCliente)

#list_display = ('created', 'cliente','evento')
