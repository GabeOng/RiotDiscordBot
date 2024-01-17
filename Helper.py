import requests
import json
apiKey='RGAPI-60a5cec5-24c2-4301-a1b0-f4de38ac2f63'

def getPuuidFromUser(region, user, tag):
    getPuuid=requests.get("https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"+user+"/"+tag+"?api_key="+apiKey+"")
    accountInfo = getPuuid.json()
    puuid=accountInfo['puuid']
    print("puuid: "+puuid)
    return puuid

def getMatches(puuid):
    getMatches=requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count=20&api_key="+apiKey+"")
    matchList=getMatches.json()
    a=1
    for i in matchList:
        print(str(a)+" "+i)
        a=a+1
    return matchList

def printMatchList(matchList,participantList):
    for i in range(20):
        getMatchInfo(matchList[i])
        
def getMatchInfo(matchId):
    seeMatch=requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/"+matchId+"?api_key="+apiKey+"")
    lMatch=seeMatch.json()
    participantList=lMatch['info']['participants']
    
    for i in range(5):
        print(participantList[i]['summonerName']+"\t "+participantList[i+5]['summonerName']+"\n    "+
              participantList[i]['championName']+"\t"+participantList[i+5]['championName']+"\n    "+
              str(participantList[i]['kills'])+"/"+str(participantList[i]['assists'])+"/"+str(participantList[i]['deaths'])+
              "\t"+str(participantList[i+5]['kills'])+"/"+str(participantList[i+5]['assists'])+"/"+str(participantList[i+5]['deaths']))
    return lMatch