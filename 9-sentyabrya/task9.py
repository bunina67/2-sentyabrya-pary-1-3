class Figure:
    def __init__(self, coords, width, color):
        self.coords = coords
        self.width = width
        self.color = color

    def draw(self):
        print("Рисуется фигура")

class Line(Figure):
    def draw(self):
        print("Рисуется линия...")

class Rect(Figure):
    def draw(self):
        print("Рисуется прямоугольник...")

class Ellipse(Figure):
    def draw(self):
        print("Рисуется эллипс...")

# Создаем список фигур
figures = [
    Line((0, 0), 2, "красный"),
    Rect((1, 1), 3, "синий"),
    Ellipse((2, 2), 4, "зеленый")
]

# Один цикл для всех
for fig in figures:
    fig.draw()

# Добавляем Triangle, не меняя цикл
class Triangle(Figure):
    def draw(self):
        print("Рисуется треугольник...")

figures.append(Triangle((3, 3), 5, "желтый"))

print("--- После добавления треугольника ---")
for fig in figures:
    fig.draw()