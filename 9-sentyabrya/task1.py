class Goods:
    title = "Мороженое"
    weight = 150
    tp = "Еда"
    price = 100

# Изменяем цену и добавляем новый атрибут через setattr
setattr(Goods, 'price', 2048)
setattr(Goods, 'inflation', 100)

print(f"Цена: {Goods.price}, Инфляция: {Goods.inflation}")