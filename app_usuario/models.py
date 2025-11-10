from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class PerfilUsuario(models.Model):
    STATUS_CHOICES = [
        ('gestor_rotas', 'gestor_rotas'), # Gestor de Rotas
        ('admin', 'Administrador'), # Administrador do sistema
        ('cidadao', 'Cidadão'), # Cidadão comum
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    email = models.EmailField(unique=True, verbose_name='Email')
    nome = models.CharField(max_length=100, verbose_name='Nome Completo')
    departamento = models.CharField(max_length=100, verbose_name='Departamento')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='cidadao',
        verbose_name='Status de Acesso'
    )
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    ativo = models.BooleanField(default=True, verbose_name='Usuário Ativo')
    
    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - {self.get_status_display()}"
    
    def get_status_display_name(self):
        return dict(self.STATUS_CHOICES)[self.status]

# Signal para criar automaticamente um perfil quando um usuário é criado
@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(
            user=instance,
            email=instance.email,
            nome=f"{instance.first_name} {instance.last_name}".strip() or instance.username,
            departamento='Não informado',
        )

# Signal para salvar automaticamente o perfil quando o usuário é atualizado
@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):
        instance.perfil.save()
