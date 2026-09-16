# Install NPCraft

The easiest installation path is the GitHub **Releases** page:

https://github.com/CesarPetrescu/npcraft/releases

## 1. Download the correct file

Under the newest tested release, expand **Assets** and download the file named like:

```text
npcraft-<version>-mc<version>.zip
```

For the current tested release this is:

```text
npcraft-0.2.0-alpha.1-mc26.3.zip
```

Do **not** download GitHub's automatically generated `Source code (zip)` or
`Source code (tar.gz)` archives. Those contain the repository layout, not the
ready-to-install datapack package.

## 2. Put the ZIP in the world

Do not extract it. Copy the downloaded ZIP to:

```text
.minecraft/saves/<WORLD>/datapacks/
```

For a dedicated server, use:

```text
<server>/<WORLD>/datapacks/
```

The final path should look similar to:

```text
.minecraft/saves/Test World/datapacks/npcraft-0.2.0-alpha.1-mc26.3.zip
```

## 3. Enable it

Open/start the world. With operator/cheat permission, run:

```mcfunction
/reload
/datapack list enabled
```

NPCraft should appear in the enabled datapacks.

Approve yourself:

```mcfunction
/function npcraft:admin/grant
```

Then open the main NPCraft controls:

```mcfunction
/trigger npcraft set 1
```

You can also press **G** when the native Quick Actions binding is available.

For the 0.2 agent/backpack panel:

```mcfunction
/trigger npcraft set 20
```

## Updating

1. Back up the entire world.
2. Stop/close the world.
3. Remove the old `npcraft-*.zip` from the world's `datapacks` directory.
4. Put the new release ZIP there.
5. Start the world and run `/reload`.
6. Keep only one NPCraft version installed at a time.

Do not downgrade a world after newer NPCraft versions have written newer persistent
agent data unless the release notes explicitly state that downgrade is supported.

## Checksums

Every automated release also attaches:

```text
npcraft-<version>-mc<version>.zip.sha256
```

You can use it to verify that the downloaded datapack ZIP matches the artifact that
was produced by CI.

## Release automation

Maintainers do not manually upload ZIP files. `.github/workflows/release.yml` runs
the repository CI, builds the deterministic installable ZIP, creates the GitHub
Release, and attaches both the ZIP and checksum.

There are two supported publication paths:

- push a tag matching `v<project.json version>`; or
- open **Actions -> Release -> Run workflow** on `main` for one-click publishing.

The workflow refuses version/tag mismatches and refuses to overwrite an existing
release.
