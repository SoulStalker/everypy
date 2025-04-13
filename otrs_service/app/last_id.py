import os

LAST_ID_FILE = 'last_ticket_id.txt'


def load_last_id():
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, 'r') as f:
            return int(f.read())
    return 0


def save_last_id(last_id):
    with open(LAST_ID_FILE, 'w') as f:
        f.write(str(last_id))
