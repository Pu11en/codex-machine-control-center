# Friend MacBook + Claude Code handoff

## What Drew gives the friend

Send the friend the public repository URL and the prompt below. Drew creates a new
Discord application/bot for this MacBook, invites it to the existing server, and
provides these four values to the friend's local setup agent:

- new bot token;
- existing Discord server ID;
- new bot application/user ID;
- friend's permanent Discord user ID.

Drew also chooses the visible category name, for example **ALEX MACBOOK CLAUDE
CONTROL CENTER**. One bot application and category belong to this one MacBook.
The friend authenticates Claude Code interactively with their own Claude account;
there is no Claude API key to copy from Drew when using a Pro/Max subscription.

Giving the new bot Discord Administrator permission is sufficient for channel
creation, though the installer only needs the narrower permissions listed in
IMAC-SETUP.md. The bot's category is private to the configured friend and bot by
default. Discord server administrators, including Drew, retain access.

## Paste this into the AI running on the friend's MacBook

Replace the two bracketed labels before sending. Credentials can be supplied when
the agent requests the four missing values.

> Set up this MacBook as [FRIEND NAME]'s independent Claude Code control center in
> Drew's existing Discord server. Use the public repository
> https://github.com/Pu11en/codex-machine-control-center. Clone it into a permanent
> local checkout, read AGENTS.md, docs/IMAC-SETUP.md, and
> docs/FRIEND-MACBOOK-CLAUDE.md completely, and finish their acceptance checklist.
> Use `--backend claude` and create the category “[FRIEND NAME] MACBOOK CLAUDE
> CONTROL CENTER.” I will provide this new bot's token, the server ID, the new bot
> ID, and my Discord user ID. Store runtime credentials outside Git with private
> permissions. Install Claude Code from Anthropic's official instructions, and let
> me complete the interactive Claude App Pro/Max login on this Mac. Verify
> `claude auth status` and `claude doctor`. Configure Ebi Agent Chat Relay, the
> project picker, workers channel, cheat sheet, macOS LaunchAgent, and the optional
> voice/workflow extensions exactly as the runbook specifies. Preserve every
> existing category and bot. Restrict this bot's normal messages and slash commands
> to its own control-center/workers channels and their threads. Prove with hostname,
> working directory, local file, restart, `/cdnew`, worker, and small GitHub
> clone/change/push checks that work actually runs on this MacBook. Report links
> and local paths without exposing any credentials.

## What the friend should expect to do

The agent can install and configure most of the system. The friend completes the
Claude browser login and any macOS authorization prompts. A real Discord voice
transcription test, if wanted, needs a person to join and speak. The Mac must be
awake and the user logged in for its LaunchAgent-hosted bot to remain available.

The friend can then use their category exactly as Drew uses the Lenovo category:
write in `#control-center`, use `/cdnew` for local projects, and continue work in
the created project thread. Their Claude subscription usage belongs to their own
Claude account.

## Sharing projects with Drew

Use GitHub as the shared history. Either person pushes a branch and gives the other
person the repo URL, branch, and commit. The other computer clones or fetches it,
installs its own dependencies, and uses its own bot's `/cdnew` to open that local
folder. Private repositories work when both GitHub accounts have access. Parallel
changes belong on separate branches and should meet through a pull request.

Secrets, ignored data, databases, dependencies, and AI conversation history do not
travel through Git. Read PROJECTS.md for the exact handoff rules.

Claude Code's official setup supports signing in with a Claude App Pro or Max plan:
https://docs.anthropic.com/en/docs/claude-code/getting-started
