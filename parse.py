import re
import urllib.request
from datetime import datetime, date, time

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
template_for_cloudiness = re.compile(b'<div class=\"cc_0\">.+<b>(.+)</b><br/>.+\'')
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
TIME = template_for_time.findall(CODERP5)
# получаем значение скорости ветра
speed = template_for_wind_speed.findall(CODERP5)
# получаем значение направления ветра
direction = template_for_wind_direction.findall(CODERP5)

convert_to_normal_view(tempr, b'')
# convert_to_normal_view(feel_like_tempr, b'')
# convert_to_normal_view(cloudiness, b' ')

convert_byte_to_string(tempr)
convert_byte_to_string(feel_like_tempr)
convert_byte_to_string(pressure)
convert_byte_to_string(wet)
convert_byte_to_string(cloudiness)
convert_byte_to_string(phenomenon)
# convert_byte_to_string(phenomenon1)
convert_byte_to_string(TIME)
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
from pyramid.renderers import render

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

from  time import time

def whats_time(TIME):
    for key, value in enumerate(feel_like_tempr):
        NOW = datetime.today()
        date = int(TIME[key])*3600 + NOW.second
        TIME[key] = time.ctime(time(date))
        return TIME

DATE = whats_time(TIME)
'''    

NOW = datetime.today()

def days(count):
    for key in range(0,23):
        if (key % 4 == 0) and (key != 0):
            count = count + 1 
        DDATE = date(NOW.year, NOW.month , int(NOW.day+count))
        TTIME = time(int(TIME[key]), 0)
        TIME[key] = datetime.combine(DDATE, TTIME)
        # TIME[key].strftime("%a, %d.%b.%y %H:%M")

days(0)

qwe = range(0,23)
asdzxc = {'city': 'Екб', 'Date': TIME, 'Temperature': tempr, 
        'FLT': feel_like_tempr, 'Pressure': pressure, 'Wet': wet, 
        'Cloudinass': cloudiness, 'Phenomenon': phenomenon, 'Speed': speed, 
        'Direction': direction, 'qwe': qwe}

def sample_view(request):
    result = render('templates/index.jinja2',
                    asdzxc,
                    request=request)
    response = Response(result)
    return response

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
    config.add_route('weather', 'weather')
    config.add_view(weather, route_name='weather')
    config.include('pyramid_jinja2')
    config.add_route('asd', '/asd')
    config.add_view(sample_view, route_name='asd')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8000, app)
    server.serve_forever()
