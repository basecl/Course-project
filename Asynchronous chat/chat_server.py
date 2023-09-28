import socket
import threading

class ChatServer:
    def __init__(self, host="127.0.0.1", port=50):
        self.host = host
        self.port = port
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.lock = threading.Lock()

    def start(self):
        try:
            self.socket_server.bind((self.host, self.port))
            self.socket_server.listen()
            print("Сервер запущен")

            while True:
                conn, addr = self.socket_server.accept()
                client_name = conn.recv(1024).decode()
                self.clients[client_name] = conn
                print(f"{client_name} присоединился!")
                threading.Thread(target=self.handle_client, args=(client_name,)).start()


        except Exception as e:
            print(f"Ошибка сервера: {e}")
            self.stop()

    def stop(self):
        self.socket_server.close()
        print("Сервер остановлен")

    def handle_client(self, client_name):
        conn = self.clients[client_name]
        try:
            while True:
                message = self.receive_message(conn)
                if message.lower() == "выход" or message.lower() == "exit":
                    self.remove_client(client_name)
                    print(f"{client_name} покинул чат.")
                    self.broadcast_message(f"{client_name} покинул чат.")
                    break
                else:
                    print(f"{client_name}: {message}")
                    self.broadcast_message(f"{client_name}: {message}")

        except Exception as e:
            print(f"Ошибка при получении сообщения от {client_name}: {e}")
            self.remove_client(client_name)

    def receive_message(self, conn):
        message = ""
        while "\n" not in message:
            try:
                chunk = conn.recv(1024).decode()
                if not chunk:
                    raise ConnectionError()
                message += chunk
            except Exception:
                raise ConnectionError("Соединение разорвано.")
        return message.strip()

    def broadcast_message(self, message):
        with self.lock:
            for client_conn in self.clients.values():
                try:
                    client_conn.send((message + "\n").encode())
                except Exception:
                    pass

    def remove_client(self, client_name):
        with self.lock:
            conn = self.clients.pop(client_name, None)
            if conn:
                conn.close()

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start()
