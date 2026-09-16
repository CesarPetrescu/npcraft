# Contributing

Use Python 3.13 and Java 25. No Python package installation is required.

```sh
python tools/generate_agent.py --check
python tools/validate.py
python -m unittest discover -s tests -v
python tools/build.py
python tools/server_test.py --accept-eula --reports reports/legacy
python tools/agent_test.py --accept-eula --reports reports/agent
```

Review the Minecraft EULA before passing the final flag. The runtime suite creates
a disposable loopback-only world; do not rewrite it to use a developer's real save.

Keep functions in `datapack/data/npcraft/function/` (singular). Preserve namespace
boundaries, finite command budgets, ID+UUID ownership checks and transaction order.
World edits belong only in the validated work action, never navigation. Preserve
full tool components. Do not reclaim “missing” controllers without proving they
are deleted rather than unloaded. See architecture for shared scratch-state rules.

Each behavior change needs a regression fixture. Update scope, limitations and
CHANGELOG alongside player-visible changes. Record manual client tests separately.
Generated ZIPs, server binaries, worlds, credentials and logs are never committed.

To release, bump project.json, pack metadata and displayed version consistently;
run all checks and the manual checklist; create `v<version>`. The release workflow
refuses a mismatched tag and publishes ZIP/checksum only after CI. It does not
create tags or silently upgrade Minecraft. Use prerelease version suffixes until
the production acceptance criteria are genuinely met.

Agent mcfunctions are generated from tools/generate_agent.py. Regenerate and commit
both sources and outputs; generator drift is a CI failure. The two graphical
client suites are part of the Required gate, not optional screenshot decoration.
Do not weaken assertions to publish a failed run. Record exact evidence provenance.
