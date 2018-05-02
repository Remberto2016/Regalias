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


    path('pdf/<int:venta_id>/factura', views.factura_pdf, name='venta-pdf-factura'),


    path('ajax/precio/clavo', views.ajax_get_precio, name='venta-ajax-precio-clavo'),

]