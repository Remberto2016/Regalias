from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('new/', views.user_creation, name='user-new'),
    path('users/index', views.user_index, name='users-index'),
    path('change/pass/', views.reset_pass, name='user-reset-pass'),
    path('change/username/', views.change_username, name='user-change-username'),
    path('user/lista/', views.lista_usuarios, name='user-list'),
    path('user/<int:user_id>/baja/', views.baja_user, name='user-baja'),
    path('user/<int:user_id>/admin/activate/', views.activate_superuser, name='user-admin-activate'),
    path('user/<int:user_id>/admin/baja/', views.deactivate_superuser, name='user-admin-baja'),
    path('user/<int:user_id>/activate/', views.activate_user, name='user-activate'),
    path('<int:user_id>/permission/', views.permisos, name='user-permission'),
    path('add/<int:grupo_id>/<int:user_id>/permission/', views.add_grupo, name='user-add-permission'),
    path('remove/<int:grupo_id>/<int:user_id>/permission/', views.remove_grupo, name='user-remove-permission'),

    path('empresa', views.info_empresa, name='empresa_info'),
    path('empresa/new', views.new_empresa, name='empresa_new'),
    path('empresa/update', views.update_empresa, name='empresa_update'),

    path('color', views.index_colores, name='color-index'),
    path('color/new', views.new_color, name='color-new'),
    path('color/<int:color_id>/update', views.update_color, name='color-update'),
    path('color/new/popup', views.new_color_popup, name='color-new-popup'),

]