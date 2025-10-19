from django.contrib import admin
from .models import ItemCardapio, Comanda, ItemComanda

@admin.register(ItemCardapio)
class ItemCardapioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'estoque')
    search_fields = ('nome',)
    list_filter = ('categoria',)

admin.site.register(Comanda)
admin.site.register(ItemComanda)

