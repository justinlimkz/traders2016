from tradersbot import TradersBot
t = TradersBot('mangocore.pw', 'justinl@mit.edu', 'never-open-students')
'''t = TradersBot('localhost', 'trader0', 'trader0')'''

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
	
	idx = 1007.000526+0.003418564*(val[0])+0.625699427*(val[1])+0.000172214*(val[3])-0.332956566*(val[4])+0.886297842*(val[5])-0.000955673*(val[6])-0.003855885*(val[7])-0.001290652*(val[8])-0.005253481*(val[9])
	print 'Estimated index: ' + str(idx)
	
t.onNews = showNews

t.run()