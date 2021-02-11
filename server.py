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

            html = "works: " + self.path
            with open("README.md", "r", encoding="utf8") as input_file:
                text = input_file.read()

            html = """<html>
            <head>
              <style>
                body {{ max-width: 1024px; border: 1px solid #E1E4E8; padding: 1em; border-radius: .2em; }}
                a {{ color: #0366d6; text-decoration: none; }}
                a:visited {{ color: #0366d6 }}
                html {{ color: #242926; font-family: -apple-system, system-ui, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji" }}
                code {{ border-radius: .2em; width: 100%; box-sizing: border-box; display: block; font-size: .8em; color: #24292e; background-color: #f6f8fa; padding: 0.5em; font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; }}
              </style>
            </head>
            <body>
            {markdown}
            </body>
            </html>
            """.format(markdown=markdown.markdown(text))

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
