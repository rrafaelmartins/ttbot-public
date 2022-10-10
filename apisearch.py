import oddsapiconsts
import json
import requests



#Odds API access and JSON return:

odds_response = requests.get("https://api.the-odds-api.com/v4/sports/{}/odds/?apiKey={}&regions={}&markets={},spreads&oddsFormat=american"
                            .format(oddsapiconsts.SPORT, oddsapiconsts.API_KEY, oddsapiconsts.REGION, oddsapiconsts.MARKET))
odds_json = json.loads(odds_response.text)



#Odds API search

def apiSearch(name, bettinghouse):
    for c in range(len(odds_json)):
        if (odds_json[c]['home_team'] == name) or (odds_json[c]['away_team'] == name):
            for bettingHouse in odds_json[c]['bookmakers']:
                if bettingHouse['key'] == (f"{bettinghouse}"):
                    tweetcontent = []
                    string1 = (f"Odds for {name}'s next fight on {bettingHouse['key']}: ")
                    odd1 = (f"{bettingHouse['markets'][0]['outcomes'][0]['name']}: {bettingHouse['markets'][0]['outcomes'][0]['price']}")
                    odd2 = (f"{bettingHouse['markets'][0]['outcomes'][1]['name']}: {bettingHouse['markets'][0]['outcomes'][1]['price']}")
                    tweetcontent.append(string1)
                    tweetcontent.append(odd1)
                    tweetcontent.append(odd2)
                    return tweetcontent

print(f"Remaining requests: {odds_response.headers['x-requests-remaining']}")
print(f"Used requests: {odds_response.headers['x-requests-used']}")