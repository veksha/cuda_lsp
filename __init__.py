from .lsp import Command
from .language import Language

import threading
import http.server
import socketserver
import html
import re

htmlpage = """
<!DOCTYPE html>
<html>
<head>
  <title>LSP monitor</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
  <script>
    $(document).ready(function() {
      $(".spoiler-content").click(function() {
        $("#dynamic-text").toggleClass("running");
      });
    
      // Function to fetch and update data
      function fetchData() {
        $.ajax({
          url: "/get",
          method: "GET",
          success: function(response) {
            // Add the received text to the DOM
            var element = $(".running")
            element.html(response);
          },
          error: function() {
            console.log("Error occurred while fetching data.");
          }
        });
      }

      // Call fetchData every second
      setInterval(fetchData, 1000);
      
      const spoilerTitle = document.querySelector('.spoiler-title');
      const spoilerContent = document.querySelector('.spoiler-content');
      
      spoilerTitle.addEventListener('click', function() {
        spoilerContent.style.display = spoilerContent.style.display === 'block' ? 'none' : 'block';
      });
    });
  </script>
  <style>
    .spoiler-content {
      display: none;
      cursor: pointer;
      padding-bottom:15px
    }
    .spoiler-content:hover {
      text-decoration: underline;
    }
    
    .spoiler-title {
      cursor: pointer;
      padding-bottom: 5px;
    }
    
    .spoiler-title:hover {
      text-decoration: underline;
    }
    .nowrap {
        white-space: pre;
    }
  </style>
</head>
<body>
  <h4 style="margin: 0px">CudaText LSP monitor</h4>
  <div class="spoiler">
    <div class="spoiler-title">
      menu
    </div>
    <div class="spoiler-content">
      pause
    </div>
  </div>
  <div id="dynamic-text" class="running nowrap">Loading...</div>
</body>
</html>
"""

lines = []

def addLine(prefix, line):
    global lines
    line = re.sub(r"^Content-Length:.+?\\r\\n\\r\\n", r"", line)
    line = re.sub(r"Content-Length:.+?\\r\\n\\r\\n{", r"\n\t\t\t     {", line)
    line = prefix + html.escape(line)
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
        self.wfile.write(text)

    
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
    httpd = socketserver.TCPServer(('127.0.0.1', 8000), handler)
    httpd.serve_forever()

# Start the HTTP server and text output threads
http_server_thread = threading.Thread(target=start_http_server)
http_server_thread.daemon = True
http_server_thread.start()
