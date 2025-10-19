from django.db import models
from django.db import models

class ItemCardapio(models.Model):
    CATEGORIAS = [
        ('ESPETO', 'Espeto'),
        ('BEBIDA', 'Bebida'),
        ('ACOMPANHAMENTO', 'Acompanhamento'),
    ]

    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nome} ({self.categoria})"

from django.db import models
from django.contrib.auth.models import User

class ItemCardapio(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    estoque = models.IntegerField(default=0)

    def __str__(self):
        return self.nome


class Comanda(models.Model):
    atendente = models.ForeignKey(User, on_delete=models.CASCADE)
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_fechamento = models.DateTimeField(null=True, blank=True)
    finalizada = models.BooleanField(default=False)

    def total(self):
        itens = self.itens.all()
        return sum(item.subtotal() for item in itens)

    def __str__(self):
        return f"Comanda #{self.id} - {self.atendente.username}"


class ItemComanda(models.Model):
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE, related_name='itens')
    item_cardapio = models.ForeignKey(ItemCardapio, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.item_cardapio.preco * self.quantidade

    def __str__(self):
        return f"{self.quantidade}x {self.item_cardapio.nome}"

