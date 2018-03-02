from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cliente-index'),
    path('new/ciudad', views.new_ciudad, name='cliente-new-ciudad'),
    path('new/pais', views.new_pais, name='cliente-new-pais'),
    path('new', views.new, name='cliente-new'),
    path('<int:cliente_id>/update', views.update, name='cliente-update'),
    path('<int:cliente_id>/baja', views.baja_cliente, name='cliente-baja'),
    path('<int:cliente_id>/activate', views.activate_cliente, name='cliente-activate'),
    path('<int:cliente_id>/detail', views.detail_cliente, name='cliente-detail'),
    path('list/bajas', views.baja_clientes, name='cliente-list-bajas'),

    path('ajax/ciudades', views.ajax_ciudades, name='cliente-ajax-ciudades'),
]