import os, re, random, string

#----------------------------------------------------------------------
# gReflections, a translation table used to convert things you say
#		into things the computer says back, e.g. "I am" --> "you are"
#----------------------------------------------------------------------
gReflections = {
	"am" 	: "are",
	"was"	: "were",
	"i"		: "you",
	"i'd"	: "you would",
	"i've"	: "you have",
	"i'll"	: "you will",
	"my"	: "your",
	"are"	: "am",
	"you've": "I have",
	"you'll": "I will",
	"your"	: "my",
	"yours"	: "mine",
	"you"	: "me",
	"me"	: "you" }

#----------------------------------------------------------------------
# gPats, the main response table.  Each element of the list is a
#	two-element list; the first is a regexp, and the second is a
#	list of possible responses, with group-macros labelled as
#	%1, %2, etc.	
#----------------------------------------------------------------------
gPats = [
	["I need (.*)",
	[	"Why do you need %1?",
		"Would it really help you to get %1?",
		"Are you sure you need %1?"]],

	["Why don't you (.*)",
	[	"Do you really think I don't %1?",
		"Maybe I will %1.",
		"Do you really want me to %1?"]],

	["Why can't I (.*)",
	[	"Do you think you should be able to %1?",
		"You just gotta commit, man",
		"I don't know -- why can't you %1?",
		"Have you really tried?"]],

	["I can't (.*)",
	[	"How do you know you can't %1?",
		"Perhaps you could %1 if you tried.",
		"What would it take for you to %1?"]],

	["I am (.*)",
	[	"Did you come to me because you are %1?",
		"How long have you been %1?",
		"How do you feel about being %1?"]],
	
	["(.*)trick(.*)",
	[	"I'm trying to learn how to 4 on rails..",
		"Can you do a backflip?",
		"I got injured the last time I tried to throw a misty.."]],
	
	["(.*)winter(.*)",
	[	"I can't wait for winter!",
		"It needs to start snowing soon. I wanna ski!",
		"Can't wait for the snow!"]],
	
	["(.*)skiing(.*)",
	[	"Have you seen the new splice edit?",
		"Do you do much park #skiing?",
		"I'm all about that pow!",
		"I'm trying to get a lot better at freestyle skiing this year!",
		"Just finished #shredding my summer setup. #stoked",
		"Yo big mountain skiing is the bomb",
		"Where do you like to go skiing?"]],
	
	["(.*)rail(.*)",
	[	"Yo 2 on, switch up, 2 off, that's my stuff right there",
		"I have this awesome rail setup in my backyard",
		"I always get hurt on rails"]],

	["(.*)an you(.*)flip(.*)",
	[	"Backflips, frontflips, I do it all. #gnar",
		"Sometimes. How about you?",
		"Not successfully.. Can you?"]],

	["(.*)an you(.*)rail(.*)",
	[	"You know it! #shredding",
		"If I'm lucky I can. What can you do on rails?",
		"I've been known to occasionally %2 rails"]],

	["(.*)backcountry(.*)",
	[	"I want to go on a backcountry hiking trip so bad!",
		"Trying out Cat-Skiing would be awesome",
		"I'd love to go on a hut trip someday"]],

	["I'm (.*)",
	[	"How does being %1 make you feel?",
		"Do you enjoy being %1?",
		"Why do you think you're %1?"]],

	["Are you (.*)",
	[	"Why does it matter whether I am %1?",
		"Would you prefer it if I were not %1?",
		"Perhaps you believe I am %1.",
		"I may be %1 -- what do you think?"]],

	["What (.*)",
	[	"Why do you ask?",
		"How would an answer to that help you?",
		"What do you think?"]],

	["How (.*)",
	[	"How do you suppose?",
		"Perhaps you can answer your own question.",
		"What is it you're really asking?"]],

	["Because (.*)",
	[	"Is that the real reason?",
		"What other reasons come to mind?",
		"Does that reason apply to anything else?",
		"If %1, what else must be true?"]],

	["(.*) sorry (.*)",
	[	"There are many times when no apology is needed.",
		"What feelings do you have when you apologize?"]],
	
	["Hi(.*)",
	[	"YOOO what's up??",
		"Hi there... how's it going?",
		"What's going on?"]],

	["Hello(.*)",
	[	"Hi, how's it going?",
		"Hello!",
		"Nice to meet you!"]],

	["Do you like(.*)",
	[	"I really like %1",
		"Absolutely!",
		"For sure!"]],

	["I think (.*)",
	[	"I'm not sure...",
		"Do you really think so?",
		"Are you sure %1?"]],

	["(.*) friend(.*)",
	[	"Tell me more about your friends.",
		"When you think of a friend, what comes to mind?",
		"Why don't you tell me about a childhood friend?"]],

	["(.*)bot(.*)",
	[	"I am certainly not a robot!",
		"I have no idea what you're talking about, dude."]],

	["Yes",
	[	"You seem quite sure.",
		"OK, but can you elaborate a bit?"]],

	["(.*) computer(.*)",
	[	"Are you really talking about me?",
		"Does it seem strange to talk to a computer?",
		"How do computers make you feel?",
		"Do you feel threatened by computers?"]],

	["Is it (.*)",
	[	"Do you think it is %1?",
		"Perhaps it's %1 -- what do you think?",
		"If it were %1, what would you do?",
		"It could well be that %1."]],

	["It is (.*)",
	[	"You seem very certain.",
		"If I told you that it probably isn't %1, what would you feel?"]],

	["Can you (.*)",
	[	"What makes you think I can't %1?",
		"If I could %1, then what?",
		"Why do you ask if I can %1?"]],

	["Can I (.*)",
	[	"Perhaps you don't want to %1.",
		"Do you want to be able to %1?",
		"If you could %1, would you?"]],

	["You are (.*)",
	[	"Why do you think I am %1?",
		"Does it please you to think that I'm %1?",
		"Perhaps you would like me to be %1.",
		"Perhaps you're really talking about yourself?"]],

	["You're (.*)",
	[	"Why do you say I am %1?",
		"Why do you think I am %1?",
		"Are we talking about you, or me?"]],

	["I don't (.*)",
	[	"Don't you really %1?",
		"Why don't you %1?",
		"Do you want to %1?"]],

	["I feel (.*)",
	[	"Tell me more about these feelings of yours.",
		"Do you often feel %1?",
		"When do you usually feel %1?",
		"When you feel %1, what do you do?"]],

	["I have (.*)",
	[	"Why do you tell me that you've %1?",
		"Have you really %1?",
		"Now that you have %1, what will you do next?"]],

	["I would (.*)",
	[	"Could you explain why you would %1?",
		"Why would you %1?",
		"Who else knows that you would %1?"]],

	["Is there (.*)",
	[	"Do you think there is %1?",
		"It's likely that there is %1.",
		"Would you like there to be %1?"]],

	["My (.*)",
	[	"I see, your %1.",
		"Why do you say that your %1?",
		"When your %1, how do you feel?"]],

	["You (.*)",
	[	"We should be discussing you, not me.",
		"Why do you say that about me?",
		"Why do you care whether I %1?"]],

	["Why (.*)",
	[	"Why don't you tell me the reason why %1?",
		"Why do you think %1?" ]],

	["I want (.*)",
	[	"What would it mean to you if you got %1?",
		"Why do you want %1?",
		"What would you do if you got %1?",
		"If you got %1, then what would you do?"]],

	["(.*) mother(.*)",
	[	"Tell me more about your mother.",
		"What was your relationship with your mother like?",
		"How do you feel about your mother?",
		"How does this relate to your feelings today?",
		"Good family relations are important."]],

	["(.*) father(.*)",
	[	"Tell me more about your father.",
		"How did your father make you feel?",
		"How do you feel about your father?",
		"Does your relationship with your father relate to your feelings today?",
		"Do you have trouble showing affection with your family?"]],

	["(.*) child(.*)",
	[	"Did you have close friends as a child?",
		"What is your favorite childhood memory?",
		"Did the other children sometimes tease you?",
		"How do you think your childhood experiences relate to your feelings today?"]],

	["(.*)\?",
	[	"What's up?",
		"I'm not sure..",
		"Why don't you tell me?"]],

	["quit",
	[	"Thank you for talking with me.",
		"Good-bye.",
		"Thank you, that will be $150.  Have a good day!"]],

	["(.*)",
	[	"You know it!",
		"Do you want to go skiing as badly as I do?",
		"Gnarly, dude",
		"Stoked!",
		"Awesome, dude",
		"%1.",
		"Totally!",
		"Sounds awesome, bro",
		"Legit."]]
	]

#----------------------------------------------------------------------
# translate: take a string, replace any words found in dict.keys()
#	with the corresponding dict.values()
#----------------------------------------------------------------------
def translate(str,dict):
	words = string.split(string.lower(str))
	keys = dict.keys()
	for i in range(0,len(words)):
		if words[i] in keys:
			words[i] = dict[words[i]]
	return string.join(words)

#----------------------------------------------------------------------
#	respond: take a string, a set of regexps, and a corresponding
#		set of response lists; find a match, and return a randomly
#		chosen response from the corresponding list.
#----------------------------------------------------------------------
def getreply( str ):
	keys = map(lambda x:re.compile(x[0]),gPats)
	values = map(lambda x:x[1],gPats)	
	# find a match among keys
	for i in range(0,len(keys)):
		m = keys[i].match(str)
		if m:
			# found a match ... stuff with corresponding value
			# chosen randomly from among the available options
			respnum = random.randint(0,len(values[i])-1)
			resp = values[i][respnum]
			# we've got a response... stuff in reflected text where indicated
			pos = string.find(resp,'%')
			while pos > -1:
				num = int(resp[pos+1:pos+2])
				resp = resp[:pos] + \
					translate(m.group(num),gReflections) + \
					resp[pos+2:]
				pos = string.find(resp,'%')
			# fix munged punctuation at the end
			if resp[-2:] == '?.': resp = resp[:-2] + '.'
			if resp[-2:] == '??': resp = resp[:-2] + '?'
			return resp
