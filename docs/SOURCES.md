# Primary technical references

Checked September 16, 2026. Implementation is original; these are API/version
references, not sources of copied add-on or pathfinding code.

- Mojang, Java 26.3 release: release date September 15, 2026, datapack 121.0, command changes.
  https://www.minecraft.net/en-us/article/minecraft-java-edition-26-3
- Mojang, Java 26.1 release: Java 25 runtime requirement.
  https://www.minecraft.net/en-us/article/minecraft-java-edition-26-1
- Mojang, Java 1.21.9 release: mannequin fields, living-entity behavior and min/max pack format metadata.
  https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21-9
- Mojang, Java 1.21.6 release: native dialogs, quick actions, pause-menu tags and command actions.
  https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21-6
- Mojang's launcher version manifest, used by the test harness to resolve the exact target and verify server downloads.
  https://piston-meta.mojang.com/mc/game/version_manifest_v2.json
- Minecraft EULA, relevant to running the optional vanilla integration test server.
  https://aka.ms/MinecraftEULA

The release-note command/schema claims are validated further by the live vanilla
integration suite. Documentation is not a substitute for testing expanded macros,
actual item transfers, client dialogs or multiplayer behavior.
