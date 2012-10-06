import subprocess, time, urllib, random
BOT_PY = 'bot.py'
REPLY_PY = 'reply.py'
while 1:
	# execute bot cycle
	try:
		print 'Executing bot cycle...\n'
		subprocess.call(["git", "pull"])
		time.sleep(5)
	except:
		print 'ERROR trickled up from script!\n'
	print 'Sleeping...\n'
	time.sleep(150)
