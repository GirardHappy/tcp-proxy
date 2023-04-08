from subprocess import run, Popen, DEVNULL,PIPE
from time import sleep
from json import loads
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

try:
    from requests import get
except:
    run("pip install requests")
    from requests import get

class  httpHandler(BaseHTTPRequestHandler):
    html = 'html ancora non letto'
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = self.html
        self.wfile.write(bytes(message, "utf8"))

def getconfig():
    r = open("./config.json","r")
    c = loads(r.read())
    r.close()
    try:
        a = c['ngrok_token']
        a = c['pagekite_url']
        a = c['pagekite_token']
    except:
        raise Exception('config.json formattato male')
    return c

def htmltostr():
    a = open("./page.html","r")
    s = a.read()
    a.close()
    return s

def httpserver():
    server_address = ('127.0.0.1', 8080)
    handelr = httpHandler
    handelr.html = htmltostr().replace("//tcp ip qua","var a = '"+getngrokip()[6:]+"'")
    httpd = HTTPServer(server_address, handelr)
    print("http server avviato | http localhost:8080")
    httpd.serve_forever()

def ngrok():
    run("ngrok.exe config add-authtoken "+config['ngrok_token'],stdout=DEVNULL,stderr=DEVNULL)
    run("taskkill /F /IM  ngrok.exe /T",stdout=DEVNULL,stderr=DEVNULL)
    Popen(["cd",os.getcwd(),"&&","ngrok.exe","tcp", "25565"], shell = True,stdout=DEVNULL,stderr=DEVNULL)
    i = 0
    while i<10:
        sleep(1)
        r = get("http://127.0.0.1:4040/api/tunnels")
        a = loads(r.text)
        if(len(a["tunnels"])>0):
            break
        i+=1
    print("ngrok avviato | tcp localhost:25565 -> "+a["tunnels"][0]["public_url"])
    return(a["tunnels"][0]["public_url"])

def kite():
    p = Popen("python pagekite.py --defaults --service_on=http,https:{0}:localhost:8080:{1}".format(config['pagekite_url'],config['pagekite_token']),stdout=DEVNULL,stderr=PIPE)
    print("pagekite avviato | http localhost:8080 -> vellabello.pagekite.me")
    a = p.stderr.read(2)
    if(a==b"\r\n"):
        raise Exception("pagekite non avviato, url o token forniti non validi")
    return

def getngrokip():
    try:
        r = get("http://127.0.0.1:4040/api/tunnels")
    except:
        raise Exception("Ngrok non avviato, token errato")
    return loads(r.text)["tunnels"][0]["public_url"]

config = getconfig()
ngrok()
kite()
httpserver()