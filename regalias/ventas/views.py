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
from django.db.models import ProtectedError, Max

from regalias.utility import admin_log_addition, admin_log_change, render_pdf

from users.models import Empresa
from clientes.models import Cliente
from pedidos.models import Pedido, DetallePedido
from ventas.models import Venta, DetalleVenta
from materiales.models import PrecioClavos

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
            clavo = form.cleaned_data['materiaprima']
            precioclavo = PrecioClavos.objects.get(id=clavo.id)
            detalle = form.save(commit=False)
            detalle.venta = venta
            detalle.costo_t = detalle.cantidad * detalle.costo_u
            detalle.precio_id = precioclavo.id
            detalle.save()
            venta.costo = venta.costo + detalle.costo_t
            venta.save()
            precioclavo.stock = precioclavo.stock - detalle.cantidad
            precioclavo.save()
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

@login_required(login_url='/login')
def ajax_get_precio(request):
    if request.is_ajax():
        id = request.GET['precio_id']
        precio = PrecioClavos.objects.filter(pk = id).values('precio', 'stock')
        return JsonResponse(list(precio), safe=False)
    else:
        raise Http404

@login_required(login_url='/login/')
def delete_material(request, detalle_id):
    detalle = get_object_or_404(DetalleVenta, pk = detalle_id)
    venta = Venta.objects.get(pk = detalle.venta.id)
    venta.costo = venta.costo - detalle.costo_t
    venta.save()
    precioclavo = PrecioClavos.objects.get(id = detalle.precio_id)
    precioclavo.stock = precioclavo.stock + detalle.cantidad
    precioclavo.save()
    detalle.delete()
    admin_log_change(request, venta, 'Costo Modificado')
    messages.error(request, 'Material Eliminado')
    return HttpResponseRedirect(reverse(new_detail_venta, args={venta.id, }))

@login_required(login_url='/login/')
def confirm_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk = venta_id)
    venta.estado = True
    ventas = Venta.objects.exclude(nro_venta=None)
    nro = 1
    if ventas:
        max = ventas.aggregate(Max('nro_venta'))
        if max['nro_venta__max']:
            nro = max['nro_venta__max'] + 1
    venta.nro_venta = nro
    venta.save()
    messages.success(request, 'Venta Confirmada Correctamente')
    '''Redireccionar al reporte detalle venta'''
    return HttpResponseRedirect(reverse(detail_venta, args={venta.id, }))

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
    ventas = Venta.objects.exclude(nro_venta=None)
    nro = 1
    if ventas:
        max = ventas.aggregate(Max('nro_venta'))
        if max['nro_venta__max']:
            nro = max['nro_venta__max'] + 1
    venta = Venta.objects.create(
        cliente=pedido.cliente,
        costo=pedido.costo,
        estado=True,
        nro_venta=nro,
    )
    admin_log_addition(request, venta, 'Venta Pedido')
    venta.save()
    for d in detalles:
        detalle = DetalleVenta.objects.create(
            material='Largo: %s ml- Ancho: %s ml'%(d.largo, d.ancho),
            descripcion=d.descripcion,
            cantidad=d.cantidad,
            costo_u=d.costo_u,
            costo_t=d.costo_t,
            venta=venta,
            unidad=d.unidad,
            largo=d.largo,
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


from regalias.factura import get_code_control, build_string_qr, get_decimal_amount
from num2words import num2words
from datetime import timedelta
from regalias.fact import controlCode

@login_required(login_url='/login/')
def factura_pdf(request, venta_id):
    venta = get_object_or_404(Venta, pk = venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    empresa = Empresa.objects.all().first()
    #articles = Article.objects.filter(billing_id=billing_id)
    #get_sum_total_of_billing(billing_id)
    cliente = Cliente.objects.get(pk=venta.cliente_id)

    code = controlCode(str(empresa.nro), str(venta.nro_venta), str(venta.cliente.nit), str(venta.fecha.strftime('%Y%m%d')), str(int(venta.costo)), str(empresa.key))

    qr_text = build_string_qr(venta, code)

    literal_amount = num2words(int(venta.costo), lang='es')
    #DECIMALESRESIDUO
    decimal_amount = get_decimal_amount(venta)

    limit_date = venta.fecha + timedelta(days=90)

    html_string = render_to_string('ventas/pdf_factura.html', {
        'empresa':empresa,
        'pagesize': 'letter',
        'cliente': cliente,
        'venta': venta,
        'detalles': detalles,
        'code_control': code,
        'qr_text': qr_text,
        'literal_amount': literal_amount,
        'decimal_amount': decimal_amount,
        'limit_date': limit_date,
    })

    return render_pdf(html_string)

@login_required(login_url='/login/')
def pdf_recibo_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    literal_amount = num2words(int(venta.costo), lang='es')
    decimal_amount = get_decimal_amount(venta)
    detalles = DetalleVenta.objects.filter(venta=venta)
    html = render_to_string('ventas/pdf/recibo.html', {
        'venta': venta,
        'detalles': detalles,
        'literal_amount': literal_amount,
        'decimal_amount': decimal_amount,
    })
    return render_pdf(html)
