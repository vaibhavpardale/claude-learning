"""Browser view of your to-do list. Run: python3 server.py, then open http://127.0.0.1:8000"""
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
            self.send_tasks()
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/api/tasks":
            self.send_error(404)
            return
        # Browsers only send JSON here after a permission check, so a random
        # web page can't add tasks through this server.
        if self.headers.get("Content-Type") != "application/json":
            self.send_json({"error": "Send the task as JSON."}, status=415)
            return
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            if not isinstance(data, dict):
                raise ValueError("Send an object with a text field and an optional due field.")
            todo.add_task(str(data.get("text", "")), data.get("due") or None)
        except ValueError as error:
            self.send_json({"error": str(error)}, status=400)
            return
        except SystemExit as error:
            # todo.load() stops with a message when todos.json is bad.
            self.send_json({"error": str(error.code)}, status=500)
            return
        self.send_tasks()

    def send_tasks(self):
        try:
            tasks = tasks_for_view()
        except SystemExit as error:
            self.send_json({"error": str(error.code)}, status=500)
            return
        self.send_json(tasks)

    def send_json(self, data, status=200):
        self.send_body(json.dumps(data).encode(), "application/json", status)

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
