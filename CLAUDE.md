# CLAUDE.md

Digital Cafe. Django + SQLite, server-rendered templates, plain CSS.
No JS framework, no build step. Project `digitalcafe`, single app `core`.

## Ground rules
- Scope every change to fit one Conventional Commit. Tell me how you scoped it.
  If it cannot be scoped cleanly, stop and ask before proceeding.
- Prefixes: feat: fix: chore: build: docs: refactor:
- Do not add a dependency without asking me first.
- Never write application code during a study or plan step.
- Before executing a plan, tell me what you need from me that you cannot
  create yourself: seed data, config values, credentials.

## Workflow
Every feature follows: study -> plan -> execute plan -> rendezvous -> sync docs.

- "study": run `date +%s` first for a real timestamp. Write a reviewable doc to
  doc/study/{timestamp}_{topic}.md covering feasibility, tradeoffs, and scope.
  Write to no other file. Commit under docs:.
- "plan": write a checklist to doc/plan/{timestamp}_{topic}.md, structured as an
  editable task board. Commit under docs:. If you need input from me, add an
  "OPEN QUESTIONS" section near the top.
- "execute plan": create a new git branch first. Execute the plan, editing the
  plan doc to track progress. Continue until done or blocked.
- "rendezvous": confirm the app runs, merge the branch to main, update docs.
- "sync docs": make doc/wiki/ reflect the current codebase.
