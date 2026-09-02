class Graph:
    def __init__(self, x=0, y=0, scale=1):
        self._x = x
        self._y = y
        self._scale = scale

    def move(self, dx, dy):
        self._x += dx
        self._y += dy

    def change_scale(self, factor):
        self._scale *= factor

    def get_state(self):
        return self._x, self._y, self._scale

g1 = Graph()
g2 = Graph(5, 10, 2)
g3 = Graph(-3, 4, 0.5)

g1.move(10, 5)
g2.change_scale(3)

print("Состояние g1:", g1.get_state())
print("Состояние g2:", g2.get_state())
print("Состояние g3:", g3.get_state())