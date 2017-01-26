import re
import io
import urllib.request
from datetime import datetime, date, time
from sqlalchemy.orm import Session
from sqlalchemy import select

from weather.database import Forecast, engine, Geobject
from pyramid.response import Response

def convert_byte_to_string(array):
    for i in range(0, len(array)):
        array[i] = array[i].decode('utf-8')
"""
this function can be replaced by this
array.decode('utf-8')
"""
def convert_to_normal_view(array, separator):
    for i in range(0, len(array)):
        array[i] = list(array[i])
        array[i] = separator.join(array[i])


def delete_excess_element(array):
    length = len(array) - 1
    for i in range(0, int(length / 2)):
        del array[i + 1]

def days(count, now, TIME, t):
    for key in range(72 - 24*(t), (72 - 24*(t-1) - 1)):
        if (int(TIME[key]) // t == 0) and (key != 0):
            count = count + 1
        if (date(now.year, now.month, int(now.day+count))):
            DDATE = date(now.year, now.month, int(now.day+count))
        else:
            DDATE = date(now.year, int(now.month+1), int(now.day))
            count = 0
        TTIME = time(int(TIME[key]), 0)
        TIME[key] = datetime.combine(DDATE, TTIME)
        TIME[key] = TIME[key].strftime("%a, %d.%m.%y %H:%M")
"""
def read_file(file_name):
    re_for_city = re.compile(b'(\d+?):\d+:\d+:\d+:.*?:.*?:.*?:(.+?):')
    os.chdir(r'C:\\WEB\\Weather\\weather\\rp5_points')
    f = open(file_name, 'rb')
    file_content = b''
    f.seek(-1, 2)
    file_size = f.tell()
    f.seek(0)
    file_content = f.read(file_size)
    city_list = re_for_city.findall(file_content)
    city_l = {}
    for i in city_list:
        city_l[int(i[0].decode('utf-8'))] = i[1].decode('utf-8')
    return city_l

def get_all_cities():
    city_l1 = read_file('.\\rp5_0-86478.dat')
    city_l2 = read_file('.\\rp5_86479-100000.dat')
    city_l3 = read_file('.\\rp5_100001-150000.dat')
    city_l4 = read_file('.\\rp5_150001-200000.dat')
    city_l5 = read_file('.\\rp5_200001-250000.dat')
    city_l6 = read_file('.\\rp5_250001-279422.dat')
    city_l7 = read_file('.\\rp5_279423-300000.dat')
    city_l8 = read_file('.\\rp5_300001-347687.dat')
    city_l9 = read_file('.\\rp5_347688-350000.dat')
    city_l10 = read_file('.\\rp5_350001-396783.dat')
    city_l11 = read_file('.\\rp5_396784-400000.dat')
    city_l12 = read_file('.\\rp5_400001-434602.dat')
    cities = []
    cities.append(city_l1)
    cities.append(city_l2)
    cities.append(city_l3)
    cities.append(city_l4)
    cities.append(city_l5)
    cities.append(city_l6)
    cities.append(city_l7)
    cities.append(city_l8)
    cities.append(city_l9)
    cities.append(city_l10)
    cities.append(city_l11)
    cities.append(city_l12)

    return cities
"""
def parse(id_city, time_reg):

    data_files = ['rp5_0-86478.dat', 'rp5_86479-100000.dat', 'rp5_100001-150000.dat',
                  'rp5_150001-200000.dat', 'rp5_200001-250000.dat', 'rp5_250001-279422.dat',
                  'rp5_279423-300000.dat', 'rp5_300001-347687.dat', 'rp5_347688-350000.dat',
                  'rp5_350001-396783.dat', 'rp5_396784-400000.dat', 'rp5_400001-434602.dat']

    line_in_file = ""
    for file_name in data_files:
        with io.open(r'C:\\WEB\\Weather\\weather\\rp5_points\\{0}'.format(file_name),
                     encoding='utf-8') as file:
            for line in file:
                if str(id_city) in line:
                    line_in_file = line
                    break
            break
    city = re.search(r'(\d+?):\d+:\d+:\d+:.*?:.*?:.*?:(.+?):', line_in_file)
    #"into file content after this strings will be byte array of file data"
    # .\\rp5_0-470000.dat'
    #print(file_content)
    #for line in f:
     #   file_content += line
    #nfc = None
    #try:
    #    file_content = file_content.decode('utf-8') #куда магию дели ?¯\_(ツ)_/¯
    #except UnicodeDecodeError:
     #   print("something shit with encoding")


    # получаем код сайта rp5 погода в Екатеринбурге
    info_page = urllib.request.urlopen("http://rp5.ru/{0}/ru".format(id_city))
    # записываем код в переменную
    coderp5 = info_page.read()

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
    # регулярное выражение для времени
    template_for_time = re.compile(b'<td colspan=\"2\" class=\".{1,2} underlineRow\">(\d+)</td>')
    # регулярное выражение для скорости ветра
    template_for_wind_speed = re.compile(b'<div class=\"wv_0\".+\((\d+) ')
    # регулярное выражение для направления ветра
    template_for_wind_direction = re.compile(b'class=\"grayLittle[nd2]{0,3}.+?\">(.{0,5})</td>')

    # получаем значения температуры
    tempr = template_for_tempr.findall(coderp5)
    # получаем значение "ощущается как"
    feel_like_tempr = template_for_feel_like.findall(coderp5)
    # получаем значения давления
    pressure = template_for_pressure.findall(coderp5)
    # получаем значения влажности
    wet = template_for_wet.findall(coderp5)
    # получаем значения облачности
    cloudiness = template_for_cloudiness.findall(coderp5)
    # получаем значения явлений погоды
    phenomenon = template_for_phenomenon.findall(coderp5)
    # получаем значение времени
    TIME = template_for_time.findall(coderp5)
    # получаем значение скорости ветра
    speed = template_for_wind_speed.findall(coderp5)
    # получаем значение направления ветра
    direction = template_for_wind_direction.findall(coderp5)

    convert_to_normal_view(tempr, b'')

    convert_byte_to_string(tempr)
    convert_byte_to_string(feel_like_tempr)
    convert_byte_to_string(pressure)
    convert_byte_to_string(wet)
    convert_byte_to_string(cloudiness)
    convert_byte_to_string(phenomenon)
    convert_byte_to_string(TIME)
    convert_byte_to_string(speed)
    convert_byte_to_string(direction)

    delete_excess_element(phenomenon)

    now = datetime.today()
    time_reg = int(time_reg)
    
    print('t1 = ' + str(time_reg))
    time_reg = int(time_reg / 3) + 1
    #  days(0, now, TIME, time_reg)
    print('t2 = ' + str(time_reg))
    qwe = range(72 - 24*(time_reg), (72 - 24*(time_reg-1) - 1))
    print('qwe = ' + str(qwe))
    id_city = city.group(2)
    asdzxc = {'city': id_city, 'Date': TIME, 'Temperature': tempr,
              'FLT': feel_like_tempr, 'Pressure': pressure, 'Wet': wet,
              'Cloudinass': cloudiness, 'Phenomenon': phenomenon, 'Speed': speed,
              'Direction': direction, 'qwe': qwe}

    return asdzxc

def select_city(current_city):
    ''''
    SESSION = Session(bind=engine)
    result = engine.execute(
                 "select name from "
                 "objects where id=current_city")
    row = result.fetchall()
    return Response(str(row))
    '''
    select_stmt = select([Geobject.id]).\
                    where(Geobject.name == current_city)
    result = engine.connect().execute(select_stmt).fetchall()
    id_cur_city = {}
    for row in result:
        id_cur_city = row
        break
    return id_cur_city[0]


"""
def insert_cities_into_db(all_cities):
    SESSION = Session(bind=engine)
    NOW = datetime.today()
    for key in all_cities:
        for i in key:
            SESSION.add(
                Geobject(
                    id=i,
                    name=key[i]
                )
            )
    SESSION.commit()


def insert_into_db():
    ENGINE = create_engine('postgresql://postgres:1@localhost:5432/Weather')
    SESSION = Session(bind=ENGINE)
    NOW = datetime.today()

    for key, value in enumerate(feel_like_tempr):
        SESSION.add(
            Forecast(
                id=key,
                priority='1',
                date_time=TIME[key],
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

def weather(request):
    SESSION = Session(bind=ENGINE)
    result = engine.execute(
                 "select data from "
                 "forecasts")
    row = result.fetchall()
    return Response(str(row))
"""
