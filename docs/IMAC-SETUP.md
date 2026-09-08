# Mac setup runbook (iMac or MacBook)

Execute on the target Mac. The intended outcome is a second independent computer
behind the same familiar Discord workflow. Default category: **IMAC CODEX CONTROL
CENTER**. The existing machine's category is **LENOVO CODEX CONTROL CENTER**.

## 1. Establish the target

Inspect `uname -s`, `uname -m`, the logged-in user's home, available disk space,
existing bot services, the selected AI CLI/version/login, `gh auth status`,
and `uv --version`. Install missing prerequisites through their official channels.
Use Python 3.12 or 3.13; `uv sync` can obtain a compatible Python if needed.
Use native macOS paths and architecture, with the user's projects under
`~/Developer`. Preserve an existing macOS CODEX_HOME; WSL/Windows paths do not apply.
Keep the setup repo in a permanent checkout, not a disposable session worktree.

The selected AI sign-in and GitHub sign-in happen on the Mac. Login prompts need
the account owner. For Claude Code, run `claude` interactively and choose the
Claude App subscription login that belongs to this Mac's user, then verify it with
`claude auth status` and `claude doctor` before starting the relay.
Never copy the Lenovo account's auth files, databases, `.venv`, or installed
executables. A shared GitHub account is fine; machine authentication is separate.

Completion: the agent can run the selected AI and GitHub CLI as the Mac user, and has a
permanent local checkout of this repo.

## 2. Identify the new bot

Ask Drew only for missing values in `.env.example`: new bot token, new application
ID, existing server ID, and authorized human user ID. Accept supplied credentials
through the session's available secure handling and store them in a private env
file (mode 0600) outside the repo. Keep token values out of command arguments,
diagnostic output, Git commits, screenshots, and public documents.

In the new application's Discord Developer Portal Bot settings, enable **Message
Content Intent**. Invite this application to the existing server with `bot` and
`applications.commands`. Request Manage Channels for provisioning, plus View
Channels, Send Messages, Send Messages in Threads, Create Public/Private Threads,
Manage Threads, Read Message History, Add Reactions, Manage Messages, Embed Links,
Attach Files, Use Application Commands, and Connect for voice. The machine bot does
not need Administrator for its coding workflow. Category permissions grant the
new bot and operator access; Discord Administrators can still see them.

The old bot has Administrator, which bypasses visibility restrictions. Message
routing, not hidden categories, enforces the computer selection. The Lenovo bot
was inspected with explicit channels and `CCDB_MENTION_ANYWHERE=false`. Preserve
those settings. Both bots have slash commands with similar names: select the
command belonging to the intended bot in Discord's command picker.

Completion: the new bot is a member of the intended server and its token resolves
to the supplied EXPECTED_BOT_ID.

## 3. Preview and provision

From the permanent kit checkout:

```sh
uv sync --locked --extra relay
uv run python -m machine_control setup --env /absolute/path/to/credentials.env
uv run python -m machine_control setup --env /absolute/path/to/credentials.env --apply
```

For Claude Code, pass `--backend claude` and the chosen `--category` to both
commands. For Codex, the default backend remains `codex`.

Before apply, inspect the preview for the correct bot and target. The existing
authorization to set up this Mac covers the apply step; do not add a redundant
permission prompt. `--apply` is refused on non-macOS hosts. Optional `--projects`,
`--data`, and `--category` select local paths and the new category name.

The private provisioning receipt records identity and every channel as it is
created. Preserve it through updates and retries. Name collision without a matching
receipt stops setup for inspection. Do not delete or repurpose the Lenovo channels.
Runtime configuration is written on first setup only; reruns preserve operator
changes. If credentials or paths change later, update the private runtime env file
explicitly rather than assuming the input file overwrites it.

Completion: one new category and five channels exist; recorded IDs belong to that
category; bot identity and local working directory match the Mac.

## 4. Start the Mac service

The installer emits a LaunchAgent plist under the private data directory.
Inspect it, then copy it into the logged-in user's `~/Library/LaunchAgents/` as
`com.ai.machine-control-center.plist`. Use `plutil -lint` on it and verify that
every executable, env, log and working-directory path exists.

Load it in the user's GUI domain using `launchctl bootstrap gui/USER_UID
/absolute/path/to/com.ai.machine-control-center.plist`, substituting the real
numeric UID from `id -u`. Inspect `launchctl print
gui/USER_UID/com.ai.machine-control-center` and the generated log paths. If a
service with that label already exists, inspect it before updating; manage only
this Mac's matching instance. Use the local `man launchctl` for installed syntax.

This LaunchAgent starts when the user logs in and relaunches a failed bot process.
It does not run while the Mac is asleep, powered off, or logged out. For unattended
availability, configure the Mac's power/login behavior with Drew. Test after a
logout/login or reboot as appropriate; do not call it boot-verified before that.

The loopback API defaults to port 9876, which may independently be used on both
computers. If that port is occupied on the Mac, select an unused local port in
the runtime env before starting. Keep API_HOST at 127.0.0.1. Source and data paths
must remain permanent after the setup agent's conversation ends.

Completion: the machine bot connects, registers `/cdnew`, and reports healthy via its
own local `/api/health`. Logs show both custom Cogs loaded, with no skipped Cog.

## 5. Finish feature parity

Read `EXTENSIONS.md` for voice and the feature-workflow coordinator. Install their
pinned source into permanent Mac checkouts, adapt OS-specific service management,
and run the listed tests. Populate the new `#cheat-sheet` with the human workflow
in README and PROJECTS, using the **new** channel IDs and local Mac project paths.
Post/update one guide, suppress mentions, and record its message IDs privately to
avoid duplicates. It is a reference channel; only control-center and workers are
configured for coding chat.

Voice channels alone do not prove transcription. A CLI skill alone does not prove
parallel worker coordination. Report base chat readiness and each extension's
verification separately.

## 6. Acceptance checklist

- [ ] Bot identity, server, category and selected AI backend match the new machine.
- [ ] Lenovo category, channel IDs, bot configuration and running sessions preserved.
- [ ] Normal messages in this Mac's control-center create threads; replies resume them.
- [ ] A thread's `hostname`, `pwd`, and a tiny created/read local file prove execution
      on the Mac. Ask for this bounded check; reading a model's claim is insufficient.
- [ ] `/cdnew` autocomplete shows Mac project folders and binds the selected folder.
- [ ] A message or this bot's slash command in another machine's category cannot start
      a run here. Other machine bots stay silent in this Mac's channels.
- [ ] An explicitly requested small worker appears in this Mac's workers channel and
      completes on the Mac. Its link and result return to the coordinating thread.
- [ ] A disposable GitHub project is cloned locally, changed on a feature branch,
      tested and pushed; its branch and commit are visible on GitHub. Use an existing
      authorized test repo, or obtain its creation/visibility choice from Drew.
- [ ] Voice: human joins, speaks, leaves; speaker-attributed Markdown updates in the
      this Mac's transcript channel and local output persists. Pause/resume is verified.
- [ ] Advanced workflow: approved plan → two isolated workers → verified integration
      works on the Mac, if reproducing the advanced workflow.
- [ ] Bot recovers after supervised restart and user login; source/state persist.
- [ ] Final handoff gives category/channel links, project directory, service/log
      locations, and any unverified check. Keep secrets out of the handoff.
