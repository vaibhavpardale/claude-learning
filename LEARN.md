# Claude Code in 10 minutes

## Start
    cd ~/claude-learning
    claude              # opens an interactive session in this folder

## Everyday use: just talk to it
- "Explain what todo.py does"
- "Add a `clear` command that removes all finished tasks"
- "Handle the error when I do `done 99`"
- "Write tests for todo.py and run them"
Claude reads files, proposes edits, and asks permission before changing things.

## Slash commands (type inside a session)
| Command    | What it does |
|------------|--------------|
| /help      | List all commands |
| /model     | Switch model (cost control!) |
| /cost      | See tokens/cost used this session |
| /clear     | Wipe conversation, start fresh (saves tokens) |
| /compact   | Summarize long chat to shrink context |
| /init      | Auto-generate a CLAUDE.md for a project |
| /resume    | Reopen a past session |
| /rewind    | Undo recent changes/turns |

## Handy shortcuts
- `Shift+Tab` cycles permission modes (ask / auto-accept edits / plan mode)
- `Esc` stops Claude mid-answer; `Esc Esc` rewinds
- `@todo.py` in a prompt attaches that file
- `!ls` runs a shell command directly

## Key concepts
- **CLAUDE.md**: notes Claude reads every session (your project's rules).
- **Plan mode**: Claude researches and proposes a plan, changes nothing.
- **Permissions**: you approve file edits/commands; allowlist safe ones.
- **Skills / hooks / MCP**: later topics: reusable workflows, automatic actions, external tools.

## Save tokens
1. Use Sonnet for most work; Haiku for simple tasks; Opus/Fable only for hard problems.
2. `/clear` between unrelated tasks.
3. Be specific ("in todo.py, add X") instead of vague.
4. Check `/cost` regularly.
