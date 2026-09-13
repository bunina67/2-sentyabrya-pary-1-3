class Point:
    def __init__(self, x, y, color='black'):
        self.x = x
        self.y = y
        self.color = color

# Создаем список из 3 точек
points = [
    Point(10, 20),
    Point(12, 5, 'red'),
    Point(7, 3, 'green')
]

for p in points:
    print(f"x={p.x}, y={p.y}, color={p.color}")