import requests
import json
import Helper
region='na1'


#get puuid from region, username and tag
puuid = Helper.getPuuidFromUser('na1', 'Chocomelk', "Choco")
#get Their last 10 games
matchList=Helper.getMatches(puuid)
#select which match to look at
matchId=matchList[5]
#for i in range(20):
Helper.getMatchInfo(matchList[6])
#get Match Info
#matchInfo=Helper.getMatchInfo(matchId)

Helper.printMatchList(matchList, puuid)




