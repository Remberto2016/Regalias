"""regalias URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings

from users.views import home


urlpatterns = [
    path('media/(<path>)', serve, {'document_root': settings.MEDIA_ROOT, }),
    path('static/(<path>)', serve, {'document_root': settings.STATIC_ROOT}),
    path('', home, name='index'),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('cliente/', include('clientes.urls')),
    path('materia/prima/', include('materiales.urls')),
    path('pedido/', include('pedidos.urls')),
    path('venta/', include('ventas.urls')),
    path('reporte/', include('reportes.urls')),
]
