import tweepy
import csv

auth = tweepy.OAuthHandler('f5G6QWK7yKOOkjRh2lGcoqFUL', 'AeFxGblr7CehCqur0djWTyYoTZYUEhFemMCVTDg5YZKo844k4r')
auth.set_access_token('15452280-wDxqy3YUrv3x5rSI5VI2nzMJSdU3PG4hctae6p1UA', 'Vu7UwTjy33GhJnnTDCLSSva8YbZumVrPLQaflLDG1zxYw')

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text+'\n')
# Iterate through the first 200 statuses in the friends timeline
f = open('output1.csv','w')
for s in tweepy.Cursor(api.user_timeline, id='republic').items(22089):
    writer = csv.writer(f)
    h = []
    for i in range(0, len(s.entities.get('hashtags'))):
        h.append(s.entities.get('hashtags')[i].get('text'))
    writer.writerow([s.id, s.text.replace('\n',''), ','.join(h)])
    # print(s.id, s.text, s.entities.get('hashtags')[0].get('text'))