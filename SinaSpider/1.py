from bs4 import BeautifulSoup
import os
from lxml import etree

f = open('1.html', 'rb')
s = f.read()
html = etree.HTML(s)

a_s = title = html.xpath('/html/head/title/text()')[0]
print(a_s)
# print(a_s.xpath('string(.)'))