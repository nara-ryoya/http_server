from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from cgi import FieldStorage

with open('index.html', 'r') as f:
    index = f.read()
with open('next.html', 'r') as f:
    next = f.read()

routes = []

def route(path, method):
    routes.append((path, method))

route('/', 'index')
route('/next', 'next')
route('/index', 'index')
route('/xml', 'xml')




class HelloServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        _url = urlparse(self.path)
        print(_url)
        for r in routes:
            if (r[0] == _url.path):
                eval(f'self.{r[1]}()')
                break
        else:
            self.error()
        return

    def do_POST(self):
        form = FieldStorage(
            fp = self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        if 'sel1' in form:
            items = str(form.getlist('sel1'))
        else:
            items = "no-item"
        res = f"your OS: items"
        self.send_response(200)
        self.end_headers()
        html = next.format(
            message = res,
            data = form
        )
        self.wfile.write(html.encode('utf-8'))
        return

    def index(self):
        _url = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        html = index.format(
            title='Hello',
            message='ようこそ、HTTPServerの世界へ！'
        )
        self.wfile.write(html.encode('utf-8'))
        return
    
    def next(self):
        _url = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        html = next.format(
            message = msg,
            data = query,
            header = self.headers
        )
        self.wfile.write(html.encode('utf-8'))
        return

    def error(self):
        self.send_header(404, "cannot access!")
        return
    
    def xml(self):
        xml =  '''<?xml version="1.0" encoding="UTF-8"?>
        <data>
            <person>
                <name>Nara Ryoya</name>
                <mail>nara_ryoya@icloud.com</mail>
                <age>39</age>
            </person>
            <message>Hello Python!</message>
        </data>
        '''
        self.send_response(200)
        self.send_header('Content-Type', \
            'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(xml.encode('utf-8'))
        return

server = HTTPServer(('', 5000), HelloServerHandler)
server.serve_forever()