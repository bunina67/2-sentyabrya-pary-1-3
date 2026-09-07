class Point:
    def __init__(self, x, y, color='black'):
        self.x = x
        self.y = y
        self.color = color

points = []
for i in range(1, 1001):
    coord = 2 * i - 1
    if i == 2:
        points.append(Point(coord, coord, 'yellow'))
    else:
        points.append(Point(coord, coord))
