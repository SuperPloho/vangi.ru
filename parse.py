import urllib.request
import re

def convertByteToString(array):
    for i in range(0, len(array)):
        array[i] = array[i].decode('utf-8')

infoPage = urllib.request.urlopen("http://rp5.ru/3034/ru")
codeRP5 = infoPage.read()
templateForFeelLike = re.compile(b'<div class="t_0">([+-]?\d+)</b></div>')
templateForTempr = re.compile(b'<div class="t_0"><b>([+-]?).{0,28}(\d+)</b></div>')
tempr = templateForTempr.findall(codeRP5)
feelLikeTempr = templateForFeelLike.findall(codeRP5)
for i in range(0, len(tempr)):
    tempr[i] = list(tempr[i])
    tempr[i] = b''.join(tempr[i])
convertByteToString(tempr)
convertByteToString(feelLikeTempr)
print(tempr)
print(feelLikeTempr)
