import requests
import json
from api import apiKey

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

def getKDA(participant) ->str:
    return (str(participant['kills'])+"/"+
     str(participant['assists'])+"/"+
     str(participant['deaths']))

def printMatchList(matchList, puuid) ->str:
    ret=""
    a=1
    for id in matchList:
        seeMatch =requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/"+str(id)+"?api_key="+apiKey+"")
        match = seeMatch.json()
        participantList=match['info']['participants']
        ret=ret+"Match "+str(a)+":\n"
        for i in participantList:
            if(i['puuid']==puuid):
                ret= ret + (i['championName']+'\n   '+
                    getKDA(i)+'\n')
        a+=1
    print(ret)
    return ret
        
def getMatchInfo(matchId):
    seeMatch=requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/"+str(matchId)+"?api_key="+apiKey+"")
    lMatch=seeMatch.json()
    #save_file = open('matchData.json', 'w')
    #json.dump(lMatch, save_file, indent=6)
    #save_file.close()
    participantList=lMatch['info']['participants']
    
    
    ret=''
    
    for i in range(5):
        print('here2')
        ret=ret+str(participantList[i]['summonerName']+"\t "+participantList[i+5]['summonerName']+"\n    "+
              participantList[i]['championName']+"\t"+participantList[i+5]['championName']+"\n    "+
              getKDA(participantList[i])+
              "\t"+getKDA(participantList[i+5])+"\n")
    
    print("meow"+ret)
    return ret
    