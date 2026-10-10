"""Read-only browser view of your to-do list. Run: python3 server.py, then open http://127.0.0.1:8000"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import todo

PAGE = Path(__file__).with_name("index.html")


def tasks_for_view():
    today = todo.today().isoformat()
    tasks = []
    for t in todo.load():
        task = dict(t)
        task["overdue"] = "due" in t and not t["done"] and t["due"] < today
        tasks.append(task)
    return tasks


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_body(PAGE.read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/tasks":
            try:
                body = json.dumps(tasks_for_view()).encode()
            except SystemExit as error:
                # todo.load() stops with a message when todos.json is bad.
                body = json.dumps({"error": str(error.code)}).encode()
                self.send_body(body, "application/json", status=500)
                return
            self.send_body(body, "application/json")
        else:
            self.send_error(404)

    def send_body(self, body, content_type, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def make_server(port=8000):
    return HTTPServer(("127.0.0.1", port), Handler)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = make_server(port)
    print(f"Open http://127.0.0.1:{port} in your browser. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
