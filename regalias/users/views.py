from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, AdminPasswordChangeForm
from django.conf import settings
from django.utils.encoding import smart_str
from django.contrib.auth.models import Permission, Group, User

from regalias.utility import admin_log_change, admin_log_addition

from users.models import Empresa,Color
from users.form import UsernameForm, EmpresaForm, ColorForm
from pedidos.models import Pedido
from ventas.models import Venta

import datetime

def home(request):
    hoy = datetime.datetime.now()
    ventas = Venta.objects.filter(fecha__year=hoy.year, estado=True)
    pedidos = Pedido.objects.filter(fecha__year=hoy.year, estado=True, venta=False)
    return render(request, 'home.html', {
        'hoy':hoy,
        'ventas':ventas,
        'pedidos':pedidos,
    })

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(user_index))
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            access = authenticate(username=username, password=password)
            if access is not None:
                if access.is_active:
                    login(request, access)
                    if 'next' in request.GET:
                        msm = "Inicio de Sesion Correcto <strong> Gracias Por Su Visita</strong>"
                        messages.add_message(request, messages.INFO, msm)
                        return HttpResponseRedirect(str(request.GET['next']))
                    else:
                        msm = "Inicio de Sesion Existoso  <strong>Gracias Por Su Visita</strong>"
                        messages.add_message(request, messages.SUCCESS, msm)
                        return HttpResponseRedirect(reverse(user_index))
                else:
                    sms = "Su Cuenta No Esta Activada <strong>Contactese con el Administrador</strong>"
                    messages.warning(request, sms)
                    return HttpResponseRedirect(reverse(user_index))
            else:
                sms = "Usted No Es Usuario Del Sistema"
                #messages.add_message(request, messages.ERROR, msm, 'danger')
                messages.error(request, sms)
                return HttpResponseRedirect(reverse(user_login))
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {
        'form': form,
    })

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    sms = 'Gracias Por Su Visita'
    messages.info(request, sms)
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def user_index(request):

    return render(request, 'users/index.html', {
    })

@login_required(login_url='/login/')
def reset_pass(request):
    if request.method == 'POST' :
        form = AdminPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(user_index))
    else:
        form = AdminPasswordChangeForm(user=request.user)
    return  render(request,'users/reset_pass.html', {
        'form' :form,
        })

@login_required(login_url='/login/')
def change_username(request):
    if request.method == 'POST' :
        form = UsernameForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            sms = 'Nombre De Usuario Modificado Correctamente'
            messages.info(request, sms)
            return HttpResponseRedirect(reverse(user_index))
    else:
        form= UsernameForm(instance=request.user)
    return  render(request, 'users/change_username.html', {
        'form' :form,
    })

@login_required(login_url='/login/')
def user_creation(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            admin_log_addition(request, user, 'Usuario Creado')
            messages.success(request, 'Usuario Creado Correctamente')
            return HttpResponseRedirect(reverse(user_index))
    else:
        form = UserCreationForm()
    return render(request, 'users/new.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def lista_usuarios(request):
    user = get_object_or_404(User, pk = request.user.id)
    users = User.objects.exclude(id = user.id)
    return render(request, 'users/lista_usuario.html', {
        'users':users,
    })

@login_required(login_url='/login/')
def permisos(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    asignados = user.groups.all()
    grupos = Group.objects.exclude(id__in = asignados.values('id'))
    return render(request, 'users/permisos.html', {
        'grupos':grupos,
        'user':user,
        'asignados':asignados,
    })

@login_required(login_url='/login/')
def add_grupo(request, grupo_id, user_id):
    grupo = get_object_or_404(Group, pk = grupo_id)
    user = get_object_or_404(User, pk=user_id)
    user.groups.add(grupo)
    admin_log_change(request, user, 'Permiso %s Agregado'%grupo.name)
    messages.info(request, 'Permiso %s Agregado'%grupo.name)
    return HttpResponseRedirect(reverse(permisos, args={user_id, }))

@login_required(login_url='/login/')
def remove_grupo(request, grupo_id, user_id):
    grupo = get_object_or_404(Group, pk = grupo_id)
    user = get_object_or_404(User, pk=user_id)
    user.groups.remove(grupo)
    admin_log_change(request, user, 'Permiso %s Retirado'%grupo.name)
    messages.warning(request, 'Permiso %s Retirado'%grupo.name)
    return HttpResponseRedirect(reverse(permisos, args={user_id, }))

@login_required(login_url='/login/')
def baja_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save()
    admin_log_change(request, user, 'Usuario Dado de Baja')
    messages.warning(request, 'Usuario Dado de Baja')
    return HttpResponseRedirect(reverse(lista_usuarios))

@login_required(login_url='/login/')
def activate_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save()
    admin_log_change(request, user, 'Usuario Activado')
    messages.success(request, 'Usuario Activado Correctamente')
    return HttpResponseRedirect(reverse(lista_usuarios))

@login_required(login_url='/login/')
def activate_superuser(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_superuser = True
    user.save()
    admin_log_change(request, user, 'Administrador Activado')
    messages.success(request, 'Administrador Activado Correctamente')
    return HttpResponseRedirect(reverse(lista_usuarios))

@login_required(login_url='/login/')
def deactivate_superuser(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_superuser = False
    user.save()
    admin_log_change(request, user, 'Administrador Desactivado')
    messages.warning(request, 'Administrador Desactivado Correctamente')
    return HttpResponseRedirect(reverse(lista_usuarios))

@login_required(login_url='/login/')
def info_empresa(request):
    if Empresa.objects.all():
        empresa = Empresa.objects.all().first()
        return render(request, 'empresa/index.html', {
            'empresa': empresa
        })
    else:
        return HttpResponseRedirect(reverse(new_empresa))

@login_required(login_url='/login/')
def new_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(info_empresa))
    else:
        form = EmpresaForm()
    return render(request, 'empresa/new.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def update_empresa(request):
    empresa = Empresa.objects.all().first()
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(info_empresa))
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'empresa/update.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def index_colores(request):
    colores = Color.objects.all()
    return render(request, 'color/index.html', {
        'colores':colores,
    })

@login_required(login_url='/login/')
def new_color(request):
    if request.method == 'POST':
        form = ColorForm(request.POST)
        if form.is_valid():
            color = form.save()
            admin_log_addition(request, color, 'Color Creado')
            sms = 'Color %s Registrado correctamente'%color.color
            messages.success(request, sms)
            return HttpResponseRedirect(reverse(index_colores))
    else:
        form = ColorForm()
    return render(request, 'color/new.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def update_color(request, color_id):
    color = get_object_or_404(Color, pk = color_id)
    if request.method == 'POST':
        form = ColorForm(request.POST, instance=color)
        if form.is_valid():
            color = form.save()
            admin_log_change(request, color, 'Color Modificado')
            sms = 'Color %s modificado correctamente'%color.color
            messages.warning(request, sms)
            return HttpResponseRedirect(reverse(index_colores))
    else:
        form = ColorForm(instance=color)
    return render(request, 'color/update.html', {
        'form':form,
    })

@login_required(login_url='/login/')
def new_color_popup(request):
    if request.method == 'POST':
        form = ColorForm(request.POST)
        if form.is_valid():
            color = form.save()
            admin_log_addition(request, color, 'Color Creado')
            return render(request, 'close_popup.html', {
                'c': color,
            })
    else:
        form = ColorForm()
    return render(request, 'color/new_popup.html', {
        'form':form,
    })