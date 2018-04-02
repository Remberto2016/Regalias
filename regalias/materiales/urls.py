from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='materia-index'),
    path('new', views.new, name='materia-new'),
    path('<int:materia_id>/update', views.update, name='materia-update'),
    path('<int:materia_id>/baja', views.baja_material, name='materia-baja'),
    path('<int:materia_id>/detail', views.detail_materia, name='materia-detail'),
    path('usada', views.materia_usada, name='materia-usada'),
    path('pdf', views.pdf_materia_prima, name='materia-pdf'),
    path('proveedor/month', views.materiap_proveedor, name='materia-proveedor'),
    path('proveedor/month/<int:proveedor_id>/<int:mes>/<int:year>/', views.pdf_materiap_proveedor, name='materia-proveedor-pdf'),


    path('proveedor', views.index_proveedor, name='proveedor-index'),
    path('proveedor/new', views.new_proveedor, name='proveedor-new'),
    path('proveedor/<int:proveedor_id>/update', views.update_proveedor, name='proveedor-update'),
    path('proveedor/<int:proveedor_id>/baja', views.baja_proveedor, name='proveedor-baja'),
    path('proveedor/<int:proveedor_id>/activate', views.activate_proveedor, name='proveedor-activate'),
    path('proveedor/<int:proveedor_id>/detail', views.detail_proveedor, name='proveedor-detail'),
    path('proveedor/bajas', views.baja_proveedores, name='proveedor-list-bajas'),
    path('proveedores/pdf/', views.pdf_proveedores, name='proveedor-pdf'),

    path('precio', views.index_precios, name='precio-index'),
    path('precio/precio', views.new_precio, name='precio-new'),
    path('precio/<int:precio_id>/update', views.update_precio, name='precio-update'),
    path('precio/bajas', views.precios_baja, name='precio-list-baja'),
    path('precio/<int:precio_id>/baja', views.baja_precio, name='precio-baja'),
    path('precio/<int:precio_id>/activate', views.active_precio, name='precio-active'),

]