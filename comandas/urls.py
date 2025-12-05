from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_atendente, name='menu_atendente'),

    # Login/logout
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),

    # Comandas ativas
    path('vendas/', views.listar_comandas, name='listar_comandas'),
    path('vendas/nova/', views.nova_comanda, name='nova_comanda'),
    path('vendas/<int:comanda_id>/', views.editar_comanda, name='editar_comanda'),
    path('vendas/<int:comanda_id>/finalizar/', views.finalizar_comanda, name='finalizar_comanda'),
    path('vendas/<int:comanda_id>/apagar/', views.apagar_comanda, name='apagar_comanda'),

    # Adicionar item
    path('vendas/<int:comanda_id>/adicionar_item/', views.adicionar_item, name='adicionar_item'),

    # Vendas finalizadas
    path('vendas/fechadas/', views.vendas_fechadas, name='vendas_fechadas'),
    path('vendas/fechadas/<int:comanda_id>/', views.detalhe_venda, name='detalhe_venda'),
    path('vendas/fechadas/<int:comanda_id>/apagar/', views.apagar_venda_finalizada, name='apagar_venda_finalizada'),

    # Remover item
    path('vendas/item/<int:item_id>/remover/', views.remover_item, name='remover_item'),
]

