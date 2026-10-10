# Claude Code Course: Build and Learn

Work through the lessons in order. Each lesson has:
- **Goal**: what you'll understand
- **Your task**: what you do (type it yourself)
- **Done when**: how you know you finished

Tell Claude "done with lesson N" and it will check and mark progress in PROGRESS.md.

---

## Lesson 1: Ask Claude a question
**Goal:** Start a session and get Claude to read your code.
**Your task:**
1. In Terminal, run: `cd ~/claude-learning` then `claude`
2. Type: `Explain todo.py in 3 bullet points`
**Done when:** Claude answers using what's in the file.

## Lesson 2: Run shell commands from inside Claude
**Goal:** Use `!` to run a command without leaving the session.
**Your task:** In the Claude prompt, type:
- `!python3 todo.py add "try the course"`
- `!python3 todo.py list`
**Done when:** You see your new task in the list.

## Lesson 3: Your first code change
**Goal:** See Claude edit a file and ask your permission.
**Your task:** Type: `Add a "clear" command to todo.py that removes all finished tasks. Update the usage text too.`
When Claude asks to edit, read the change and approve it.
**Done when:** `!python3 todo.py clear` removes completed tasks.

## Lesson 4: Plan mode (think before changing)
**Goal:** Get a plan without any files changing.
**Your task:**
1. Press `Shift+Tab` until you see "plan mode".
2. Type: `Plan how to handle "done 99" when task 99 doesn't exist. Don't change any files.`
3. Read the plan. Press `Shift+Tab` to go back to normal mode, then tell Claude to implement it.
**Done when:** You've read a plan and then had it applied.

## Lesson 5: Attach files and keep context small
**Goal:** Point Claude at exact files and manage the conversation size.
**Your task:**
1. Type: `Look at @todo.py and tell me the one riskiest line.`
2. Run `/cost` to see what the session has used.
3. Run `/clear`, then ask a new unrelated question.
**Done when:** You've used `@`, `/cost` and `/clear`.

## Lesson 6: Tests
**Goal:** Have Claude write and run tests.
**Your task:** Type: `Write test_todo.py using Python's built-in unittest. Cover add, done, remove and clear. Run the tests and show me the result.`
**Done when:** Tests run and pass.

## Lesson 7: CLAUDE.md (project memory)
**Goal:** Teach Claude a permanent rule for this project.
**Your task:** Type: `Add a rule to CLAUDE.md: always run the tests after changing todo.py.`
Then start a new session with `claude` and ask: `What rules do you follow in this project?`
**Done when:** The new session repeats your rule.

## Lesson 8: Permissions
**Goal:** Control what Claude may do without asking.
**Your task:**
1. Run `/permissions` and look at the current rules.
2. Run `/help` and find two commands you haven't used yet. Write down what they do.
**Done when:** You can explain the difference between "ask", "auto-accept" and "plan" modes.

## Lesson 9: Save, resume and undo
**Goal:** Pick up old work and undo mistakes.
**Your task:**
1. Exit with `/exit` (or Ctrl+D), then run `claude --continue`. Check that your last conversation is back.
2. Run `/rewind` and look at the options. Don't pick one unless you want to.
**Done when:** You've resumed a past session.

## Lesson 10: Git and commits
**Goal:** Track changes with git, with Claude writing the commit.
**Your task:**
1. Type: `!git init` then `!git add -A`
2. Type: `Write a good commit message for the current changes and commit them.`
**Done when:** `git log` shows your commit.

## Lesson 11: Your own slash command
**Goal:** Turn a repeated request into a shortcut.
**Your task:** Create the file `.claude/commands/review.md` containing:
```
Review todo.py for bugs and unclear code. List problems in order of importance. Don't change anything.
```
Start a new session and type `/review`.
**Done when:** `/review` runs your instructions.

## Lesson 12: Hooks and MCP (read and understand)
**Goal:** Know what these are, even if you don't build them yet.
**Your task:** Ask Claude: `Explain hooks and MCP servers in Claude Code with one simple example each. Don't change any files.`
**Done when:** You can explain each in one sentence.

## Lesson 13: Graduation project
**Goal:** Use everything on your own.
**Your task:** Pick one feature for todo.py (for example, due dates or priorities). Use plan mode, implement it, write tests, and commit.
**Done when:** The feature works, the tests pass and it's committed.
