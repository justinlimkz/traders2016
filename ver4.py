from tradersbot import TradersBot
'''t = TradersBot('mangocore.pw', 'justinl@mit.edu', 'never-open-students')'''
t = TradersBot('localhost', 'trader0', 'trader0')

C = ['EUR', 'USD', 'CHF', 'JPY', 'CAD']
id = {'EUR':0, 'USD':1, 'CHF':2, 'JPY':3, 'CAD':4}
LP = {}

for cur in C:
	LP[cur] = {}
	for cur2 in C:
		LP[cur][cur2] = 0.0
		
def conv(a, b):
	if id[a] > id[b]:
		a, b = b, a
	return a+b

count = 0

def f(msg, order):
	global count
	count += 1
	if count < 10:
		count += 1
		return
	else:
		count = 0
	for i in C:
		for j in C:
			for k in C:
				if id[i] < id[j] and id[j] < id[k]:
					if LP[i][j] * LP[j][k] < LP[i][k]:
						if LP[i][j]*LP[j][k]*LP[i][k] == 0.0:
							continue
						#print i, j, k
						#print str(LP[i][j]), str(LP[j][k]), str(LP[i][k])
						order.addBuy(j+k, int(LP[i][j]*500), LP[j][k])
						order.addBuy(i+j, 500, LP[i][j])
						order.addSell(i+k, 500, LP[i][k])
						#print 'buying', int(LP[i][j]*200), 'of', j+k, 'at', LP[j][k]
						#print 'buying', 200, 'of', i+j, 'at', LP[i][j]
						#print 'selling', 200, 'of', i+k, 'at', LP[i][k]
						#print 'trade'

def upd(msg, order):
	cur = msg['trades'][0]['ticker']
	price = msg['trades'][0]['price']
	a = cur[0:3]
	b = cur[3:6]
	LP[a][b] = price
	LP[b][a] = price
            
t.onMarketUpdate = f
t.onTrade = upd

t.run()