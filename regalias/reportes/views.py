from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, AdminPasswordChangeForm
from django.conf import settings
from django.db.models import ProtectedError

from regalias.utility import admin_log_addition, admin_log_change, render_pdf

from ventas.models import Venta, DetalleVenta
from reportes.form import FechaSearchForm, MonthSelect, YearForm, EntreFechasSearchForm

import datetime

@login_required(login_url='/login/')
def ventas_fecha(request):
    fecha = datetime.datetime.now()
    form = FechaSearchForm(request.GET or None)
    if form.is_valid():
        fecha = form.cleaned_data['fecha']
    ventas = Venta.objects.filter(fecha=fecha)
    return render(request, 'reportes/ventas/ventasfecha.html', {
        'fecha':fecha,
        'ventas':ventas,
        'form':form,
    })

@login_required(login_url='/login/')
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk = venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    return render(request, 'reportes/ventas/detail_venta.html', {
        'venta': venta,
        'detalles': detalles,
    })

@login_required(login_url='/login/')
def pdf_ventas_fecha(request, year, month, day):
    fecha = datetime.date(year, month, day)
    ventas = Venta.objects.filter(fecha=fecha)
    html = render_to_string('reportes/ventas/pdf_ventasfecha.html', {
        'ventas':ventas,
        'fecha':fecha,
    })
    return render_pdf(html)

@login_required(login_url='/login/')
def ventas_mes(request):
    fecha = datetime.datetime.now()
    form = MonthSelect(request.GET or None)
    if form.is_valid():
        month = form.cleaned_data['month']
        year = form.cleaned_data['year']
        fecha = datetime.date(int(year), int(month), 1)
    ventas = Venta.objects.filter(fecha__month=fecha.month, fecha__year=fecha.year)
    return render(request, 'reportes/ventas/ventasmes.html', {
        'fecha': fecha,
        'ventas': ventas,
        'form': form,
    })

@login_required(login_url='/login/')
def pdf_ventas_mes(request, year, month):
    fecha = datetime.date(year, month, 1)
    ventas = Venta.objects.filter(fecha__month=fecha.month, fecha__year=fecha.year)
    html = render_to_string('reportes/ventas/pdf_ventasmes.html', {
        'ventas':ventas,
        'fecha':fecha,
    })
    return render_pdf(html)

@login_required(login_url='/login/')
def ventas_gestion(request):
    fecha = datetime.datetime.now()
    form = YearForm(request.GET or None)
    if form.is_valid():
        year = form.cleaned_data['year']
        fecha = datetime.date(int(year), 1, 1)
    ventas = Venta.objects.filter(fecha__year=fecha.year)
    return render(request, 'reportes/ventas/ventasyear.html', {
        'fecha': fecha,
        'ventas': ventas,
        'form': form,
    })

@login_required(login_url='/login/')
def pdf_ventas_gestion(request, year):
    fecha = datetime.date(year, 1, 1)
    ventas = Venta.objects.filter(fecha__year=fecha.year)
    html = render_to_string('reportes/ventas/pdf_ventasyear.html', {
        'ventas':ventas,
        'fecha':fecha,
    })
    return render_pdf(html)