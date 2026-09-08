# AI Machine Control Center

Give each computer and person an independent Discord bot and control-center category.
Conversations run either Codex or Claude Code on that computer against its local folders.

This is an install kit and agent handoff for the Lenovo → iMac setup. It uses the
same pinned Ebi Agent Chat Relay version and project picker as the source machine.
It creates an independent category with `cheat-sheet`, `control-center`, `workers`,
`🎙️ Auto Transcripts`, and `voice-transcripts`. Voice and advanced planning have
separate installation steps; creating their channels does not activate them.

## Give this to the iMac agent

> Set up this computer using https://github.com/Pu11en/codex-machine-control-center.
> Read AGENTS.md and docs/IMAC-SETUP.md and follow their verification checklist.
> Use the new iMac Discord bot and create IMAC CODEX CONTROL CENTER in my existing
> server. Keep projects local to this Mac. I will supply the new bot credentials
> and Discord IDs here. Preserve the Lenovo category and bot. Reproduce the project
> picker, workers, cheat sheet, and voice/workflow features described in the guide.
> Tell me which steps need my login or an actual Discord microphone test.

The iMac agent needs to run **on the iMac** (or have authorized remote shell access
to it). Giving a Windows-hosted agent a new token does not move execution to the Mac.

## Give this to a friend's Claude Code agent

Use the ready-to-paste prompt in [FRIEND-MACBOOK-CLAUDE.md](docs/FRIEND-MACBOOK-CLAUDE.md).
It creates a new category with a new bot on the friend's MacBook, signs Claude Code
into the friend's own Pro/Max subscription, and can authorize both the friend and Drew.
It does not share Drew's AI login, bot token, project files, or session history.

## Quick start for the agent

Use a permanent checkout under the Mac user's `~/Developer` directory. Install uv,
Git, GitHub CLI, and the selected AI CLI; complete that AI's login and GitHub sign-in
on the Mac. Then run:

```sh
uv sync --locked --extra relay
uv run python -m machine_control setup --env /absolute/path/to/credentials.env
# Inspect the identity and target category in that preview, then:
uv run python -m machine_control setup --env /absolute/path/to/credentials.env --apply
```

For Claude Code, add `--backend claude` and choose a distinct category with
`--category "FRIEND NAME MACBOOK CLAUDE CONTROL CENTER"` on both setup commands.

The credentials file has four required fields plus an optional additional-user list;
`.env.example` is the template. The setup
stores channel IDs, local configuration, and the generated LaunchAgent outside Git
under `~/Library/Application Support/AIMachineControl/`. Follow
[the Mac guide](docs/IMAC-SETUP.md) to start the service and verify it in Discord.

The installer creates only its own resources. It refuses a mismatched bot identity,
an existing category without a receipt, and a receipt belonging to a different
machine. Repeating a successful setup reuses its recorded channels. If Discord
accepted a create request but the receipt could not be saved, inspect the existing
resource and repair the private receipt before retrying. It never deletes channels.

## Moving a project between computers

GitHub holds the shared history; each computer has its own checkout.
Repos can be **private or public**. Each machine needs GitHub access to private repos.

1. In the Lenovo project thread: “Commit and push this project's current work to
   GitHub, keeping secrets and local data out. Give me the repo URL and the branch
   containing the work.” Create a repo only if one does not already exist; choose
   visibility explicitly.
2. In the iMac's `#control-center`: “Clone REPO_URL into my local projects folder.
   Check out BRANCH, install dependencies for this Mac, and tell me when it is ready
   to open with /cdnew.”
3. Use the **iMac bot's** `/cdnew`, select that local folder, and continue in its new
   thread. “Build and test [change] here, then commit and push the work to GitHub.”
4. Back on Lenovo: “Fetch the iMac changes. Check my local work, then bring the
   agreed branch up to date without discarding changes, install any changed
   dependencies, and run the relevant checks.”

If both machines work at the same time, use different feature branches and PRs.
Fetching is safe; pulling/merging requires checking local changes first. There is
no automatic file sync, and a push only updates the branch that was pushed.
`main` includes that work after the PR merges.

See [PROJECTS.md](docs/PROJECTS.md) for the precise Git operations, local files that
do not move, and cross-machine worktree precautions.

## Administrator on join

The kit also includes a one-time role assignment helper:

```sh
uv run python -m machine_control admin-once --env /private/current-bot.env \
  --guild GUILD_ID --user EXACT_USER_ID --state /private/admin-grant.json
```

It prepares a `Server Admin` role, waits if that exact account has not joined,
verifies the assigned role, and records completion. Run it on a timer while pending.
After success, later manual role removal is respected; it does not continually
re-grant access. The bot requires Administrator and a higher role position to
provision this role. This command is separate from installing a machine bot.

Server Administrator does not override the relay's owner-only computer access.
Sharing machine execution requires an explicit additional user-access configuration.

## Validation

```sh
uv sync --locked --extra relay
uv run pytest -q --basetemp=/tmp/codex-control-tests
uv run ruff check machine_control tests extensions/project_picker
uv run ruff format --check machine_control tests extensions/project_picker
uv run pyright machine_control
```

The automated suite checks provisioning, one-time authorization, macOS service
configuration, scoped slash commands, and the imported folder picker. Live Mac
acceptance requires the real computer and new bot; see the guide's checklist.
Dependency versions are frozen in `uv.lock`; upstream code provenance is in
[SOURCES.md](SOURCES.md).
