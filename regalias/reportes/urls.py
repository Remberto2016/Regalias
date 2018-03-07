from django.urls import path
from . import views

urlpatterns = [
    path('ventas/fecha', views.ventas_fecha, name='reporte-venta-fecha'),
    path('ventas/<int:venta_id>/detail', views.detalle_venta, name='reporte-venta-detail'),
    path('pdf/ventas/<int:year>/<int:month>/<int:day>/fecha/', views.pdf_ventas_fecha, name='reporte-pdf-ventas-fecha'),
    path('ventas/mes', views.ventas_mes, name='reporte-venta-mes'),
    path('pdf/ventas/<int:year>/<int:month>/mes/', views.pdf_ventas_mes, name='reporte-pdf-ventas-mes'),
    path('ventas/gestion', views.ventas_gestion, name='reporte-venta-year'),
    path('pdf/ventas/<int:year>/gestion/', views.pdf_ventas_gestion, name='reporte-pdf-ventas-year'),

]