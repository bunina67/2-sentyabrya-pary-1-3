class TravelBlog:
    total_blogs = 0

# Первый экземпляр
tb1 = TravelBlog()
tb1.name = 'Франция'
tb1.days = 6
TravelBlog.total_blogs += 1

# Второй экземпляр
tb2 = TravelBlog()
tb2.name = 'Италия'
tb2.days = 5
TravelBlog.total_blogs += 1

# Выводим итоговое значение
print(TravelBlog.total_blogs)