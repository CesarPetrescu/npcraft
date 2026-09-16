"""Apply observed vanilla regressions to the canonical generator; temporary bootstrap."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'tools/generate_agent.py'
s=p.read_text()
s=s.replace('execute unless function npcraft:action/check with entity @s data.agent.target run', 'execute unless function npcraft:action/valid run')
if "fn('action/valid'" not in s:
    s=s.replace("    fn('action/mine',", "    fn('action/valid', 'return run function npcraft:action/check with entity @s data.agent.target')\n    fn('action/mine',")
p.write_text(s)
