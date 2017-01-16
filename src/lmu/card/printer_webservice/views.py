
from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(context, request):
    import ipdb; ipdb.set_trace()
    return {'project': 'lmu.card.printer_webservice'}
