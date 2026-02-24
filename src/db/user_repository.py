from src.db.mongo_client import get_db

COLLECTION = "users"


def create_user(user_data: dict):

    db = get_db()

    users = db[COLLECTION]

    existing = users.find_one({"email": user_data["email"]})

    if existing:
        return False

    users.insert_one(user_data)

    print("[MongoDB] User saved:", user_data["email"])

    return True


def validate_user(email: str, password: str):

    db = get_db()

    users = db[COLLECTION]

    user = users.find_one({
        "email": email,
        "password": password
    })

    return user is not None