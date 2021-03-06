from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext, Context
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, AdminPasswordChangeForm
from django.conf import settings
from django.db.models import ProtectedError, Max

from regalias.utility import admin_log_addition, admin_log_change, render_pdf

from clientes.models import Cliente
from materiales.models import Precio, MateriaPrima, PrecioCalamina
from pedidos.models import Pedido, DetallePedido

from pedidos.form import DetallePedidoForm, ConfirmForm
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext, Context
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, AdminPasswordChangeForm
from django.conf import settings
from django.db.models import ProtectedError, Max

from regalias.utility import admin_log_addition, admin_log_change, render_pdf

from clientes.models import Cliente
from materiales.models import Precio, MateriaPrima
from pedidos.models import Pedido, DetallePedido

from pedidos.form import DetallePedidoForm, ConfirmForm
import datetime

from datetime import timedelta
@login_required(login_url='/login/')
def index(request):
    pedidos = Pedido.objects.filter(estado=True, venta=False)
    return render(request, 'pedidos/index.html', {
        'pedidos':pedidos,
    })

@login_required(login_url='/login/')
def new_list_cliente(request):
    clientes = Cliente.objects.filter(estado=True)
    messages.warning(request, 'Selecione Clente Para la Cotización')
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
    precios = PrecioCalamina.objects.filter(estado=True)
    return render(request, 'pedidos/new_detail_pedido.html', {
        'pedido':pedido,
        'detalles':detalles,
        'precios':precios,
    })


@login_required(login_url='/login')
def add_new_material_calamina(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    if request.method == 'POST':
        stock = 0
        codigo = request.POST['preciocalamina_id'] #PrecioCalamina_id
        preciocalamina = get_object_or_404(PrecioCalamina, pk = codigo)
        cantidad = request.POST['cantidad_id']
        largo = request.POST['largo_id']
        totalm = float(cantidad) * float(largo)
        materials = MateriaPrima.objects.filter(estado=True, color=preciocalamina.color.color, espesor=preciocalamina.espesor, stock__gte=float(totalm))
        #=color, stock__gte=float(totalm), ancho=materia_id.ancho)
        if not materials:
            messages.error(request, 'No Exite Materia Prima Disponible')
            return HttpResponseRedirect(reverse(add_new_material_calamina, args={pedido.id, }))
        else:
            detalle = DetallePedido.objects.create(
                unidad = 'Calamina',
                preciocalamina=preciocalamina,
                descripcion=preciocalamina.tipo.tipo,
                cantidad=int(cantidad),
                largo=largo,
                costo_u=preciocalamina.precio,
                costo_t=preciocalamina.precio * totalm,
                pedido=pedido,
                color=preciocalamina.color.color,
                ancho=preciocalamina.ancho,
                totalm=totalm,
            )
            detalle.save()
            for materia in materials:
                stock += materia.stock
                stock += materia.stock
                if stock >= totalm:
                    detalle.material.add(materia)
                    materia.salida = materia.salida + totalm
                    materia.stock = materia.stock - totalm
                    materia.save()
                    break
            pedido.costo = pedido.costo + detalle.costo_t
            pedido.save()
            admin_log_addition(request, detalle, 'Detalle pedido Creado')
            admin_log_change(request, pedido, 'Costo Modificado')
            messages.success(request, 'Material Agredado Correctemente')
            return HttpResponseRedirect(reverse(new_detail_pedido, args={pedido_id, }))
    else:
        return HttpResponseRedirect(reverse(new_detail_pedido, args={pedido_id, }))

@login_required(login_url='/login/')
def add_material(request, pedido_id):
    #
    colors = MateriaPrima.objects.filter(estado=True, stock__gte = 1)
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    if request.method == 'POST':
        form = DetallePedidoForm(request.POST)
        if form.is_valid():
            stock = 0
            color = form.cleaned_data['color']
            materia_id = form.cleaned_data['anchocalamina']
            precioc = form.cleaned_data['calamina']
            umedida = form.cleaned_data['unidad']
            largo = float(form.cleaned_data['largo'])
            cantidad = form.cleaned_data['cantidad']
            totalm = float(form.cleaned_data['total_m'])
            costo_u = float(form.cleaned_data['costo_u'])
            costo_t = float(form.cleaned_data['costo_t'])
            print(type(materia_id.ancho))
            tipo = materia_id.tipo
            #m = MateriaPrima.objects.get(id = int(materia_id))
            materials = MateriaPrima.objects.filter(estado=True, color=color, stock__gte=float(totalm), ancho=materia_id.ancho)
            if not materials:
                messages.error(request, 'No Exite Materia Prima Disponible')
            else:
                detalle = DetallePedido.objects.create(
                    descripcion=precioc.descripcion,
                    unidad=umedida,
                    cantidad=cantidad,
                    largo=largo,
                    costo_u=costo_u,
                    costo_t=costo_t,
                    pedido=pedido,
                    color=color,
                    ancho=materia_id.ancho,
                    totalm=totalm,
                    tipo=tipo,
                )
                #mejorar control
                for materia in materials:
                    stock += materia.stock
                    if stock >= totalm:
                        detalle.material.add(materia)
                        materia.salida = materia.salida + totalm
                        materia.stock = materia.stock - totalm
                        materia.save()
                        break
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
        'materiales':colors,
    })

@login_required(login_url='/login/')
def update_material(request, pedido_id, detalle_id):
    detalle = get_object_or_404(DetallePedido, pk = detalle_id)
    colors = MateriaPrima.objects.filter(estado=True, stock__gte = 1)
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    if request.method == 'POST':
        form = DetallePedidoForm(request.POST, detalle)
        if form.is_valid():
            stock = 0
            color = form.cleaned_data['color']
            materia_id = form.cleaned_data['anchocalamina']
            precioc = form.cleaned_data['calamina']
            umedida = form.cleaned_data['unidad']
            largo = float(form.cleaned_data['largo'])
            cantidad = form.cleaned_data['cantidad']
            totalm = float(form.cleaned_data['total_m'])
            costo_u = float(form.cleaned_data['costo_u'])
            costo_t = float(form.cleaned_data['costo_t'])
            tipo = materia_id.tipo
            #m = MateriaPrima.objects.get(id = int(materia_id))
            materials = MateriaPrima.objects.filter(estado=True, color=color, stock__gte=float(totalm), ancho=materia_id.ancho)
            if not materials:
                messages.error(request, 'No Exite Materia Prima Disponible')
                return HttpResponseRedirect(reverse(new_detail_pedido, args={pedido.id, }))
            else:
                pedido.costo = pedido.costo - detalle.costo_t
                pedido.save()
                detalle.costo_t = 0
                detalle.costo_u = 0
                detalle.largo = 0
                detalle.totalm = 0
                detalle.cantidad = 0
                detalle.save()
                detalle.costo_u = costo_u
                detalle.costo_t = costo_t
                detalle.cantidad = cantidad
                detalle.totalm = totalm
                detalle.largo = largo
                #mejorar control
                for materia in materials:
                    stock += materia.stock
                    if stock >= totalm:
                        detalle.material.add(materia)
                        materia.salida = materia.salida + totalm
                        materia.stock = materia.stock - totalm
                        materia.save()
                        break
                detalle.save()
                pedido.costo = pedido.costo + detalle.costo_t
                pedido.save()
                admin_log_addition(request, detalle, 'Detalle Creado')
                admin_log_change(request, pedido, 'Costo Modificado')
                messages.success(request, 'Material Agredado Correctemente')
                return HttpResponseRedirect(reverse(new_detail_pedido, args={pedido.id, }))
    else:
        form = DetallePedidoForm(instance=detalle)
    return render(request, 'pedidos/update_material.html', {
        'pedido':pedido,
        'form':form,
        'materiales':colors,
    })

@login_required(login_url='/login/')
def ajax_get_precio(request):
    if request.is_ajax():
        id = request.GET['precio_id']
        precio = get_object_or_404(Precio, pk = id)
        precios = Precio.objects.filter(pk = id).values('precio', 'color', 'espesor', 'materia__ancho', 'materia__cantidad', 'materia__longitud', 'materia_id', 'materia__stock')
        #return JsonResponse(precio.precio, safe=False)
        return JsonResponse(list(precios), safe=False)
    else:
        raise Http404

@login_required(login_url='/login/')
def ajax_get_materiales(request):
    if request.is_ajax():
        color = request.GET['color']
        materiales = MateriaPrima.objects.filter(color=color)
        html = render_to_string('pedidos/__ajax_materiales.html', {
            'materiales':materiales,
        })
        return JsonResponse(html, safe=False)
    else:
        raise Http404

@login_required(login_url='/login/')
def delete_material(request, detalle_id):
    detalle = get_object_or_404(DetallePedido, pk = detalle_id)
    pedido = Pedido.objects.get(pk = detalle.pedido.id)
    detallem = detalle.material.first()
    material = MateriaPrima.objects.get(id = detallem.id)
    material.stock = material.stock + detalle.totalm
    material.save()
    pedido.costo = pedido.costo - detalle.costo_t
    pedido.save()
    detalle.delete()
    admin_log_change(request, pedido, 'Costo Modificado')
    messages.error(request, 'Material Eliminado')
    return HttpResponseRedirect(reverse(new_detail_pedido, args={pedido.id, }))

@login_required(login_url='/login/')
def confirm_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    if request.method == 'POST':
        form = ConfirmForm(request.POST, instance=pedido)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedidos = Pedido.objects.exclude(nro_pedido=None)
            nro = 1
            if pedidos:
                max = pedidos.aggregate(Max('nro_pedido'))
                if max['nro_pedido__max']:
                    nro = max['nro_pedido__max'] + 1
            pedido.nro_pedido = nro
            pedido.estado = True
            pedido.fecha = datetime.datetime.now()
            pedido.usuario = request.user
            
            pedido.save()
            messages.success(request, 'Pedido Confirmado Correctamente')
            return HttpResponseRedirect(reverse(detail_pedido, args={pedido.id, }))
    else:
        form = ConfirmForm(instance=pedido)
    return render(request, 'pedidos/confirm_pedido.html', {
        'pedido':pedido,
        'form':form,
    })

@login_required(login_url='/login/')
def pedidos_no_confirmados(request):
    pedidos = Pedido.objects.filter(estado=False, venta=False)
    return render(request, 'pedidos/no_confirmados.html', {
        'pedidos':pedidos,
    })

@login_required(login_url='/login/')
def delete_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    detalle = DetallePedido.objects.filter(pedido=pedido)
    for d in detalle:
        detallem = d.material.first()
        material = MateriaPrima.objects.get(id=detallem.id)
        material.stock = material.stock + d.totalm
        material.save()
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

@login_required(login_url='/login/')
def pdf_detail_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    html = render_to_string('pedidos/pdf/o_produccion.html', {
        'pedido': pedido,
        'detalles': detalles,
        'request':request,
    })
    return render_pdf(html)

@login_required(login_url='/login/')
def pdf_proforma(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    html = render_to_string('pedidos/pdf/detail.html', {
        'pedido': pedido,
        'detalles': detalles,
        'request': request,
    })
    return render_pdf(html)

@login_required(login_url='/login')
def list_orden_produccion(request):
    pedidos = Pedido.objects.filter(estado=True, venta=True)
    return render(request, 'pedidos/list_orden_produccion.html', {
        'pedidos':pedidos,
    })

@login_required(login_url='/login/')
def realizar_orden(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    pedido.estado = False
    pedido.save()
    admin_log_change(request, pedido, 'Orden de Produccion Realizado')
    messages.success(request, 'Orden de Produccion Realizado')
    return HttpResponseRedirect(reverse(list_orden_produccion))

@login_required(login_url='/login')
def list_orden_produccion_realizado(request):
    pedidos = Pedido.objects.filter(estado=False, venta=True)
    return render(request, 'pedidos/list_orden_produccion_realizado.html', {
        'pedidos':pedidos,
    })