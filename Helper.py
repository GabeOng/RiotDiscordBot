import requests
import json
from api import apiKey

def show_table(table):
    new_string = '```'

    widths = [max([len(col) for col in cols]) for cols in zip(*table)]

    for i in table:
        for j in range(len(i)):
            new_string += '| {:{}} '.format(i[j], widths[j])
        new_string += '|\n'

    new_string=new_string+"```"
    return new_string

def getPuuidFromUser(region, user, tag):
    getPuuid=requests.get("https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"+user+"/"+tag+"?api_key="+apiKey+"")
    accountInfo = getPuuid.json()
    puuid=accountInfo['puuid']
    print("puuid: "+puuid)
    return puuid

def getMatches(puuid):
    getMatches=requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count=20&api_key="+apiKey+"")
    matchList=getMatches.json()
    return matchList

def getKDA(participant) ->str:
    return (str(participant['kills'])+"/"+
     str(participant['assists'])+"/"+
     str(participant['deaths']))

def printMatchList(matchList, puuid) ->str:
    
    a=1
    element=[[""]*3 for _ in range(len(matchList))]
    for id in matchList:
        ret=""
        seeMatch =requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/"+str(id)+"?api_key="+apiKey+"")
        match = seeMatch.json()
        participantList=match['info']['participants']
        adding=str("Match "+str(a))
        element[a-1][0]=adding
        for i in range(len(matchList)):
            if(participantList[i]['puuid']==puuid):
                element[a-1][1]=str(participantList[i]['championName'])
                element[a-1][2]=str(getKDA(participantList[i]))
                break
        
        a+=1
    ret= show_table(element)
    return ret
        
def getMatchInfo(matchId):
    seeMatch=requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/"+str(matchId)+"?api_key="+apiKey+"")
    lMatch=seeMatch.json()
    #save_file = open('matchData.json', 'w')
    #json.dump(lMatch, save_file, indent=6)
    #save_file.close()
    participantList=lMatch['info']['participants']
    
    
    ret=''
    
    for i in range(len(participantList)/2):
        ret=ret+str(participantList[i]['summonerName']+"\t "+participantList[i+len(participantList)/2]['summonerName']+"\n    "+
              participantList[i]['championName']+"\t"+participantList[i+len(participantList)/2]['championName']+"\n    "+
              getKDA(participantList[i])+
              "\t"+getKDA(participantList[i+len(participantList)/2])+"\n")

    return ret
    