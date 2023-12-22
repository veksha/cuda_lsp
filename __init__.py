from .lsp import Command
from .language import Language
from .util import generate_color

import threading
import http.server
import socketserver
import html
import re
import os

lines = []

def addLine(prefix, line):
    global lines
    line = re.sub(r"^Content-Length:.+?\\r\\n\\r\\n", r"", line)
    line = re.sub(r"Content-Length:.+?\\r\\n\\r\\n{", r"\n\t\t\t     {", line)
    
    m = re.search(r'"id":\s*(\d+)', line)
    if m:
        id = "ID: "+m.group(1)
        line = "<span style='color:"+generate_color(id)+"'>"+id + "</span>, " + prefix + html.escape(line)
    else:
        line = "--------" + prefix + html.escape(line)
    line = re.sub(r'(&quot;method&quot;:\s*&quot;)(.+?)(&quot;)', r"\1<span style='color:OrangeRed'>\2</span>\3", line)
    line = re.sub(r"(ID:\s*\d+),", r"<span style='color:red'>\1</span>", line)
    line = str(len(lines)+1) + ". " + line
    lines.append(line)

# Define the HTTP request handler
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return # disables logging
  
    def send(self, text):
        text = text.encode()
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-length", str(len(text)))
        self.end_headers()
        try:
            self.wfile.write(text)
        except BrokenPipeError:
            pass

    
    def do_GET(self):
        global lines
        # Define the response content
        if self.path == "/":
            self.send(htmlpage)
        elif self.path == "/get":
            self.send("\n".join(lines))

# Start the HTTP server in a separate thread
def start_http_server():
    Language.logHTML = addLine
    handler = MyRequestHandler
    socketserver.TCPServer.allow_reuse_address = True # needed for linux
    try:
        httpd = socketserver.TCPServer(('127.0.0.1', 8000), handler)
        httpd.serve_forever()
    except OSError as e:

        print("Error: Cuda_LSP, html log: " + str(e))

# load page
f = open(os.path.dirname(os.path.abspath(__file__)) + "/log_page.html")
htmlpage = f.read()
f.close()

# Start the HTTP server and text output threads
http_server_thread = threading.Thread(target=start_http_server)
http_server_thread.daemon = True
http_server_thread.start()
