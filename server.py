import http.server
import socketserver
import markdown
import sys
import argparse


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a markdown server on localhost", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--port", type=int, default=8080, help="set the port which the local server is listening to")

    args = parser.parse_args()

    # handler = http.server.SimpleHTTPRequestHandler
    handler = MyHTTPHandler

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", args.port), handler) as httpd:
        print("Server started at http://localhost:" + str(args.port))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            sys.exit(0)
