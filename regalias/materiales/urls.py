from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='materia-index'),
    path('alambron', views.index_alambron, name='materia-index-alambrom'),

    path('new', views.new, name='materia-new'),
    path('<int:materia_id>/update', views.update, name='materia-update'),
    path('<int:materia_id>/baja', views.baja_material, name='materia-baja'),

    path('<int:materia_id>/detail', views.detail_materia, name='materia-detail'),
    path('usada', views.materia_usada, name='materia-usada'),
    path('usada/<int:materia_id>/activate', views.activate_materia, name='materia-activate'),
    path('pdf', views.pdf_materia_prima, name='materia-pdf'),
    path('pdf/alambron', views.pdf_materia_prima_alambron, name='materia-pdf-alambron'),
    path('proveedor/month', views.materiap_proveedor, name='materia-proveedor'),
    path('proveedor/month/<int:proveedor_id>/<int:mes>/<int:year>/', views.pdf_materiap_proveedor, name='materia-proveedor-pdf'),
    path('inventario', views.inventario_calaminas, name='inventario-calamina'),

    path('new/popup', views.new_popup, name='materia-new-popup'),

    path('new/popup/codigo/materia', views.new_popup_codigomateria, name='materia-new-popup-codigo'),

    path('configuracion', views.codigos_materiales_primas, name='index-configuracion'),
    path('configuracion/<int:codprimas_id>', views.update_codigo_materia_prima, name='update-codigo-materia-prima-configuracion-popup'),
    #path('configuracion/<int:codprimas_id>/eliminado/', views.delete_codigo_materia_prima, name='delete-codigo-materia-prima'),
    #path('configuracion/<int:codprimas_id>/activado/', views.activate_codigo_materia_prima, name='activate-codigo-materia-prima'),
    path('configuracion/precio/<int:codprecios_id>/', views.update_codigo_precio_calamina, name='update-codigo-precio-calamina-popup'),

    path('configuracion/precio/<int:codtipos_id>/tipo/', views.update_tipo_calamina, name='update-tipo-calamina-popup'),
    path('configuracion/precio/<int:codclavos_id>/clavo/', views.update_codigo_clavo, name='update-codigo-clavo-popup'),

    path('proveedor', views.index_proveedor, name='proveedor-index'),
    path('proveedor/new', views.new_proveedor, name='proveedor-new'),
    path('popup/proveedor/new', views.new_proveedor_popup, name='proveedor-new-popup'),
    path('popup/<int:proveedor_id>/update', views.update_proveedor_popup, name='proveedor-update-popup'),
    path('proveedor/<int:proveedor_id>/update', views.update_proveedor, name='proveedor-update'),
    path('proveedor/<int:proveedor_id>/baja', views.baja_proveedor, name='proveedor-baja'),
    path('proveedor/<int:proveedor_id>/activate', views.activate_proveedor, name='proveedor-activate'),
    path('proveedor/<int:proveedor_id>/detail', views.detail_proveedor, name='proveedor-detail'),
    path('proveedor/bajas', views.baja_proveedores, name='proveedor-list-bajas'),
    path('proveedores/pdf/', views.pdf_proveedores, name='proveedor-pdf'),

    path('precio', views.index_precios, name='precio-index'),
    path('precio/precio', views.new_precio, name='precio-new'),
    path('precio/new/codigocalamina/popup', views.new_codigo_calamina_popup, name='precio-codigo-calamina-popup'),
    path('precio/new/tipocalamina/popup', views.new_tipocalamina_popup, name='precio-tipo-calamina-popup'),
    path('precio/popup/<int:precio_id>/update', views.update_precio_precio_popup, name='precio-precio-update-popup'),


    path('precio/<int:precio_id>/update', views.update_precio, name='precio-update'),
    path('precio/bajas', views.precios_baja, name='precio-list-baja'),
    path('precio/<int:precio_id>/baja', views.baja_precio, name='precio-baja'),
    path('precio/<int:precio_id>/activate', views.active_precio, name='precio-active'),

    path('clavo/precio', views.index_precios_clavos, name='precio-index-clavos'),
    path('clavo/precio/precio', views.new_precio_clavo, name='precio-new-clavo'),
    path('clavo/new/codigoclavo/popup', views.new_codigo_clavo_popup, name='precio-codigo-clavo-popup'),
    path('clavo/precio/<int:precio_id>/update', views.update_precio_clavo, name='precio-update-clavo'),
    path('clavo/precio/bajas', views.precios_baja_clavo, name='precio-list-baja-clavo'),
    path('clavo/precio/<int:precio_id>/baja', views.baja_precio_clavo, name='precio-baja-clavo'),
    path('clavo/precio/<int:precio_id>/activate', views.active_precio_clavo, name='precio-active-clavo'),
    path('clavo/<int:precio_id>/stock', views.stock_clavo, name='precio-stock-clavo'),

    path('clavo/inventario/', views.index_inventario, name='index_inventario'),
    path('clavo/inventario/pdf/', views.pdf_inventario_clavo, name='pdf-inventario-clavo'),

    


    path('ajax/material', views.ajax_get_material, name='material-ajax-material'),

    path('ajax/colored/list', views.ajax_color_codigo, name='material-ajax-color-colored'),
    path('ajax/colored/colored/list', views.ajax_color_colored, name='material-ajax-color-colored-nombre'),

]