from src.repository.result import Item

def test_item_from_json():
    item_json = {
    "item": "Smartphone",
    "qtd": 1,
    "total": 2345.12,
    "natureza": "saida",
    "parcelado": False,
    "parcelas": 1,
    "parcela_atual": 1,
    }

    item = Item.from_json(item_json)
    item.distribuir_parcelas_e_inserir()