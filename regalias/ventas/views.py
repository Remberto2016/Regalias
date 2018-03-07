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

from clientes.models import Cliente
from pedidos.models import Pedido, DetallePedido
from ventas.models import Venta, DetalleVenta

from ventas.form import DetalleVentaForm

@login_required(login_url='/login/')
def index(request):
    ventas = Venta.objects.filter(estado=True)
    return render(request, 'ventas/index.html', {
        'ventas':ventas,
    })

@login_required(login_url='/login/')
def new_list_cliente(request):
    clientes = Cliente.objects.filter(estado=True)
    return render(request, 'ventas/new_list_clientes.html', {
        'clientes':clientes,
    })

@login_required(login_url='/login/')
def new_venta(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk = cliente_id)
    venta = Venta.objects.create(
        cliente=cliente,
    )
    venta.save()
    admin_log_addition(request, venta, 'Venta Creada')
    messages.success(request, 'Empiece a Agregar Materiales')
    return HttpResponseRedirect(reverse(new_detail_venta, args={venta.id, }))

@login_required(login_url='/login/')
def new_detail_venta(request, venta_id):
    venta =  get_object_or_404(Venta, pk = venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    return render(request, 'ventas/new_detail_venta.html', {
        'venta':venta,
        'detalles':detalles,
    })

@login_required(login_url='/login/')
def add_material(request, venta_id):
    venta = get_object_or_404(Venta, pk = venta_id)
    if request.method == 'POST':
        form = DetalleVentaForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.venta = venta
            detalle.costo_t = detalle.cantidad * detalle.costo_u
            detalle.save()
            venta.costo = venta.costo + detalle.costo_t
            venta.save()
            admin_log_addition(request, detalle, 'Detalle Venta Creado')
            admin_log_change(request, venta, 'Costo Modificado')
            messages.success(request, 'Material Agredado Correctemente')
            return HttpResponseRedirect(reverse(new_detail_venta, args={venta.id, }))
    else:
        form = DetalleVentaForm()
    return render(request, 'ventas/add_material.html', {
        'venta':venta,
        'form':form,
    })

@login_required(login_url='/login/')
def delete_material(request, detalle_id):
    detalle = get_object_or_404(DetalleVenta, pk = detalle_id)
    venta = Venta.objects.get(pk = detalle.venta.id)
    venta.costo = venta.costo - detalle.costo_t
    venta.save()
    detalle.delete()
    admin_log_change(request, venta, 'Costo Modificado')
    messages.error(request, 'Material Eliminado')
    return HttpResponseRedirect(reverse(new_detail_venta, args={venta.id, }))

@login_required(login_url='/login/')
def confirm_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk = venta_id)
    venta.estado = True
    venta.save()
    messages.success(request, 'Venta Confirmada Correctamente')
    '''Redireccionar al reporte detalle venta'''
    return HttpResponseRedirect(reverse(index))

@login_required(login_url='/login/')
def ventas_no_confirmados(request):
    ventas = Venta.objects.filter(estado=False)
    return render(request, 'ventas/no_confirmados.html', {
        'ventas':ventas,
    })

@login_required(login_url='/login/')
def delete_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk = venta_id)
    detalle = DetalleVenta.objects.filter(venta=venta)
    for d in detalle:
        d.delete()
    venta.delete()
    messages.error(request, 'Pedido Eliminado')
    return HttpResponseRedirect(reverse(ventas_no_confirmados))

@login_required(login_url='/login/')
def detail_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk = venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    return render(request, 'ventas/detail_venta.html', {
        'venta': venta,
        'detalles': detalles,
    })

@login_required(login_url='/login/')
def list_pedidos(request):
    pedidos = Pedido.objects.filter(estado=True, venta=False)

    return render(request, 'ventas/pedidos_confirm.html', {
        'pedidos':pedidos,
    })

@login_required(login_url='/login/')
def detail_pedido_venta(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    return render(request, 'ventas/detail_pedido.html', {
        'pedido': pedido,
        'detalles': detalles,
    })

@login_required(login_url='/login/')
def venta_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    venta = Venta.objects.create(
        cliente=pedido.cliente,
        costo=pedido.costo,
        estado=True,
    )
    admin_log_addition(request, venta, 'Venta Pedido')
    venta.save()
    for d in detalles:
        detalle = DetalleVenta.objects.create(
            material=d.material,
            descripcion=d.descripcion,
            cantidad=d.cantidad,
            costo_u=d.costo_u,
            costo_t=d.costo_t,
            venta=venta,
        )
        detalle.save()
        admin_log_addition(request, detalle, 'Material Agregado')
        admin_log_change(request, venta, 'Material Agregado')
    pedido.venta = True
    pedido.save()
    return HttpResponseRedirect(reverse(detail_venta, args={venta.id, }))

@login_required(login_url='/login/')
def pdf_detail_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    html = render_to_string('ventas/pdf/detail.html', {
        'venta': venta,
        'detalles': detalles,
    })
    return render_pdf(html)