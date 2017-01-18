import re
import urllib.request
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database import Forecast, engine


def convert_byte_to_string(array):
    for i in range(0, len(array)):
        array[i] = array[i].decode('utf-8')


def convert_to_normal_view(array, separator):
    for i in range(0, len(array)): 
        array[i] = list(array[i])
        array[i] = separator.join(array[i])


def delete_excess_element(array):
    length = len(array) - 1
    for i in range(0, int(length / 2)):
        del array[i + 1]


# получаем код сайта rp5 погода в Екатеринбурге
INFO_PAGE = urllib.request.urlopen("http://rp5.ru/3034/ru")
# записываем код в переменную
CODERP5 = INFO_PAGE.read()

# регулярное выражение для "Ощущается как, °C"
template_for_feel_like = re.compile(b'<div class=\"t_0\">([+-]?\d+)</b></div>')
# регулярное выражение для "Температура, °C"
template_for_tempr = re.compile(b'<div class=\"t_0\"><b>([+-]?).{0,28}?(\d+)</b></div>')
# регулярное выражение для "Давление, мм рт. ст."
template_for_pressure = re.compile(b'<div class=\"p_0\">[<b>]{0,3}(\d+)[</b>]{0,4}</div>')
# регулярное выражение для "Влажность, %"
template_for_wet = re.compile(b'\)\">[<b>]{0,3}(\d+)</td>')
# регулярное выражение для "Облачность, %"
template_for_cloudiness = re.compile(b'<div class=\"cc_0\">.+<b>(.+)</b><br/>\((.+)\)\'')
# регулярное выражение для "Явления погоды"
template_for_phenomenon = re.compile(b'<div class=\"pr_0\".+\'(.+)\' ,')

# регулярное выражение для "Явления погоды1"
# template_for_phenomenon1 = re.compile(b' class=\" litegrey .{1,2}.+\%\" .+\'(.+)\' ,')

# регулярное выражение для времени
template_for_time = re.compile(b'<td colspan=\"2\" class=\".{1,2} underlineRow\">(\d+)</td>')
# регулярное выражение для скорости ветра
template_for_wind_speed = re.compile(b'<div class=\"wv_0\".+\((\d+) ')
# регулярное выражение для направления ветра
template_for_wind_direction = re.compile(b'class=\"grayLittle[nd2]{0,3}.+?\">(.{0,5})</td>')

# получаем значения температуры
tempr = template_for_tempr.findall(CODERP5)
# получаем значение "ощущается как"
feel_like_tempr = template_for_feel_like.findall(CODERP5)
# получаем значения давления
pressure = template_for_pressure.findall(CODERP5)
# получаем значения влажности
wet = template_for_wet.findall(CODERP5)
# получаем значения облачности
cloudiness = template_for_cloudiness.findall(CODERP5)
# получаем значения явлений погоды
phenomenon = template_for_phenomenon.findall(CODERP5)

# получаем значения явлений погоды
# phenomenon1 = template_for_phenomenon1.findall(CODERP5)

# получаем значение времени
time = template_for_time.findall(CODERP5)
# получаем значение скорости ветра
speed = template_for_wind_speed.findall(CODERP5)
# получаем значение направления ветра
direction = template_for_wind_direction.findall(CODERP5)

convert_to_normal_view(tempr, b'')
# convert_to_normal_view(feel_like_tempr, b'')
convert_to_normal_view(cloudiness, b' ')

convert_byte_to_string(tempr)
convert_byte_to_string(feel_like_tempr)
convert_byte_to_string(pressure)
convert_byte_to_string(wet)
convert_byte_to_string(cloudiness)
convert_byte_to_string(phenomenon)
# convert_byte_to_string(phenomenon1)
convert_byte_to_string(time)
convert_byte_to_string(speed)
convert_byte_to_string(direction)

delete_excess_element(phenomenon)
''''
print(tempr)
print(len(tempr))
print(feel_like_tempr)
print(len(feel_like_tempr))
print(pressure)
print(len(pressure))
print(wet)
print(len(wet))
print(cloudiness)
print(len(cloudiness))
print(phenomenon)
print(len(phenomenon))
print(time)
print(len(time))
print(speed)
print(len(speed))
print(direction)
print(len(direction))

ENGINE = create_engine('postgresql://postgres:1@localhost:5432/Weather')
SESSION = Session(bind=ENGINE)
NOW = datetime.today()

for key, value in enumerate(feel_like_tempr):
    SESSION.add(
        Forecast(
            id=key,
            priority='1',
            date_time=time[key],
            update_datetime=NOW,
            data={
                "температура": feel_like_tempr[key],
                "давление": pressure[key],
                "влажность": wet[key],
                "ожидаемая": tempr[key],
                "облачность": cloudiness[key],
                "явление погоды": phenomenon[key],
                "скорость": speed[key],
                "направление": direction[key],
            }
        )
    )
SESSION.commit()
'''
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def index(request):
    return Response("""<a href="index.html">Относительная</a> |
    <a href="C:/WebServers/home/myproject/index.html">Абсолютная</a>""")


def about(request):
    return Response("""<a href="about/aboutme.html">Относительная</a> |
    <a href="C:/WebServers/home/myproject/about/abotme.html">Абсолютная</a>""")
'''
def weather_(request):
    for key, value in enumerate(feel_like_tempr):
        return Response(
            "Дата: " + time[key] + "<hr>" +
            "Температура: "+ feel_like_tempr[key]+ "<br>" +
            "Давление: "+ pressure[key]+"<br>" +
            "Влажность: "+ wet[key]+"<br>" +
            "Ожидаемая: "+ tempr[key]+"<br>" +
            "Облачность: "+ cloudiness[key]+"<br>" +
            "Явление погоды: "+ phenomenon[key]+"<br>" +
            "Скорость: "+ speed[key]+"<br>" +
            "Направление: "+ direction[key]
        )
'''


def weather(request):
    ENGINE = create_engine('postgresql://postgres:1@localhost:5432/Weather')
    SESSION = Session(bind=ENGINE)
    result = engine.execute(
                 "select data from "
                 "forecasts")
    row = result.fetchall()
    return Response(str(row))

if __name__ == '__main__':
    config = Configurator()
    config.add_route('index', '/')
    config.add_view(index, route_name='index')
    config.add_route('about', 'about')
    config.add_view(about, route_name='about')
    config.add_route('weather', 'weather')
    config.add_view(weather, route_name='weather')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8000, app)
    server.serve_forever()
