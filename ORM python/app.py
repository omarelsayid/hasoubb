import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from Model import Model
from Field import *
from Database import Database

Model.db = Database('website.db')
Model.connection = Model.db.connect()

class Post(Model):
    title = CharField()
    body = TextField()
    created_at = DatatTime()
    published = BooleanField()

if __name__ == '__main__':
    class MyHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/posts':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(Post.all()).encode('utf-8'))

    PORT = 8000
    with HTTPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()