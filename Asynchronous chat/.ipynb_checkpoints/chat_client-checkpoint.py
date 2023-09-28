import socket
import threading
import time

class ChatClient:
    def __init__(self, host="127.0.0.1", port=50):
        self.host = host
        self.port = port
        self.socket_client = None

    def connect(self):
        while True:
            try:
                self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket_client.connect((self.host, self.port))
                print("Подключено к серверу")
                name = input("Введите имя: ")
                self.socket_client.send(name.encode())
                receive_thread = threading.Thread(target=self.receive_messages)
                receive_thread.start()

                while True:
                    message = input("")
                    self.socket_client.send((message + "\n").encode())

            except Exception as e:
                print(f"Ошибка клиента: {e}")
                print("Переподключение...")
                time.sleep(3)
                if self.socket_client:
                    self.socket_client.close()

    def login(self):
        while True:
            name = input("Введите имя: ")
            self.socket_client.send(name.encode())
            response = self.socket_client.recv(1024).decode()
            if response == "OK":
                print(f"Добро пожаловать, {name}!")
                break
            else:
                print("Имя уже занято. Пожалуйста, выберите другое имя.")

    def receive_messages(self):
        try:
            while True:
                message = self.receive_message()
                print(message)
        except Exception as e:
            print(f"Ошибка при получении сообщений: {e}")
            self.disconnect()

    def receive_message(self):
        message = ""
        while "\n" not in message:
            try:
                chunk = self.socket_client.recv(1024).decode()
                if not chunk:
                    raise ConnectionError()
                message += chunk
            except Exception:
                raise ConnectionError("Соединение разорвано.")
        return message.strip()

    def disconnect(self):
        self.socket_client.close()
        print("Отключено от сервера")

if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.connect()
