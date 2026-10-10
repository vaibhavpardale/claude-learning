"""Tests for todo.py. Run with: python3 -m unittest test_todo -v"""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import todo


class TodoTests(unittest.TestCase):
    def setUp(self):
        # Use a temporary todos file so the real todos.json is never touched.
        self.tmp = tempfile.TemporaryDirectory()
        self.file = Path(self.tmp.name) / "todos.json"
        patcher = mock.patch.object(todo, "FILE", self.file)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)

    def read_todos(self):
        return json.loads(self.file.read_text())

    def test_add_creates_task(self):
        todo.main(["add", "buy", "milk"])
        self.assertEqual(self.read_todos(), [{"text": "buy milk", "done": False}])

    def test_done_marks_task_finished(self):
        todo.main(["add", "buy milk"])
        todo.main(["done", "1"])
        self.assertTrue(self.read_todos()[0]["done"])

    def test_done_rejects_bad_number(self):
        todo.main(["add", "buy milk"])
        todo.main(["done", "99"])
        self.assertFalse(self.read_todos()[0]["done"])

    def test_remove_deletes_task(self):
        todo.main(["add", "first"])
        todo.main(["add", "second"])
        todo.main(["remove", "1"])
        self.assertEqual(self.read_todos(), [{"text": "second", "done": False}])

    def test_clear_removes_only_finished_tasks(self):
        todo.main(["add", "finished"])
        todo.main(["add", "still open"])
        todo.main(["done", "1"])
        todo.main(["clear"])
        self.assertEqual(self.read_todos(), [{"text": "still open", "done": False}])


if __name__ == "__main__":
    unittest.main()
