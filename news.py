from tradersbot import TradersBot
'''t = TradersBot('mangocore.pw:10914', 'justinl@mit.edu', 'never-open-students')'''
t = TradersBot('localhost', 'trader0', 'trader0')

def showNews(msg, order):
	a = msg['news']['body'].split()
	val = []
	for word in a:
		word = word.strip(';')
		try:
			num = float(word)
			val.append(num)
		except:
			continue
	print val
	
	idx = 

t.onNews = showNews

t.run()