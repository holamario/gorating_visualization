import urllib.request as request
import re
from pymongo import MongoClient as mc

url="http://www.goratings.org/"
original=request.urlopen(url)
response=original.read().decode('utf8')

pattern=re.compile('''<tr><td class="r">(.*?)</td><td><a href="./(.*?).html">(.*?)</a></td><td class="c"><span style=".*?">(.*?)</span></td><td class="c"><img src="/flags/(.*?).svg" style="height:1em;vertical-align:middle" alt=".*?" /></td><td>(.*?)</td>
</tr>''')
result=re.findall(pattern,response)
print(result)

client=mc()
db=client.GoRatings
ratings=db.TopRatings
for each in result:
    ratings.insert_one({"rating":each[0],"playerid":each[1].split('/')[1],"name":each[2],"gender":each[3],"nationality":each[4],"elo":each[5]})

ratings.insert_one({"rating":2,"playerid":1718,"name":'Google AlphaGo',"gender":'none',"nationality":'none',"elo":'3586'})