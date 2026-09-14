class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def clone(self):
        return Point(self.x, self.y)

# Проверка
pt = Point(10, 20)
pt_clone = pt.clone()

print(f"Оригинал: x={pt.x}, y={pt.y}")
print(f"Копия: x={pt_clone.x}, y={pt_clone.y}")
