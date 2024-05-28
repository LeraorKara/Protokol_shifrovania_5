import os
import random

class DiffieHellman:
    def __init__(self, p, g, private_key_file='private_key.txt', public_key_file='public_key.txt'):
        self.p = p
        self.g = g
        self.private_key_file = private_key_file
        self.public_key_file = public_key_file

        if os.path.exists(private_key_file) and os.path.exists(public_key_file):
            self.a = self.load_key(private_key_file)
            self.A = self.load_key(public_key_file)
        else:
            self.a = random.randint(1, p - 1)
            self.A = pow(g, self.a, p)
            self.save_key(private_key_file, self.a)
            self.save_key(public_key_file, self.A)

    def save_key(self, key_file, key):
        with open(key_file, 'w') as f:
            f.write(str(key))

    def load_key(self, key_file):
        with open(key_file, 'r') as f:
            return int(f.read())

    def compute_shared_key(self, public_key):
        return pow(public_key, self.a, self.p)

    def encrypt(self, message, key):
        return ''.join(chr((ord(char) + key) % 256) for char in message)

    def decrypt(self, message, key):
        return ''.join(chr((ord(char) - key) % 256) for char in message)
