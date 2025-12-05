from django.contrib.auth import logout
from .models import Comanda, ItemCardapio, ItemComanda
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 SISTEMA DE PERMISSÕES AQUI
            if user.is_superuser or user.is_staff:
                return redirect('/admin/')        # admin
            else:
                return redirect('menu_atendente') # atendente

        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, 'login.html')



@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def menu_atendente(request):
    """Menu principal do atendente"""
    return render(request, 'menu_atendente.html')


@login_required
def listar_comandas(request):
    comandas = Comanda.objects.filter(atendente=request.user, finalizada=False)
    return render(request, 'listar_comandas.html', {'comandas': comandas})


@login_required
def nova_comanda(request):
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        comanda = Comanda.objects.create(cliente=cliente, atendente=request.user)
        return redirect('editar_comanda', comanda_id=comanda.id)
    return render(request, 'nova_comanda.html')

@login_required
def editar_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id, atendente=request.user)
    itens_cardapio = ItemCardapio.objects.all()

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantidade = int(request.POST.get('quantidade', 1))

        item = ItemCardapio.objects.get(id=item_id)

        ItemComanda.objects.create(
            comanda=comanda,
            item_cardapio=item,
            quantidade=quantidade
        )

        return redirect('editar_comanda', comanda_id=comanda.id)

    return render(request, 'editar_comanda.html', {
        'comanda': comanda,
        'itens_cardapio': itens_cardapio
    })


@login_required
def finalizar_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id, atendente=request.user)
    comanda.finalizada = True
    comanda.save()
    return redirect('listar_comandas')

@login_required
def apagar_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id)

    # Apenas atendente dono da comanda OU admin pode excluir
    if request.user == comanda.atendente or request.user.is_staff:
        comanda.delete()
        return redirect('listar_comandas')  
    else:
        return redirect('menu_atendente')


@login_required
def vendas_fechadas(request):
    vendas = Comanda.objects.filter(finalizada=True).order_by('-data_fechamento')

    return render(request, 'vendas_fechadas.html', {
        'vendas': vendas
    })

def detalhe_venda(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id, finalizada=True)
    itens = comanda.itens.all()

    return render(request, 'detalhe_venda.html', {
        'comanda': comanda,
        'itens': itens
    })

def apagar_venda_finalizada(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id, finalizada=True)
    comanda.delete()
    return redirect('vendas_fechadas')

@login_required
def remover_item(request, item_id):
    item = get_object_or_404(ItemComanda, id=item_id)

    # Permitir remover apenas se o atendente for o dono da comanda
    if item.comanda.atendente != request.user:
        return redirect('menu_atendente')

    comanda_id = item.comanda.id
    item.delete()

    return redirect('editar_comanda', comanda_id=comanda_id)

@login_required
def adicionar_item(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id, atendente=request.user)

    if request.method == "POST":
        item_id = request.POST.get("item_id")
        quantidade = int(request.POST.get("quantidade", 1))

        item = get_object_or_404(ItemCardapio, id=item_id)

        ItemComanda.objects.create(
            comanda=comanda,
            item_cardapio=item,
            quantidade=quantidade
        )

    return redirect('editar_comanda', comanda_id=comanda.id)



