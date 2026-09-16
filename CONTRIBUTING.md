# Contributing

Use Python 3.13, Java 25, and exact Minecraft Java 26.3. Core build tools use the
standard library. Read AGENTS.md and docs/IRON_SURVIVAL_RIVAL.md first.

```sh
python tools/validate.py
python -m unittest discover -s tests -v
python tools/build.py
python tools/server_test.py --accept-eula
python tools/v03_adversarial_tests.py --accept-eula --reports reports/adversarial
python tools/reliability_tests.py --accept-eula --reports reports/reliability
python tools/soak_test.py --accept-eula --agents 1,4,8,16 --ticks 6000
```

Review the EULA before using runtime flags. GUI dependencies and all three real-client
commands are in `.github/workflows/client-playtest.yml`. Use disposable worlds.
Never point a fixture harness at a real saved world or a public multiplayer server.

Keep actual source and evidence changes reviewable in a feature PR. Tests must cover
negative cases and conservation, not merely parse the pack. Do not copy paid
Marketplace assets or license-incompatible third-party code. New schemas require
migrations preserving old backpack/timber/ownership records.

No navigation block mutations or production force-loading. Action/transfer commits
must revalidate current state. Do not leave global scratch live across a yield or
nest interleaved agent execution. Consent, owner UUID and persistent approval are
separate concerns; deny by default and allow consent revocation from anywhere.

Update version metadata and compatibility evidence together. Releases require all
CI layers and tag/version agreement; adding a workflow does not create a release
or branch protection. Do not commit server JARs, worlds, account tokens or properties.
