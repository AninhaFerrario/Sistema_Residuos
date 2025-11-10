from django.urls import path
from app_usuario import views

urlpatterns = [
    path('', views.login, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout_view, name="logout"),
    path('usuarios/', views.gerenciar_usuarios, name="gerenciar_usuarios"),
    path('usuarios/<int:pk>/alterar-status/', views.alterar_status_usuario, name="alterar_status_usuario"),
]