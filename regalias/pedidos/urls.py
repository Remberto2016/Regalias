from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='pedido-index'),
    path('new/clientes', views.new_list_cliente, name='pedido-list-clientes'),
    path('new/<int:cliente_id>/pedido', views.new_pedido, name='pedido-new'),
    path('new/<int:pedido_id>/detail', views.new_detail_pedido, name='pedido-new-detail'),
    path('new/<int:pedido_id>/<int:detalle_id>/update/material', views.update_material, name='pedido-update-material'),
    path('new/<int:pedido_id>/add/material', views.add_material, name='pedido-new-add-material'),
    path('new/<int:detalle_id>/delete/material', views.delete_material, name='pedido-new-delete-material'),
    path('confirm/<int:pedido_id>', views.confirm_pedido, name='pedido-confirm'),
    path('detail/<int:pedido_id>', views.detail_pedido, name='pedido-detail'),

    path('pedido/<int:pedido_id>/add/new/material', views.add_new_material_calamina, name='pedido-new-add-material-calamina-new'),


    path('no/confirm/', views.pedidos_no_confirmados, name='pedido-no-confirmados'),
    path('<int:pedido_id>/delete', views.delete_pedido, name='pedido-delete'),
    path('vendidos/', views.pedidos_vendidos, name='pedido-vendidos'),

    path('pdf/detail/<int:pedido_id>', views.pdf_detail_pedido, name='pedido-pdf-detail'),
    path('pdf/proforma/<int:pedido_id>', views.pdf_proforma, name='pedido-pdf-proforma'),


    path('ajax/precio/', views.ajax_get_precio, name='pedido-ajax-precio'),
    path('ajax/material/color', views.ajax_get_materiales, name='pedido-ajax-material'),

    path('list/orden/production', views.list_orden_produccion, name='pedido-list-orden-production'),
    path('list/orden/<int:pedido_id>', views.realizar_orden, name='pedido-list-realizar-orden'),
    path('list/orden/production/realizado', views.list_orden_produccion_realizado, name='pedido-list-orden-production-realizado'),
]