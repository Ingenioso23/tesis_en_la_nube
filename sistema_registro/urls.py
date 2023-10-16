from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import CustomLogoutView
from .views import terminar_sesion
#from .views import cerrar_sesion

urlpatterns = [
    path('login/', views.iniciar_sesion, name='login'),
    path('index/', views.index, name='index'),  # Agrega esta línea
    path('recuperar-contrasena/', auth_views.PasswordResetView.as_view(
        template_name='registration/recuperar_contrasena.html',
        email_template_name='registration/recuperar_contrasena_email.html',
        subject_template_name='registration/recuperar_contrasena_subject.txt'
    ), name='password_reset'),
    path('accounts/recuperar-contrasena/', auth_views.PasswordResetView.as_view(), name='recuperar_contrasena'),
    path('accounts/recuperar-contrasena/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('configuracion/crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('configuracion/desactivar-usuario/<int:usuario_id>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('configuracion/editar-usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('configuracion/listar_usuarios/', views.ListarUsuariosView.as_view(), name='listar_usuarios'),
    path('registro/', views.registro_usuario, name='registro'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('terminar_sesion/', views.terminar_sesion, name='terminar_sesion'),
 



]




