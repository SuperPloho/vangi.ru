from pyramid.view import view_config
from weather.parseRP5 import parse, select_city
"""
@view_config(route_name='home', renderer='templates/asd.jinja2')
def my_view(request):
    return {'project': 'Weather'}
"""

@view_config(route_name='weather', renderer='templates/index.jinja2')
def weather(request):
    return parse(request.matchdict['id_url_city'], 1)

@view_config(route_name='home', renderer='templates/home.jinja2')
def cities(request):
    return {}

@view_config(route_name='zzz', renderer='templates/index.jinja2')
def zzz(request):
    return parse(select_city(request.matchdict['name_cur_city']), request.matchdict['time_reg'])