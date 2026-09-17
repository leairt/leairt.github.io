from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlsplit,unquote
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
class Handler(SimpleHTTPRequestHandler):
 extensions_map={**SimpleHTTPRequestHandler.extensions_map,'.mjs':'text/javascript','.webp':'image/webp','.woff2':'font/woff2'}
 def do_GET(self):
  route=unquote(urlsplit(self.path).path).strip('/')
  if route and Path(route,'index.html').is_file():
   self.path='/'+route+'/index.html'
  super().do_GET()
if __name__=='__main__':
 print('Local: http://localhost:8000',flush=True)
 ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()
