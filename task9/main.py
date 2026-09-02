class Figure:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_coords(self):
        return self._x, self._y

    def set_coords(self, x, y):
        self._x = x
        self._y = y

class Circle(Figure):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def calculate_area(self):
        return 3.14159 * self.radius ** 2

class Square(Figure):
    def __init__(self, x, y, side):
        super().__init__(x, y)
        self.side = side

    def calculate_area(self):
        return self.side ** 2

figures = [
    Circle(0, 0, 5),
    Square(10, 10, 4),
    Circle(2, 3, 2),
    Square(1, 1, 6),
    Circle(5, 5, 3)
]

total_area = 0
for fig in figures:
    total_area += fig.calculate_area()

print("Общая площадь всех фигур:", total_area)