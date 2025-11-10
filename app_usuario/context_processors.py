def permissoes_usuario(request):
    """
    Injeta informações de papel/permissões do usuário autenticado
    no contexto de templates.
    """
    role = None

    if request.user.is_authenticated:
        perfil = getattr(request.user, 'perfil', None)
        if perfil:
            role = perfil.status

    return {
        'user_role': role,
        'is_gestor': role == 'gestor_rotas',
        'is_admin': role == 'admin',
        'is_cidadao': role == 'cidadao',
        'can_manage_resources': role in ('gestor_rotas', 'admin'),
    }

