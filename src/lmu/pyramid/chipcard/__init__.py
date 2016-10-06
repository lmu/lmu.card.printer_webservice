from pyramid.config import Configurator
from spyne.server.pyramid import PyramidApplication

from lmu.pyramid.chipcard.soap import anau_soap_webservice_application


def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=root_factory, settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    soap_app = PyramidApplication(anau_soap_webservice_application)
    config.add_route('soap', '/soap/')
    config.add_view(soap_app, route_name='soap')
    config.scan()
    return config.make_wsgi_app()
