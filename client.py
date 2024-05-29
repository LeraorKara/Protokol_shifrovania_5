import socket
from criptography import DiffieHellman

if __name__ == "__main__":
    HOST = input('HOST (default "localhost"): ')
    HOST = 'localhost' if not HOST else HOST
    PORT = input('PORT (default 8000)')
    PORT = int(PORT) if PORT else 8000
    dh_client = DiffieHellman(523, 64)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        s.sendall(str(dh_client.A).encode())

        server_public_key = int(s.recv(1024).decode())
        print(f"Публичный ключ сервера: {server_public_key}")

        shared_key = dh_client.compute_shared_key(server_public_key)
        print(f"Общий ключ: {shared_key}")

        message = input('Сообщение для сервера: ')
        encrypted_message = dh_client.encrypt(message, shared_key)
        

        encrypted_response = s.recv(1024).decode()
        print(f'Зашифрованное сообщение от сервера: {encrypted_message} ')
        decrypted_response = dh_client.decrypt(encrypted_response, shared_key)
        print(f"Дешифрованное сообщение: {decrypted_response}")
