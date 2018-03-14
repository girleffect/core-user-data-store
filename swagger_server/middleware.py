import os

from werkzeug.wrappers import Request, Response


class AuthMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        key = request.headers.get("X-Api-Key", None)
        keys = set(os.getenv("ALLOWED_API_KEYS").split(","))
        if key:
            if key in keys:
                return self.app(environ, start_response)
            response = Response("Forbidden", status="403")
            return response(environ, start_response)
        response = Response("Unauthorized", status="401")
        return response(environ, start_response)
