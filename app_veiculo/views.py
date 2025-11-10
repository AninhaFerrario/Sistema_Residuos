from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import json
from app_usuario.decorators import role_required
from .models import Veiculo, Rota, ProblemaColeta
from .forms import VeiculoForm, RotaForm, ProblemaColetaForm, DenunciaProblemaForm

# Views para Veículos
@login_required
def veiculo_list(request):
    """Lista todos os veículos com filtros e paginação"""
    try:
        veiculos = Veiculo.objects.all()

        # Filtros
        search = request.GET.get('search', '')
        tipo_filter = request.GET.get('tipo', '')
        ativo_filter = request.GET.get('ativo', '')

        if search:
            veiculos = veiculos.filter(
                Q(placa__icontains=search) |
                Q(numero_caminhao__icontains=search)
            )

        if tipo_filter:
            veiculos = veiculos.filter(tipo=tipo_filter)

        if ativo_filter != '':
            veiculos = veiculos.filter(ativo=ativo_filter == 'true')

        # Paginação
        paginator = Paginator(veiculos, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'search': search,
            'tipo_filter': tipo_filter,
            'ativo_filter': ativo_filter,
            'tipos': Veiculo.TIPO_CHOICES,
        }
        return render(request, 'app_veiculo/veiculo_list.html', context)
    except Exception as e:
        return HttpResponse(f"Erro: {str(e)}")

@login_required
def veiculo_detail(request, pk):
    """Detalhes de um veículo específico"""
    veiculo = get_object_or_404(Veiculo, pk=pk)
    rotas = veiculo.rotas.all().order_by('horario')
    
    context = {
        'veiculo': veiculo,
        'rotas': rotas,
    }
    return render(request, 'app_veiculo/veiculo_detail.html', context)

@role_required('gestor_rotas', 'admin')
def veiculo_create(request):
    """Criar novo veículo"""
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo cadastrado com sucesso!')
            return redirect('veiculo:veiculo_list')
    else:
        form = VeiculoForm()
    
    context = {'form': form}
    return render(request, 'app_veiculo/veiculo_form.html', context)

@role_required('gestor_rotas', 'admin')
def veiculo_update(request, pk):
    """Atualizar veículo existente"""
    veiculo = get_object_or_404(Veiculo, pk=pk)
    
    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo atualizado com sucesso!')
            return redirect('veiculo:veiculo_detail', pk=veiculo.pk)
    else:
        form = VeiculoForm(instance=veiculo)
    
    context = {
        'form': form,
        'veiculo': veiculo,
        'is_update': True,
    }
    return render(request, 'app_veiculo/veiculo_form.html', context)

@role_required('gestor_rotas', 'admin')
def veiculo_delete(request, pk):
    """Deletar veículo"""
    veiculo = get_object_or_404(Veiculo, pk=pk)
    
    if request.method == 'POST':
        veiculo.delete()
        messages.success(request, 'Veículo removido com sucesso!')
        return redirect('veiculo:veiculo_list')
    
    context = {'veiculo': veiculo}
    return render(request, 'app_veiculo/veiculo_confirm_delete.html', context)

@require_POST
@role_required('gestor_rotas', 'admin')
def veiculo_toggle_status(request, pk):
    """Alternar status ativo/inativo do veículo"""
    veiculo = get_object_or_404(Veiculo, pk=pk)
    veiculo.ativo = not veiculo.ativo
    veiculo.save()
    
    status = 'ativado' if veiculo.ativo else 'desativado'
    messages.success(request, f'Veículo {status} com sucesso!')
    
    return JsonResponse({
        'success': True,
        'ativo': veiculo.ativo,
        'message': f'Veículo {status} com sucesso!'
    })

# Views para Rotas
@login_required
def rota_list(request):
    """Lista todas as rotas com filtros e paginação"""
    rotas = Rota.objects.select_related('veiculo').all()
    
    # Filtros
    search = request.GET.get('search', '')
    veiculo_filter = request.GET.get('veiculo', '')
    concluida_filter = request.GET.get('concluida', '')
    
    if search:
        rotas = rotas.filter(
            Q(local__icontains=search) |
            Q(veiculo__placa__icontains=search)
        )
    
    if veiculo_filter:
        rotas = rotas.filter(veiculo_id=veiculo_filter)
    
    if concluida_filter != '':
        rotas = rotas.filter(concluida=concluida_filter == 'true')
    
    # Paginação
    paginator = Paginator(rotas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'veiculo_filter': veiculo_filter,
        'concluida_filter': concluida_filter,
        'veiculos': Veiculo.objects.filter(ativo=True),
    }
    return render(request, 'app_veiculo/rota_list.html', context)

@login_required
def rota_detail(request, pk):
    """Detalhes de uma rota específica"""
    rota = get_object_or_404(Rota, pk=pk)
    
    context = {'rota': rota}
    return render(request, 'app_veiculo/rota_detail.html', context)

@role_required('gestor_rotas', 'admin')
def rota_create(request):
    """Criar nova rota"""
    if request.method == 'POST':
        form = RotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rota cadastrada com sucesso!')
            return redirect('veiculo:rota_list')
    else:
        form = RotaForm()
    
    context = {'form': form}
    return render(request, 'app_veiculo/rota_form.html', context)

@role_required('gestor_rotas', 'admin')
def rota_update(request, pk):
    """Atualizar rota existente"""
    rota = get_object_or_404(Rota, pk=pk)
    
    if request.method == 'POST':
        form = RotaForm(request.POST, instance=rota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rota atualizada com sucesso!')
            return redirect('veiculo:rota_detail', pk=rota.pk)
    else:
        form = RotaForm(instance=rota)
    
    context = {
        'form': form,
        'rota': rota,
        'is_update': True,
    }
    return render(request, 'app_veiculo/rota_form.html', context)

@role_required('gestor_rotas', 'admin')
def rota_delete(request, pk):
    """Deletar rota"""
    rota = get_object_or_404(Rota, pk=pk)
    
    if request.method == 'POST':
        rota.delete()
        messages.success(request, 'Rota removida com sucesso!')
        return redirect('veiculo:rota_list')
    
    context = {'rota': rota}
    return render(request, 'app_veiculo/rota_confirm_delete.html', context)

@require_POST
@role_required('gestor_rotas', 'admin')
def rota_toggle_status(request, pk):
    """Alternar status concluída da rota"""
    rota = get_object_or_404(Rota, pk=pk)
    rota.concluida = not rota.concluida
    rota.save()
    
    status = 'concluída' if rota.concluida else 'reaberta'
    messages.success(request, f'Rota {status} com sucesso!')
    
    return JsonResponse({
        'success': True,
        'concluida': rota.concluida,
        'message': f'Rota {status} com sucesso!'
    })

# Views para Relatórios
@role_required('gestor_rotas', 'admin')
def relatorio_servico(request):
    """Relatório geral de serviços do sistema"""
    # Estatísticas gerais
    total_veiculos = Veiculo.objects.count()
    veiculos_ativos = Veiculo.objects.filter(ativo=True).count()
    veiculos_inativos = Veiculo.objects.filter(ativo=False).count()
    
    total_rotas = Rota.objects.count()
    rotas_concluidas = Rota.objects.filter(concluida=True).count()
    rotas_pendentes = Rota.objects.filter(concluida=False).count()
    
    # Estatísticas por tipo de veículo
    veiculos_por_tipo = Veiculo.objects.values('tipo').annotate(
        total=Count('id'),
        ativos=Count('id', filter=Q(ativo=True))
    ).order_by('tipo')
    
    # Rotas por veículo
    rotas_por_veiculo = Veiculo.objects.annotate(
        total_rotas=Count('rotas'),
        rotas_concluidas=Count('rotas', filter=Q(rotas__concluida=True)),
        rotas_pendentes=Count('rotas', filter=Q(rotas__concluida=False))
    ).order_by('placa')
    
    # Filtros de data (últimos 30 dias)
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    if not data_inicio:
        data_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    if not data_fim:
        data_fim = datetime.now().strftime('%Y-%m-%d')
    
    # Rotas por período
    rotas_periodo = Rota.objects.filter(
        data_cadastro__date__range=[data_inicio, data_fim]
    )
    
    context = {
        'total_veiculos': total_veiculos,
        'veiculos_ativos': veiculos_ativos,
        'veiculos_inativos': veiculos_inativos,
        'total_rotas': total_rotas,
        'rotas_concluidas': rotas_concluidas,
        'rotas_pendentes': rotas_pendentes,
        'veiculos_por_tipo': veiculos_por_tipo,
        'rotas_por_veiculo': rotas_por_veiculo,
        'rotas_periodo': rotas_periodo,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    
    return render(request, 'app_veiculo/relatorio_servico.html', context)

@role_required('gestor_rotas', 'admin')
def relatorio_veiculos(request):
    """Relatório detalhado de veículos"""
    veiculos = Veiculo.objects.all().order_by('placa')
    
    # Filtros
    tipo_filter = request.GET.get('tipo', '')
    status_filter = request.GET.get('status', '')
    
    if tipo_filter:
        veiculos = veiculos.filter(tipo=tipo_filter)
    
    if status_filter != '':
        veiculos = veiculos.filter(ativo=status_filter == 'true')
    
    # Adicionar estatísticas de rotas para cada veículo
    veiculos_com_stats = []
    for veiculo in veiculos:
        stats = {
            'veiculo': veiculo,
            'total_rotas': veiculo.rotas.count(),
            'rotas_concluidas': veiculo.rotas.filter(concluida=True).count(),
            'rotas_pendentes': veiculo.rotas.filter(concluida=False).count(),
        }
        veiculos_com_stats.append(stats)
    
    context = {
        'veiculos_com_stats': veiculos_com_stats,
        'tipo_filter': tipo_filter,
        'status_filter': status_filter,
        'tipos': Veiculo.TIPO_CHOICES,
    }
    
    return render(request, 'app_veiculo/relatorio_veiculos.html', context)

@role_required('gestor_rotas', 'admin')
def relatorio_rotas(request):
    """Relatório detalhado de rotas"""
    rotas = Rota.objects.select_related('veiculo').all()
    
    # Filtros
    veiculo_filter = request.GET.get('veiculo', '')
    status_filter = request.GET.get('status', '')
    dias_filter = request.GET.get('dias', '')
    
    if veiculo_filter:
        rotas = rotas.filter(veiculo_id=veiculo_filter)
    
    if status_filter != '':
        rotas = rotas.filter(concluida=status_filter == 'true')
    
    if dias_filter:
        rotas = rotas.filter(dias_semana__icontains=dias_filter)
    
    # Paginação
    paginator = Paginator(rotas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'veiculo_filter': veiculo_filter,
        'status_filter': status_filter,
        'dias_filter': dias_filter,
        'veiculos': Veiculo.objects.filter(ativo=True),
    }
    
    return render(request, 'app_veiculo/relatorio_rotas.html', context)

# Views para Problemas de Coleta
@login_required
def problema_list(request):
    """Lista todos os problemas de coleta com filtros e paginação"""
    problemas = ProblemaColeta.objects.select_related('veiculo', 'rota').all()
    
    # Filtros
    search = request.GET.get('search', '')
    veiculo_filter = request.GET.get('veiculo', '')
    tipo_filter = request.GET.get('tipo', '')
    status_filter = request.GET.get('status', '')
    prioridade_filter = request.GET.get('prioridade', '')
    
    if search:
        problemas = problemas.filter(
            Q(descricao__icontains=search) |
            Q(local_problema__icontains=search) |
            Q(responsavel_relato__icontains=search) |
            Q(veiculo__placa__icontains=search)
        )
    
    if veiculo_filter:
        problemas = problemas.filter(veiculo_id=veiculo_filter)
    
    if tipo_filter:
        problemas = problemas.filter(tipo_problema=tipo_filter)
    
    if status_filter:
        problemas = problemas.filter(status=status_filter)
    
    if prioridade_filter:
        problemas = problemas.filter(prioridade=prioridade_filter)
    
    # Paginação
    paginator = Paginator(problemas, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'veiculo_filter': veiculo_filter,
        'tipo_filter': tipo_filter,
        'status_filter': status_filter,
        'prioridade_filter': prioridade_filter,
        'veiculos': Veiculo.objects.filter(ativo=True),
        'tipos': ProblemaColeta.TIPO_PROBLEMA_CHOICES,
        'status_choices': ProblemaColeta.STATUS_CHOICES,
        'prioridade_choices': ProblemaColeta.PRIORIDADE_CHOICES,
    }
    
    return render(request, 'app_veiculo/problema_list.html', context)

@login_required
def problema_detail(request, pk):
    """Detalhes de um problema específico"""
    problema = get_object_or_404(ProblemaColeta, pk=pk)
    
    context = {
        'problema': problema,
    }
    
    return render(request, 'app_veiculo/problema_detail.html', context)

@role_required('gestor_rotas', 'admin')
def problema_create(request):
    """Criar um novo problema de coleta"""
    if request.method == 'POST':
        form = ProblemaColetaForm(request.POST)
        if form.is_valid():
            problema = form.save()
            messages.success(request, 'Problema de coleta cadastrado com sucesso!')
            return redirect('veiculo:problema_detail', pk=problema.pk)
    else:
        form = ProblemaColetaForm()
    
    context = {
        'form': form,
        'title': 'Cadastrar Problema de Coleta',
        'button_text': 'Cadastrar Problema',
    }
    
    return render(request, 'app_veiculo/problema_form.html', context)


@role_required('cidadao')
def problema_denuncia(request):
    """Permite que um cidadão registre uma denúncia de falta de coleta."""
    if request.method == 'POST':
        form = DenunciaProblemaForm(request.POST, user=request.user)
        if form.is_valid():
            problema = form.save()
            messages.success(
                request,
                'Denúncia registrada com sucesso. Nossa equipe analisará a ocorrência.',
            )
            return redirect('veiculo:problema_detail', pk=problema.pk)
    else:
        form = DenunciaProblemaForm(user=request.user)

    context = {
        'form': form,
        'title': 'Denunciar Falta de Coleta',
        'button_text': 'Enviar Denúncia',
    }

    return render(request, 'app_veiculo/denuncia_form.html', context)

@role_required('gestor_rotas', 'admin')
def problema_update(request, pk):
    """Atualizar um problema de coleta"""
    problema = get_object_or_404(ProblemaColeta, pk=pk)
    
    if request.method == 'POST':
        form = ProblemaColetaForm(request.POST, instance=problema)
        if form.is_valid():
            problema = form.save()
            messages.success(request, 'Problema de coleta atualizado com sucesso!')
            return redirect('veiculo:problema_detail', pk=problema.pk)
    else:
        form = ProblemaColetaForm(instance=problema)
    
    context = {
        'form': form,
        'problema': problema,
        'title': 'Atualizar Problema de Coleta',
        'button_text': 'Atualizar Problema',
    }
    
    return render(request, 'app_veiculo/problema_form.html', context)

@role_required('gestor_rotas', 'admin')
def problema_delete(request, pk):
    """Deletar um problema de coleta"""
    problema = get_object_or_404(ProblemaColeta, pk=pk)
    
    if request.method == 'POST':
        problema.delete()
        messages.success(request, 'Problema de coleta excluído com sucesso!')
        return redirect('veiculo:problema_list')
    
    context = {
        'problema': problema,
    }
    
    return render(request, 'app_veiculo/problema_confirm_delete.html', context)

@require_POST
@csrf_exempt
@role_required('gestor_rotas', 'admin')
def problema_toggle_status(request, pk):
    """Alterar status do problema via AJAX"""
    try:
        problema = get_object_or_404(ProblemaColeta, pk=pk)
        
        # Alternar entre status
        if problema.status == 'aberto':
            problema.status = 'em_andamento'
        elif problema.status == 'em_andamento':
            problema.status = 'resolvido'
            problema.data_resolucao = datetime.now()
        elif problema.status == 'resolvido':
            problema.status = 'aberto'
            problema.data_resolucao = None
        
        problema.save()
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
    status = problema.get_status_display()
    messages.success(request, f'Status alterado para: {status}')
    
    return JsonResponse({
        'success': True,
        'status': problema.status,
        'status_display': status,
        'message': f'Status alterado para: {status}'
    })
