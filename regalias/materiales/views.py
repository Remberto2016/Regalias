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
from django.db.models import ProtectedError, Sum, Max

from regalias.utility import admin_log_addition, admin_log_change, render_pdf

from users.models import Color
from materiales.models import MateriaPrima, Proveedor, Precio, PrecioClavos, DetallePrecioClavo, TipoCalamina, CodigoCalamina, PrecioCalamina, CodigoMateriaPrima, CodigoClavo
from materiales.form import MateriaPForm, ProveedorForm, SearchProveedor, PrecioForm, PrecioClavoForm, StockClavos, TipoCalaminaForm, PrecioCalaminaForm, CodigoCalaminaForm, CodigoMateriaPrimaForm, PrecioCalaminaPrecioForm, CodigoClavoForm

import datetime

@login_required(login_url='/login/')
def index(request):
    materiales = MateriaPrima.objects.filter(estado=True, unidad='Bobina')
    return render(request, 'materiap/index.html', {
        'materiales':materiales,
    })
@login_required(login_url='/login/')
def index_alambron(request):
    materiales = MateriaPrima.objects.filter(estado=True, unidad='Alambron')
    referer = request.META.get('HTTP_REFERER')
    print(referer)
    return render(request, 'materiap/index-alambron.html', {
        'materiales':materiales,
    })


import string
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Función para generar valores aleatorios
    Puede recibir:
        size = longitud de la cadena
            Defecto 6
        chars = caracteres a utilizar para buscar la cadena
            Defecto letras mayusculas y numeros
    """
    return ''.join(random.choice(chars) for _ in range(size))


@login_required(login_url='/login/')
def new(request):
    colores = Color.objects.all()
    if request.method == 'POST':
        form = MateriaPForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            if form.cleaned_data['colores'] != None:
                c_id = form.cleaned_data['colores']
                print(c_id.codigo)
                #color = Color.objects.get(id=c_id)
                m.color = c_id
            m.user = request.user
            if form.cleaned_data['longitud']:
                m.stock = m.longitud
            m.save()
            admin_log_addition(request, m, 'Materia Prima Creada')
            messages.success(request, 'Materia Prima Creada Correctamente')
            return HttpResponseRedirect(reverse(index))
    else:
        form = MateriaPForm()
    return render(request, 'materiap/new.html', {
        'form':form,
        'colores':colores,
    })

@login_required(login_url='/login/')
def update(request, materia_id):
    materia = get_object_or_404(MateriaPrima, pk = materia_id)
    colores = Color.objects.all()
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
        'colores':colores,
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
def activate_materia(request, materia_id):
    materia = get_object_or_404(MateriaPrima, pk = materia_id)
    materia.estado = True
    materia.save()
    admin_log_change(request, materia, 'Material Activado')
    messages.info(request, 'Material Activado')
    return HttpResponseRedirect(reverse(index))

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

@login_required(login_url='/login/')
def pdf_proveedores(request):
    proveedores = Proveedor.objects.filter(estado=True)
    html = render_to_string('proveedores/pdf_proveedores.html', {
        'proveedores':proveedores,
    })
    return render_pdf(html)

@login_required(login_url='/login/')
def pdf_materia_prima(request):
    materiales = MateriaPrima.objects.filter(estado = True, unidad='Bobina')
    html = render_to_string('materiap/pdf_materiap.html', {
        'materiales':materiales,
    })
    return render_pdf(html)

@login_required(login_url='/login/')
def pdf_materia_prima_alambron(request):
    materiales = MateriaPrima.objects.filter(estado = True, unidad='Alambron' )
    html = render_to_string('materiap/pdf_materiap_alambron.html', {
        'materiales':materiales,
    })
    return render_pdf(html)

@login_required(login_url='/login/')
def materiap_proveedor(request):
    hoy = datetime.datetime.now()
    proveedor = Proveedor.objects.filter(estado=True).first()
    year = hoy.year
    mes = hoy.month
    form = SearchProveedor(request.GET or None)
    if form.is_valid():
        year = form.cleaned_data['year']
        mes = form.cleaned_data['month']
        hoy = datetime.date(int(year), int(mes), 1)
        proveedor = form.cleaned_data['proveedor']
    materiales = MateriaPrima.objects.filter(proveedor=proveedor, fecha__month=mes, fecha__year=year)
    return render(request, 'materiap/materia_proveedor.html', {
        'materiales':materiales,
        'form':form,
        'proveedor':proveedor,
        'mes':mes,
        'year':year,
        'fecha':hoy,
    })

@login_required(login_url='/login/')
def pdf_materiap_proveedor(request, proveedor_id, mes, year):
    hoy = datetime.date(int(year), int(mes), 1)
    proveedor = get_object_or_404(Proveedor, pk = proveedor_id)
    materiales = MateriaPrima.objects.filter(proveedor=proveedor, fecha__month=mes, fecha__year=year)
    
    html = render_to_string('materiap/pdf_materiap_proveedor.html', {
        
        'materiales':materiales,
        'proveedor':proveedor,
        'fecha': hoy,
    })
    return render_pdf(html)

@login_required(login_url='/login/')
def index_precios(request):
    precios = PrecioCalamina.objects.filter(estado=True)
    return render(request, 'materiap/index_precio.html', {
        'precios':precios,
    })

@login_required(login_url='/login/')
def new_precio(request):
    if request.method == 'POST':
        form = PrecioCalaminaForm(request.POST)
        if form.is_valid():
            precio = form.save(commit=False)
            precio.save()
            admin_log_addition(request, precio, 'Precio Calamina Creado')
            sms = 'Precio Creado Correctamente'
            messages.success(request, sms)
            return HttpResponseRedirect(reverse(index_precios))
    else:
        form = PrecioCalaminaForm()
    return render(request, 'materiap/new_precio_calamina.html', {
        'form':form,
    })

@login_required(login_url='/login')
def new_codigo_calamina_popup(request):
    if request.method == 'POST':
        form = CodigoCalaminaForm(request.POST)
        if form.is_valid():
            c = form.save()
            admin_log_addition(request, c, 'Codigo Registrado')
            return render(request, 'close_popup.html', {
                'c': c,
            })
    else:
        form = CodigoCalaminaForm()
    return render(request, 'materiap/new_codigocalamina_popup.html', {
        'form':form,
    })

@login_required(login_url='/login')
def new_tipocalamina_popup(request):
    if request.method == 'POST':
        form = TipoCalaminaForm(request.POST)
        if form.is_valid():
            c = form.save()
            admin_log_addition(request, c, 'Tipo Calamina Registrado')
            return render(request, 'close_popup.html', {
                'c': c,
            })
    else:
        form = TipoCalaminaForm()
    return render(request, 'materiap/new_tipocalamina_popup.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def update_precio(request, precio_id):
    colores = Color.objects.all()
    precio = get_object_or_404(PrecioCalamina, pk = precio_id)
    if request.method == 'POST':
        form = PrecioCalaminaForm(request.POST, instance=precio)
        if form.is_valid():
            precio = form.save()
            admin_log_change(request, precio, 'Precio Modificado')
            sms = 'Precio Modificado Correctamente'
            messages.warning(request, sms)
            return HttpResponseRedirect(reverse(index_precios))
    else:
        form = PrecioCalaminaForm(instance=precio)
    return render(request, 'materiap/update_precio.html', {
        'form':form,
        'colores':colores,
    })
@login_required(login_url='/login/')
def update_precio_precio_popup(request, precio_id):
    colores = Color.objects.all()
    precio = get_object_or_404(PrecioCalamina, pk = precio_id)
    if request.method == 'POST':
        form = PrecioCalaminaPrecioForm(request.POST, instance=precio)
        if form.is_valid():
            precio = form.save()
            admin_log_change(request, precio, 'Costo Modificado')
            sms = 'Costo Modificado Correctamente'
            messages.success(request, sms)
            return render(request, 'close_popup.html', {
            })
    else:
        form = PrecioCalaminaPrecioForm(instance=precio)
    return render(request, 'materiap/update_precio_precio_popup.html', {
        'form':form,
        'colores':colores,
    })

@login_required(login_url='/login/')
def baja_precio(request, precio_id):
    precio = get_object_or_404(PrecioCalamina, pk = precio_id)
    precio.estado = False
    precio.save()
    admin_log_change(request, precio, 'Precio Dado De Baja')
    sms = 'Precio dado de baja correctamente'
    messages.error(request, sms)
    return HttpResponseRedirect(reverse(index_precios))

@login_required(login_url='/login/')
def precios_baja(request):
    precios = PrecioCalamina.objects.filter(estado=False)
    return render(request, 'materiap/index_precio_baja.html', {
        'precios':precios,
    })

@login_required(login_url='/login/')
def active_precio(request, precio_id):
    precio = get_object_or_404(PrecioCalamina, pk=precio_id)
    precio.estado = True
    precio.save()
    admin_log_change(request, precio, 'Precio Activado Correctamente')
    sms = 'Precio activado correctamente'
    messages.success(request, sms)
    return HttpResponseRedirect(reverse(precios_baja))


@login_required(login_url='/login/')
def index_precios_clavos(request):
    precios = PrecioClavos.objects.filter(estado=True)
    return render(request, 'clavos/index_precio.html', {
        'precios':precios,
    })

@login_required(login_url='/login/')
def new_precio_clavo(request):
    if request.method == 'POST':
        form = PrecioClavoForm(request.POST)
        if form.is_valid():
            precio = form.save()
            admin_log_addition(request, precio, 'Precio Creado')
            sms = 'Precio Creado Correctamente'
            messages.success(request, sms)
            return HttpResponseRedirect(reverse(index_precios_clavos))
    else:
        form = PrecioClavoForm()
    return render(request, 'clavos/new_precio.html', {
        'form':form,

    })

@login_required(login_url='/login/')
def update_precio_clavo(request, precio_id):
    precio = get_object_or_404(PrecioClavos, pk = precio_id)
    if request.method == 'POST':
        form = PrecioClavoForm(request.POST, instance=precio)
        if form.is_valid():
            precio = form.save()
            admin_log_change(request, precio, 'Precio Modificado')
            sms = 'Precio Modificado Correctamente'
            messages.warning(request, sms)
            return HttpResponseRedirect(reverse(index_precios_clavos))
    else:
        form = PrecioClavoForm(instance=precio)
    return render(request, 'clavos/update_precio.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def baja_precio_clavo(request, precio_id):
    precio = get_object_or_404(PrecioClavos, pk = precio_id)
    precio.estado = False
    precio.save()
    admin_log_change(request, precio, 'Precio Dado De Baja')
    sms = 'Precio dado de baja correctamente'
    messages.error(request, sms)
    return HttpResponseRedirect(reverse(index_precios_clavos))

@login_required(login_url='/login/')
def precios_baja_clavo(request):
    precios = PrecioClavos.objects.filter(estado=False)
    return render(request, 'clavos/index_precio_baja.html', {
        'precios':precios,
    })

@login_required(login_url='/login/')
def active_precio_clavo(request, precio_id):
    precio = get_object_or_404(PrecioClavos, pk=precio_id)
    precio.estado = True
    precio.save()
    admin_log_change(request, precio, 'Precio Activado Correctamente')
    sms = 'Precio activado correctamente'
    messages.success(request, sms)
    return HttpResponseRedirect(reverse(precios_baja_clavo))

@login_required(login_url='/login/')
def pdf_inventario_clavo(request):
    inventarios = PrecioClavos.objects.filter(estado=True)
    html = render_to_string('clavos/pdf_inventario_clavo.html', {
        'inventarios':inventarios,
    })
    return render_pdf(html)

@login_required(login_url='/login/')
def index_inventario(request):
    inventarios = PrecioClavos.objects.filter(estado=True)
    return render(request, 'clavos/index_inventario.html', {
        'inventarios':inventarios,
    })


@login_required(login_url='/login/')
def inventario_calaminas(request):
    materiap = MateriaPrima.objects.filter(tipo='Calamina')
    return render(request, 'materiap/index_inventario.html', {
        'materiap':materiap,
    })

@login_required(login_url='/login/')
def stock_clavo(request, precio_id):
    precio = get_object_or_404(PrecioClavos, pk = precio_id)
    if request.method == 'POST':
        form = StockClavos(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            d = DetallePrecioClavo.objects.create(
                precioclavo=precio,
                cantidad=cantidad,
            )
            d.save()
            precio.stock = precio.stock + cantidad
            precio.save()
            admin_log_change(request, precio, 'Stock Modificado')
            sms = 'Stock de material %s modificado'%precio
            messages.info(request, sms)
            return HttpResponseRedirect(reverse(index_inventario))
    else:
        form = StockClavos()
    return render(request, 'clavos/add_stock.html', {
        'form':form,
    })

def ajax_get_material(request):
    if request.is_ajax():
        id = request.GET['id']
        material = MateriaPrima.objects.filter(id = id).values('espesor', 'ancho', 'color', 'stock', 'longitud', 'id', 'precioc')
        return JsonResponse(list(material), safe=False)
    else:
        return Http404

@login_required(login_url='/login/')
def new_proveedor_popup(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            pro = form.save()
            admin_log_addition(request, pro, 'Proveedor Registrado')
            return render(request, 'close_popup.html', {
                'c':pro,
            })
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/new_popup.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def new_popup(request):
    colores = Color.objects.all()
    if request.method == 'POST':
        form = MateriaPForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            if form.cleaned_data['colores'] != None:
                c_id = form.cleaned_data['colores']
                #print(c_id)
                #color = Color.objects.get(id=c_id)
                m.color = c_id
            m.user = request.user
            if form.cleaned_data['longitud']:
                m.stock = m.longitud
            m.save()
            admin_log_addition(request, m, 'Materia Prima Creada')
            return render(request, 'close_popup.html', {
                'c':m,
            })
    else:
        form = MateriaPForm()
    return render(request, 'materiap/new_popup.html', {
        'form':form,
        'colores':colores,
    })

def ajax_color_codigo(request):
    if request.is_ajax():
        color = request.GET['id']
        color = Color.objects.filter(id=color)
        q1 = color.values('color', 'codigo')
        return JsonResponse(list(q1), safe=False)
    else:
        raise Http404


def ajax_color_colored(request):
    if request.is_ajax():
        color = request.GET['id']
        color = Color.objects.filter(color=color)
        q1 = color.values('color', 'codigo')
        return JsonResponse(list(q1), safe=False)
    else:
        raise Http404


@login_required(login_url='/login/')
def new_popup_codigomateria(request):
    if request.method == 'POST':
        form = CodigoMateriaPrimaForm(request.POST)
        if form.is_valid():
            pro = form.save()
            admin_log_addition(request, pro, 'Codigo Registrado')
            return render(request, 'close_popup.html', {
                'c':pro,
            })
    else:
        form = CodigoMateriaPrimaForm()
    return render(request, 'materiap/new_codigo_materia_popup.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def update_proveedor_popup(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk = proveedor_id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            pro = form.save()
            admin_log_change(request, pro, 'Proveedor Modificado')
            messages.warning(request, 'Proveedor Modificado Correctamente')
            return render(request, 'close_popup.html',{
            })
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/update_proveedor_popup.html', {
        'form':form,
    })

@login_required(login_url='/login')
def new_codigo_clavo_popup(request):
    if request.method == 'POST':
        form = CodigoClavoForm(request.POST)
        if form.is_valid():
            c = form.save()
            admin_log_addition(request, c, 'Codigo Registrado')
            return render(request, 'close_popup.html', {
                'c': c,
            })
    else:
        form = CodigoClavoForm()
    return render(request, 'clavos/new_codigoclavo_popup.html', {
        'form':form,
    })
#--------------------------------------------------------
@login_required(login_url='/login')
def codigos_materiales_primas(request):
    codprima = CodigoMateriaPrima.objects.filter()
    codtipo = TipoCalamina.objects.all()
    codprecio = CodigoCalamina.objects.all()
    codclavo = CodigoClavo.objects.all()
    return render(request, 'configuracion/index_configuracion.html', {
        'codprima':codprima,
        'codprecio':codprecio,
        'codtipo':codtipo,
        'codclavo':codclavo,
        
    })

@login_required(login_url='/login/')
def update_codigo_materia_prima(request, codprimas_id):
    codigomateriaprima = get_object_or_404(CodigoMateriaPrima, pk = codprimas_id)
    if request.method == 'POST':
        form = CodigoMateriaPrimaForm(request.POST, instance=codigomateriaprima)
        if form.is_valid():
            cpm = form.save()
            admin_log_change(request, cpm, 'Codigo Modificado')
            messages.warning(request, 'Codigo Modificado Correctamente')
            return render(request, 'close_popup.html',{
            })
    else:
        form = CodigoMateriaPrimaForm(instance=codigomateriaprima)
    return render(request, 'configuracion/update_codigo_materia_prima_popup.html', {
        'form':form,
    })

@login_required(login_url='/login')
def update_codigo_precio_calamina(request, codprecios_id):
    codigopreciocalamina = get_object_or_404(CodigoCalamina, pk = codprecios_id)
    if request.method == 'POST':
        form = CodigoCalaminaForm(request.POST, instance=codigopreciocalamina)
        if form.is_valid():
            cpc = form.save()
            admin_log_change(request, cpc, 'Codigo Modificado')
            messages.warning(request, 'Codigo Modificado Correctamente')
            return render(request, 'close_popup.html',{

                })
    else:
        form = CodigoCalaminaForm(instance=codigopreciocalamina)
    return render(request, 'configuracion/update_codigo_precio_calamina_popup.html',{
        'form':form,
    })

@login_required(login_url='/login')
def update_tipo_calamina(request, codtipos_id):
    codigotipocalamina = get_object_or_404(TipoCalamina, pk = codtipos_id)
    if request.method == 'POST':
        form = TipoCalaminaForm(request.POST, instance=codigotipocalamina)
        if form.is_valid():
            ctc = form.save()
        admin_log_change(request, ctc, 'Codigo Modificado')
        messages.warning(request, 'Codigo Modificado Correctamente')
        return render (request, 'close_popup.html',{

        })
    else:
        form = TipoCalaminaForm(instance=codigotipocalamina)
    return render(request,  'configuracion/update_tipo_calamina-popup.html',{
        'form':form,
        })

@login_required(login_url='/login')
def update_codigo_clavo(request, codclavos_id):
    codigoprecioclavo = get_object_or_404(CodigoClavo, pk = codclavos_id)
    if request.method == 'POST':
        form = CodigoClavoForm(request.POST, instance=codigoprecioclavo)
        if form.is_valid():
            cpcl = form.save()
        admin_log_change(request, ctcl, 'Codigo Modificado')
        messages.warning(request, 'Codigo Modificado Correctamente')
        return render (request, 'close_popup.html',{

        })
    else:
        form = CodigoClavoForm(instance=codigoprecioclavo)
    return render(request,  'configuracion/update_codigo_clavo-popup.html',{
        'form':form,
        })