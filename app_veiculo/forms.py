from django import forms
from django.utils import timezone

from .models import Veiculo, Rota, ProblemaColeta

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'tipo', 'numero_caminhao', 'ativo']
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: ABC1234 ou ABC1D23',
                'maxlength': '8'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'numero_caminhao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número do caminhão'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'placa': 'Placa do Veículo',
            'tipo': 'Tipo do Veículo',
            'numero_caminhao': 'Número do Caminhão',
            'ativo': 'Veículo Ativo',
        }

    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        if placa:
            placa = placa.upper()
        return placa

class RotaForm(forms.ModelForm):
    class Meta:
        model = Rota
        fields = ['veiculo', 'local', 'horario', 'dias_semana', 'observacoes', 'concluida']
        widgets = {
            'veiculo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'local': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Local da coleta'
            }),
            'horario': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'dias_semana': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Seg, Ter, Qua ou Segunda, Terça'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações adicionais (opcional)'
            }),
            'concluida': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'veiculo': 'Veículo',
            'local': 'Local da Coleta',
            'horario': 'Horário da Coleta',
            'dias_semana': 'Dias da Semana',
            'observacoes': 'Observações',
            'concluida': 'Rota Concluída',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas veículos ativos
        self.fields['veiculo'].queryset = Veiculo.objects.filter(ativo=True)

class ProblemaColetaForm(forms.ModelForm):
    class Meta:
        model = ProblemaColeta
        fields = [
            'veiculo', 'rota', 'tipo_problema', 'prioridade', 'status',
            'descricao', 'local_problema', 'data_ocorrencia', 
            'responsavel_relato', 'solucao', 'observacoes'
        ]
        widgets = {
            'veiculo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'rota': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tipo_problema': forms.Select(attrs={
                'class': 'form-control'
            }),
            'prioridade': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva detalhadamente o problema ocorrido'
            }),
            'local_problema': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Rua Principal, 123 - Centro'
            }),
            'data_ocorrencia': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'responsavel_relato': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do responsável que relatou'
            }),
            'solucao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva a solução aplicada (opcional)'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observações adicionais (opcional)'
            }),
        }
        labels = {
            'veiculo': 'Veículo',
            'rota': 'Rota (Opcional)',
            'tipo_problema': 'Tipo do Problema',
            'prioridade': 'Prioridade',
            'status': 'Status',
            'descricao': 'Descrição do Problema',
            'local_problema': 'Local do Problema',
            'data_ocorrencia': 'Data e Hora da Ocorrência',
            'responsavel_relato': 'Responsável pelo Relato',
            'solucao': 'Solução Aplicada',
            'observacoes': 'Observações',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas veículos ativos
        self.fields['veiculo'].queryset = Veiculo.objects.filter(ativo=True)
        
        # Filtrar rotas do veículo selecionado
        if 'veiculo' in self.data:
            try:
                veiculo_id = int(self.data.get('veiculo'))
                self.fields['rota'].queryset = Rota.objects.filter(veiculo_id=veiculo_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['rota'].queryset = self.instance.veiculo.rotas.all()
        else:
            self.fields['rota'].queryset = Rota.objects.none()


class DenunciaProblemaForm(forms.ModelForm):
    class Meta:
        model = ProblemaColeta
        fields = ['rota', 'local_problema', 'data_ocorrencia', 'descricao', 'observacoes']
        widgets = {
            'rota': forms.Select(attrs={'class': 'form-control'}),
            'local_problema': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Rua das Flores, nº 123 - Bairro Centro'
            }),
            'data_ocorrencia': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva como a coleta deixou de acontecer na sua rua'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Informações adicionais (opcional)'
            }),
        }
        labels = {
            'rota': 'Rota relacionada',
            'local_problema': 'Local da ocorrência',
            'data_ocorrencia': 'Data e hora observadas',
            'descricao': 'Relato do cidadão',
            'observacoes': 'Observações adicionais',
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['rota'].queryset = Rota.objects.select_related('veiculo').order_by('local')

        if not self.initial.get('data_ocorrencia') and 'data_ocorrencia' not in self.data:
            now = timezone.localtime().replace(second=0, microsecond=0)
            self.fields['data_ocorrencia'].initial = now.strftime('%Y-%m-%dT%H:%M')

    def save(self, commit=True):
        denuncia = super().save(commit=False)
        rota = self.cleaned_data['rota']
        denuncia.veiculo = rota.veiculo
        denuncia.tipo_problema = 'coleta_nao_feita'
        denuncia.prioridade = 'media'
        denuncia.status = 'aberto'
        if self.user and hasattr(self.user, 'perfil'):
            denuncia.responsavel_relato = self.user.perfil.nome
        else:
            denuncia.responsavel_relato = 'Cidadão'
        if commit:
            denuncia.save()
        return denuncia
