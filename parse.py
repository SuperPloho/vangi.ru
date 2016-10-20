import urllib.request
import re

infoPage = urllib.request.urlopen("http://rp5.ru/3034/ru")
codeRP5 = infoPage.read()
regex = re.compile(b'<div class="t_0">([+-]{0,1}\d{0,2})</b></div>')
expectedTempr = re.findall(regex, codeRP5)
for i in range(0, len(expectedTempr)):
    expectedTempr[i] = expectedTempr[i].decode('utf-8')
print(expectedTempr)
