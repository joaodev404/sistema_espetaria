from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import ItemCardapio


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 👇 Se for superusuário (admin), vai para o painel
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('cardapio')  # 👈 se for atendente
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha incorretos'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
        return redirect('cardapio')

@login_required
def cardapio_view(request):
    itens = ItemCardapio.objects.all()
    return render(request, 'cardapio.html', {'itens': itens})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comanda, ItemComanda, ItemCardapio
from django.utils import timezone

@login_required
def listar_comandas(request):
    comandas = Comanda.objects.filter(atendente=request.user, finalizada=False)
    return render(request, 'comandas/listar_comandas.html', {'comandas': comandas})

@login_required
def nova_comanda(request):
    comanda = Comanda.objects.create(atendente=request.user)
    return redirect('editar_comanda', comanda_id=comanda.id)

@login_required
def editar_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id)
    itens_cardapio = ItemCardapio.objects.all()

    if request.method == 'POST':
        item_id = request.POST.get('item_cardapio')
        quantidade = int(request.POST.get('quantidade', 1))
        item_cardapio = get_object_or_404(ItemCardapio, id=item_id)

        ItemComanda.objects.create(comanda=comanda, item_cardapio=item_cardapio, quantidade=quantidade)
        return redirect('editar_comanda', comanda_id=comanda.id)

    return render(request, 'comandas/editar_comanda.html', {'comanda': comanda, 'itens_cardapio': itens_cardapio})

@login_required
def finalizar_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id)
    comanda.finalizada = True
    comanda.data_fechamento = timezone.now()
    comanda.save()
    return redirect('listar_comandas')
