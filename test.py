from tradersbot import TradersBot
import time
'''t = TradersBot('mangocore.pw:10914', 'justinl@mit.edu', 'never-open-students')'''
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

def f(msg, order):
	count = 0
	for i in C:
		for j in C:
			for k in C:
				if i != j and i != k and j != k:
					if LP[i][j] * LP[j][k] > LP[i][k]:
						order.addBuy(conv(i, j), int(LP[i][j]*LP[j][k]*100), LP[i][j])
						order.addBuy(conv(j, k), int(LP[j][k]*100), LP[j][k])
						order.addSell(conv(i, k), 100, LP[i][k])
						count += 3
						print 'trading ' + conv(i, j) + ' at ' + str(LP[i][j])
						if count > 2:
							return
		'''
		if LP['EURUSD']*LP["USDJPY"] < LP["EURUSD"]:
			order.addBuy('EURUSD', 100)
			order.addBuy('USDJPY', 100)
			order.addSell('EURUSD', 100)
		cur = msg['market_state']['ticker']
		order.addBuy(cur, 10, lastprice-0.1)
		order.addSell(cur, 10, lastprice)
		'''

def upd(msg, order):
	cur = msg['trades'][0]['ticker']
	price = msg['trades'][0]['price']
	a = cur[0:3]
	b = cur[3:6]
	LP[a][b] = price
	LP[b][a] = price
	print 'updating ' + a + b + ' to ' + str(price)

t.onMarketUpdate = f
t.onTrade = upd

t.run()