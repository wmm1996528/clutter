import requests
import re
import json
url = 'https://s.taobao.com/search?q=iphonex&app=detailproduct&through=1'

with open('1.html', 'r') as f:
    text = f.read()
    s = re.findall('({"pageName":.+"shopcardOff":false}})',text, re.S)[0]
    js = json.loads(s)
    itemlist = js['mods']['itemlist']['data']['auctions']
    print(itemlist)
    for item in itemlist:
        tiltle =item['raw_title']
        detail_url = item['detail_url']
        view_price = item['view_price']
        item_loc = item['item_loc']
        reserve_price = item['reserve_price']
        view_sales = item['view_sales']
        comment_count = item['comment_count']
        nick = item['nick']
        data = {
            'tiltle':tiltle,
            'detail_url':detail_url,
            'view_price':view_price,
            'item_loc':tiltle,
            'reserve_price':reserve_price,
            'view_sales':view_sales,
            'comment_count':comment_count,
            'nick':nick,
        }
        print(data)

