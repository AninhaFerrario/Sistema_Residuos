from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from app_usuario.decorators import role_required
from app_usuario.forms import UsuarioCreateForm
from app_usuario.models import PerfilUsuario


def login(request):
    if request.method == 'GET':
        return render(request, "app_usuario/login.html")

    email = request.POST.get('login')
    senha = request.POST.get('senha')

    perfil = PerfilUsuario.objects.filter(email=email).first()

    if perfil is None or not perfil.ativo:
        messages.error(request, 'Usuário não encontrado ou inativo.')
        return render(request, "app_usuario/login.html")

    user = perfil.user

    user_authenticated = authenticate(request, username=user.username, password=senha)

    if user_authenticated is None or not user_authenticated.is_active:
        messages.error(request, 'Credenciais inválidas.')
        return render(request, "app_usuario/login.html")

    auth_login(request, user_authenticated)
    messages.success(request, f'Bem-vindo(a), {perfil.nome}!')
    return redirect('dashboard')


@login_required
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'Sessão encerrada com sucesso.')
    return redirect('login')


@login_required
def dashboard(request):
    return render(request, "app_usuario/dashboard.html")


@role_required('admin')
def gerenciar_usuarios(request):
    usuarios = PerfilUsuario.objects.select_related('user').order_by('nome')

    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso.')
            return redirect('gerenciar_usuarios')
    else:
        form = UsuarioCreateForm()

    context = {
        'form': form,
        'usuarios': usuarios,
    }
    return render(request, "app_usuario/usuario_list.html", context)


@role_required('admin')
def alterar_status_usuario(request, pk):
    if request.method != 'POST':
        return redirect('gerenciar_usuarios')

    perfil = get_object_or_404(PerfilUsuario, pk=pk)

    if perfil.user == request.user:
        messages.error(request, 'Você não pode alterar o próprio status.')
        return redirect('gerenciar_usuarios')

    perfil.ativo = not perfil.ativo
    perfil.save(update_fields=['ativo'])

    perfil.user.is_active = perfil.ativo
    perfil.user.save(update_fields=['is_active'])

    status_text = 'ativado' if perfil.ativo else 'desativado'
    messages.success(request, f'Usuário {perfil.nome} {status_text} com sucesso.')
    return redirect('gerenciar_usuarios')
