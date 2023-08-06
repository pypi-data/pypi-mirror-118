import requests
import socket
import json
import os
import datetime
import threading
import time
from tqdm import tqdm
global runurl,trainurl
runurl="http://52.91.40.112:5000/run_autoscraper"
trainurl="http://52.91.40.112:5000/start_training"
progressurl="http://52.91.40.112:5000/get_scraper_progress"
global global_user
global_user=""
def getargs(argss,kwargs):
    args={}
    i=0
    for a in argss:
        args[str(i)]=a
        i=i+1
    args.update(kwargs)
    return args
def get_links(pages):
    links=[]
    for i in range(0,len(pages)):
        links.append("link"+str(i))
    return links
def getipaddress():
    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)
    ipaddress=ipaddress.replace('.','-')
    return ipaddress
def gettheuserid():
    try:
        userid=getipaddress()
    except:
        userid="unknown"
    return userid
def set_api_key():
    global global_user
    userid=gettheuserid()
    global_user=userid
def fetch_progress():
    global global_user,progressurl
    headers = {'Content-type': 'application/json'}
    res=requests.post(url = progressurl, data = json.dumps({"user":global_user}), headers=headers)
    try:
        res=json.loads(res.text)
    except:
        res=res.text
    prog=res["progress"]
    return prog
def show_progress():
    prog=5
    last=5
    with tqdm(total=200, desc="Progress") as progress:
        progress.update(4)
        while(prog!=100):
            last=prog
            prog=fetch_progress()
            time.sleep(0.5)
            if(prog==0 or prog<=4):
                pass
            else:
                final=prog-last
                progress.update(final+final)
    progress.close()
class scraper():
    def __init__(self):
        set_api_key()
    def train(self,*argss):
        headers = {'Content-type': 'application/json'}
        links=get_links(argss)
        start_time = threading.Timer(1,show_progress)
        start_time.start()
        res=requests.post(url = trainurl, data = json.dumps({"user":global_user,"pages":argss,"links":links,"is_pypi":True,"bot":"autoscraper"}), headers=headers)
        try:
            res=json.loads(res.text)
        except:
            res=res.text
        print("Build Scraper successfully")
        return res
    def run(self,*argss,**kwargs):
        headers = {'Content-type': 'application/json'}
        args=getargs(argss,kwargs)
        if("html" not in args):
            args["html"]=args["0"]
        else:
            args["page"]=args["html"]
        if("id" not in args):
            args["botid"]=args["1"]
        else:
            args["botid"]=args["id"]
        args["user"]=global_user
        res=requests.post(url = runurl, data = json.dumps(args), headers=headers)
        try:
            res=json.loads(res.text)
        except:
            res=res.text
        print("Run successfully")
        return res
