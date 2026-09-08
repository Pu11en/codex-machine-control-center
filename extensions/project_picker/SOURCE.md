# Project picker

Original source: cKreymborg/claude-code-discord-bridge commit
780510047b2317d5ba8a45a6c60d963341209568, MIT (LICENSE included).
The current-machine adapter and original behavioral tests were imported into this
kit with formatting changes only. See ../../SOURCES.md for the adaptation summary.

`machine_scope.py` is this kit's additional channel restriction for slash commands.
The chat counterpart uses the relay's existing `CCDB_MENTION_ANYWHERE=false` and
explicit `CCDB_CHANNEL_IDS` settings. `/cdnew` suggests folders under
`CCDB_PROJECT_ROOTS`; that list is navigation, not a filesystem sandbox.
Discord autocomplete values are limited to 100 characters. Longer absolute paths
are omitted from suggestions; enter the path directly in `/cdnew` instead.
