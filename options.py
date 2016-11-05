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
		VOL = c.impliedVolatility
		print VOL
		vols[K] = VOL
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

def status(msg, order):
	global TMX
	global endTime
	totalDelta = 0.0
	totalVega = 0.0
	for key in msg['trader_state']['positions']:
		quant = msg['trader_state']['positions'][key]
		print key, quant
		try:
			K = int(key[1:-1])
		except:
			continue
		v = vols[K]
		if vols[K] == 0.0 or vols[K] == None:
			v = 20
		c = mibian.BS([TMX, K, 0.0, (endTime-time.time())/15.0], volatility = v)
		type = key[-1]
		if type == 'P':
			totalDelta += (c.putDelta)*quant
		else:
			totalDelta += (c.callDelta)*quant
		totalVega += c.vega*quant
	print 'Total delta: ' + str(totalDelta*100)
	print 'Total vega: ' + str(totalVega*100)

t.onMarketUpdate = upd
t.onTraderUpdate = status

t.run()