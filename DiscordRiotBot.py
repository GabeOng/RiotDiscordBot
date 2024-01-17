import requests
import json
import Helper
region='na1'
apiKey='RGAPI-60a5cec5-24c2-4301-a1b0-f4de38ac2f63'

#get puuid from region, username and tag
puuid = Helper.getPuuidFromUser('na1', 'Chocomelk', "Choco")
#get Their last 10 games
matchList=Helper.getMatches(puuid)
#select which match to look at
matchId=matchList[5]
for i in range(20):
    Helper.getMatchInfo(matchList[i])
#get Match Info
matchInfo=Helper.getMatchInfo(matchId)


save_file = open('matchData.json', 'w')
json.dump(matchInfo, save_file, indent=6)
save_file.close()

