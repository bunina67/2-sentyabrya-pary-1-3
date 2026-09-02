class Figure:
    def __init__(self, coords, width, color):
        self.coords = coords
        self.width = width
        self.color = color

class Line(Figure):
    def __init__(self, coords, width, color, length):
        super().__init__(coords, width, color)
        self.length = length

class Rect(Figure):
    def __init__(self, coords, width, color, height):
        super().__init__(coords, width, color)
        self.height = height

class Ellipse(Figure):
    def __init__(self, coords, width, color, radius):
        super().__init__(coords, width, color)
        self.radius = radius

line = Line((0, 0), 2, "красный", 10)
rect = Rect((1, 1), 3, "синий", 5)
ellipse = Ellipse((2, 2), 4, "зеленый", 7)

print(f"Линия: координаты {line.coords}, ширина {line.width}, цвет {line.color}, длина {line.length}")
print(f"Прямоугольник: координаты {rect.coords}, ширина {rect.width}, цвет {rect.color}, высота {rect.height}")
print(f"Эллипс: координаты {ellipse.coords}, ширина {ellipse.width}, цвет {ellipse.color}, радиус {ellipse.radius}")