from functools import wraps

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect


def role_required(*roles):
    """
    Decorator que garante que o usuário autenticado possua
    pelo menos um dos papéis informados.
    """

    if not roles:
        raise ValueError("Informe ao menos um papel para o decorator role_required.")

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            perfil = getattr(request.user, 'perfil', None)
            if not perfil or perfil.status not in roles:
                # Diferenciar resposta para requisições AJAX/JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
                    return JsonResponse(
                        {
                            'success': False,
                            'error': 'Você não possui permissão para realizar esta ação.',
                        },
                        status=403,
                    )

                messages.error(request, 'Você não possui permissão para acessar este recurso.')
                return redirect('dashboard')

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator

