from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='venta-index'),
    path('new/clientes', views.new_list_cliente, name='venta-list-clientes'),
    path('new/<int:cliente_id>/', views.new_venta, name='venta-new'),
    path('new/<int:venta_id>/detail', views.new_detail_venta, name='venta-new-detail'),
    path('new/<int:venta_id>/add/material', views.add_material, name='venta-new-add-material'),
    path('new/<int:detalle_id>/delete/material', views.delete_material, name='venta-new-delete-material'),
    path('confirm/<int:venta_id>', views.confirm_venta, name='venta-confirm'),

    path('no/confirm/', views.ventas_no_confirmados, name='venta-no-confirmados'),
    path('<int:venta_id>/delete', views.delete_venta, name='venta-delete'),
    path('<int:venta_id>/detail', views.detail_venta, name='venta-detail'),
    path('pedidos/', views.list_pedidos, name='venta-list-pedidos'),
    path('pedido/<int:pedido_id>/detail', views.detail_pedido_venta, name='venta-pedido-detail'),
    path('pedido/<int:pedido_id>/vent/', views.venta_pedido, name='venta-pedido-vent'),

    path('pdf/<int:venta_id>/detail', views.pdf_detail_venta, name='venta-pdf-detail'),
    path('pdf/<int:venta_id>/recibo', views.pdf_recibo_venta, name='venta-pdf-recibo'),


    path('pdf/<int:venta_id>/factura', views.factura_pdf, name='venta-pdf-factura'),


    path('ajax/precio/clavo', views.ajax_get_precio, name='venta-ajax-precio-clavo'),

    path('calamina/new/clientes', views.calamina_new_list_cliente, name='venta-list-clientes-calamina'),
    path('calamina/new/<int:cliente_id>/', views.calamina_new_venta, name='venta-new-calamina'),
    path('calamina/new/<int:venta_id>/detail', views.calamina_new_detail_venta, name='venta-new-detail-calamina'),

    path('calamina/add/new/material/<int:venta_id>/calamina', views.add_new_material_calamina, name='venta-new-add-material-calamina-new'),

    path('calamina/new/<int:venta_id>/add/material', views.calamina_add_material, name='venta-new-add-material-calamina'),
    path('calamina/<int:detalle_id>/delete', views.calamina_delete_material, name='venta-delete-calamina'),

    path('ajax/calamina/precio/', views.ajax_get_precio_calamina, name='pedido-ajax-precio-calamina'),
    path('ajax/calamina/material/color', views.ajax_get_materiales_calamina, name='pedido-ajax-material-calamina'),


    path('ajax/preiciocalamina/material', views.ajax_precio_calamina, name='pedido-ajax-precio-calamina'),

]