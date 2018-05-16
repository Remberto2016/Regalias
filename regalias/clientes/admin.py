from django.contrib import admin

from clientes.models import Cliente, Ciudad, Pais

admin.site.register(Pais)
admin.site.register(Ciudad)
admin.site.register(Cliente)