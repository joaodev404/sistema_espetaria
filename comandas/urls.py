from django.urls import path
from . import views

urlpatterns = [
    # --- Login e Logout ---
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # --- Cardápio ---
    path('cardapio/', views.cardapio_view, name='cardapio'),

    # --- Sistema de Vendas ---
    path('vendas/', views.listar_comandas, name='listar_comandas'),
    path('vendas/nova/', views.nova_comanda, name='nova_comanda'),
    path('vendas/<int:comanda_id>/', views.editar_comanda, name='editar_comanda'),
    path('vendas/<int:comanda_id>/finalizar/', views.finalizar_comanda, name='finalizar_comanda'),

    # --- Página inicial (opcional) ---
    path('', views.login_view, name='home'),  # agora "/" abre o login
]

