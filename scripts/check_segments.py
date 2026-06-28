#!/usr/bin/env python3
"""Walidator spójności: narracja per język ↔ timeline flipbooka.

Dla każdego odcinka w episodes/ sprawdza, że KAŻDY plik narration/<lang>.md
zawiera dokładnie te same segmenty [Sxx] co timeline.json (ten sam timeline
flipbooka dla wszystkich języków). Raportuje też segmenty nieprzetłumaczone
(placeholdery TODO / puste).

Użycie:
    python3 scripts/check_segments.py
Kod wyjścia 1 = niespójność segmentów (brakujące lub nadmiarowe [Sxx]).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPISODES = ROOT / "episodes"
SEG_HEADER = re.compile(r"^##\s*\[(S\d+)\]", re.MULTILINE)
TODO = re.compile(r"<!--\s*TODO", re.IGNORECASE)


def check_episode(ep_dir: Path) -> bool:
    timeline_path = ep_dir / "timeline.json"
    if not timeline_path.exists():
        print(f"  ⚠️  brak timeline.json w {ep_dir.name} — pomijam")
        return True

    timeline = json.loads(timeline_path.read_text(encoding="utf-8"))
    timeline_ids = [s["id"] for s in timeline.get("segments", [])]
    timeline_set = set(timeline_ids)
    print(f"\n📺 {ep_dir.name}: timeline = {len(timeline_ids)} segmentów {timeline_ids}")

    ok = True
    narration_dir = ep_dir / "narration"
    for md in sorted(narration_dir.glob("*.md")) if narration_dir.exists() else []:
        text = md.read_text(encoding="utf-8")
        found = SEG_HEADER.findall(text)
        found_set = set(found)
        missing = [i for i in timeline_ids if i not in found_set]
        extra = [i for i in found if i not in timeline_set]
        todo = len(TODO.findall(text))

        status = "✅"
        if missing or extra:
            status, ok = "❌", False
        print(f"  {status} {md.name}: {len(found)} segm."
              f"{'  BRAK: ' + str(missing) if missing else ''}"
              f"{'  NADMIAR: ' + str(extra) if extra else ''}"
              f"{f'  ({todo} do tłumaczenia)' if todo else ''}")
    return ok


def main() -> int:
    if not EPISODES.exists():
        print("Brak katalogu episodes/")
        return 1
    all_ok = True
    for ep_dir in sorted(p for p in EPISODES.iterdir() if p.is_dir()):
        all_ok &= check_episode(ep_dir)
    print("\n" + ("✅ Segmenty spójne z timeline." if all_ok
                  else "❌ Niespójność — popraw nagłówki [Sxx]."))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
