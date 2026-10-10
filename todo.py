"""Tiny to-do CLI. Usage: python3 todo.py add "buy milk" | list | done 1 | remove 1 | clear"""
import json
import sys
from pathlib import Path

FILE = Path(__file__).with_name("todos.json")


def load():
    return json.loads(FILE.read_text()) if FILE.exists() else []


def save(todos):
    FILE.write_text(json.dumps(todos, indent=2))


def main(args):
    todos = load()
    if not args or args[0] == "list":
        for i, t in enumerate(todos, 1):
            print(f"{i}. [{'x' if t['done'] else ' '}] {t['text']}")
        if not todos:
            print("Nothing to do!")
    elif args[0] == "add" and len(args) > 1:
        todos.append({"text": " ".join(args[1:]), "done": False})
        save(todos)
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
