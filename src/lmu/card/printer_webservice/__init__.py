from lmu.card.printer_webservice.resources import root_factory
from lmu.card.printer_webservice.soap import AnaUSOAPWebService
from pyramid.config import Configurator
from pyramid.view import view_config
from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.pyramid import PyramidApplication


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=root_factory,
                          settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    anau_soap_webservice_application = Application(
        [AnaUSOAPWebService],
        tns='http://webcardmanagement.ana-u.com/',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11(validator='lxml', pretty_print=True)
    )

    soap_app = PyramidApplication(anau_soap_webservice_application)
    config.add_route('soap', '/soap/')
    config.add_view(soap_app, route_name='soap')
    config.scan()
    return config.make_wsgi_app()
