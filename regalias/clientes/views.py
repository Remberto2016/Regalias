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

from clientes.models import Pais, Ciudad, Cliente
from clientes.form import ClienteForm, CiudadForm, PaisForm

@login_required(login_url='/login/')
def index(request):
    clientes = Cliente.objects.filter(estado=True)
    return render(request, 'clientes/index.html', {
        'clientes':clientes,
    })

@login_required(login_url='/login/')
def new_pais(request):
    if request.method == 'POST':
        form = PaisForm(request.POST)
        if form.is_valid():
            p = form.save()
            admin_log_addition(request, p, 'Pais Creado')
            messages.success(request, 'Pais Registrado Correctamente')
            return HttpResponseRedirect(reverse(index))
    else:
        form = PaisForm()
    return render(request, 'clientes/new_pais.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def new_ciudad(request):
    ref = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CiudadForm(request.POST)
        if form.is_valid():
            c = form.save()
            admin_log_addition(request, c, 'Ciudad Creada')
            messages.success(request, 'Ciudad Registrada Correctamente')
            return HttpResponseRedirect(reverse(index))
    else:
        form = CiudadForm()
    return render(request, 'clientes/new_ciudad.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def new(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            c = form.save()
            admin_log_addition(request, c, 'Cliente Creado')
            messages.success(request, 'Cliente Registrado Correctamente')
            return HttpResponseRedirect(reverse(index))
    else:
        form = ClienteForm()
    return render(request, 'clientes/new.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def ajax_ciudades(request):
    if request.is_ajax():
        pais = get_object_or_404(Pais, pk = request.GET['id'])
        ciudades = Ciudad.objects.filter(pais=pais)
        html = render_to_string('clientes/__ajax_ciudades.html', {
            'ciudades':ciudades,
        })
        return JsonResponse(html, safe=False)
    else:
        raise Http404

@login_required(login_url='/login/')
def update(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk = cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            c = form.save()
            admin_log_addition(request, c, 'Cliente Modificado')
            messages.warning(request, 'Cliente Modificado Correctamente')
            return HttpResponseRedirect(reverse(index))
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/update.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def detail_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    return render(request, 'clientes/detail.html', {
        'cliente':cliente,
    })

@login_required(login_url='/login/')
def baja_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk = cliente_id)
    cliente.estado = False
    cliente.save()
    admin_log_change(request, cliente, 'Cliente Dado de Baja')
    messages.warning(request, 'Cliente Dado de Baja')
    return HttpResponseRedirect(reverse(index))

@login_required(login_url='/login/')
def baja_clientes(request):
    clientes = Cliente.objects.filter(estado = False)
    return render(request, 'clientes/baja_clientes.html', {
        'clientes':clientes,
    })

@login_required(login_url='/login/')
def activate_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    cliente.estado = True
    cliente.save()
    admin_log_change(request, cliente, 'Cliente Activado')
    messages.info(request, 'Cliente Activado')
    return HttpResponseRedirect(reverse(baja_clientes))

@login_required(login_url='/login/')
def pdf_clientes(request):
    clientes = Cliente.objects.filter(estado=True)
    html = render_to_string('clientes/pdf_clientes.html ', {
        'clientes':clientes,
    })
    return render_pdf(html)

@login_required(login_url='/login/')
def new_ciudad_popup(request):
    if request.method == 'POST':
        form = CiudadForm(request.POST)
        if form.is_valid():
            c = form.save()
            admin_log_addition(request, c, 'Ciudad Creada')
            return render(request, 'close_popup.html', {
                'c':c,
            })
    else:
        form = CiudadForm()
    return render(request, 'clientes/new_ciudad_popup.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def new_pais_popup(request):
    if request.method == 'POST':
        form = PaisForm(request.POST)
        if form.is_valid():
            p = form.save()
            admin_log_addition(request, p, 'Pais Creado')
            return render(request, 'close_popup.html', {
                'c':p,
            })
    else:
        form = PaisForm()
    return render(request, 'clientes/new_pais_popup.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def new_cliente_popup(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            p = form.save()
            admin_log_addition(request, p, 'Cliente Creado')
            return render(request, 'close_popup.html', {
                'c':p,
            })
    else:
        form = ClienteForm()
    return render(request, 'clientes/new_cliente_popup.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def update_cliente_popup(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk = cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            p = form.save()
            admin_log_addition(request, p, 'Cliente Modificado')
            messages.warning(request, 'Cliente Modificado Correctamente')
            return render(request, 'close_popup.html', {
            })
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/update_cliente_popup.html', {
        'form':form,
    })

