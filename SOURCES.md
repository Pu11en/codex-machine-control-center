# Sources and replication boundary

Source machine inspected September 7, 2026. This public kit contains no source
machine credentials, server IDs, conversation contents, session databases or projects.

| Component | Pinned source |
| --- | --- |
| Ebi Agent Chat Relay 4.0.26 | [ebibibi/ebi-agent-chat-relay, 7fc303c33cfa97e9c17966227dd3c85d787d32d0](https://github.com/ebibibi/ebi-agent-chat-relay/tree/7fc303c33cfa97e9c17966227dd3c85d787d32d0) |
| Project picker original | [cKreymborg/claude-code-discord-bridge, 780510047b2317d5ba8a45a6c60d963341209568](https://github.com/cKreymborg/claude-code-discord-bridge/tree/780510047b2317d5ba8a45a6c60d963341209568) |
| Voice companion | [Pu11en/ebi-agent-chat-relay, e581115aa14e4169a52353bd533c76f2d7548521](https://github.com/Pu11en/ebi-agent-chat-relay/tree/e581115aa14e4169a52353bd533c76f2d7548521/extensions/voice_transcripts) |
| Feature coordinator | [Pu11en/ebi-agent-chat-relay, 42a68fcd602c898acf828096bc1ddbef0194651d](https://github.com/Pu11en/ebi-agent-chat-relay/tree/42a68fcd602c898acf828096bc1ddbef0194651d/extensions/feature_workflow) |

The imported project picker combines its original two modules into a supported
custom Cog. Source-machine adaptations preserve chat authorization, autocomplete
authorization, normalized paths, bounded suggestions, thread locking, deferred
responses, and requester membership. Its MIT license and 29 tests are included.
This kit adds `machine_scope.py` to restrict slash commands by configured channel.

The relay is installed as an immutable Git dependency, with transitive dependency
versions recorded in `uv.lock`. Voice and coordinator sources are referenced at
immutable public commits; their macOS services require the adaptation described
in `docs/EXTENSIONS.md`. They are not silently enabled by the base installer.

Primary references:

- [Discord permissions and role hierarchy](https://docs.discord.com/developers/topics/permissions)
- [Discord guild channels and member role endpoints](https://docs.discord.com/developers/resources/guild)
- [Discord Message Content intent](https://docs.discord.com/developers/events/gateway)
- [Apple LaunchAgents](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html)
- [Apple launchctl guidance](https://support.apple.com/guide/terminal/script-management-with-launchd-apdc6c1077b-5d5d-4d35-9c19-60f2397b2369/mac)
