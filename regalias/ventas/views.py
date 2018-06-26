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
from materiales.models import PrecioClavos, Precio, MateriaPrima

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
            detalle.tipo = detalle.material
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
            tipo=d.tipo,
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

@login_required(login_url='/login/')
def calamina_new_list_cliente(request):
    clientes = Cliente.objects.filter(estado=True)
    return render(request, 'ventas/calamina/new_list_clientes.html', {
        'clientes':clientes,
    })

@login_required(login_url='/login/')
def calamina_new_venta(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk = cliente_id)
    venta = Venta.objects.create(
        cliente=cliente,
    )
    venta.save()
    admin_log_addition(request, venta, 'Venta Creada')
    messages.success(request, 'Empiece a Agregar Materiales')
    return HttpResponseRedirect(reverse(calamina_new_detail_venta, args={venta.id, }))

@login_required(login_url='/login/')
def calamina_new_detail_venta(request, venta_id):
    venta =  get_object_or_404(Venta, pk = venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    return render(request, 'ventas/calamina/new_detail_venta.html', {
        'venta':venta,
        'detalles':detalles,
    })

from pedidos.form import DetallePedidoForm
@login_required(login_url='/login/')
def calamina_add_material(request, venta_id):
    colors = MateriaPrima.objects.filter(estado=True, stock__gte = 1)
    venta = get_object_or_404(Venta, pk = venta_id)
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
                detalle = DetalleVenta.objects.create(
                    material='Largo: %s ml- Ancho: %s ml' % (largo, materia_id.ancho),
                    descripcion=precioc.descripcion,
                    cantidad=cantidad,
                    costo_u=costo_u,
                    costo_t=costo_t,
                    venta=venta,
                    unidad=umedida,
                    largo=largo,
                    tipo=tipo,
                    materia_id=materia_id,
                )
                detalle.save()
                venta.costo = venta.costo + detalle.costo_t
                venta.save()
                admin_log_addition(request, detalle, 'Detalle Creado')
                admin_log_change(request, venta, 'Costo Modificado')
                messages.success(request, 'Material Agredado Correctemente')
                return HttpResponseRedirect(reverse(calamina_new_detail_venta, args={venta.id, }))
    else:
        form = DetallePedidoForm()
    return render(request, 'ventas/calamina/add_material.html', {
        'venta':venta,
        'form':form,
        'materiales':colors,
    })

@login_required(login_url='/login/')
def ajax_get_precio_calamina(request):
    if request.is_ajax():
        id = request.GET['precio_id']
        precio = get_object_or_404(Precio, pk = id)
        precios = Precio.objects.filter(pk = id).values('precio', 'color', 'espesor', 'materia__ancho', 'materia__cantidad', 'materia__longitud', 'materia_id', 'materia__stock')
        #return JsonResponse(precio.precio, safe=False)
        return JsonResponse(list(precios), safe=False)
    else:
        raise Http404

@login_required(login_url='/login/')
def ajax_get_materiales_calamina(request):
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
def calamina_delete_material(request, detalle_id):
    detalle = get_object_or_404(DetalleVenta, pk = detalle_id)
    pedido = Venta.objects.get(pk = detalle.venta.id)
    material = MateriaPrima.objects.get(id = detalle.materia_id.id)
    material.stock = material.stock + (detalle.cantidad * detalle.largo)
    material.save()
    pedido.costo = pedido.costo - detalle.costo_t
    pedido.save()
    detalle.delete()
    admin_log_change(request, pedido, 'Costo Modificado')
    messages.error(request, 'Material Eliminado')
    return HttpResponseRedirect(reverse(calamina_new_detail_venta, args={pedido.id, }))