from Crypto.Cipher import AES
from pathlib import Path
from os import path
import yaml
import json


class Config:
    def __init__(self):
        # Get home path for config
        home = str(Path.home())
        full_path = path.join(home, '.config/mongo_passkeep/config.yml')
        self.path = full_path
        self.config = self.get_config()

    def get_config(self):
        # Get config and parse yaml
        config_file = open(self.path)
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        return config


class Encrypt:
    def __init__(self, message):
        self.config = Config()
        # Get key from config
        self.key = self.config.config['key']
        self.message = message
        self.obj = self.aes()

    def aes(self):
        # Make AES object
        obj = AES.new(self.key, AES.MODE_CBC, 'This is an IV456')
        return obj

    def encrypt(self):
        # Make message dict into string
        self.message = json.dumps(self.message)
        # Add characters until message is a multiple of 16
        while len(self.message) % 16 != 0:
            self.message += " "
        # Return encrypted message
        return self.obj.encrypt(self.message)

    def decrypt(self):
        # Return decrypted message and remove extra characters
        message = self.obj.decrypt(self.message).decode("utf-8").rstrip()
        # Make message back into a dictionary
        return json.loads(message)
