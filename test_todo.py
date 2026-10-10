"""Tests for todo.py. Run with: python3 -m unittest test_todo -v"""
import contextlib
import io
import json
import tempfile
import unittest
from datetime import date
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

    def test_corrupt_file_stops_without_overwriting(self):
        self.file.write_text("{not json")
        with self.assertRaises(SystemExit):
            todo.main(["add", "new"])
        self.assertEqual(self.file.read_text(), "{not json")

    def test_empty_file_stops_with_message(self):
        self.file.write_text("")
        with self.assertRaises(SystemExit):
            todo.main(["list"])

    def test_entries_missing_fields_do_not_crash(self):
        self.file.write_text(json.dumps([{"text": "x"}]))
        todo.main(["list"])
        todo.main(["done", "1"])
        self.assertEqual(self.read_todos(), [{"text": "x", "done": True}])

    def test_save_leaves_no_temp_files(self):
        todo.main(["add", "buy milk"])
        self.assertEqual([p.name for p in Path(self.tmp.name).iterdir()], ["todos.json"])

    def run_list(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            todo.main(["list"])
        return out.getvalue()

    def test_add_with_due_date(self):
        todo.main(["add", "buy", "milk", "--due", "2026-10-20"])
        self.assertEqual(self.read_todos(), [{"text": "buy milk", "done": False, "due": "2026-10-20"}])

    def test_due_flag_can_come_before_text(self):
        todo.main(["add", "--due", "2026-10-20", "buy", "milk"])
        self.assertEqual(self.read_todos(), [{"text": "buy milk", "done": False, "due": "2026-10-20"}])

    def test_invalid_due_date_saves_nothing(self):
        todo.main(["add", "buy milk", "--due", "tomorrow"])
        self.assertFalse(self.file.exists())

    def test_due_flag_without_value_saves_nothing(self):
        todo.main(["add", "buy milk", "--due"])
        self.assertFalse(self.file.exists())

    def test_add_without_text_saves_nothing(self):
        todo.main(["add", "--due", "2026-10-20"])
        self.assertFalse(self.file.exists())

    def test_list_shows_due_date(self):
        self.file.write_text(json.dumps([{"text": "buy milk", "done": False, "due": "2026-10-20"}]))
        with mock.patch("todo.today", return_value=date(2026, 10, 10)):
            self.assertEqual(self.run_list(), "1. [ ] buy milk (due 2026-10-20)\n")

    def test_list_marks_overdue_unfinished_task(self):
        self.file.write_text(json.dumps([{"text": "pay rent", "done": False, "due": "2026-10-01"}]))
        with mock.patch("todo.today", return_value=date(2026, 10, 10)):
            self.assertIn("OVERDUE", self.run_list())

    def test_list_does_not_mark_finished_task_overdue(self):
        self.file.write_text(json.dumps([{"text": "pay rent", "done": True, "due": "2026-10-01"}]))
        with mock.patch("todo.today", return_value=date(2026, 10, 10)):
            self.assertNotIn("OVERDUE", self.run_list())

    def test_list_does_not_mark_future_task_overdue(self):
        self.file.write_text(json.dumps([{"text": "pay rent", "done": False, "due": "2026-10-20"}]))
        with mock.patch("todo.today", return_value=date(2026, 10, 10)):
            self.assertNotIn("OVERDUE", self.run_list())

    def test_due_date_survives_save_and_load(self):
        todo.main(["add", "pay rent", "--due", "2026-10-01"])
        todo.main(["add", "buy milk"])
        todo.main(["done", "2"])
        self.assertEqual(self.read_todos(), [
            {"text": "pay rent", "done": False, "due": "2026-10-01"},
            {"text": "buy milk", "done": True},
        ])

    def test_failed_save_keeps_old_file(self):
        todo.main(["add", "keep me"])
        with mock.patch("todo.json.dump", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                todo.main(["add", "lost"])
        self.assertEqual(self.read_todos(), [{"text": "keep me", "done": False}])
        self.assertEqual([p.name for p in Path(self.tmp.name).iterdir()], ["todos.json"])


if __name__ == "__main__":
    unittest.main()
