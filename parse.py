import urllib.request
import re
f = urllib.request.urlopen("http://rp5.ru/3034/ru")
regex = re.compile(b'<td class="title underlineRow toplineRow">')
#result = regex.search(f.read())
test = f[20:40]
#result = re.split(regex, f.read())

print(test)
