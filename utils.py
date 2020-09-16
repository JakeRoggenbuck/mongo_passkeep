from encrypt import Encrypt
import argparse
import json


class Promt:
    def __init__(self):
        self.get_entry()

    def get_entry(self):
        title = input("Title: ")
        desc = input("Desc: ")
        if title != "" and desc != "":
            self.get_secret()
            secret = {
                "username": self.username,
                "email": self.email,
                "password": self.password,
                "message": self.message
            }
            secret = json.dumps(secret)
            secret = Encrypt(secret).encrypt()
            self.entry = {
                "title": title,
                "desc": desc,
                "secret": secret,
            }

    def get_secret(self):
        self.username = input("Username: ")
        self.email = input("Email: ")
        self.password = input("Password: ")
        self.message = input("Message: ")


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="Search phrase")
    parser.add_argument("-r", help="Read hash")
    parser.add_argument("-d", help="Delete hash")
    parser.add_argument("-e", help="Edit hash")
    parser.add_argument("-w", help="Write", action='store_true')
    parser.add_argument("-a", help="View all", action='store_true')
    args = parser.parse_args()
    return args
