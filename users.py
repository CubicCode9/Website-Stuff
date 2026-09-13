import json
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

KEYPATH = Path.home() / ".config" / "horizonxs" / "key.bin"
DATAPATH = Path("userData.bin")


def get_default_accounts():
    return {
        "setup123": ["Pa55w0rd", "Admin"],
        "CubicCode9": ["OptionalHomework", "Member"],
        "GuestUser": ["", "Guest"],
    }


def getKey():
    KEYPATH.parent.mkdir(parents=True, exist_ok=True)
    if not KEYPATH.exists():
        KEYPATH.write_bytes(Fernet.generate_key())
    return KEYPATH.read_bytes()

def add(username, password, role):
    accounts = load()
    accounts[username] = [password, role]
    key = getKey()
    cipher = Fernet(key)
    encrypted = cipher.encrypt(json.dumps(accounts).encode())
    with DATAPATH.open("wb") as f:
        f.write(encrypted)


def load():
    key = getKey()
    cipher = Fernet(key)

    if DATAPATH.exists():
        try:
            with DATAPATH.open("rb") as f:
                encrypted = f.read()
            decrypted = cipher.decrypt(encrypted).decode()
            return json.loads(decrypted)
        except (InvalidToken, json.JSONDecodeError):
            print("Stored user data does not match the current key or is invalid. Recreating file.")
            DATAPATH.unlink(missing_ok=True)

    accounts = get_default_accounts()
    encrypted = cipher.encrypt(json.dumps(accounts).encode())
    with DATAPATH.open("wb") as f:
        f.write(encrypted)
    return accounts


def add(username, password, role):
    accounts = load()
    accounts[username] = [password, role]
    key = getKey()
    cipher = Fernet(key)
    encrypted = cipher.encrypt(json.dumps(accounts).encode())
    with DATAPATH.open("wb") as f:
        f.write(encrypted)


if __name__ == "__main__":
    print(load())