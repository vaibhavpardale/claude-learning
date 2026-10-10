"""Tiny to-do CLI. Usage: python3 todo.py add "buy milk" [--due YYYY-MM-DD] | list | done 1 | remove 1 | clear"""
import json
import os
import sys
import tempfile
from datetime import date
from pathlib import Path

FILE = Path(__file__).with_name("todos.json")


def load():
    if not FILE.exists():
        return []
    try:
        data = json.loads(FILE.read_text())
    except json.JSONDecodeError:
        # Stop instead of crashing, and leave the file alone so nothing is lost.
        sys.exit(f"{FILE.name} is not valid JSON. Fix it or delete it, then try again.")
    if not isinstance(data, list):
        sys.exit(f"{FILE.name} should contain a list of tasks. Fix it or delete it, then try again.")
    # Fill in missing fields so older or hand-edited entries don't crash the commands.
    tasks = []
    for t in data:
        task = {"text": str(t.get("text", "")), "done": bool(t.get("done", False))}
        if "due" in t:
            task["due"] = t["due"]
        tasks.append(task)
    return tasks


def save(todos):
    # Write to a temporary file first, then swap it in. If the program stops
    # mid-write, the old todos.json is still intact.
    fd, tmp_name = tempfile.mkstemp(dir=FILE.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(todos, f, indent=2)
        os.replace(tmp_name, FILE)
    except BaseException:
        os.unlink(tmp_name)
        raise


def today():
    return date.today()


def add_task(text, due=None):
    """Save a new task. Raises ValueError if the text is empty or the due date is bad."""
    text = text.strip()
    if not text:
        raise ValueError('Please give a task, e.g. add "buy milk"')
    task = {"text": text, "done": False}
    if due:
        try:
            task["due"] = date.fromisoformat(due).isoformat()
        except ValueError:
            raise ValueError(f"Invalid date '{due}'. Use YYYY-MM-DD, e.g. 2026-10-20")
    todos = load()
    todos.append(task)
    save(todos)
    return task


def main(args):
    todos = load()
    if not args or args[0] == "list":
        for i, t in enumerate(todos, 1):
            line = f"{i}. [{'x' if t['done'] else ' '}] {t['text']}"
            if "due" in t:
                line += f" (due {t['due']})"
                if not t["done"] and t["due"] < today().isoformat():
                    line += " OVERDUE"
            print(line)
        if not todos:
            print("Nothing to do!")
    elif args[0] == "add" and len(args) > 1:
        words = args[1:]
        due = None
        if "--due" in words:
            i = words.index("--due")
            if i + 1 >= len(words):
                print("Please give a date after --due, e.g. --due 2026-10-20")
                return
            due = words[i + 1]
            del words[i:i + 2]
        try:
            add_task(" ".join(words), due)
        except ValueError as error:
            print(error)
    elif args[0] == "clear":
        todos = [t for t in todos if not t["done"]]
        save(todos)
    elif args[0] in ("done", "remove") and len(args) > 1:
        try:
            i = int(args[1]) - 1
        except ValueError:
            print("Please give a task number, e.g. done 1")
            return
        if not 0 <= i < len(todos):
            print(f"No task number {args[1]}. You have {len(todos)} task(s).")
            return
        if args[0] == "done":
            todos[i]["done"] = True
        else:
            todos.pop(i)
        save(todos)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
