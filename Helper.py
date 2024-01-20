import requests
import json
from api import apiKey
from tabulate import tabulate

def show_table(table):
    new_string = '```'

    widths = [max([len(col) for col in cols]) for cols in zip(*table)]

    for i in table:
        for j in range(len(i)):
            new_string += '| {:{}} '.format(i[j], widths[j])
        new_string += '|\n'

    new_string=new_string+"```"
    return new_string

def getProfileData(region, user, tag) -> str:
    puuid = getPuuidFromUser(region, user, tag)
    accountId = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/"+puuid+"?api_key="+apiKey+"")
    accountId=accountId.json()
    aid=accountId['id']
    print(aid)
    info = requests.get("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/"+aid+"?api_key="+apiKey+"")
    info=info.json()
    name=user+" #"+tag
    rank =info[1]["tier"]+" " +info[1]["rank"]+ "  "+str(info[1]['leaguePoints'])+" LP"
    
    wr=str(float(int(info[1]['wins'])/(int(info[1]['wins']+int(info[1]['losses'])))*100))+"% wr"
    
    string=[[name], [rank], [str(wr)]]
    print("meow")
    ret=tabulate(string, tablefmt="fancy_grid")
    endcap='```'
    ret=endcap+ret+endcap
    
    return ret
    
    
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
    
    element=[[""]*2 for _ in range(int(len(participantList)/2))]
    ret=''
    for i in range(int(len(participantList)/2)):
        element[i][0]=str(participantList[i]['summonerName']+"\n"+
                          participantList[i]['championName']+"\n"+
                          getKDA(participantList[i]))
        element[i][1]=str(participantList[i+int(len(participantList)/2)]['summonerName']+"\n"+
                          participantList[i+int(len(participantList)/2)]['championName']+"\n"+
                          getKDA(participantList[i+int(len(participantList)/2)])+"\n")
            
        ret=ret+str(participantList[i]['summonerName']+"\t "+participantList[i+int(len(participantList)/2)]['summonerName']+"\n    "+
              participantList[i]['championName']+"\t"+participantList[i+int(len(participantList)/2)]['championName']+"\n    "+
              getKDA(participantList[i])+
              "\t"+getKDA(participantList[i+int(len(participantList)/2)])+"\n")
    ret=tabulate(element, tablefmt="fancy_grid")
    endcap='```'
    ret=endcap+ret+endcap
    return ret
    