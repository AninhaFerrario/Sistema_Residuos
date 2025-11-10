from django.db import models
from django.core.validators import RegexValidator

class Veiculo(models.Model):
    TIPO_CHOICES = [
        ('compactador', 'Compactador'),
        ('caçamba', 'Caçamba'),
    ]
    
    placa = models.CharField(
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{3}[0-9]{4}$|^[A-Z]{3}[0-9][A-Z][0-9]{2}$',
                message='Formato de placa inválido. Use o formato ABC1234 ou ABC1D23'
            )
        ],
        help_text='Formato: ABC1234 ou ABC1D23'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        help_text='Selecione o tipo do veículo'
    )
    numero_caminhao = models.CharField(
        max_length=20,
        unique=True,
        help_text='Número identificador do caminhão'
    )
    ativo = models.BooleanField(default=True, help_text='Veículo ativo no sistema')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        db_table = "veiculos"
        ordering = ['placa']
    
    def __str__(self):
        return f"{self.placa} - {self.get_tipo_display()}"

class Rota(models.Model):
    DIAS_SEMANA_CHOICES = [
        ('seg', 'Segunda-feira'),
        ('ter', 'Terça-feira'),
        ('qua', 'Quarta-feira'),
        ('qui', 'Quinta-feira'),
        ('sex', 'Sexta-feira'),
        ('sab', 'Sábado'),
        ('dom', 'Domingo'),
    ]
    
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        related_name='rotas',
        help_text='Veículo responsável pela rota'
    )
    local = models.CharField(
        max_length=200,
        help_text='Local da coleta'
    )
    horario = models.TimeField(help_text='Horário da coleta')
    dias_semana = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='Dias da semana (ex: Seg, Ter, Qua)'
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        help_text='Observações adicionais'
    )
    concluida = models.BooleanField(
        default=False,
        help_text='Rota concluída'
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Rota"
        verbose_name_plural = "Rotas"
        db_table = "rotas"
        ordering = ['horario']
        unique_together = ['veiculo', 'horario']
    
    def __str__(self):
        return f"{self.veiculo.placa} - {self.local} ({self.horario})"

class ProblemaColeta(models.Model):
    TIPO_PROBLEMA_CHOICES = [
        ('coleta_nao_feita', 'Coleta sem ser feita'),
        ('area_dificil_acesso', 'Áreas de difícil acesso'),
        ('problema_mecanico', 'Problema mecânico'),
        ('outros', 'Outros'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em Andamento'),
        ('resolvido', 'Resolvido'),
        ('cancelado', 'Cancelado'),
    ]
    
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        related_name='problemas',
        help_text='Veículo relacionado ao problema'
    )
    rota = models.ForeignKey(
        Rota,
        on_delete=models.CASCADE,
        related_name='problemas',
        null=True,
        blank=True,
        help_text='Rota relacionada ao problema (opcional)'
    )
    tipo_problema = models.CharField(
        max_length=30,
        choices=TIPO_PROBLEMA_CHOICES,
        help_text='Tipo do problema identificado'
    )
    prioridade = models.CharField(
        max_length=10,
        choices=PRIORIDADE_CHOICES,
        default='media',
        help_text='Prioridade do problema'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='aberto',
        help_text='Status atual do problema'
    )
    descricao = models.TextField(
        help_text='Descrição detalhada do problema'
    )
    local_problema = models.CharField(
        max_length=200,
        help_text='Local onde ocorreu o problema'
    )
    data_ocorrencia = models.DateTimeField(
        help_text='Data e hora da ocorrência do problema'
    )
    responsavel_relato = models.CharField(
        max_length=100,
        help_text='Nome do responsável que relatou o problema'
    )
    solucao = models.TextField(
        blank=True,
        null=True,
        help_text='Solução aplicada (preenchido quando resolvido)'
    )
    data_resolucao = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Data e hora da resolução do problema'
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        help_text='Observações adicionais'
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Problema de Coleta"
        verbose_name_plural = "Problemas de Coleta"
        db_table = "problemas_coleta"
        ordering = ['-data_ocorrencia', '-prioridade']
    
    def __str__(self):
        return f"{self.get_tipo_problema_display()} - {self.veiculo.placa} ({self.data_ocorrencia.date()})"