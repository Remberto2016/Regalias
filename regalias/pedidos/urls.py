from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='pedido-index'),
    path('new/clientes', views.new_list_cliente, name='pedido-list-clientes'),
    path('new/<int:cliente_id>/pedido', views.new_pedido, name='pedido-new'),
    path('new/<int:pedido_id>/detail', views.new_detail_pedido, name='pedido-new-detail'),
    path('new/<int:pedido_id>/add/material', views.add_material, name='pedido-new-add-material'),
    path('new/<int:detalle_id>/delete/material', views.delete_material, name='pedido-new-delete-material'),
    path('confirm/<int:pedido_id>', views.confirm_pedido, name='pedido-confirm'),
    path('detail/<int:pedido_id>', views.detail_pedido, name='pedido-detail'),

    path('no/confirm/', views.pedidos_no_confirmados, name='pedido-no-confirmados'),
    path('<int:pedido_id>/delete', views.delete_pedido, name='pedido-delete'),
    path('vendidos/', views.pedidos_vendidos, name='pedido-vendidos'),

]