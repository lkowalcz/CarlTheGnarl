import twitter, os, sys, re, random
import reply

####################################################
# TODO: prune favorites after removing friends? (delete and favorited tweets of no longer friends)
###################################################

# main directory
DIRECTORY = 'C:\Twitterbot\CarlTheGnarl'

# log files
LAST_MENTION_ID = 'log/last_id.txt'

# authentication info
CONSUMER_KEY='KrYmGq2yTOof2wt33nKNg'
CONSUMER_SECRET='WAEDzQJAEIuiYWyjLxBERjdjgPFMCQpSFtlMBBIiRg'
ACCESS_TOKEN_KEY='783117738-kb7DUZtCypv8DH8aq4g0AKiuQRiYK8xLMIBUYMaW'
ACCESS_TOKEN_SECRET='g0pMGqMIFrYrW7cG5nzjw90NZHgKEH2QlkxQeaC7Ic'

# chance of dropping an unfollowing friend
PRUNE_PROB = 0.5
# ADD_NUM = number of friends to add each cycle
ADD_NUM = 10
# ADD_NUM = number of friends of friends to add each cycle
BRANCH_NUM = 2
# chance of favoriting a new friend's status
FAVORITE_PROB = 0.4
# chance of following a person mentioned by a follower 
BRANCH_PROB = 0.3
# chance of replying to someone who has mentioned bot
REPLY_PROB = 0.05

# ski content that bot searches for to add friends
SEARCH_TERMS = ['stoked ski', 'skiing powder', 'skiing', 'freeskiing', 'winter', 'big mountain skiing', 'park skiing', 'ski boots', 'ski mountain', 'newschoolers']
# things bot likes to tweet about
TWEET_TERMS = ['stoked ski', 'skiing powder', 'skiing', 'freeskiing', 'winter', 'big mountain skiing', 'park skiing', 'ski boots', 'ski mountain', 'newschoolers', 'san francisco', 'bay area', '49ers', 'wine', 'cooking', 'grilling', 'gym', 'workout', 'fantasy league', 'protein', 'golfing', 'baseball', 'wakeboarding', 'fishing', 'broing out', 'killin it', 'kayaking', 'mountain biking', 'cliff diving', 'basketball', 'paintball', 'kiteboarding', 'motocross', 'dirtbike', 'throwing down', 'rager', 'bench press', 'gnarly', 'urban skiing', 'jim wendler'] 
# things carl doesn't like
BLACKLIST = ['http', '@', 'shit', 'fuck', 'asshole', 'ass', 'bitch', 'nigga', 'nigger', 'motherfucker', 'fucker', 'niggas', 'cunt', 'bastard', 'boner', 'cock', 'ho', 'whore', 'pussy', 'slut'] 

followers = []
friends = []

##################
# get stored info
##################
try:
	os.chdir(DIRECTORY)
except:
	print 'Error changing directory\n'

try:
	# get last status mention id used
	if os.path.exists(LAST_MENTION_ID):
		fp = open(LAST_MENTION_ID)
		last_mention_id = fp.read().strip()
		fp.close()
		if(last_mention_id == ''):
			last_mention_id = 0
	else:
		last_mention_id = 0
except:
	print 'Error reading log files\n'

###############
# authenticate
###############
try:
	api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
except:
	print 'Error authenticating\n'
	sys.exit()

##################################
# build friend and follower lists
##################################

# temporary fix due to this twitter wrapper using API version 1 - need to migrate to different wrapper
def MyGetFollowerIDs(api, cursor):
	url = 'http://api.twitter.com/1.1/followers/ids.json?cursor=' + str(cursor) + '&screen_name=carlthegnarl'
	json = api._FetchUrl(url)
	data = api._ParseAndCheckTwitter(json)
	return data

print 'Building friend/followers id lists\n'
cursor = -1
while cursor != 0:
	ret = MyGetFollowerIDs(api, cursor)
	cursor = ret["next_cursor"]
	followers.extend(ret["ids"])
cursor = -1
while cursor != 0:
	ret = api.GetFriendIDs(cursor=cursor)
	cursor = ret["next_cursor"]
	friends.extend(ret["ids"])
print 'Found ' + str(len(friends)) + ' friends and ' + str(len(followers)) + ' followers!\n'

###########################################
# friend any followers that aren't friends
###########################################
try:
	print 'Friending any followers who are not friends...\n'
	newFollowers = filter((lambda follower: follower not in friends), followers)
	for follower in newFollowers:
		print 'Following: ' + str(follower) + '\n'
		try:
			api.CreateFriendship(follower)
		except:
			print 'Error making friend\n'
except:
	print 'Error following followers\n'

####################
# prune friend list
####################
try:
	print 'Pruning friend list...\n'
	for friend in friends:
		if friend not in followers:
			# if friend is not following back, remove him with PRUNE_PROB probability
			if random.random() < PRUNE_PROB:
				print 'Removing: ' + str(friend) + '\n'
				try:
					api.DestroyFriendship(friend)
				except:
					print 'Error removing friend\n'
except:
	print 'Error pruning friend list\n'

##################
# add new friends
##################

# using random keyword
try:	
	toAdd = ADD_NUM
	toSearch = random.choice(SEARCH_TERMS)
	print '\nSearching for new friends who tweet about: ' + toSearch
	candidates = api.GetSearch(toSearch)
	for candidate in candidates:
		if toAdd < 0:
			break
		name = candidate.GetUser().GetScreenName()
		if name.lower() != 'carlthegnarl':
			print '\nAdding: ' + name
			try:
				if random.random() < FAVORITE_PROB:
					print '. Favoriting his tweet too!'
					api.CreateFavorite(candidate)
				api.CreateFriendship(name)
				toAdd -= 1
			except:
				print '\nError adding ' + name
except:
	print '\nError looking for new friends'

# branching from current friends
pattern = re.compile('@[^\s]*')
toAdd = BRANCH_NUM
# this is messy and needs to be cleaned up
for follower in followers:
	if toAdd < 0:
		break
	try:
		statuses = api.GetUserTimeline(id=follower)
		for status in statuses:
			text = status.GetText()
			users = pattern.findall(text)
			for user in users:
				ustrip = user.strip()
				if ustrip != '' and ustrip[1:].lower() != 'carlthegnarl':
					tofriend = ustrip[1:];
					print 'Following user: '+ tofriend + '\n'
					try:
						if random.random() < BRANCH_PROB:
							toAdd = toAdd - 1
							api.CreateFriendship(tofriend)
					except:
						print 'Error creating friendship with ' + tofriend + '\n'
	except:
		print 'Error accessing timeline for' + str(follower)

###############
# post a tweet
###############
try:
	print 'Looking for status to tweet..\n'
	candidates = api.GetSearch(random.choice(TWEET_TERMS))
	for candidate in candidates:
		try:
			text = candidate.GetText()
			# if a status doesn't mention anyone and doesn't have a link and doesn't use profanity, use it
			if all(text.find(term) == -1 for term in BLACKLIST):
				# check if status is from a follower, if so, don't use it
				candidate_id = candidate.GetUser().id
				if candidate_id not in followers:
					# check if status has been used already
					notrepeat = 1
					mystatuses = api.GetUserTimeline()
					for status in mystatuses:
						if status.GetText().find(text) != -1:
							notrepeat = 0
					if notrepeat:
						print 'Tweeting: ' + text + '\n'
						api.PostUpdate(text)
						break
		except:
			print 'Error trying use a candidate tweet\n'
except:
	print 'Error trying to post.\n'

#############################
# get mentions since last id
#############################
try:
	pattern = re.compile('@[^\s]*')
	mentions = api.GetMentions(since_id=last_mention_id)
	for status in mentions:
		if random.random() < REPLY_PROB:
			statusid = status.GetId()
			poster = status.GetUser()
			text = status.GetText()
			print 'Found status: ' + text + '\n'
			rep = reply.getreply(text)
			if rep != '':
				replying = '@' + poster.GetScreenName() + ' ' + rep
				print 'Replying: ' + replying + '\n'
				api.PostUpdate(replying, in_reply_to_status_id=statusid)
			else:
				print '\Not replying..\n'
			users = pattern.findall(text)
			for user in users:
				ustrip = user.strip()
				if ustrip != '' and ustrip[1:].lower() != 'carlthegnarl':
					tofriend = ustrip[1:];
					print 'Following user: '+ tofriend + '\n'
					try:
						api.CreateFriendship(tofriend)
					except:
						print 'Error creating friendship with ' + tofriend + '\n'
		else:
			# don't favorite spam mentions - check to see that at most 2 other people are also mentioned in the status
			if len(list(re.finditer('@', status.GetText()))) < 3:
				api.CreateFavorite(status)
except:
	print 'Error processing mentions\n'

##############
# update logs
##############
try:
	if len([x.id for x in mentions]) > 0 :
		print 'Writing new last_id...\n'
		fp = open(LAST_MENTION_ID, 'w')
		fp.write(str(max([x.id for x in mentions])))
		fp.close()
except:
	print 'Error writing log files\n'
