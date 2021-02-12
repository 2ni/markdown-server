import http.server
import socketserver
import markdown
import sys


class MyHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith(".md"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("github-markdown.css", "r", encoding="utf8") as css_file:
                css = css_file.read()

            with open(self.path[1:], "r", encoding="utf8") as input_file:
                text = input_file.read()

            html = """<html>
            <head>
              <style type="text/css">
              {css}
              </style>
            </head>
            <body>
            <div class="markdown-body">
            {markdown}
            </div>
            </body>
            </html>
            """.format(markdown=markdown.markdown(text), css=css)

            self.wfile.write(bytes(html, "utf8"))

            return
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)


PORT = 8080

# handler = http.server.SimpleHTTPRequestHandler
handler = MyHTTPHandler

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("Server started at http://localhost:" + str(PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        sys.exit(0)
