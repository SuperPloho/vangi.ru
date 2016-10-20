import urllib.request
import re

def convertByteToString(array):
    for i in range(0, len(array)):
        array[i] = array[i].decode('utf-8')

infoPage = urllib.request.urlopen("http://rp5.ru/3034/ru") # get code site
codeRP5 = infoPage.read() # read code site

templateForFeelLike = re.compile(b'<div class="t_0">([+-]?\d+)</b></div>') # regular for feels temperature
templateForTempr = re.compile(b'<div class="t_0"><b>([+-]?).{0,28}(\d+)</b></div>') # regular for temperature
templateForPressure = re.compile(b'<div class="p_0"><b>(\d+)</b></div>') # template for pressure
templateForWet = re.compile(b'\)">([0-9]+)</td>') # regular for wet
tempr = templateForTempr.findall(codeRP5) #find all temperature
feelLikeTempr = templateForFeelLike.findall(codeRP5) # find all feel like temperature
pressure = templateForPressure.findall(codeRP5) # find all pressure
wet = templateForWet.findall(codeRP5) # find all wet
for i in range(0, len(tempr)): # convert tempr to normal view
    tempr[i] = list(tempr[i])
    tempr[i] = b''.join(tempr[i])
convertByteToString(tempr)
convertByteToString(feelLikeTempr)
convertByteToString(pressure)
convertByteToString(wet)
print(tempr)
print(feelLikeTempr)
print(pressure)
print(wet)
