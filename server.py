from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# In-memory user store
USERS = {}


@app.get("/")
def root():
    return {"message": "AI Test Agent Server Running"}


# -------------------------
# REGISTER PAGE
# -------------------------

@app.get("/register", response_class=HTMLResponse)
def register_page():
    return """
    <html>
    <body>

        <h2>Register Page</h2>

        <form method="post" action="/register">

            <input data-test="register-name" name="name" placeholder="Name"/>

            <input data-test="register-email" name="email" placeholder="Email"/>

            <input data-test="register-password" name="password" type="password" placeholder="Password"/>

            <button data-test="register-submit" type="submit">Register</button>

        </form>

        <div data-test="register-success" style="display:none;color:green;">
            Register success
        </div>

        <div data-test="register-error" style="display:none;color:red;">
            Register failed
        </div>

    </body>
    </html>
    """


@app.post("/register")
def register(name: str = Form(...), email: str = Form(...), password: str = Form(...)):

    if email in USERS:
        return HTMLResponse("""
        <div data-test="register-error">User already exists</div>
        """)

    USERS[email] = {
        "name": name,
        "password": password
    }

    return HTMLResponse("""
    <div data-test="register-success">Register success</div>
    """)


# -------------------------
# LOGIN PAGE
# -------------------------

@app.get("/login", response_class=HTMLResponse)
def login_page():
    return """
    <html>
    <body>

        <h2>Login Page</h2>

        <form method="post" action="/login">

            <input data-test="login-email" name="email" placeholder="Email"/>

            <input data-test="login-password" name="password" type="password" placeholder="Password"/>

            <button data-test="login-submit" type="submit">Login</button>

        </form>

        <div data-test="login-error" style="display:none;color:red;">
            Invalid credentials
        </div>

    </body>
    </html>
    """


@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):

    if email in USERS and USERS[email]["password"] == password:

        return RedirectResponse("/dashboard", status_code=302)

    return HTMLResponse("""
    <div data-test="login-error">Invalid credentials</div>
    """)


# -------------------------
# DASHBOARD
# -------------------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """
    <html>
    <body>
        <h2>Dashboard</h2>
    </body>
    </html>
    """