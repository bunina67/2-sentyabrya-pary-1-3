class Graph:
    def __init__(self, data):
        self.data = data[:]
        self.is_show = True

    def show_table(self):
        if not self.is_show:
            print("Отображение данных закрыто")
        else:
            print(' '.join(map(str, self.data)))

    def set_show(self, fl_show):
        self.is_show = fl_show

# Тест
gr = Graph([1, 2, 3, 4, 5])
gr.show_table()
gr.set_show(False)
gr.show_table()