import traceback
import tweepy
from time import sleep
import apisearch
import twitterapiconsts

#Twitter API setup
client = tweepy.Client(twitterapiconsts.BEARER_TOKEN, twitterapiconsts.API_KEY, twitterapiconsts.API_SECRET, twitterapiconsts.ACCESS_TOKEN, twitterapiconsts.ACCESS_TOKEN_SECRET)
auth = tweepy.OAuth1UserHandler(twitterapiconsts.API_KEY, twitterapiconsts.API_SECRET, twitterapiconsts.ACCESS_TOKEN, twitterapiconsts.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#Retrieving last mention id
f = open("lastTweet.txt","r")
mention_id = int(f.readline())
f.close()

#Reading mentions and tweeting if necessary
lastStatus = 'not duplicate'
nextStatus = True
while True:
    if lastStatus != 'duplicate' and nextStatus == True:
        mentions = api.mentions_timeline(since_id = mention_id)
        for mention in mentions:
            if mention.in_reply_to_status_id is None:
                if '@mmaoddwatch' in mention.text:
                    if (',' in mention.text):
                        try:
                            fulltweet = mention.text.split('@mmaoddwatch ')
                            formatedtweet = fulltweet[1].strip().split(',')
                            name = formatedtweet[0].strip()
                            bettinghouse = formatedtweet[1].strip()
                            tweet = apisearch.apiSearch(name, bettinghouse)
                            print(type(bettinghouse))
                            print(name, bettinghouse)
                            print(lastStatus)
                            try:
                                api.update_status(status = f" @{mention.author.screen_name} {tweet[0]} \n {tweet[1]} \n {tweet[2]}", in_reply_to_status_id = mention.id )
                                print(tweet)
                                lastStatus = 'not duplicate'
                            except:
                                lastStatus = 'duplicate'
                                traceback.print_exc()
                                continue
                        except:
                            continue
            if mention.id > mention_id:
                mention_id = mention.id
                f = open("lastTweet.txt","w")
                f.write(str(mention_id))
                f.close()
            sleep(15)
        nextStatus = False
    else:
        print("Waiting for new mentions...")
        for c in range(60,0,-1):
            print(c)
            sleep(1)
        nextStatus = True
    
