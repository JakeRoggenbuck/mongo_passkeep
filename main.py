import json
from utils import Promt, parse
from database import Database


if __name__ == "__main__":
    ARGS = parse()
    DATABASE = Database()
    DATABASE.connect()
    if ARGS.w is True:
        PROMPT = Promt()
        DATABASE.write(PROMPT.entry)
    if ARGS.a is True:
        DATABASE.view_all()
    if ARGS.d is not None:
        DATABASE.delete_document(ARGS.d)
    if ARGS.e is not None:
        DATABASE.edit(ARGS.e)
    if ARGS.r is not None:
        doc = DATABASE.read(ARGS.r)
        sec = doc['secret']
        sec = json.loads(sec)
        DATABASE.secret_view(sec)
