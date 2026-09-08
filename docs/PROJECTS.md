# Working on one project from two computers

## GitHub is the handoff

Each computer has a separate folder, dependency installation, environment file,
Git working tree and running development server. GitHub carries committed source
history between them. A private repo works as well as a public one when both
machines are authenticated. Publishing every project publicly is unnecessary.

Before sending a project, inspect `git status`, `git remote -v`, and the current
branch. Review the files being committed. Push to the existing authorized GitHub
repo or create one with the visibility the user chose. Return the exact repo URL,
branch and commit; a default-branch clone does not include unmerged feature work.

On the receiving computer, inspect whether the destination folder already exists.
For a new checkout, use argument-safe Git calls equivalent to:

```sh
git clone -- https://github.com/OWNER/PROJECT.git /absolute/local/project/path
git -C /absolute/local/project/path fetch origin
git -C /absolute/local/project/path switch --track origin/FEATURE_BRANCH
```

The final command is only for a branch that does not exist locally. For the default
branch or an existing tracking branch, inspect and switch to the existing branch.
If there is already a folder, inspect it and its remote instead of cloning over it.

Install dependencies with the project's own lockfiles and build instructions on
the receiving OS. Keep both checkouts attached to the **same repository**. Do not
create another GitHub repo just because a second computer now has a clone.

## The Discord steps

In the receiving computer's `#control-center`, a normal message creates a new
conversation thread. Ask it to clone the repo into its local projects folder and
check out the named branch. Then use that computer's `/cdnew` to pick the folder
and open the project conversation. Continue work by replying in that thread.
`/cdnew` chooses an existing folder; it does not clone a repo itself.

To return later, reopen the same project thread or use `/search`. A new `/cdnew`
starts fresh conversation context even when it points at the same folder.

The GitHub URL is the cross-machine identifier. A phrase such as “the repository
from the other category” is not enough: each relay has its own local session and
folder database. Supply the branch and commit too when the wanted version is not
already the default branch's tip.

## Receiving subsequent changes

Inspect status and branch, then fetch. If the local branch is clean and only behind
its remote, `git pull --ff-only` is appropriate. If histories diverged, merge/rebase
deliberately and resolve conflicts. Preserve local uncommitted changes; do not reset
the working tree to make a pull succeed. A commit pushed to a feature branch is not
on `main` until integrated. Fetch/select that branch or merge its PR first.

For simultaneous development, use distinct branches such as `imac/feature-name`
and `lenovo/other-feature`. Agree on owned files for overlapping work and integrate
through PRs. An unpushed local branch exists only on its own computer.

## What Git does not transfer

Secrets and `.env`, ignored datasets, databases, media caches, dependencies,
running processes, and Discord/CLI conversation history remain local. Transfer
needed data separately within the user's authorized scope. Recreate configuration
from templates and install dependencies on the target OS; Windows or Linux binary
packages cannot simply be reused on a Mac.

The relay's localhost lounge/claims coordinate only sessions using that one relay.
Separate machines do not share that database or a global worktree lock. GitHub
branches/PRs and explicit task ownership are the cross-computer coordination layer.
Each relay's limit of three active sessions is independent.
