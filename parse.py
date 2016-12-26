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
    lenght = len(array) - 1
    for i in range(0, (int)(lenght / 2)):
        del array[i + 1]

# получаем код сайта rp5 погода в Екатеринбурге
INFO_PAGE = urllib.request.urlopen("http://rp5.ru/3034/ru")
CODERP5 = INFO_PAGE.read() # записываем код в переменную

template_for_feelLike = re.compile(b'<div class=\"t_0\">([+-]?\d+)</b></div>') # регулярное выражение для "Ощущается как, °C"
template_for_tempr = re.compile(b'<div class=\"t_0\"><b>([+-]?).{0,28}?(\d+)</b></div>') # регулярное выражение для "Температура, °C"
template_for_pressure = re.compile(b'<div class=\"p_0\">[<b>]{0,3}(\d+)[</b>]{0,4}</div>') # регулярное выражение для "Давление, мм рт. ст."
template_for_wet = re.compile(b'\)\">[<b>]{0,3}(\d+)</td>') # регулярное выражение для "Влажность, %"
template_for_cloudiness = re.compile(b'<div class=\"cc_0\">.+<b>(.+)</b><br/>\((.+)\)\'') # регулярное выражение для "Облачность, %"
template_for_phenomenon = re.compile(b'<div class=\"pr_0\".+\'(.+)\' ,') # регулярное выражение для "Явления погоды"
#template_for_phenomenon1 = re.compile(b' class=\" litegrey .{1,2}.+\%\" .+\'(.+)\' ,') # регулярное выражение для "Явления погоды1"
template_for_time = re.compile(b'<td colspan=\"2\" class=\".{1,2} underlineRow\">(\d+)</td>') # регулярное выражение для времени
template_for_wind_speed = re.compile(b'<div class=\"wv_0\".+\((\d+) ') # регулярное выражение для скорости ветра
template_for_wind_direction = re.compile(b'class=\"grayLittle[nd2]{0,3}.+?\">(.{0,5})</td>') # регулярное выражение для направления ветра

tempr = template_for_tempr.findall(CODERP5) # получаем значения температуры
feelLikeTempr = template_for_feelLike.findall(CODERP5) # получаем значение "ощущается как"
pressure = template_for_pressure.findall(CODERP5) # получаем значения давления
wet = template_for_wet.findall(CODERP5) # получаем значения влажности
cloudiness = template_for_cloudiness.findall(CODERP5) # получаем значения облачности
phenomenon = template_for_phenomenon.findall(CODERP5) # получаем значения явлений погоды
#phenomenon1 = template_for_phenomenon1.findall(CODERP5) # получаем значения явлений погоды
time = template_for_time.findall(CODERP5) # получаем значение времени
speed = template_for_wind_speed.findall(CODERP5) # получаем значение скорости ветра
direction = template_for_wind_direction.findall(CODERP5) # получаем значение направления ветра

convert_to_normal_view(tempr, b'')
#convert_to_normal_view(feelLikeTempr, b'')
convert_to_normal_view(cloudiness, b' ')

convert_byte_to_string(tempr)
convert_byte_to_string(feelLikeTempr)
convert_byte_to_string(pressure)
convert_byte_to_string(wet)
convert_byte_to_string(cloudiness)
convert_byte_to_string(phenomenon)
#convert_byte_to_string(phenomenon1)
convert_byte_to_string(time)
convert_byte_to_string(speed)
convert_byte_to_string(direction)

delete_excess_element(phenomenon)
''''
print(tempr)
print(len(tempr))
print(feelLikeTempr)
print(len(feelLikeTempr))
print(pressure)
print(len(pressure))
print(wet)
print(len(wet))
print(cloudiness)
print(len(cloudiness))
print(phenomenon)
print(len(phenomenon))
#print(phenomenon1)
print(time)
print(len(time))
print(speed)
print(len(speed))
print(direction)
print(len(direction))
'''
ENGINE = create_engine('postgresql://postgres:1@localhost:5432/Weather')
SESSION = Session(bind=ENGINE)
NOW = datetime.today()

for key, value in enumerate(tempr):
    SESSION.add(
        Forecast(
            id=key,
            priority='1',
            date_time=time[key],
            update_datetime=NOW,
            data={
                "температура": feelLikeTempr[key],
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
