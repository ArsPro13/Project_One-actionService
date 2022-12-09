from urllib.request import urlopen
from urllib.request import Request
import re

f = open('recipes.txt', 'a')

spis = []
for i in range(1, 2000):
    try:
        r = Request('https://ru.inshaker.com/cocktails/' + str(i), headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        res = urlopen(r).read().decode('utf8')
        pattern = 'ingredientGaEvent.*?\\)">(.*?)</a></td><td class="amount">(.*?)</td><td class="unit">(.*?)<'
        for elem in re.findall(pattern, res):
            if ("<i>" in elem[0]):
                print(elem[0])
                f.write(elem[0][:elem[0].index('<')] + ";")
            else:
                print(elem[0])
                f.write(elem[0] + ";")
        f.write('\n')
        print(i)
    except:
        spis.append(i)
f.close()
print(*spis)