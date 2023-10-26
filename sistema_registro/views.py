
from django.contrib.auth.views import LogoutView
from control_inventarios.decorators import decorator
from .forms import CustomAuthenticationForm, CustomUserChangeForm
from django.http import HttpResponse
from .forms import CrearUsuarioForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario
#from .forms import UsuarioForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from .forms import CrearUsuarioForm
from django.contrib.auth.decorators import login_required
from .models import Usuario
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User  # Asume que tienes un modelo de usuario personalizado
from .models import Usuario
from django.shortcuts import render
from django.views import View
from .models import Usuario
from django.contrib.auth import logout
from control_inventarios.decorators import decorator
from urllib.parse import unquote
class ListarUsuariosView(View):
    template_name = 'listar_usuarios.html'

    def get(self, request, *args, **kwargs):
        usuarios = Usuario.objects.all()
        return render(request, self.template_name, {'usuarios': usuarios})

    


@login_required(login_url='login')
@decorator
def iniciar_sesion(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    # Después de autenticar al usuario correctamente
                    if 'next' in request.GET:
                        # Utiliza unquote para decodificar la URL almacenada en 'next'
                        next_url = unquote(request.GET['next'])
                        return redirect(next_url)
                    else:
                        return redirect('index')
                else:
                    return HttpResponse("Tu cuenta está desactivada.")
            else:
                messages.error(request, "Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")
        else:
            messages.error(request, "Por favor, corrige los errores a continuación.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'mostrar_notificaciones': False, 'form': form})

class RegistroView(FormView):
    template_name = 'registration/registro.html'
    form_class = CrearUsuarioForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
        return super().form_valid(form)

class RecuperarContrasenaView(PasswordResetView):
    template_name = 'registration/recuperar_contrasena.html'
    success_url = reverse_lazy('login')
    email_template_name = 'registration/recuperar_contrasena_email.html'
    subject_template_name = 'registration/recuperar_contrasena_subject.txt'

    def form_valid(self, form):
        messages.success(self.request, 'Se ha enviado un correo electrónico con las instrucciones para restablecer tu contraseña.')
        return super().form_valid(form)


def registro_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Obtén el rol solicitado del formulario y guárdalo en el modelo de Usuario

    else:
            form = CrearUsuarioForm()
    return render(request, 'registration/registro.html', {'form': form})

def crear_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El usuario ha sido creado correctamente.')
            return redirect('configuracion')  # Redirige de nuevo a la página de configuración
    else:
        messages.error(request, 'Hubo un error al crear el usuario. Por favor, revisa los datos ingresados.')
        form = CrearUsuarioForm()
    return render(request, 'crear_usuario.html', {'form': form})

def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'El usuario ha sido actualizado correctamente.')
            return redirect('configuracion')  # Redirige de nuevo a la página de configuración
    else:
        form = CustomUserChangeForm(instance=usuario)

    context = {
        'form': form,
        'usuario': usuario,
    }
    return render(request, 'editar_usuario.html', context)

def desactivar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        usuario.estado = 'inactivo'
        usuario.save()
        messages.success(request, 'El usuario ha sido desactivado correctamente.')
        return redirect('configuracion')  # Redirige de nuevo a la página de configuración

    context = {
        'usuario': usuario,
    }
    return render(request, 'desactivar_usuario.html', context)

def configuracion(request):
    # Recupera el usuario que deseas editar, por ejemplo, el usuario actualmente autenticado
    usuario = request.user  # Esto asume que el usuario actualmente autenticado es el que deseas editar

    # Verifica que el usuario esté autenticado antes de usarlo
    if request.user.is_authenticated:
        return render(request, 'configuracion.html', {'usuario': usuario})
    else:
        # Maneja el caso en el que el usuario no esté autenticado
        # Puedes redirigirlo a una página de inicio de sesión u otra acción apropiada.
        return redirect('login')
#...........................




#........................
@login_required  # Este decorador asegura que solo los usuarios autenticados puedan acceder a esta vista
def index(request):
    # Agrega cualquier lógica adicional que necesites aquí antes de renderizar la página
    return render(request, 'index.html')




class CustomLogoutView(LogoutView):
    def get_next_page(self):
            next_page = reverse_lazy('login')  # Especifica el nombre de la URL de inicio de sesión
            return next_page
    
def terminar_sesion(request):
    request.session.clear()
    request.session['sesion_terminada'] = True

    # Luego, cerrar sesión
    logout(request)

    # Redirigir a la página de sesión terminada
    return render(request, 'registration/sesion_terminada.html', {'user': request.user})

@login_required(login_url='login')
def tu_vista_protegida(request):
    sesion_terminada = request.session.pop('sesion_terminada', False)

    if sesion_terminada:
        # Realizar acciones adicionales si la sesión ha terminado, por ejemplo, mostrar un mensaje.
        mensaje = "La sesión ha terminado. Por favor, inicia sesión nuevamente."
        return render(request, 'registration/sesion_terminada.html', {'mensaje': mensaje})
    
def password_reset_done(request):
    return render(request, 'registration/recuperar_contrasena_done.html')