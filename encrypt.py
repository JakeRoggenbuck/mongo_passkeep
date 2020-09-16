from Crypto.Cipher import AES
from pathlib import Path
from os import path
import yaml
import json


class Config:
    def __init__(self):
        home = str(Path.home())
        print(home)
        full_path = path.join(home, '.config/mongo_passkeep/config.yml')
        self.path = full_path
        self.config = self.get_config()

    def get_config(self):
        config_file = open(self.path)
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        return config


class Encrypt:
    def __init__(self, message):
        self.config = Config()
        self.key = self.config.config['key']
        self.message = message
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
