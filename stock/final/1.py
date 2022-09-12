import twstock
stock = {}

std = twstock.realtime.get('2330')
stock.update({'sname':std.get('info').get('name')})

stock.update({'scode':std.get('info').get('code')})
stock.update({'stime':std.get('info').get('time')})
stock.update({'sfullname':std.get('info').get('fullname')})
stock.update({'buy_price':std.get('realtime').get('best_bid_price')})
stock.update({'buy_volume':std.get('realtime').get('best_bid_volume')})
stock.update({'sell_price':std.get('realtime').get('best_ask_price')})
stock.update({'sell_volume':std.get('realtime').get('best_ask_volume')})
print(stock)