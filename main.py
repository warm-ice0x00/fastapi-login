import base64
from typing import Annotated

from fastapi import Cookie, FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

USERNAME = "user"
PASSWORD = "password"
TOKEN = base64.b64encode(b"\x00" * 16).decode("ascii")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def read_file(path: str) -> bytes:
    with open(path, "rb") as file:
        return file.read()


@app.get("/", response_class=HTMLResponse)
async def index(token: Annotated[str, Cookie()] = ""):
    if token != TOKEN:
        return HTMLResponse(read_file("login.html"))
    return HTMLResponse(read_file("logout.html"))


@app.post("/login", response_class=HTMLResponse)
async def login(username: Annotated[str, Form()] = "",
                password: Annotated[str, Form()] = ""):
    username = username.lower()
    password = password.lower()
    if username != USERNAME or password != PASSWORD:
        return RedirectResponse("/", 302)
    response = RedirectResponse("/", 302)
    max_age = 31536000
    response.set_cookie("token", TOKEN, max_age, max_age)
    return response


@app.post("/logout", response_class=HTMLResponse)
async def logout():
    response = RedirectResponse("/", 302)
    response.delete_cookie("token")
    return response
