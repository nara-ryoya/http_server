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
route('/index', 'index')

data = [
    ['それは人間のペットですか', 1, 2],
    ['それはにゃーと鳴きますか', 'ネコ', "イヌ" ],
    ["それは食べるとおいしいですか", "うし", "ライオン"]
]


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
        _url = urlparse(self.path)
        if _url.path == "/":
            self.quiz()
        elif _url.path == "/end":
            self.end()
        return


    def error(self):
        self.send_error(404, "cannot access!")
        return

    def quiz(self):
        form = FieldStorage(
            fp = self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        
        try:
            answer = int(form["answer"].value)
            if  answer == -1:
                html = index.format(
                    title="Animal",
                    message="やったー！",
                    last=-1,
                    animal="",
                    yes = 0,
                    no = 0
                )
            elif answer == -2:
                html = next.format(
                    title='Animal',
                    message='うーん、答えを教えて。',
                    last=form['last'].value,
                    animal=form['animal'].value
                )
            else:
                html = index.format(
                    title='Animal',
                    message=data[answer][0],
                    last = answer,
                    animal=form['answer'].value,
                    yes=data[answer][1],
                    no=data[answer][2]
                )
        except:
            html=index.format(
                title='Animal',
                message = f'それは、{form["answer"].value}ですか。',
                last=form['last'].value,
                animal=form['answer'].value,
                yes = -1,
                no = -2,
            )
        self.send_response(200)
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
        return

    def index(self):
        self.send_response(200)
        self.end_headers()
        html = index.format(
            title='Hello',
            message='質問に答えて！',
            last=-1,
            animal="",
            yes=0,
            no=0
        )
        self.wfile.write(html.encode('utf-8'))
        return

    def end(self):
        form=FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        animalname = form['animalname'].value
        question = form['question'].value
        last = int(form['last'].value)
        animal = form['animal'].value
        newdata = [question, animalname, animal]
        n = len(data)
        if data[last][1] == animal:
            data[last][1] = n
        elif data[last][2] == animal:
            data[last][2] = n
        data.append(newdata)

        html = index.format(
            title='Animal',
            message='なるほど、分かりました',
            last=-1,
            animal='',
            yes=0,
            no=0
        )

        self.send_response(200)
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
        return




server = HTTPServer(('', 8000), HelloServerHandler)
server.serve_forever()