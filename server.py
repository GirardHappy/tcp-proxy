from subprocess import run, Popen, DEVNULL
from requests import get
from time import sleep
from json import loads
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

publictcp = 'ngrok non ancora avviato'


class  httpHandler(BaseHTTPRequestHandler):
    html = 'html ancora non letto'
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = self.html
        self.wfile.write(bytes(message, "utf8"))


def htmltostr():
    a = open("./page.html","r")
    s = a.read()
    a.close()
    return s

def httpserver():
    server_address = ('127.0.0.1', 8080)
    handelr = httpHandler
    handelr.html = htmltostr().replace("//tcp ip qua","var a = '"+publictcp[6:]+"'")
    httpd = HTTPServer(server_address, handelr)
    print("http server avviato | http localhost:8080")
    httpd.serve_forever()

def ngrok():
    run("ngrok.exe config add-authtoken 2L9EDmtuhkFOsGFAYEdcMUa6ujc_6evbbSpM7yrdPRmuKrF5z",stdout=DEVNULL,stderr=DEVNULL)
    run("taskkill /F /IM  ngrok.exe /T",stdout=DEVNULL,stderr=DEVNULL)
    Popen(["cd",os.getcwd(),"&&","ngrok.exe","tcp", "25565"], shell = True,stdout=DEVNULL,stderr=DEVNULL)
    sleep(1)
    r = get("http://127.0.0.1:4040/api/tunnels")
    a = loads(r.text)
    print("ngrok avviato | tcp localhost:25565 -> "+a["tunnels"][0]["public_url"])
    return(a["tunnels"][0]["public_url"])

def kite():
    Popen("python3 pagekite.py 8080 vellabello.pagekite.me",stdout=DEVNULL,stderr=DEVNULL)
    print("pagekite avviato | http localhost:8080 -> vellabello.pagekite.me")
    return

publictcp = ngrok()
kite()
httpserver()