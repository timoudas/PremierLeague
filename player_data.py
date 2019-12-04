import requests
import json
from bs4 import BeautifulSoup
import requests

response = requests.get('https://footballapi.pulselive.com/football/competitions/1/compseasons?page=0&pageSize=100').json() # request to obtain the id values and corresponding season 

id = int(response["content"][0]["id"]) # converts current season id which is a decimal point value to interger

players = {} # dictionary to store players data

playersAndStats = {} # dictionary to store player name and associated stats

numEntries = 100

page = 0

# loop to get player name and id
while True: 
    print('looping:', page)
    params = (
      ('pageSize', '100'),
      ('compSeasons', str(id)), 
      ('altIds', 'true'),
      ('page', str(page)),
      ('type', 'player'),
      ('id', '-1'),
      ('compSeasonId', str(id)),
  )

    response = requests.get('https://footballapi.pulselive.com/football/players',params=params).json()

    playersData = response["content"]

    for playerData in playersData:
        players[playerData["id"]] = playerData["name"]["display"]

    page += 1

    if page == response["pageInfo"]["numPages"]:
        break

print("Total no. of players :",len(players))

count = 0 
total = len(players)

# loop to get player stats 
for player in players:

    count += 1
    print(count,"/",total)

    params = (
      ('comps', '1'),
      ('compSeasons', str(id)), # setting season id to current season id
  )

    playerId = str(int(player))

  # gets the stat of the player using playerId 
    response = requests.get('https://footballapi.pulselive.com/football/stats/player/'+playerId,params=params).json()

    playerInfo = response["entity"]

    stats = response["stats"]

    # creating a stat dict for the player
    playersAndStats[players[player]] = {"playerInfo":{},"stats":{}}

  # storing player info
    playersAndStats[players[player]]["playerInfo"]["name"] = playerInfo["name"]["display"]
    if "age" in playerInfo:
        playersAndStats[players[player]]["playerInfo"]["age"] = playerInfo["age"]
    if "country" in playerInfo["nationalTeam"]:
        playersAndStats[players[player]]["playerInfo"]["country"] = playerInfo["nationalTeam"]["country"]
    if "date" in playerInfo["birth"]:
        playersAndStats[players[player]]["playerInfo"]["birthdate"] = playerInfo["birth"]["date"]["label"]
        playersAndStats[players[player]]["playerInfo"]["name"] = playerInfo["name"]["display"]
        playersAndStats[players[player]]["playerInfo"]["position"] = playerInfo["info"]["position"]
        playersAndStats[players[player]]["playerInfo"]["positionInfo"] = playerInfo["info"]["positionInfo"]
    if "shirtNum" in playerInfo["info"]:
        playersAndStats[players[player]]["playerInfo"]["shirtNum"] = str(int(playerInfo["info"]["shirtNum"]))
        
        
  # loop to store each stat associated with the player
    for stat in stats:
        playersAndStats[players[player]]["stats"][stat["name"].replace("_"," ").capitalize()] = int(stat["value"])

# to store data to a json file 
f = open("data.json","w")

# pretty prints and writes the same to the json file 
f.write(json.dumps(playersAndStats,indent=4, sort_keys=True))
f.close()

print("Saved to data.json")
