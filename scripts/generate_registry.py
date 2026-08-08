#!/usr/bin/env python3
"""Generate registry/churches.md from data/churches.json.

The registry table is generated, never hand-edited — as in COECDR and CRMEDR.

Usage:
  python3 generate_registry.py [repo_root]
"""

import json
import sys
from pathlib import Path

# Display order of the traditions: the Latin Church first, then the five of
# CCEO can. 28 §2 in the order that canon names them.
TRADITION_ORDER = [
    "trad:latin",
    "trad:alexandrian",
    "trad:antiochene",
    "trad:armenian",
    "trad:east-syriac",
    "trad:byzantine",
]

HEADER = """# Churches *sui iuris*

{count} canonical draft IDs for the Churches *sui iuris* of the Catholic Church: the
Latin Church and the {eastern} Eastern Catholic Churches, grouped by liturgical
tradition, in the order CCEO can. 28 §2 names them. **Status** is the canonical
category of the Code of Canons of the Eastern Churches, a `cstat:` cross-reference
into [`data/canonical_status.json`](../data/canonical_status.json) — patriarchal
(CCEO can. 55-150), major archiepiscopal (can. 151-154), metropolitan *sui iuris*
(can. 155-173), and other *sui iuris* (can. 174-176); the Latin Church is governed by
the 1983 Code instead and takes none of them. The tradition headings are likewise
`trad:` cross-references into [`data/tradition.json`](../data/tradition.json).
**Head** is
the title of the one who governs the Church; **See** is the seat of that governance,
blank for the Churches that have no single head. `Country` is the ISO 3166-1 alpha-2
code of the see. Circumscriptions of these Churches are identified in the
[CECDR](../../cecdr) with `circ:` IDs, whose `church_sui_iuris` field is a
cross-reference into this registry.

All IDs are drafts pending CETF review ([schema proposal](../docs/schema-proposal.md)).
The Annuario Pontificio is the authority for every field here and has not been
consulted; `see`, `country` and the notes are the least verified.
"""


def main():
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    def load(name):
        return json.load(open(repo_root / "data" / name, encoding="utf-8"))

    data = load("churches.json")
    entries = data["entries"]
    traditions = {t["id"]: t for t in load("tradition.json")["entries"]}
    statuses = {s["id"]: s for s in load("canonical_status.json")["entries"]}

    ids = [e["id"] for e in entries]
    assert len(ids) == len(set(ids)), "duplicate ids"
    assert len(entries) == data["entry_count"], "entry_count out of step with entries"
    # `tradition` and `canonical_status` are cross-references; an unresolvable
    # one would silently produce a broken registry table.
    unknown = {e["tradition"] for e in entries} - set(traditions)
    assert not unknown, f"unknown traditions: {sorted(unknown)}"
    unknown = {e["canonical_status"] for e in entries} - set(statuses)
    assert not unknown, f"unknown canonical statuses: {sorted(unknown)}"
    assert set(TRADITION_ORDER) == set(traditions), "TRADITION_ORDER out of step with tradition.json"

    eastern = sum(1 for e in entries if e["tradition"] != "trad:latin")
    out = [HEADER.format(count=len(entries), eastern=eastern)]

    for key in TRADITION_ORDER:
        rows = [e for e in entries if e["tradition"] == key]
        if not rows:
            continue
        t = traditions[key]
        out.append(f"\n## {t['name_en'].replace(' tradition', ' Tradition')}\n")
        out.append(f"`{t['id']}` · *{t['name_la']}*"
                   + (f" · {t['cceo_reference']}" if t["cceo_reference"] else "")
                   + f" — {len(rows)} " + ("Church" if len(rows) == 1 else "Churches") + "\n")
        out.append("| ID | Church | Status | Head | See | Country | Notes |")
        out.append("| --- | --- | --- | --- | --- | --- | --- |")
        for e in rows:
            s = statuses[e["canonical_status"]]
            label = s["name_en"] if s["cceo_category"] else "—"
            out.append(
                f"| `{e['id']}` | {e['name_en']} | {label} "
                f"| {e['head_title']} | {e['see'] or ''} | {e['country'] or ''} "
                f"| {e.get('note', '')} |"
            )

    path = repo_root / "registry" / "churches.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} churches to {path}")


if __name__ == "__main__":
    main()
