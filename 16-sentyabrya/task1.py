class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip


class Server:
    __ip_counter = 0

    def __init__(self):
        Server.__ip_counter += 1
        self.ip = Server.__ip_counter
        self.buffer = []

    def send_data(self, data):
        router.buffer.append(data)

    def get_data(self):
        data = self.buffer[:]
        self.buffer.clear()
        return data

    def get_ip(self):
        return self.ip


class Router:
    def __init__(self):
        self.buffer = []
        self.servers = []

    def link(self, server):
        self.servers.append(server)

    def unlink(self, server):
        if server in self.servers:
            self.servers.remove(server)

    def send_data(self):
        for data in self.buffer:
            for server in self.servers:
                if server.get_ip() == data.ip:
                    server.buffer.append(data)
                    break
        self.buffer.clear()


if __name__ == "__main__":
    router = Router()
    sv_from = Server()
    sv_from2 = Server()
    router.link(sv_from)
    router.link(sv_from2)
    router.link(Server())
    router.link(Server())
    sv_to = Server()
    router.link(sv_to)

    sv_from.send_data(Data("Hello", sv_to.get_ip()))
    sv_from2.send_data(Data("Hello", sv_to.get_ip()))
    sv_to.send_data(Data("Hi", sv_from.get_ip()))
    router.send_data()

    msg_lst_from = sv_from.get_data()
    msg_lst_to = sv_to.get_data()

    print("Сообщения для sv_from:", [d.data for d in msg_lst_from])
    print("Сообщения для sv_to:", [d.data for d in msg_lst_to])
