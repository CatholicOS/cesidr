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
**Head** is the title of the one who governs the Church, blank for the Russian Church,
which has no hierarch of its own, and for the Italo-Albanian, which has no single head. **Title** is the city from which the head takes his
title, and **See** is the seat of governance in the CCEO's sense: for a patriarchal or
major archiepiscopal Church the fixed residence of its head (can. 57 §3, applied by
can. 152), which need not be the city of the title; for a metropolitan Church *sui
iuris* the see in the city of the title (can. 158 §1), unless the act erecting the
Church provides otherwise, as the Hungarian Church's does. Title is blank for the other
Churches *sui iuris*, to which neither canon applies, and See is blank for the Churches
that have no single head. **Country** is the ISO 3166-1 alpha-2 code of the see or, for a
Church with no see, of the country where its faithful are. Circumscriptions of these Churches are identified in the
[CECDR](../../cecdr) with `circ:` IDs, whose `church_sui_iuris` field is a
cross-reference into this registry.

All IDs are drafts pending CETF review ([schema proposal](../docs/schema-proposal.md)).
The Annuario Pontificio is the authority for every field here and has not been
consulted; `see`, `title_city`, `country` and the notes are the least verified.
"""


def load(repo_root, name):
    return json.loads((repo_root / "data" / name).read_text(encoding="utf-8"))


def validate(data, traditions, statuses):
    """Raise ValueError describing every problem found in the seed.

    Deliberately not `assert`: Python strips assertions under -O, and when
    these guards were assertions an unresolvable `tradition` made the church
    vanish from the table while the run exited 0. Every problem is collected
    so that repairing the seed does not take one run per error.
    """
    entries = data["entries"]
    problems = []

    ids = [e["id"] for e in entries]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        problems.append(f"duplicate ids: {dupes}")

    if data.get("entry_count") != len(entries):
        problems.append(f"entry_count is {data.get('entry_count')!r} "
                        f"but there are {len(entries)} entries")

    # `tradition` and `canonical_status` are cross-references; an unresolvable
    # one would silently produce a broken registry table.
    unknown = sorted({e["tradition"] for e in entries} - set(traditions))
    if unknown:
        problems.append(f"unknown traditions: {unknown}")
    unknown = sorted({e["canonical_status"] for e in entries} - set(statuses))
    if unknown:
        problems.append(f"unknown canonical statuses: {unknown}")

    # A tradition missing from TRADITION_ORDER would drop every church in it.
    missing = sorted(set(traditions) - set(TRADITION_ORDER))
    if missing:
        problems.append(f"traditions missing from TRADITION_ORDER: {missing}")
    extra = sorted(set(TRADITION_ORDER) - set(traditions))
    if extra:
        problems.append(f"TRADITION_ORDER names traditions not in tradition.json: {extra}")

    if problems:
        raise ValueError("; ".join(problems))


def render(data, traditions, statuses):
    """Return the registry table as Markdown.

    The counts in the header are taken from the rows actually rendered, so
    the header cannot claim more churches than the table holds; a church that
    was not reached is an error, not a silent omission.
    """
    entries = data["entries"]
    sections = []
    rendered = []
    for key in TRADITION_ORDER:
        rows = [e for e in entries if e["tradition"] == key]
        if not rows:
            continue
        rendered.extend(rows)
        t = traditions[key]
        sections.append(f"\n## {t['name_en'].replace(' tradition', ' Tradition')}\n")
        sections.append(f"`{t['id']}` · *{t['name_la']}*"
                        + (f" · {t['cceo_reference']}" if t["cceo_reference"] else "")
                        + f" — {len(rows)} " + ("Church" if len(rows) == 1 else "Churches") + "\n")
        sections.append("| ID | Church | Status | Head | Title | See | Country | Notes |")
        sections.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for e in rows:
            s = statuses[e["canonical_status"]]
            label = s["name_en"] if s["cceo_category"] else "—"
            sections.append(
                f"| `{e['id']}` | {e['name_en']} | {label} "
                f"| {e['head_title'] or ''} | {e['title_city'] or ''} | {e['see'] or ''} | {e['country'] or ''} "
                f"| {e.get('note', '')} |"
            )

    unrendered = sorted({e["id"] for e in entries} - {e["id"] for e in rendered})
    if unrendered or len(rendered) != len(entries):
        raise ValueError(f"churches not rendered: {unrendered}")

    eastern = sum(1 for e in rendered if e["tradition"] != "trad:latin")
    return "\n".join([HEADER.format(count=len(rendered), eastern=eastern)] + sections) + "\n"


def main():
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    data = load(repo_root, "churches.json")
    traditions = {t["id"]: t for t in load(repo_root, "tradition.json")["entries"]}
    statuses = {s["id"]: s for s in load(repo_root, "canonical_status.json")["entries"]}

    try:
        validate(data, traditions, statuses)
        text = render(data, traditions, statuses)
    except ValueError as exc:
        sys.exit(f"generate_registry.py: {exc}")

    path = repo_root / "registry" / "churches.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    # render() has already refused to return unless every entry was rendered.
    print(f"Wrote {len(data['entries'])} churches to {path}")


if __name__ == "__main__":
    main()
