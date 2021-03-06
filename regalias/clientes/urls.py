from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cliente-index'),
    path('new/ciudad', views.new_ciudad, name='cliente-new-ciudad'),
    path('popup/new/ciudad', views.new_ciudad_popup, name='cliente-new-ciudad-popup'),
    path('new/pais', views.new_pais, name='cliente-new-pais'),
    path('popup/new/pais', views.new_pais_popup, name='cliente-new-pais-popup'),
    path('new', views.new, name='cliente-new'),
    path('popup/new', views.new_cliente_popup, name='cliente-new-popup'),
        path('popup/<int:cliente_id>/update', views.update_cliente_popup, name='update_cliente_popup'),
    path('<int:cliente_id>/update', views.update, name='cliente-update'),
    path('<int:cliente_id>/baja', views.baja_cliente, name='cliente-baja'),
    path('<int:cliente_id>/activate', views.activate_cliente, name='cliente-activate'),
    path('<int:cliente_id>/detail', views.detail_cliente, name='cliente-detail'),
    path('list/bajas', views.baja_clientes, name='cliente-list-bajas'),
    path('pdf/clientes', views.pdf_clientes, name='cliente-pdf'),


    path('ajax/ciudades', views.ajax_ciudades, name='cliente-ajax-ciudades'),
]