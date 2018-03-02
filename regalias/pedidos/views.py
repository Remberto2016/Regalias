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

from clientes.models import Cliente
from pedidos.models import Pedido, DetallePedido

from pedidos.form import DetallePedidoForm

@login_required(login_url='/login/')
def index(request):
    pedidos = Pedido.objects.filter(estado=True, venta=False)
    return render(request, 'pedidos/index.html', {
        'pedidos':pedidos,
    })

@login_required(login_url='/login/')
def new_list_cliente(request):
    clientes = Cliente.objects.filter(estado=True)
    return render(request, 'pedidos/new_list_clientes.html', {
        'clientes':clientes,
    })

@login_required(login_url='/login/')
def new_pedido(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk = cliente_id)
    pedido = Pedido.objects.create(
        cliente=cliente,
    )
    pedido.save()
    admin_log_addition(request, pedido, 'Pedido Creado')
    messages.success(request, 'Empiece a Agregar Materiales')
    return HttpResponseRedirect(reverse(new_detail_pedido, args={pedido.id, }))

@login_required(login_url='/login/')
def new_detail_pedido(request, pedido_id):
    pedido =  get_object_or_404(Pedido, pk = pedido_id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    return render(request, 'pedidos/new_detail_pedido.html', {
        'pedido':pedido,
        'detalles':detalles,
    })

@login_required(login_url='/login/')
def add_material(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    if request.method == 'POST':
        form = DetallePedidoForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.pedido = pedido
            detalle.costo_t = detalle.cantidad * detalle.costo_u
            detalle.save()
            pedido.costo = pedido.costo + detalle.costo_t
            pedido.save()
            admin_log_addition(request, detalle, 'Detalle Creado')
            admin_log_change(request, pedido, 'Costo Modificado')
            messages.success(request, 'Material Agredado Correctemente')
            return HttpResponseRedirect(reverse(new_detail_pedido, args={pedido.id, }))
    else:
        form = DetallePedidoForm()
    return render(request, 'pedidos/add_material.html', {
        'pedido':pedido,
        'form':form,
    })

@login_required(login_url='/login/')
def delete_material(request, detalle_id):
    detalle = get_object_or_404(DetallePedido, pk = detalle_id)
    pedido = Pedido.objects.get(pk = detalle.pedido.id)
    pedido.costo = pedido.costo - detalle.costo_t
    pedido.save()
    detalle.delete()
    admin_log_change(request, pedido, 'Costo Modificado')
    messages.error(request, 'Material Eliminado')
    return HttpResponseRedirect(reverse(new_detail_pedido, args={pedido.id, }))

@login_required(login_url='/login/')
def confirm_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    pedido.estado = True
    pedido.save()
    messages.success(request, 'Pedido Confirmado Correctamente')
    return HttpResponseRedirect(reverse(index))

@login_required(login_url='/login/')
def pedidos_no_confirmados(request):
    pedidos = Pedido.objects.filter(estado=False)
    return render(request, 'pedidos/no_confirmados.html', {
        'pedidos':pedidos,
    })

@login_required(login_url='/login/')
def delete_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    detalle = DetallePedido.objects.filter(pedido=pedido)
    for d in detalle:
        d.delete()
    pedido.delete()
    messages.error(request, 'Pedido Eliminado')
    return HttpResponseRedirect(reverse(pedidos_no_confirmados))

@login_required(login_url='/login/')
def pedidos_vendidos(request):
    pedidos = Pedido.objects.filter(venta=True)
    return render(request, 'pedidos/pedidos_vendidos.html', {
        'pedidos':pedidos,
    })

@login_required(login_url='/login/')
def detail_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    html = render_to_string('pedidos/pdf/detail.html', {
        'pedido':pedido,
        'detalles':detalles,
    })
    return render(request, 'pedidos/detail_pedido.html', {
        'pedido': pedido,
        'detalles': detalles,
        'html':html,
    })