import mibian
'''
c = mibian.GK([1.4565, 1.45, 1, 2, 30], volatility=20)
print c.callPrice
'''
from tradersbot import TradersBot
import time
t = TradersBot('mangocore.pw', 'justinl@mit.edu', 'never-open-students')
'''t = TradersBot('localhost', 'trader0', 'trader0')'''

P = {90: 0.0, 95: 0.0, 100: 0.0, 105: 0.0, 110: 0.0}
C = {90: 0.0, 95: 0.0, 100: 0.0, 105: 0.0, 110: 0.0}
TMX = 100.0

vols = {90: 0.0, 95: 0.0, 100: 0.0, 105: 0.0, 110: 0.0}
prices = [90, 95, 100, 105, 110]

endTime = time.time()+450

def calc():
	global TMX
	global endTime
	for K in prices:
		c = mibian.BS([TMX, K, 0.0, (endTime-time.time())/15.0], callPrice = C[K])
		print c.impliedVolatility
	print

count = 0
def upd(msg, order):
	global TMX
	global count
	ticker = msg['market_state']['ticker']
	price = msg['market_state']['last_price']
	time = msg['market_state']['time']
	if ticker == 'TAMITINDEX':
		TMX = price
		return
	try:
		K = int(ticker[1:-1])
	except:
		return
	type = ticker[-1]
	if type == 'P':
		P[K] = price
	else:
		C[K] = price
	count += 1
	if count == 50:
		calc()
		count = 0

t.onMarketUpdate = upd

t.run()