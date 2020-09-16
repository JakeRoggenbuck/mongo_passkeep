from pymongo import MongoClient
from bson.objectid import ObjectId
from encrypt import Encrypt
from termcolor import colored


class Database:
    def __init__(self, location="localhost", ip="127.0.0.1"):
        """Sets defaults for parameters"""
        self.location = location
        self.ip = ip

    def connect(self):
        """Make the client, connect the db and create the collections"""
        self.client = MongoClient()
        self.db = self.client.password_keeper
        self.entries = self.db.entries

    def check_multiple_input(self, entry):
        if self.entries.find_one(entry['title']) is None:
            return True
        else:
            return False

    def make_view(self, obj):
        title = obj['title']
        desc = obj['desc']
        _id = obj['_id']

        c_title = colored(title, "blue", attrs=['bold'])
        c_id = colored(_id, "yellow")
        return f"{c_title}: {c_id}\n-- {desc}\n"

    def secret_view(self, obj):
        username = obj['username']
        email = obj['email']
        password = obj['password']
        message = obj['message']

        c_username = colored(username, "blue", attrs=['bold'])
        c_email = colored(email, "blue")
        c_password = colored(password, "green", attrs=['bold'])
        c_message = colored(message, "green")

        print(f"Username: {c_username}")
        print(f"Email: {c_email}")
        print(f"Password: {c_password}")
        print(f"Message: {c_message}")

    def view_all(self):
        for entry in self.entries.find({}):
            print(self.make_view(entry))

    def write(self, entry):
        if self.check_multiple_input(entry):
            self.entries.insert_one(entry)

    def read(self, _id):
        doc = self.get_document(_id)
        entry = self.entries.find_one(doc['_id'])
        get_secret = Encrypt(entry['secret'])
        secret = get_secret.decrypt()
        new_dict = {
            "title": entry['title'],
            "desc": entry['desc'],
            "secret": secret
        }
        return new_dict

    def get_document(self, object_id):
        _id = {"_id": ObjectId(object_id)}
        doc = self.entries.find_one(_id)
        return {"_id": _id, "doc": doc}

    def edit(self, object_id):
        doc = self.get_document(object_id)
        print(self.make_view(doc['doc']))
        edit = input("Change title or desc: [t/d]: ")
        if edit.upper() == "T":
            new_title = input("New title: ")
            self.entries.find_one_and_update(
                    doc['_id'],
                    {"$set": {"title": new_title}}
            )
            print(new_title)
        elif edit.upper() == "D":
            new_desc = input("New desc: ")
            self.entries.find_one_and_update(
                doc['_id'],
                {"$set": {"desc": new_desc}}
            )
            print(new_desc)

    def delete_document(self, object_id):
        doc = self.get_document(object_id)
        delete = input(f"{doc['rep']}\nDelete the document [Y/n]: ")
        if delete.upper() == "Y":
            print(self.entries.delete_one(doc['_id']))
