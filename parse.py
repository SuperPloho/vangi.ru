# вытащили температуру, ощущается как, давление и влажность
# осталось местное время - сконвертировать, облачность/явления погоды, ветер
# солнце/луна/фаза - надо или нет?
import urllib.request
import re

def convertByteToString(array):
    for i in range(0, len(array)):
        array[i] = array[i].decode('utf-8')

def convertToNormalView(array, separator):
    for i in range(0, len(array)): 
        array[i] = list(array[i])
        array[i] = separator.join(array[i])

infoPage = urllib.request.urlopen("http://rp5.ru/3034/ru") # получаем код сайта rp5 погода в Екатеринбурге
codeRP5 = infoPage.read() # записываем код в переменную

templateForFeelLike = re.compile(b'<div class=\"t_0\">([+-]?\d+)</b></div>') # регулярное выражение для "Ощущается как, °C"
templateForTempr = re.compile(b'<div class=\"t_0\"><b>([+-]?).{0,28}(\d+)</b></div>') # регулярное выражение для "Температура, °C"
templateForPressure = re.compile(b'<div class=\"p_0\">[<b>]{0,3}(\d+)[</b>]{0,3}</div>') # регулярное выражение для "Давление, мм рт. ст."
templateForWet = re.compile(b'\)\">[<b>]{0,3}(\d+)</td>') # регулярное выражение для "Влажность, %"
templateForCloudiness = re.compile(b'<div class=\"cc_0\">.+<b>(.+)</b><br/>\((.+)\)\'') # регулярное выражение для "Облачность, %"
templateForPhenomenon = re.compile(b'<div class=\"pr_0\".+\'(.+)\' ,') # регулярное выражение для "Явления погоды"
templateForPhenomenon1 = re.compile(b' class=\" litegrey .{1,2}.+\%\" .+\'(.+)\' ,') # регулярное выражение для "Явления погоды1"

tempr = templateForTempr.findall(codeRP5) # получаем значения температуры
feelLikeTempr = templateForFeelLike.findall(codeRP5) # получаем значение "ощущается как"
pressure = templateForPressure.findall(codeRP5) # получаем значения давления
wet = templateForWet.findall(codeRP5) # получаем значения влажности
cloudiness = templateForCloudiness.findall(codeRP5) # получаем значения облачности
phenomenon = templateForPhenomenon.findall(codeRP5) # получаем значения явлений погоды
phenomenon1 = templateForPhenomenon1.findall(codeRP5) # получаем значения явлений погоды

convertToNormalView(tempr, b'')
convertToNormalView(cloudiness, b' ')

convertByteToString(tempr)
convertByteToString(feelLikeTempr)
convertByteToString(pressure)
convertByteToString(wet)
convertByteToString(cloudiness)
convertByteToString(phenomenon)
convertByteToString(phenomenon1)

print(tempr)
print(feelLikeTempr)
print(pressure)
print(wet)
print(cloudiness)
print(phenomenon)
print(phenomenon1)
