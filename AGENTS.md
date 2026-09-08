# Machine control-center setup

For installation or replication, read `docs/IMAC-SETUP.md` completely before
changing Discord or installing services. Finish against its acceptance checklist;
report any unverified items explicitly. Use the operator's new machine identity,
local paths, and supplied credentials. The source computer's token, IDs, session
databases, and personal files stay with that computer.

For a friend-owned MacBook using Claude Code, also read
`docs/FRIEND-MACBOOK-CLAUDE.md`. Use `--backend claude`, the friend's Discord user
ID, the new bot identity, and that person's own Claude login. Treat the category
name supplied by the operator as its permanent machine label.

For moving or continuing a project across computers, read `docs/PROJECTS.md`.
For voice or advanced workflow parity, read `docs/EXTENSIONS.md` and follow the
source documents at their pinned commits in `SOURCES.md`.

Keep runtime code in a permanent checkout on a deployment branch. The relay may
remove clean `session/<thread>` worktrees after a turn. Keep credentials, receipts,
databases and logs in the private application-data directory outside Git.

Before changing an existing deployment, inspect active sessions and the current
configuration. Restrict actions to the selected machine. Same-named channels under
another category belong to another machine. Configure receipt-backed IDs, not names.

For code changes: use an isolated worktree, add a failing behavioral test for new
logic, implement, and run the README validation commands. Review credential flows
and mutation targets before commit. Push completed work through a feature branch/PR.
The owner chooses repo visibility for each project; only this setup kit is public
by default. Publish source and templates, keeping operational data private.
