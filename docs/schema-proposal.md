# CESIDR schema proposal (draft for committee review)

## Identifier scheme

```
esi:<slug>
```

- **`esi:`** — namespace prefix for *ecclesia sui iuris* (placeholder, like `circ:`
  in the CECDR and `mr:` in the CRMEDR, pending a committee decision on prefixes
  across the registries).
- **`<slug>`** — the distinguishing element of the Church's name, ASCII-folded,
  lowercase, hyphenated, with the generic words *Church*, *Catholic* and *Greek
  Catholic* stripped: `ukrainian`, `maronite`, `syro-malabar`, `italo-albanian`.
  The type is an attribute, not part of the identity — the same principle as
  CECDR rule 1.

### Rules

1. **Continuity with CECDR.** The slugs are deliberately identical to the values
   CECDR's `church_sui_iuris` field already carries (`latin`, `ukrainian`,
   `maronite`, `syro-malabar`), so that field becomes a cross-reference into this
   registry without rewriting a single value.
2. **Canonical status is an attribute, not identity.** A Church raised from
   metropolitan *sui iuris* to major archiepiscopal, or from an exarchate to an
   eparchial Church, keeps its ID. The Hungarian Church did not become a different
   Church in 2015, nor the Slovak in 2008.
3. **Erection and separation.** A Church erected by separation from another takes a
   new ID; the parent keeps its own. `esi:eritrean` was erected in 2015 out of the
   Ethiopian Church, and `esi:ethiopian` is unchanged by it.
4. **Suppression.** Should a Church *sui iuris* ever be suppressed or absorbed, its
   ID is retained and flagged, never deleted — historical data must remain
   referenceable, as in CECDR rule 3.
5. **Rites are not Churches.** A rite is a patrimony (CCEO can. 28); a Church *sui
   iuris* is a community joined by a hierarchy (can. 27). Several Churches share the
   Byzantine rite, and this registry identifies the Churches, not the rites. The
   liturgical tradition is carried as the `tradition` attribute.

## Entry shape

```json
{
  "id": "esi:melkite",
  "name_en": "Melkite Greek Catholic Church",
  "tradition": "trad:byzantine",
  "canonical_status": "cstat:patriarchal",
  "head_title": "patriarch",
  "see": "Damascus",
  "country": "SY"
}
```

Neither `tradition` nor `canonical_status` is a free string: both are
cross-references into companion registries in this repository, following the same
convention CECDR uses for `"type": "ctype:diocese"` and the family uses for `rp:`
and `mr:` references.

- **`data/tradition.json`** (`trad:<slug>`) — the six liturgical traditions, each
  with its Latin name and, for the five of CCEO can. 28 §2, that citation. The Latin
  tradition is flagged `"in_cceo_can_28": false`, the CCEO governing the Eastern
  Churches only.
- **`data/canonical_status.json`** (`cstat:<slug>`) — the four CCEO categories, each
  with its Latin name, governing canons, the title of its head and its governing
  body, plus `cstat:latin` flagged `"cceo_category": false`.

`scripts/generate_registry.py` asserts that every `tradition` and every
`canonical_status` resolves, so an unresolvable cross-reference fails the build.

Planned beyond the seed: `name_la` (the Annuario's Latin nomenclature), `erected`
(date, with the act that erected it), `members` (with the Annuario year it is drawn
from), `circumscription_count`, and `historical_names`.

## Seed and its limits

- **The Annuario Pontificio has not been consulted.** It is the authority for every
  field in this registry and is not published online. The canonical categories come
  from the CCEO itself; the rest was assembled from Catholic-Hierarchy and GCatholic,
  which the CDCF treats as verification aids and not as authorities.
- **`see` and `country` are the least verified fields.** Several are the residence of
  the head rather than the titular see — the Syriac patriarchal see is Antioch while
  the patriarch resides in Beirut, and the same distinction affects the Melkite,
  Maronite, Chaldean and Armenian entries.
- **Three Churches have no single head**, and carry `"see": null`: the Belarusian
  (served under an apostolic visitator), the Russian (no functioning hierarchy since
  the Soviet period), and the Italo-Albanian (three circumscriptions, none
  metropolitan over the others).
- **`esi:ruthenian` is canonically irregular.** The metropolitan see is Pittsburgh,
  but the Church also comprises the Eparchy of Mukachevo and the Apostolic Exarchate
  of the Czech Republic, both immediately subject to the Holy See rather than to the
  metropolitan. Catholic-Hierarchy indexes "Byzantine" and "Ruthenian" as separate
  entries for this reason; this registry treats them as one Church.

## Open questions for the committee

1. The namespace prefix (`esi:`) and its coordination with the other registries'
   prefixes.
2. The name and slug of `esi:croatian-serbian`. Sources disagree: "Greek Catholic
   Church of Croatia and Serbia", "Croatian Greek Catholic Church", and
   Catholic-Hierarchy's bare "Križevci". Since 2018 it comprises two eparchies in two
   nations, which tells against both national forms.
3. Whether `tradition` should distinguish the Antiochene (West Syriac) and Chaldean
   (East Syriac) traditions as this seed does, or follow the sources that group both
   as Syriac.
4. Whether the Latin Church's `canonical_status` should be its own value, as seeded,
   or `patriarchal` — the title Patriarch of the West was restored to the Annuario in
   2024, after having been dropped in 2006.
5. Whether to carry membership figures at all. They are the most-requested field and
   the least stable, and are only meaningful when stamped with the Annuario year they
   are drawn from.
6. Whether the CECDR's `church_sui_iuris` field should be migrated to carry the full
   `esi:` ID (`"church_sui_iuris": "esi:latin"`) or keep the bare slug and resolve it
   by convention. The former is explicit and matches how CECDR now carries
   `"type": "ctype:diocese"`; the latter leaves 2,935 entries untouched.
