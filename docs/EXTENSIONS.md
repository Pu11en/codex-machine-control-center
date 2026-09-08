# Reproduce the newer voice and planning features

The base installer reproduces coding chat, project selection, worker channels,
reference and voice-channel layout. To match the newer source-machine features,
the Mac agent must also install these two components and verify them on macOS.
Use the immutable commits in SOURCES.md, not a moving branch or the source
machine's private runtime directories.

## Voice transcription

Check out the voice source commit into a permanent Mac directory. Read its
`extensions/voice_transcripts/README.md`, `VERIFICATION.md`, `.env.example`,
`package.json`, and `ops/voice-transcripts.service` before adapting the service.

Use Node 22.12+ and `npm ci --omit=dev` in that extension. Create a separate Python
environment and install its pinned requirements; preload the `base.en`
faster-whisper model. Check Intel vs Apple Silicon dependency support on the actual
Mac. Start with CPU recognition, matching the source setup's local recognition
contract. Verify model loading offline before attempting Discord audio.

Use the newly generated provisioning receipt for voice and transcript channel IDs.
The channels already exist: do not invoke the source channel-creation helper again.
Write a private voice env file with those IDs, a Mac data path, and the absolute
Python executable. Point VOICE_BRIDGE_ENV_FILE at this Mac's `relay.env` and
VOICE_CONFIG_FILE at the private voice env file. The companion intentionally uses
the **same new machine bot identity** as the relay, with no message handler and
no slash-command registration. Do not use the Lenovo token or channels.

Translate its systemd launcher to a macOS LaunchAgent with an absolute Node
executable and source working directory. Preserve private umask, failure restart,
separate logs and a singleton lock. The Linux `/usr/bin/flock` command is not a
stock macOS dependency: provide an equivalent BSD `fcntl.flock` lock wrapper or
verified local lock utility, passing command arguments without a shell. Test that
a duplicate companion cannot start. Scope the lock to this bot and machine.

Run the source Node tests and dependency checks. Keep the original disclosure,
pause/resume, local persistence, retention, offline inference, speaker attribution
and credential isolation behavior. Do not bypass failed disclosure to record.
The first Discord recording should be part of Drew's actual join/speak/leave test.
Report dependency or audio failures honestly; empty voice channels are not parity.

## Feature planning and worker coordination

Check out the coordinator source commit into a separate permanent Mac directory.
Read `extensions/feature_workflow/SOURCES.md`, its skill and required references,
and `coordinator.py --help`. That adapter uses the relay's existing REST API and
does not require replacing its core Cogs.

Install the pinned OpenSpec CLI and the two specific coordination skills named in
SOURCES.md into the Mac's discovered Codex skills location. Install only the
selected workflow; Portable Planner is retired. Preserve existing project plans.
Install the adapter's skill and executable with Mac paths; do not copy WSL absolute
paths from an existing generated skill. Use this Mac's API URL and **its workers
channel ID** for every dispatch. Preserve the approved-plan revision, committed
foundation, isolated worktrees, bounded worker queue and integration checks.

Replace the runbook's transient `systemd-run --user` watcher with a scoped Mac
LaunchAgent or equivalent supervised process outside the manager's turn. Use a
unique job label and private state directory per run. Run `watch` as a one-shot
watcher that exits after handoff, as the coordinator expects; do not blindly restart
it forever with KeepAlive. Ending an idle manager turn must allow queued workers
to acquire execution slots. Keep source and state outside disposable worktrees.

Run the source coordinator tests. With Drew's setup-trial authorization, prove two
small planned tasks, separate worker threads and branches, returned results, and
integration. Reuse an authorized test repo, or obtain its visibility choice before
creating a new remote. A planning discussion alone is not a coordination test.

The source workflow was still receiving improvements during the snapshot. The pin
is a reproducible baseline, not a claim that every future upstream change has been
included. Report which commit was installed and which acceptance checks passed.
