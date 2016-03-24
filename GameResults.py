import urllib.request as request
import re
from pymongo import MongoClient as mc
import datetime
from time import sleep
from random import random as r
from eventlet.timeout import Timeout



client = mc()
db = client.GoRatings
players = db.TopRatings.find({'isCrawled': 0})
games = db.GameResults
ratings = db.TopRatings
num = players.count()
for player in players:
    sleep(4 * r())
    player_name = player['name']
    print(player_name)
    url = "http://www.goratings.org/players/" + str(player['playerid']) + ".html"
    original = request.urlopen(url)
    response = original.read().decode('utf8')

    print('there are something')
    pattern = re.compile('''<tr><td>(.*?)</td><td>(.*?)</td>
<td>(.*?)</td>
<td>(.*?)</td>
<td><a href="(.*?)\.html">(.*?)</a></td>
<td>(.*?)</td>
<td><a href="http://www.go4go.net/go/games/sgfview/(.*?)">View game</a></td>
</tr>''')
    '''Date	Rating	Color	Result	Opponent	Opponent's Rating	Kifu'''
    results = re.findall(pattern, response)
    print(results)
    for each in results:
        date = each[0]
        rating = each[1]
        color = each[2]
        result = each[3]
        opponentid = each[4]
        opponent = each[5]
        opponentrating = each[6]
        gameid = each[7]
        games.insert_one(
            {'date': date, 'rating': rating, 'color': color, 'result': result, 'opponentid': opponentid,
             'player_opponent': opponent, 'opponentrating': opponentrating, 'gameid': gameid,
             'player_this': player['name'], 'bothid': str(player['playerid']) + '&' + str(opponentid)})
        # iscrawled set to 1
    ratings.update_one({'playerid': player['playerid']},
                       {'$set': {'isCrawled': datetime.datetime.now().isoformat()}})
    num -= 1
    print(num)
    pattern2 = re.compile(
        '<table><tr><th class="r">Wins</th><td class="r">(.*?)</td></tr><tr><th class="r">Losses</th><td class="r">(.*?)</td></tr><tr><th class="r">Total</th><td class="r">(.*?)</td></tr><tr><th class="r">Chinese Name</th><td>(.*?)</td></tr></table>')
    results2 = re.findall(pattern2, response)
    print(results2)
    for each in results2:
        wins = each[0]
        losses = each[1]
        total = each[2]
        chinese = each[3]
        ratings.update_one({'playerid': player['playerid']},
                           {'$set': {'wins': wins, 'losses': losses, 'total': total, 'chinese': chinese}})