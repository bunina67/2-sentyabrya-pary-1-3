class Application:
    def __init__(self, name):
        self.name = name
        self.blocked = False


class AppStore:
    def __init__(self):
        self.apps = []
    
    def add_application(self, app):
        self.apps.append(app)
    
    def remove_application(self, app):
        if app in self.apps:
            self.apps.remove(app)
    
    def block_application(self, app):
        app.blocked = True
    
    def total_apps(self):
        return len(self.apps)


# Проверка
store = AppStore()
app_youtube = Application("Youtube")
app_vk = Application("VK")

store.add_application(app_youtube)
store.add_application(app_vk)

print("Всего приложений:", store.total_apps())  # 2

store.block_application(app_youtube)
print("Youtube заблокирован:", app_youtube.blocked)  # True

store.remove_application(app_youtube)
print("Всего приложений:", store.total_apps())  # 1
