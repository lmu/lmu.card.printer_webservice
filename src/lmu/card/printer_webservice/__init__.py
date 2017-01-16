from lmu.card.printer_webservice.resources import root_factory
from lmu.card.printer_webservice.soapV1 import anau_soap_webservice_application
from pyramid.config import Configurator
from pyramid.view import view_config


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=root_factory,
                          settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('soap', '/soap/')
    config.add_view(anau_soap_webservice_application, route_name='soap')
    config.add_route('soapV1', '/api/v1/')
    config.add_view(anau_soap_webservice_application, route_name='soapV1')
    config.scan()
    return config.make_wsgi_app()
