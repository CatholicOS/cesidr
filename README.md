# CESIDR

The home of the **Common Ecclesiae Sui Iuris Data Repository**, curated by the **Catholic Engineering Task Force** of the [Catholic Digital Commons Foundation](https://github.com/CatholicOS).

## What is CESIDR?

The Common Ecclesiae Sui Iuris Data Repository (CESIDR) provides a canonicalized list of identifiers for the **24 Churches *sui iuris*** of the Catholic Church: the Latin Church and the 23 Eastern Catholic Churches, across the six liturgical traditions — Latin, Byzantine, Alexandrian, Antiochene (West Syriac), Chaldean (East Syriac), and Armenian.

A Church *sui iuris* is, in the words of CCEO can. 27, "a community of the Christian faithful joined together by a hierarchy according to the norm of law which the supreme authority of the Church expressly or tacitly recognizes as *sui iuris*". Each is in full communion with the Roman Pontiff while retaining its own hierarchy, liturgical tradition, theological heritage, and canonical discipline. They are not rites: a rite is a liturgical, theological, spiritual and disciplinary patrimony (CCEO can. 28), and several Churches *sui iuris* share one.

## Why?

The Church *sui iuris* is an attribute of almost every other Catholic entity a registry needs to identify:

- **ecclesiastical circumscriptions**, whose `church_sui_iuris` field in the [CECDR](https://github.com/CatholicOS/cecdr) becomes a cross-reference into this registry — an eparchy belongs to a Church *sui iuris*, and where a Latin see and an Eastern eparchy share a city the identifier is qualified by it;
- **liturgical books and calendars**, which are proper to a Church *sui iuris* rather than to the Catholic Church as a whole;
- **clergy, faithful and sacramental records**, since ascription to a Church *sui iuris* is a canonical status of persons (CCEO can. 29-38), not merely a preference.

## The identifier scheme (draft)

```
esi:<slug>
```

Examples: `esi:latin`, `esi:ukrainian`, `esi:maronite`, `esi:syro-malabar`, `esi:italo-albanian`. The slugs are deliberately identical to the values CECDR's `church_sui_iuris` field already carries, so that field can become a cross-reference without rewriting its data. The full proposal is in [docs/schema-proposal.md](docs/schema-proposal.md). **All IDs are drafts pending committee review.**

## Repository contents

- [`data/churches.json`](data/churches.json) — the seed registry: 24 Churches *sui iuris*, each with its draft canonical ID, English name, liturgical tradition, canonical status under the CCEO, the title of the one who governs it, and its see.
- [`data/tradition.json`](data/tradition.json) — the liturgical traditions (`trad:byzantine`, `trad:alexandrian`, …), each with its Latin name and its CCEO can. 28 §2 citation. Each Church's `tradition` field is a cross-reference into this file.
- [`data/canonical_status.json`](data/canonical_status.json) — the CCEO categories (`cstat:patriarchal`, `cstat:major-archiepiscopal`, …), each with its Latin name, governing canons, the title of its head and its governing body. Each Church's `canonical_status` field is a cross-reference into this file.
- [`registry/churches.md`](registry/churches.md) — the human-readable table, grouped by liturgical tradition. Generated, never hand-edited.
- [`docs/schema-proposal.md`](docs/schema-proposal.md) — the proposed schema and the open questions for the committee.
- [`scripts/generate_registry.py`](scripts/generate_registry.py) — regenerates the registry table from the seed.

## Canonical status

The Code of Canons of the Eastern Churches sorts the Eastern Churches *sui iuris* into four categories, and this registry records which each belongs to:

| status | CCEO | count |
| --- | --- | --- |
| patriarchal | can. 55-150 | 6 |
| major archiepiscopal | can. 151-154 | 4 |
| metropolitan *sui iuris* | can. 155-173 | 5 |
| other *sui iuris* | can. 174-176 | 8 |

The Latin Church is governed by the 1983 Code of Canon Law rather than the CCEO and takes none of these categories; it carries its own `canonical_status` value.

## Sources and verification

**The Annuario Pontificio is the authority for the content of this registry, and it has not been consulted** — it is not published online. The seed was assembled from the Code of Canons of the Eastern Churches for the canonical categories, and from [Catholic-Hierarchy](https://www.catholic-hierarchy.org/rite/) and [GCatholic](https://gcatholic.org/) as verification aids. Their compiled data is not incorporated wholesale.

Every field is therefore draft. The `see`, `country` and `erected` values are the least verified, and the naming of the Greek Catholic Church of Croatia and Serbia is itself unsettled between sources. Corrections against the Annuario are the most useful contribution this repository can receive.

## License

The data and documentation in this repository are licensed under the [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/) (CC BY-NC-ND 4.0). See [`LICENSE`](LICENSE) for the full legal code.

The source code in [`scripts/`](scripts/) is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). See [`scripts/LICENSE`](scripts/LICENSE).
