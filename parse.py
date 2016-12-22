# осталось местное время - сконвертировать
import urllib.request
import re

def convertByteToString(array):
    for i in range(0, len(array)):
        array[i] = array[i].decode('utf-8')

def convertToNormalView(array, separator):
    for i in range(0, len(array)): 
        array[i] = list(array[i])
        array[i] = separator.join(array[i])

def deleteExcessElement(array):
    lenght = len(array) - 1
    for i in range(0, (int)(lenght / 2)):
        del array[i + 1]

infoPage = urllib.request.urlopen("http://rp5.ru/3034/ru") # получаем код сайта rp5 погода в Екатеринбурге
codeRP5 = infoPage.read() # записываем код в переменную

templateForFeelLike = re.compile(b'<div class=\"t_0\">([+-]?\d+)</b></div>') # регулярное выражение для "Ощущается как, °C"
templateForTempr = re.compile(b'<div class=\"t_0\"><b>([+-]?).{0,28}(\d+)</b></div>') # регулярное выражение для "Температура, °C"
templateForPressure = re.compile(b'<div class=\"p_0\">[<b>]{0,3}(\d+)[</b>]{0,4}</div>') # регулярное выражение для "Давление, мм рт. ст."
templateForWet = re.compile(b'\)\">[<b>]{0,3}(\d+)</td>') # регулярное выражение для "Влажность, %"
templateForCloudiness = re.compile(b'<div class=\"cc_0\">.+<b>(.+)</b><br/>\((.+)\)\'') # регулярное выражение для "Облачность, %"
templateForPhenomenon = re.compile(b'<div class=\"pr_0\".+\'(.+)\' ,') # регулярное выражение для "Явления погоды"
#templateForPhenomenon1 = re.compile(b' class=\" litegrey .{1,2}.+\%\" .+\'(.+)\' ,') # регулярное выражение для "Явления погоды1"
templateForTime = re.compile(b'<td colspan=\"2\" class=\".{1,2} underlineRow\">(\d+)</td>') # регулярное выражение для времени
templateForWindSpeed = re.compile(b'<div class=\"wv_0\".+\((\d+) ') # регулярное выражение для скорости ветра
templateForWindDirection = re.compile(b'class=\"grayLittle[nd2]{0,3}.+?\">(.{0,5})</td>') # регулярное выражение для направления ветра

tempr = templateForTempr.findall(codeRP5) # получаем значения температуры
feelLikeTempr = templateForFeelLike.findall(codeRP5) # получаем значение "ощущается как"
pressure = templateForPressure.findall(codeRP5) # получаем значения давления
wet = templateForWet.findall(codeRP5) # получаем значения влажности
cloudiness = templateForCloudiness.findall(codeRP5) # получаем значения облачности
phenomenon = templateForPhenomenon.findall(codeRP5) # получаем значения явлений погоды
#phenomenon1 = templateForPhenomenon1.findall(codeRP5) # получаем значения явлений погоды
time = templateForTime.findall(codeRP5) # получаем значение времени
speed = templateForWindSpeed.findall(codeRP5) # получаем значение скорости ветра
direction = templateForWindDirection.findall(codeRP5) # получаем значение направления ветра

convertToNormalView(tempr, b'')
#convertToNormalView(feelLikeTempr, b'')
convertToNormalView(cloudiness, b' ')

convertByteToString(tempr)
convertByteToString(feelLikeTempr)
convertByteToString(pressure)
convertByteToString(wet)
convertByteToString(cloudiness)
convertByteToString(phenomenon)
#convertByteToString(phenomenon1)
convertByteToString(time)
convertByteToString(speed)
convertByteToString(direction)

deleteExcessElement(phenomenon)

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


from sqlalchemy import create_engine
#engine = create_engine('postgresql://postgres:1@localhost:5432/Weather')

from datetime import datetime
now = datetime.today()

from database import Forecast, engine

from sqlalchemy.orm import Session
session = Session(bind=engine)

for key, value in enumerate(tempr):
    session.add(
        Forecast(
            priority='1',
            date_time=now,
            update_datetime=now
        )
    )

session.commit()
