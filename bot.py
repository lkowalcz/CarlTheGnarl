import twitter, os, re, random
import reply

####################################################
#
# TODO: prune favorites after removing friends? (delete and favorited tweets of no longer friends)
#
###################################################
#ugly try catch all
try:
	# log files
	LAST_MENTION_ID = 'log/last_id.txt'
	LAST_MESSAGE_ID = 'log/last_mid.txt'

	# authentication info
	CONSUMER_KEY='KrYmGq2yTOof2wt33nKNg'
	CONSUMER_SECRET='WAEDzQJAEIuiYWyjLxBERjdjgPFMCQpSFtlMBBIiRg'
	ACCESS_TOKEN_KEY='783117738-kb7DUZtCypv8DH8aq4g0AKiuQRiYK8xLMIBUYMaW'
	ACCESS_TOKEN_SECRET='g0pMGqMIFrYrW7cG5nzjw90NZHgKEH2QlkxQeaC7Ic'

	# chance of dropping an unfollowing friend
	PRUNE_PROB = 0.06
	# ADD_PROB * number of following = number of friends to add each cycle
	ADD_PROB = 0.04
	# chance of favoriting a new friend's status
	FAVORITE_PROB = 0.4
	# chance of following a person mentioned by a follower 
	BRANCH_PROB = 0.3
	# chance of replying to someone who has mentioned bot
	REPLY_PROB = 0.05

	# ski content that bot searches for to add friends
	SEARCH_TERMS = ['stoked ski', 'skiing powder', 'skiing', 'freeskiing', 'winter', 'big mountain skiing', 'park skiing', 'ski boots', 'ski mountain', 'newschoolers']
	# things bot likes to tweet about
	TWEET_TERMS = ['stoked ski', 'skiing powder', 'skiing', 'freeskiing', 'winter', 'big mountain skiing', 'park skiing', 'ski boots', 'ski mountain', 'newschoolers', 'san francisco', 'bay area', '49ers', 'wine', 'cooking', 'grilling', 'gym', 'workout', 'fantasy league', 'protein', 'golfing', 'baseball']

	# get stored info
	os.chdir('C:\Twitterbot\CarlTheGnarl')

	# get last status mention id used
	if os.path.exists(LAST_MENTION_ID):
		fp = open(LAST_MENTION_ID)
		last_mention_id = fp.read().strip()
		fp.close()
		if(last_mention_id == ''):
			last_mention_id = 0
	else:
		last_mention_id = 0

	# get last direct message id used
	if os.path.exists(LAST_MESSAGE_ID):
		fp = open(LAST_MESSAGE_ID)
		last_message_id = fp.read().strip()
		fp.close()
		if(last_message_id == ''):
			last_message_id = 0
	else:
		last_message_id = 0

	# authenticate
	api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

	# friend any followers that aren't friends
	try:
		print 'Friending any followers who are not friends...\n'
		followers = api.GetFollowers()
		friends = api.GetFriends()
		for follower in followers:
			notfollowing = 1
			toFollow = follower.GetScreenName()
			for friend in friends:
				if friend.GetScreenName() == toFollow:
					notfollowing = 0
			if notfollowing:
				print 'Following: ' + toFollow + '\n'
				try:
					api.CreateFriendship(toFollow)
				except:
					print 'Error making friend\n'
	except:
		print '\nError following people'

	# prune friend list
	print '\nPruning friend list...'
	try:
		followers = api.GetFollowers()
		for friend in friends:
			notfollowing = 1
			toCheck = friend.GetScreenName()
			for follower in followers:
				if follower.GetScreenName() == toCheck:
					notfollowing = 0
			if notfollowing:
				if random.random() < PRUNE_PROB:
					print '\nRemoving: ' + toCheck
					api.DestroyFriendship(toCheck)
				else:
					if len(api.GetFriends(toCheck)) < 5:
						print '\nRemoving: ' + toCheck
						api.DestroyFriendship(toCheck)
	except:
		print '\nError pruning friend list.'


	# add new friends
	friend_people = 1
	if friend_people:
		try:
			toAdd = int(ADD_PROB * len(friends))
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
						toAdd = toAdd - 1
					except:
						print '\nError adding ' + name
		except:
			print '\nError looking for new friends'

	# branch from current friends
	branch = 1
	if branch:
		pattern = re.compile('@[^\s]*')
		followers = api.GetFollowers()
		friends = api.GetFriends()
		toAdd = int(ADD_PROB * len(friends))
		for follower in followers:
			if toAdd < 0:
				break
			name = follower.GetScreenName()
			try:
				statuses = api.GetUserTimeline(name)
				for status in statuses:
					text = status.GetText()
					users = pattern.findall(text)
					for user in users:
						ustrip = user.strip()
						if ustrip != '' and ustrip[1:].lower() != 'carlthegnarl':
							tofriend = ustrip[1:];
							if any(s.GetScreenName().lower() == tofriend.lower() for s in friends):
								continue
							else:
								print '\nFollowing user: '+ tofriend
								try:
									if random.random() < BRANCH_PROB:
										toAdd = toAdd - 1
										api.CreateFriendship(tofriend)
								except:
									print 'error creating friendship with ' + tofriend
			except:
				print 'Error accessing timeline for' + name

	# try to post something
	tweet = 1
	if tweet:
		try:
			print '\nLooking for status to tweet..'
			candidates = api.GetSearch(random.choice(TWEET_TERMS))
			for candidate in candidates:
				try:
					text = candidate.GetText()
					# if a status doesn't mention anyone and doesn't have a link, use it
					if text.find('@') == -1 and text.find('http') == -1:
						# check if status is from a follower, if so, don't use it
						candidate_name = candidate.GetUser().GetScreenName()
						notfollower  = 1
						for follower in followers:
							if follower.GetScreenName() == candidate_name:
								notfollower = 0
						if notfollower:
							# check if status has been used already
							notrepeat = 1
							mystatuses = api.GetUserTimeline()
							for status in mystatuses:
								if status.GetText().find(text) != -1:
									notrepeat = 0
							if notrepeat:
								print '\nTweeting: ' + text
								api.PostUpdate(text)
								break
				except:
					print '\nError trying use a candidate tweet'
		except:
			print '\nError trying to post.'

	# get direct messages since last id
	checkmessages = 0
	if checkmessages:
		messages = api.GetDirectMessages(since_id=last_message_id)
		for message in messages:
			text = message.GetText()
			print '\nGot message: ' + text
			if random.random() < REPLY_PROB:
				rep = reply.getreply(text)
				if(rep != ''):
					print '\nReplying: ' + rep
					try:
						api.PostDirectMessage(message.GetSenderId(), rep)
					except:
						print '\nError sending message!'
				else:
					print '\nNot replying'
			else:
				print '\nNot replying'
		print '\nDone with messages'

	# get mentions since last id
	try:
		pattern = re.compile('@[^\s]*')
		mentions = api.GetMentions(since_id=last_mention_id)
		friends = api.GetFriends()
		for status in mentions:
			if random.random() < REPLY_PROB:
				statusid = status.GetId()
				poster = status.GetUser()
				text = status.GetText()
				print '\nFound status: ' + text
				rep = reply.getreply(text)
				if rep != '':
					replying = '@' + poster.GetScreenName() + ' ' + rep
					print '\nReplying: ' + replying
					api.PostUpdate(replying, in_reply_to_status_id=statusid)
				else:
					print '\nNot replying..'
				users = pattern.findall(text)
				for user in users:
					ustrip = user.strip()
					if ustrip != '' and ustrip[1:].lower() != 'carlthegnarl':
						tofriend = ustrip[1:];
						if any(s.GetScreenName().lower() == tofriend.lower() for s in friends):
							continue
						else:
							print '\nFollowing user: '+ tofriend
							try:
								api.CreateFriendship(tofriend)
							except:
								print 'error creating friendship with ' + tofriend
			else:
				api.CreateFavorite(status)

	except:
		print '\nError processing mentions'

	print '\nDone with mentions'

	# update logs
	if checkmessages:
		if len([x.id for x in messages]) > 0 :
			print '\nWriting new last_mid...'
			fp = open(LAST_MESSAGE_ID, 'w')
			fp.write(str(max([x.id for x in messages])))
			fp.close()
	if len([x.id for x in mentions]) > 0 :
		print '\nWriting new last_id...'
		fp = open(LAST_MENTION_ID, 'w')
		fp.write(str(max([x.id for x in mentions])))
		fp.close()
except:
	print 'Error in script caught in ugly try-catch all'
