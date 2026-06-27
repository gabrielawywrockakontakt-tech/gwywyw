# Janusz biznesu

Projekt serii odcinków „Janusz biznesu". Animacja (**flipbook**) jest renderowana raz na
**timeline** o stałych ujęciach/timecode'ach. Narracja (lektor) jest **osobna dla każdego języka**
i nakładana na **ten sam timeline**.

> **Cel tego repo:** trzymać tekst narracji tak, żeby nowy język = nowy plik tłumaczenia
> na **istniejącym timeline flipbooka** — bez ruszania animacji.

---

## Jak to działa (timeline ↔ narracja)

```
flipbook (animacja, render raz)
        │  ma stałe segmenty: S01, S02, S03 ...  (każdy = ujęcie + timecode)
        ▼
timeline.json  ──────────────  języko­wo NEUTRALNY (id + start/end + strona flipbooka)
        │
        ├─ narration/pl.md   ← tekst PL  (segmenty S01, S02, ...)
        ├─ narration/es.md   ← tekst ES  (TE SAME segmenty)
        └─ narration/<xx>.md ← nowy język = kopiujesz szablon i tłumaczysz segmenty
```

Klej między animacją a tekstem to **ID segmentu** (`S01`, `S02`, ...). Występuje:
- w `timeline.json` — gdzie segment jest w czasie (start/end) i na której stronie flipbooka,
- jako nagłówek `## [S01] ...` w każdym pliku `narration/<lang>.md`.

Dzięki temu lektor w dowolnym języku trafia w te same ujęcia co animacja.

---

## Struktura

```
episodes/
  odc-01/
    meta.json              # metadane odcinka: tytuł per język, status, długość
    timeline.json          # JĘZYKOWO NEUTRALNY: segmenty flipbooka + timecode
    narration/
      pl.md                # narracja PL (oryginał)
      de.md                # narracja DE (szablon do tłumaczenia — te same ID)
      es.md                # narracja ES (szablon do tłumaczenia — te same ID)
    source/
      pl_oryginal.md       # surowy tekst źródłowy „od Janusza" (zanim pociąć na segmenty)
```

> ⚠️ Wszystkie pliki `odc-01/` zawierają teraz **przykładowe (MOCK) dane** — pokazują format.
> Prawdziwy odcinek 1 wejdzie w te same miejsca.

---

## Języki narracji

Obecnie: **PL** (oryginał), **DE**, **ES**.

## Dodanie kolejnego języka narracji

1. Skopiuj `episodes/odc-01/narration/de.md` → `narration/<xx>.md`.
2. Zostaw **nagłówki `## [Sxx] ...` bez zmian** (wiążą tekst z timeline.json).
3. Przetłumacz tylko tekst pod każdym segmentem.
4. Dopisz tytuł w `meta.json` (`titles.<xx>`).
5. Timeline (`timeline.json`) i flipbook — **nie ruszasz**. Lektor nagrywasz pod te same timecode'y.

---

## Reguły

- **Nie zmieniaj ID segmentów** (`S01`...) ani ich timecode'ów bez ponownego renderu flipbooka —
  to one synchronizują narrację z animacją.
- Tekst narracji per język żyje **wyłącznie** w `narration/<lang>.md`.
- `source/` to materiał wejściowy (przed cięciem na segmenty); nie jest używany do produkcji bezpośrednio.
