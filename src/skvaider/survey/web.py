from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.response import Response

from .config import Config


def hello_world(request):
    return Response("Hello Runner!")


def main(app_config: Config):
    with Configurator() as config:
        settings = config.get_settings()
        settings["skvaider.config"] = app_config
        config.include("pyramid_chameleon")
        config.include(".models")
        config.include(".routes")
        config.scan()

        config.add_route("hello", "/")
        config.add_view(hello_world, route_name="hello")
        app = config.make_wsgi_app()
    server = make_server(app_config.server.host, app_config.server.port, app)
    server.serve_forever()
