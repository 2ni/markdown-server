# Markdown server

This is a simple web application converting markdown files to HTML and responding  with text/html.

## Installation
Clone the project to markdown-server. Then run:
```
$ cd markdown-server
$ pyenv virtualenv 3.9.0 pyenv-markdownserver
$ pyenv local pyenv-markdownserver
(pyenv-markdownserver) $ pip install -r requirements.txt
```

## Run
```
(pyenv-markdownserver) $ python server.py
Server started at http://localhost:8080
```

Navigate to the url and open this markdown file.
