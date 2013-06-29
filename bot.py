import oauth2 as oauth
import json

# authentication info
CONSUMER_KEY='KrYmGq2yTOof2wt33nKNg'
CONSUMER_SECRET='WAEDzQJAEIuiYWyjLxBERjdjgPFMCQpSFtlMBBIiRg'
ACCESS_TOKEN_KEY='783117738-kb7DUZtCypv8DH8aq4g0AKiuQRiYK8xLMIBUYMaW'
ACCESS_TOKEN_SECRET='g0pMGqMIFrYrW7cG5nzjw90NZHgKEH2QlkxQeaC7Ic'

# ski content that bot searches for to add friends
SEARCH_TERMS = ['stoked ski', 'skiing powder', 'skiing', 'freeskiing', 'winter', 'big mountain skiing', 'park skiing', 'ski boots', 'ski mountain', 'newschoolers']
# things bot likes to tweet about
TWEET_TERMS = ['stoked ski', 'skiing powder', 'skiing', 'freeskiing', 'winter', 'big mountain skiing', 'park skiing', 'ski boots', 'ski mountain', 'newschoolers', 'san francisco', 'bay area', '49ers', 'wine', 'cooking', 'grilling', 'gym', 'workout', 'fantasy league', 'protein', 'golfing', 'baseball', 'wakeboarding', 'fishing', 'broing out', 'killin it', 'kayaking', 'mountain biking', 'cliff diving', 'basketball', 'paintball', 'kiteboarding', 'motocross', 'dirtbike', 'throwing down', 'rager', 'bench press', 'gnarly', 'urban skiing', 'jim wendler'] 
# things carl doesn't like
BLACKLIST = ['http', '@', 'shit', 'fuck', 'asshole', 'ass', 'bitch', 'nigga', 'nigger', 'motherfucker', 'fucker', 'niggas', 'cunt', 'bastard', 'boner', 'cock', 'ho', 'whore', 'pussy', 'slut'] 

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
token = oauth.Token(key=ACCESS_TOKEN_KEY, secret=ACCESS_TOKEN_SECRET)
client = oauth.Client(consumer,token)

get_followers_url='https://api.twitter.com/1.1/followers/ids.json?count=5000'
resp, content = client.request(get_followers_url, method='GET')
follow_data = json.loads(content)
followers = follow_data['ids']

f=open('friends.txt', 'r')
friends=[]
for line in f:
	friends.append(int(line.strip()))

friend_url='https://api.twitter.com/1.1/friendships/create.json?follow=true&user_id='
for follower in followers:
	if follower not in friends:
		print 'Friending ' + str(follower) + '\n'
		client.request(friend_url + str(follower), method='POST')
		friends.append(follower)

out = ''
for friend in friends:
	out += str(friend) + '\n'
f = open('friends.txt', 'w')
f.write(out)
f.close()

print 'Done\n'
