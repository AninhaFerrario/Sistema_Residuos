from django.urls import path
from . import views

app_name = 'veiculo'

urlpatterns = [
    # URLs para Veículos
    path('', views.veiculo_list, name='veiculo_list'),
    path('veiculo/<int:pk>/', views.veiculo_detail, name='veiculo_detail'),
    path('veiculo/create/', views.veiculo_create, name='veiculo_create'),
    path('veiculo/<int:pk>/update/', views.veiculo_update, name='veiculo_update'),
    path('veiculo/<int:pk>/delete/', views.veiculo_delete, name='veiculo_delete'),
    path('veiculo/<int:pk>/toggle-status/', views.veiculo_toggle_status, name='veiculo_toggle_status'),
    
    # URLs para Rotas
    path('rotas/', views.rota_list, name='rota_list'),
    path('rota/<int:pk>/', views.rota_detail, name='rota_detail'),
    path('rota/create/', views.rota_create, name='rota_create'),
    path('rota/<int:pk>/update/', views.rota_update, name='rota_update'),
    path('rota/<int:pk>/delete/', views.rota_delete, name='rota_delete'),
    path('rota/<int:pk>/toggle-status/', views.rota_toggle_status, name='rota_toggle_status'),
    
    # URLs para Relatórios
    path('relatorios/', views.relatorio_servico, name='relatorio_servico'),
    path('relatorios/veiculos/', views.relatorio_veiculos, name='relatorio_veiculos'),
    path('relatorios/rotas/', views.relatorio_rotas, name='relatorio_rotas'),
    
    # URLs para Problemas de Coleta
    path('problemas/', views.problema_list, name='problema_list'),
    path('problema/denuncia/', views.problema_denuncia, name='problema_denuncia'),
    path('problema/<int:pk>/', views.problema_detail, name='problema_detail'),
    path('problema/create/', views.problema_create, name='problema_create'),
    path('problema/<int:pk>/update/', views.problema_update, name='problema_update'),
    path('problema/<int:pk>/delete/', views.problema_delete, name='problema_delete'),
    path('problema/<int:pk>/toggle-status/', views.problema_toggle_status, name='problema_toggle_status'),
]
