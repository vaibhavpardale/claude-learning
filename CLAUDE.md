# Project notes for Claude
- Tiny Python to-do CLI (`todo.py`), data stored in `todos.json`.
- Keep it dependency-free (standard library only).
- Run with: `python3 todo.py list`
- Always run the tests after changing todo.py (`python3 -m unittest -v`).

## How to run the course (LESSONS.md + PROGRESS.md)
- This folder is a guided course. The learner is a beginner; explain in plain words.
- When the learner asks for the next lesson or says "start", show only the current lesson from LESSONS.md (from PROGRESS.md), and stop. Don't do the learner's task for them.
- When the learner says "done with lesson N": check the "Done when" condition (run commands or look at files). If it's met, tick the box in PROGRESS.md, update "Current lesson" and "Completed", and give brief feedback. If not met, explain what's missing and give a hint, not the answer.
- Show progress as a short summary when asked.
