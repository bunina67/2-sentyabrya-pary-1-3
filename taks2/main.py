class Cat:
    def __init__(self, breed, name, age):
        self.breed = breed
        self.name = name
        self.age = age

    def draw(self):
        print(f"На экране рисуется кот {self.name}, порода {self.breed}")

cat1 = Cat("Британская", "Мурзик", 2)
cat2 = Cat("Сиамская", "Саймон", 4)
cat3 = Cat("Дворовая", "Барсик", 1)

cat1.draw()
cat2.draw()
cat3.draw()