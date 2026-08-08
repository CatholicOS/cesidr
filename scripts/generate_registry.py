#!/usr/bin/env python3
"""Generate registry/churches.md from data/churches.json.

The registry table is generated, never hand-edited — as in COECDR and CRMEDR.

Usage:
  python3 generate_registry.py [repo_root]
"""

import json
import sys
from pathlib import Path

TRADITIONS = [
    ("latin", "Latin (Western) Tradition"),
    ("byzantine", "Byzantine Tradition"),
    ("alexandrian", "Alexandrian Tradition"),
    ("antiochene", "Antiochene (West Syriac) Tradition"),
    ("east-syriac", "Chaldean (East Syriac) Tradition"),
    ("armenian", "Armenian Tradition"),
]

STATUS_LABEL = {
    "patriarchal": "patriarchal",
    "major-archiepiscopal": "major archiepiscopal",
    "metropolitan": "metropolitan *sui iuris*",
    "other": "other *sui iuris*",
    "latin": "—",
}

HEADER = """# Churches *sui iuris*

{count} canonical draft IDs for the Churches *sui iuris* of the Catholic Church: the
Latin Church and the {eastern} Eastern Catholic Churches, grouped by liturgical
tradition. **Status** is the canonical category of the Code of Canons of the Eastern
Churches — patriarchal (CCEO can. 55-150), major archiepiscopal (can. 151-154),
metropolitan *sui iuris* (can. 155-173), and other *sui iuris* (can. 174-176); the
Latin Church is governed by the 1983 Code instead and takes none of them. **Head** is
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
    data = json.load(open(repo_root / "data" / "churches.json", encoding="utf-8"))
    entries = data["entries"]

    ids = [e["id"] for e in entries]
    assert len(ids) == len(set(ids)), "duplicate ids"
    assert len(entries) == data["entry_count"], "entry_count out of step with entries"
    known = {t for t, _ in TRADITIONS}
    unknown = {e["tradition"] for e in entries} - known
    assert not unknown, f"unknown traditions: {sorted(unknown)}"

    eastern = sum(1 for e in entries if e["tradition"] != "latin")
    out = [HEADER.format(count=len(entries), eastern=eastern)]

    for key, label in TRADITIONS:
        rows = [e for e in entries if e["tradition"] == key]
        if not rows:
            continue
        out.append(f"\n## {label}\n")
        out.append("| ID | Church | Status | Head | See | Country | Notes |")
        out.append("| --- | --- | --- | --- | --- | --- | --- |")
        for e in rows:
            out.append(
                f"| `{e['id']}` | {e['name_en']} | {STATUS_LABEL[e['canonical_status']]} "
                f"| {e['head_title']} | {e['see'] or ''} | {e['country'] or ''} "
                f"| {e.get('note', '')} |"
            )

    path = repo_root / "registry" / "churches.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} churches to {path}")


if __name__ == "__main__":
    main()
