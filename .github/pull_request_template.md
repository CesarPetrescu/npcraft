## Change
Describe player-visible behavior and the reason for the change.

## Scope and safety
- [ ] Update the implemented/planned distinction in the scope and README.
- [ ] Navigation does not break/place blocks or force-load chunks.
- [ ] Revalidate ownership, reach, plot bounds and item transfers at mutation time.
- [ ] No unreviewed Minecraft version/pack-format compatibility claims.

## Evidence
- [ ] `python tools/validate.py`
- [ ] `python -m unittest discover -s tests -v`
- [ ] Vanilla integration job passes; attach failure logs when it does not.
- [ ] Record visual/multiplayer playtesting separately; headless tests are not visual playtests.
