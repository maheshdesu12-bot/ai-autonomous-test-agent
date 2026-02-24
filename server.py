from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from src.db.mongo_client import users_collection

app = FastAPI()


@app.get("/")
def root():
    return {"message": "AI Autonomous Test Agent Server Running"}


# REGISTER PAGE

@app.get("/register", response_class=HTMLResponse)
def register_page():
    return """
    <html>
    <body>

        <h2>Register</h2>

        <form method="post" action="/register">

            <input data-test="register-name" name="name" />

            <input data-test="register-email" name="email" />

            <input data-test="register-password" name="password" type="password"/>

            <button data-test="register-submit" type="submit">
                Register
            </button>

        </form>

    </body>
    </html>
    """


@app.post("/register")
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):

    print(f"[DB] Register attempt: {email}")

    # check existing
    existing_user = users_collection.find_one({"email": email})

    if existing_user:

        print("[DB] User already exists")

        return {
            "status": "failed",
            "error": "User already exists"
        }

    # save to MongoDB
    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": password
    })

    print("[DB] User saved successfully")

    return {
        "status": "success"
    }


# LOGIN PAGE

@app.get("/login", response_class=HTMLResponse)
def login_page():
    return """
    <html>
    <body>

        <h2>Login</h2>

        <form method="post" action="/login">

            <input data-test="login-email" name="email" />

            <input data-test="login-password" name="password" type="password"/>

            <button data-test="login-submit" type="submit">
                Login
            </button>

        </form>

    </body>
    </html>
    """


@app.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...)
):

    print(f"[DB] Login attempt: {email}")

    # validate from MongoDB
    user = users_collection.find_one({
        "email": email,
        "password": password
    })

    if user:

        print("[DB] Login success")

        return {
            "status": "success"
        }

    print("[DB] Login failed")

    return {
        "status": "failed",
        "error": "Invalid credentials"
    }