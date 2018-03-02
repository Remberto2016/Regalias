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

from regalias.utility import admin_log_addition, admin_log_change

from materiales.models import MateriaPrima, Proveedor

from materiales.form import MateriaPForm, ProveedorForm

@login_required(login_url='/login/')
def index(request):
    materiales = MateriaPrima.objects.filter(estado=True)
    return render(request, 'materiap/index.html', {
        'materiales':materiales,
    })

@login_required(login_url='/login/')
def new(request):
    if request.method == 'POST':
        form = MateriaPForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            m.user = request.user
            m.save()
            admin_log_addition(request, m, 'Materia Prima Creada')
            messages.success(request, 'Materia Prima Creada Correctamente')
            return HttpResponseRedirect(reverse(index))
    else:
        form = MateriaPForm()
    return render(request, 'materiap/new.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def update(request, materia_id):
    materia = get_object_or_404(MateriaPrima, pk = materia_id)
    if request.method == 'POST':
        form = MateriaPForm(request.POST, instance=materia)
        if form.is_valid():
            m = form.save()
            admin_log_change(request, m, 'Materia Prima Modificada')
            messages.warning(request, 'Materia Prima Modificada Correctamente')
            return HttpResponseRedirect(reverse(index))
    else:
        form = MateriaPForm(instance=materia)
    return render(request, 'materiap/update.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def baja_material(request, materia_id):
    materia = get_object_or_404(MateriaPrima, pk = materia_id)
    materia.estado = False
    materia.save()
    admin_log_change(request, materia, 'Materia Dado de Baja')
    messages.warning(request, 'Materia Prima dado de baja')
    return HttpResponseRedirect(reverse(index))

@login_required(login_url='/login/')
def detail_materia(request, materia_id):
    materia = get_object_or_404(MateriaPrima, pk = materia_id)
    return render(request, 'materiap/detail.html', {
        'materia':materia,
    })

@login_required(login_url='/login/')
def materia_usada(request):
    materiales = MateriaPrima.objects.filter(estado=False)
    return render(request, 'materiap/materia_usada.html', {
        'materiales':materiales,
    })

@login_required(login_url='/login/')
def index_proveedor(request):
    proveedores = Proveedor.objects.filter(estado=True)
    return render(request, 'proveedores/index.html', {
        'proveedores':proveedores,
    })

@login_required(login_url='/login/')
def new_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            pro = form.save()
            admin_log_addition(request, pro, 'Proveedor Registrado')
            sms = 'Proveedor Registrado Correctamente'
            messages.success(request, sms)
            return HttpResponseRedirect(reverse(index_proveedor))
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/new.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def update_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk = proveedor_id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            pro = form.save()
            admin_log_change(request, pro, 'Proveedor Modificado')
            sms = 'Proveedor Modificado Correctamente'
            messages.warning(request, sms)
            return HttpResponseRedirect(reverse(index_proveedor))
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/update.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def baja_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk = proveedor_id)
    proveedor.estado = False
    proveedor.save()
    admin_log_change(request, proveedor, 'Proveedor Dado de Baja')
    messages.error(request, 'Proveedor Dado de Baja')
    return HttpResponseRedirect(reverse(index_proveedor))

@login_required(login_url='/login/')
def activate_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk = proveedor_id)
    proveedor.estado = True
    proveedor.save()
    admin_log_change(request, proveedor, 'Proveedor Activado')
    messages.info(request, 'Proveedor Activado')
    return HttpResponseRedirect(reverse(index_proveedor))

@login_required(login_url='/login/')
def detail_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk = proveedor_id)
    return render(request, 'proveedores/detail.html', {
        'proveedor':proveedor,
    })

@login_required(login_url='/login/')
def baja_proveedores(request):
    proveedores = Proveedor.objects.filter(estado=False)
    return render(request, 'proveedores/baja_proveedores.html', {
        'proveedores':proveedores,
    })