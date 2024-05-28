import socket
from criptography import DiffieHellman

if __name__ == "__main__":
    HOST = input('HOST (default "localhost"): ')
    HOST = 'localhost' if not HOST else HOST
    PORT = input('PORT (default 8000)')
    PORT = int(PORT) if PORT else 8000
    print(f"Сервер запущен на данном адресе {HOST}:{PORT} ...")
    dh_server = DiffieHellman(523, 64)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Новое подключение  {addr}")
            client_public_key = int(conn.recv(1024).decode())
            print(f"Публичный ключ клиента: {client_public_key}")

            conn.sendall(str(dh_server.A).encode())

            shared_key = dh_server.compute_shared_key(client_public_key)
            print(f"Общий ключ: {shared_key}")

            encrypted_message = conn.recv(1024).decode()
            print(f'Зашифрованное сообщение: {encrypted_message} ')
            decrypted_message = dh_server.decrypt(encrypted_message, shared_key)
            print(f"Дешифрованное сообщение: {decrypted_message}")

            response = input('Ответ для клиента: ')
            encrypted_response = dh_server.encrypt(response, shared_key)
            conn.sendall(encrypted_response.encode())
