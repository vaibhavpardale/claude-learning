"""Tests for server.py. Run with: python3 -m unittest -v"""
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from unittest import mock

import server
import todo


class TasksForViewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.file = Path(self.tmp.name) / "todos.json"
        patcher = mock.patch.object(todo, "FILE", self.file)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)

    def test_marks_only_unfinished_past_due_tasks_overdue(self):
        self.file.write_text(json.dumps([
            {"text": "late", "done": False, "due": "2026-10-01"},
            {"text": "late but done", "done": True, "due": "2026-10-01"},
            {"text": "future", "done": False, "due": "2026-10-20"},
            {"text": "no date", "done": False},
        ]))
        with mock.patch("todo.today", return_value=date(2026, 10, 10)):
            tasks = server.tasks_for_view()
        self.assertEqual([t["overdue"] for t in tasks], [True, False, False, False])

    def test_empty_list(self):
        self.assertEqual(server.tasks_for_view(), [])


class HttpTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.file = Path(self.tmp.name) / "todos.json"
        self.file.write_text(json.dumps([{"text": "buy milk", "done": False}]))
        patcher = mock.patch.object(todo, "FILE", self.file)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)

        self.httpd = server.make_server(0)
        self.addCleanup(self.httpd.server_close)
        thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(self.httpd.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def get(self, path):
        with urllib.request.urlopen(self.base + path) as response:
            return response.status, response.headers.get("Content-Type"), response.read()

    def test_root_serves_the_page(self):
        status, content_type, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertTrue(content_type.startswith("text/html"))
        self.assertIn(b"My To-Dos", body)

    def test_api_returns_tasks_as_json(self):
        status, content_type, body = self.get("/api/tasks")
        self.assertEqual(status, 200)
        self.assertEqual(content_type, "application/json")
        self.assertEqual(json.loads(body), [{"text": "buy milk", "done": False, "overdue": False}])

    def test_corrupt_file_gives_error_json(self):
        self.file.write_text("{not json")
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.get("/api/tasks")
        self.assertEqual(caught.exception.code, 500)
        self.assertIn("not valid JSON", json.loads(caught.exception.read())["error"])

    def test_unknown_path_is_404(self):
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.get("/nope")
        self.assertEqual(caught.exception.code, 404)

    def test_write_requests_are_refused(self):
        request = urllib.request.Request(self.base + "/api/tasks", data=b"{}", method="POST")
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(request)
        self.assertEqual(caught.exception.code, 501)
        self.assertEqual(json.loads(self.file.read_text()), [{"text": "buy milk", "done": False}])


if __name__ == "__main__":
    unittest.main()
