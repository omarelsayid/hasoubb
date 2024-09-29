from datetime import datetime
import json
from Model import Model
from Field import *
from Database import Database
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse

Model.db = Database('database.sqlite')
Model.connection = Model.db.connect()

PORT = 8000


class Post(Model):
    title = CharField()
    body = TextField()
    created_at = DateTimeField()
    published = BooleanField()


class User(Model):
    first_name = CharField()
    last_name = CharField(max_length=225)
    age = IntegerField()


if __name__ == '__main__':

    class MyHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                return SimpleHTTPRequestHandler.do_GET(self)

            elif self.path == '/posts':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(Post.all()).encode('utf-8'))
            else:
                post_id = int(self.path.split('/')[-1])
                result = Post.get(post_id)
                if result is False:
                    self.send_response(404)
                    self.wfile.write(b'Not found')
                    return
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(Post.get(post_id)).encode('utf-8'))

        def do_POST(self):
            length = int(self.headers.get('Content-length'))
            body = self.rfile.read(length)
            string = urlparse(body)
            post = parse_qs(string.path.decode('utf-8'))
            Post.create(title=post['title'][0], body=post['body'][0], created_at=datetime.now(), published=False)
            self.send_response(301)
            self.send_header('Location', 'localhost:8000')
            self.end_headers()


    with HTTPServer(("", PORT), MyHandler) as httpd:
        print('Serving at PORT', PORT)
        httpd.serve_forever()
