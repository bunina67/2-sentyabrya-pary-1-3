class TriangleChecker:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def is_triangle(self):
        if not all(isinstance(x, (int, float)) for x in [self.a, self.b, self.c]):
            return 1
        if self.a <= 0 or self.b <= 0 or self.c <= 0:
            return 1
        if self.a + self.b > self.c and self.a + self.c > self.b and self.b + self.c > self.a:
            return 3
        return 2

a, b, c = map(int, input().split())
tr = TriangleChecker(a, b, c)
print(tr.is_triangle())
