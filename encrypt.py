from Crypto.Cipher import AES
import json


class Encrypt:
    def __init__(self, message, key='This is a key123'):
        self.message = message
        self.key = key
        self.obj = self.aes()

    def aes(self):
        obj = AES.new(self.key, AES.MODE_CBC, 'This is an IV456')
        return obj

    def encrypt(self):
        self.message = json.dumps(self.message)
        while len(self.message) % 16 != 0:
            self.message += " "
        return self.obj.encrypt(self.message)

    def decrypt(self):
        a = self.obj.decrypt(self.message).decode("utf-8").rstrip()
        return json.loads(a)
