from daemon import create_backend
import secrets, time

SESSIONS = {}

def route_login(headers, body, cookies):
    params = dict(pair.split("=") for pair in body.split("&"))
    user, pwd = params["username"], params["password"]

    if user == "admin" and pwd == "password":
        token = secrets.token_hex(32)
        SESSIONS[token] = {"username": user, "exp": time.time() + 3600}

        return {
            "cookie": f"sessionid={token}; HttpOnly; Path=/",
            "html": "<h1>Login success</h1>",
        }

    return {"html": "Unauthorized"}


def route_private(headers, body, cookies):
    token = cookies.get("sessionid")
    session = SESSIONS.get(token)

    if not session:
        return "Unauthorized"

    if session["exp"] < time.time():
        return "Session expired"

    return "<h1>Welcome to private zone</h1>"


def route_index(headers, body, cookies):
    token = cookies.get("sessionid")
    if token in SESSIONS:
        return {"html": "<h1>Welcome Home</h1>"}
    else:
        return {
            "status": 401,
            "html": "<h1>401 Unauthorized</h1>"
        }



# def route_index(headers, body, cookies):
#     if cookies.get("auth") == "true":
#         return {
#             "html": "<h1>Welcome</h1>"
#         }
#     else:
#         return {
#             "status": 401,
#             "html": "<h1>401 Unauthorized</h1>"
#         }



routes = {
    ('POST', '/login'): route_login,
    ('GET', '/'): route_index,
    ('GET', '/private'): route_private
}
# IP, Port, Routes
create_backend('0.0.0.0', 8000, routes)