from datakund_scraper import *
import json
import datetime
def read_file(file):
    with open(file+".txt",encoding="utf-8") as d:
        html=d.read()
    return html
print(datetime.datetime.now())
html1=read_file("html1")
html2=read_file("html2")
res=scraper.train(html1,html2)
#res=scraper.run(html1,id="QMEWUC0UX2EDL07")
print("res",res)
print(datetime.datetime.now())