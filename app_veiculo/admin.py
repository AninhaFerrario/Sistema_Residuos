from django.contrib import admin
from .models import Veiculo, Rota, ProblemaColeta

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ['placa', 'tipo', 'numero_caminhao', 'ativo', 'data_cadastro']
    list_filter = ['tipo', 'ativo', 'data_cadastro']
    search_fields = ['placa', 'numero_caminhao']
    list_editable = ['ativo']
    ordering = ['placa']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('placa', 'tipo', 'numero_caminhao')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )

@admin.register(Rota)
class RotaAdmin(admin.ModelAdmin):
    list_display = ['veiculo', 'local', 'horario', 'dias_semana', 'concluida', 'data_cadastro']
    list_filter = ['concluida', 'veiculo__tipo', 'veiculo']
    search_fields = ['local', 'veiculo__placa', 'dias_semana']
    list_editable = ['concluida']
    ordering = ['horario']
    
    fieldsets = (
        ('Informações da Rota', {
            'fields': ('veiculo', 'local', 'horario', 'dias_semana')
        }),
        ('Status e Observações', {
            'fields': ('concluida', 'observacoes')
        }),
    )

@admin.register(ProblemaColeta)
class ProblemaColetaAdmin(admin.ModelAdmin):
    list_display = [
        'tipo_problema', 'veiculo', 'prioridade', 'status', 
        'data_ocorrencia', 'responsavel_relato'
    ]
    list_filter = [
        'tipo_problema', 'prioridade', 'status', 'data_ocorrencia', 
        'veiculo__tipo', 'veiculo'
    ]
    search_fields = [
        'descricao', 'local_problema', 'responsavel_relato', 
        'veiculo__placa', 'solucao'
    ]
    list_editable = ['status', 'prioridade']
    ordering = ['-data_ocorrencia', '-prioridade']
    date_hierarchy = 'data_ocorrencia'
    
    fieldsets = (
        ('Informações do Problema', {
            'fields': ('veiculo', 'rota', 'tipo_problema', 'prioridade', 'status')
        }),
        ('Detalhes da Ocorrência', {
            'fields': ('descricao', 'local_problema', 'data_ocorrencia', 'responsavel_relato')
        }),
        ('Resolução', {
            'fields': ('solucao', 'data_resolucao', 'observacoes')
        }),
    )
    
    readonly_fields = ['data_cadastro', 'data_atualizacao']
