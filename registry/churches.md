# Churches *sui iuris*

24 canonical draft IDs for the Churches *sui iuris* of the Catholic Church: the
Latin Church and the 23 Eastern Catholic Churches, grouped by liturgical
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


## Latin (Western) Tradition

`trad:latin` · *traditio Latina* — 1 Church

| ID | Church | Status | Head | Title | See | Country | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `esi:latin` | Latin Church | — | Roman Pontiff | Rome | Rome | VA | The Western Church, comprising the great majority of the faithful. Governed by the 1983 Code of Canon Law rather than the CCEO, and headed by the Roman Pontiff directly; `canonical_status` is therefore its own value rather than one of the four CCEO categories. The title Patriarch of the West, dropped from the Annuario Pontificio in 2006, was restored in 2024. |

## Alexandrian Tradition

`trad:alexandrian` · *traditio Alexandrina* · CCEO can. 28 §2 — 3 Churches

| ID | Church | Status | Head | Title | See | Country | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `esi:coptic` | Coptic Catholic Church | patriarchal Church | patriarch | Alexandria | Cairo | EG | Patriarchate of Alexandria of the Copts, erected 1824 and restored 1895. |
| `esi:eritrean` | Eritrean Catholic Church | metropolitan Church sui iuris | metropolitan | Asmara | Asmara | ER | Erected as a metropolitan Church sui iuris on 19 January 2015, separating from the Ethiopian Catholic Church. The most recently erected Church sui iuris. |
| `esi:ethiopian` | Ethiopian Catholic Church | metropolitan Church sui iuris | metropolitan | Addis Ababa | Addis Ababa | ET | Uses the Ge'ez liturgical tradition. |

## Antiochene (West Syriac) Tradition

`trad:antiochene` · *traditio Antiochena* · CCEO can. 28 §2 — 3 Churches

| ID | Church | Status | Head | Title | See | Country | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `esi:maronite` | Maronite Church | patriarchal Church | patriarch | Antioch | Bkerké | LB | Patriarchate of Antioch of the Maronites. The only Eastern Catholic Church with no counterpart outside communion with Rome. |
| `esi:syriac` | Syriac Catholic Church | patriarchal Church | patriarch | Antioch | Beirut | LB | Patriarchate of Antioch of the Syriacs. The patriarch takes his title from Antioch; his see, the fixed residence of CCEO can. 57 §3, is Beirut. |
| `esi:syro-malankara` | Syro-Malankara Catholic Church | major archiepiscopal Church | major archbishop | Trivandrum | Trivandrum | IN | Entered full communion in 1930 through the Reunion Movement led by Mar Ivanios. Raised to a major archiepiscopal Church in 2005. |

## Armenian Tradition

`trad:armenian` · *traditio Armena* · CCEO can. 28 §2 — 1 Church

| ID | Church | Status | Head | Title | See | Country | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `esi:armenian` | Armenian Catholic Church | patriarchal Church | patriarch | Cilicia | Beirut | LB | Patriarchate of Cilicia of the Armenians. The Armenian is the only liturgical tradition represented by a single Church sui iuris. |

## Chaldean (East Syriac) Tradition

`trad:east-syriac` · *traditio Chaldaea* · CCEO can. 28 §2 — 2 Churches

| ID | Church | Status | Head | Title | See | Country | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `esi:chaldean` | Chaldean Catholic Church | patriarchal Church | patriarch | Baghdad | Baghdad | IQ | Patriarchate of Baghdad of the Chaldeans since 19 February 2022, when the Holy See approved the Synod's request to change the title from Patriarchate of Babylon of the Chaldeans. |
| `esi:syro-malabar` | Syro-Malabar Catholic Church | major archiepiscopal Church | major archbishop | Ernakulam-Angamaly | Ernakulam-Angamaly | IN | Traces its origin to the mission of the Apostle Thomas. Raised to a major archiepiscopal Church in 1992. |

## Byzantine Tradition

`trad:byzantine` · *traditio Constantinopolitana* · CCEO can. 28 §2 — 14 Churches

| ID | Church | Status | Head | Title | See | Country | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `esi:albanian` | Albanian Greek Catholic Church | other Church sui iuris | apostolic administrator |  | Vlorë | AL | Governed by the Apostolic Administration of Southern Albania. |
| `esi:belarusian` | Belarusian Greek Catholic Church | other Church sui iuris | apostolic visitator |  |  | BY | Descends from the Union of Brest (1596). Has no eparchial hierarchy of its own; the faithful are served under an apostolic visitator. |
| `esi:bulgarian` | Bulgarian Greek Catholic Church | other Church sui iuris | eparchial bishop |  | Sofia | BG | Originates in the appointment in 1861 of Joseph Sokolsky as archbishop of the Bulgarian Catholics of the Byzantine rite. Comprises the Eparchy of Saint John XXIII of Sofia, raised from an apostolic exarchate erected in 1926. That exarchate replaced three earlier jurisdictions, all suppressed into it: the apostolic vicariates of Thessalonica (Macedonia) and Adrianople (Thrace), both erected in 1883, and the apostolic administration at Constantinople. |
| `esi:croatian-serbian` | Greek Catholic Church of Croatia and Serbia | other Church sui iuris | eparchial bishop |  | Križevci | HR | Comprises the Eparchy of Križevci (erected 1777, covering Croatia, Slovenia and Bosnia and Herzegovina) and the Eparchy of Saint Nicholas of Ruski Krstur (Serbia, raised from an apostolic exarchate on 6 December 2018). Naming is unsettled: also styled the Croatian Greek Catholic Church, and indexed by Catholic-Hierarchy simply as Križevci. |
| `esi:greek` | Greek Byzantine Catholic Church | other Church sui iuris | apostolic exarch |  | Athens | GR | Comprises the Apostolic Exarchate of Greece and the Apostolic Exarchate of Istanbul; a very small body. |
| `esi:hungarian` | Hungarian Greek Catholic Church | metropolitan Church sui iuris | metropolitan | Hajdúdorog | Debrecen | HU | Raised to a metropolitan Church sui iuris in 2015, the Metropolia of Hajdúdorog. CCEO can. 158 §1 places the see of a metropolitan Church sui iuris in the city from which the metropolitan takes his title, but the apostolic constitution of 19 March 2015 that erected it set its principal see at Debrecen ("cum sede principe in urbe Debrecensi"), so the title is Hajdúdorog and the see Debrecen. |
| `esi:italo-albanian` | Italo-Albanian Catholic Church | other Church sui iuris |  |  |  | IT | Never formally out of communion with Rome. Has three circumscriptions and no single head: the Eparchies of Lungro and of Piana degli Albanesi, and the Exarchic Monastery of Santa Maria di Grottaferrata, exarchic since 1937 and immediately subject to the Congregation for the Oriental Churches. |
| `esi:macedonian` | Macedonian Greek Catholic Church | other Church sui iuris | eparchial bishop |  | Strumica | MK | Comprises the Eparchy of the Assumption of the Blessed Virgin Mary in Strumica-Skopje, raised from an apostolic exarchate. |
| `esi:melkite` | Melkite Greek Catholic Church | patriarchal Church | patriarch | Antioch | Damascus | SY | Patriarchate of Antioch and all the East, of Alexandria and of Jerusalem. The largest Byzantine-tradition Catholic body in the Middle East. |
| `esi:romanian` | Romanian Greek Catholic Church | major archiepiscopal Church | major archbishop | Făgăraș and Alba Iulia | Blaj | RO | Major Archiepiscopal Church of Făgăraș and Alba Iulia, the title the major archbishop bears; Blaj has been the residence of its heads since 1737 and is the see in the sense of CCEO can. 57 §3 (applied by can. 152). Suppressed under the communist regime in 1948 and restored in 1990. |
| `esi:russian` | Russian Greek Catholic Church | other Church sui iuris |  |  |  | RU | Has no hierarch of its own and so no head: its Apostolic Exarchates of Russia (1917) and Harbin (1928) have had no exarch since the Soviet period. Since 2004 the Latin bishop of the Transfiguration at Novosibirsk has been the ordinary for Byzantine-rite Catholics in Russia, a pastoral oversight that does not make him the hierarch presiding over the Church in the sense of CCEO can. 174. Communities are dispersed. |
| `esi:ruthenian` | Ruthenian Greek Catholic Church | metropolitan Church sui iuris | metropolitan | Pittsburgh | Pittsburgh | US | Also styled the Byzantine Catholic Church in America. Canonically unusual: the metropolitan see is the Metropolia of Pittsburgh, but the Church also includes the Eparchy of Mukachevo (Ukraine) and the Apostolic Exarchate of the Czech Republic, both immediately subject to the Holy See rather than to Pittsburgh. |
| `esi:slovak` | Slovak Greek Catholic Church | metropolitan Church sui iuris | metropolitan | Prešov | Prešov | SK | Raised to a metropolitan Church sui iuris in 2008. |
| `esi:ukrainian` | Ukrainian Greek Catholic Church | major archiepiscopal Church | major archbishop | Kyiv-Halyč | Kyiv | UA | Major Archiepiscopal Church of Kyiv-Halyč; the see was transferred from Lviv to Kyiv in 2005. In 2000 the largest of the Eastern Catholic Churches, with a little over 5,000,000 faithful against about 3,300,000 Syro-Malabar (Dizionario Enciclopedico dell'Oriente Cristiano, Rome 2000, pp. 122, 701, 786); the present ranking awaits a dated Annuario figure — see open question 5 in docs/schema-proposal.md. |
