from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('registration/login', views.iniciar_sesion, name='login'),
    path('index/', views.index, name='index'),
    path('recuperar-contrasena/', auth_views.PasswordResetView.as_view(
        template_name='registration/recuperar_contrasena.html',
        email_template_name='registration/recuperar_contrasena_email.html',
        subject_template_name='registration/recuperar_contrasena_subject.txt'
    ), name='password_reset'),
    path('recuperar-contrasena/done/', views.password_reset_done , name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('configuracion/crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('configuracion/desactivar-usuario/<int:usuario_id>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('configuracion/editar-usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('configuracion/listar_usuarios/', views.ListarUsuariosView.as_view(), name='listar_usuarios'),
    path('registro/', views.registro_usuario, name='registro'),
    path('terminar_sesion/', views.terminar_sesion, name='terminar_sesion'),
]




