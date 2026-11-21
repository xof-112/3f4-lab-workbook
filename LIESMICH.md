# 3F4-Lab Workbook · Bausatz

Quellen der HTML-Seite „3F4-Lab Workbook“
Veröffentlicht: https://claude.ai/artifact/WLhQ4AnPvsSz9kW7jgHpFR
Stand: Fassung 2.5, 21. November 2026 (Bauplan, Band 1–3, 44 Modulporträts, Patch-Bibliothek KWP-01–20, Teil VI „Am Pult prüfen“; Farbsystem „Kante“)

## So geht es in einem neuen Gespräch weiter
1. Dieses ZIP anhängen und den Artifact-Link oben nennen.
2. Auftrag nennen, z. B. „B3-06 ausarbeiten“.
3. Claude entpackt das ZIP, baut mit `python3 build.py` und veröffentlicht `3f4-lab-workbook.html` auf dieselbe Artifact-URL.
4. Vorher prüfen: Stimmt die Fassungsnummer hier mit der veröffentlichten Seite überein (Titelzeile „Fassung …“)? Sonst ist das ZIP veraltet. So geschehen bei 1.3 gegen 1.7 und am 21.11.2026: ZIP 1.11 gegen Seite 2.4 (die ZIPs 1.12–2.4 fehlten), siehe „Herkunft“.
5. Veröffentlichen mit publish_files (Datei 3f4-lab-workbook.html als index.html), die Seite ist rund 3 MB groß.

## Herkunft (wichtig)
Fassung 2.5 wurde aus der veröffentlichten Seite 2.4 zurückgewonnen: Die Seite wurde wortgetreu in die Dateien unten zerlegt, `build.py` baut sie Byte für Byte nach (geprüft). Folgen:
- Texte, Tabellen, Modulübersicht, Rezeptverzeichnis, Verweisregister, Patch-Anker und Querverweis-Links stehen **fertig im HTML**. `register.py` gibt es nicht mehr: Die Fassung aus 1.11 kannte die Seiten aus 1.12–2.4 nicht (Modulporträts, B3-00 … B3-05, KWP) und brach daran ab. Neue IDs, Register-Zeilen und Fundstellen deshalb von Hand eintragen, Links als `<a class="xref" href="#…">`.
- Aus Python kommen nur noch die 31 Grafiken im Dict `F` in `build.py` (figs*.py, Stand 1.11, deren Ausgabe noch exakt der Seite entsprach). Alle anderen Grafiken, auch die Patchpläne der Kapitel 08 und 09, die Pult-Karte (F-03), A-03 und alle neueren, stehen als fertiges SVG im HTML. Änderungen daran direkt im SVG oder neu in einer figsN.py.

## Aufbau
| Datei | Inhalt |
|---|---|
| head.html | `<title>`, `<meta name="color-scheme" content="dark">`, Schriften, gesamtes CSS |
| body1.html | Seitenleiste, Titel, Inhaltsverzeichnis, Teil I Bauplan, „Was sich geändert hat“ (`#aenderungen`, je Fassung ein `<h4 id="aend-NN">`) |
| body2.html | Teil II Kopf + Band 1 Kapitel 01 |
| ch02.html … ch10.html | Band 1 Kapitel 02–10 |
| band2.html | Teil III Band 2 (A-01 … F-04, Modulübersicht, Verweisregister, Modulporträts `mp-…`) |
| band3.html | Teil IV Band 3 (B3-00 … B3-05) |
| kwp.html | Teil V Patch-Bibliothek „Klangwege im Pult“ (KWP-01 … KWP-20) |
| pruefen.html | Teil VI „Am Pult prüfen“: alle offenen Marken |
| anhang.html | Quellen, Fußzeile (mit Fassungsnummer) |
| script.html | gesamtes JavaScript: Spielplätze (u. a. fbplay, Formleiste Kap. 09 `formplay` mit Ton, localStorage „wb-form9“; Pegelrechner `pegelplay`; Patchkarte `pcard`, localStorage „wb-card10“), Vorlesefunktion, Seitenleiste |
| figs.py … figs7.py | Grafik-Generatoren (siehe „Herkunft“), Regler `knob()`, Patchplan-Generator `patchplan()` in figs2.py |
| build.py | setzt alles zusammen → 3f4-lab-workbook.html |
| shot.js | Playwright-Prüfung (Bildschirmfotos, Konsolenfehler) |

Neue Kapitel oder Teile: als eigene .html anlegen und in `build.py` in ORDER eintragen; neue Grafiken in einer `figsN.py` und in das Dict `F`. SVG-Marker-IDs müssen auf der ganzen Seite eindeutig sein.

## Platzhalter (von build.py ersetzt)
- `{{FIG:name}}` → SVG aus figs*.py
- `{{KNOB:stunde|Beschriftung|Untertitel}}`, mit `|b` für bipolar
- `{{READER}}` (Vorlese-Leiste), `{{BACK}}` (Rücksprung zum Inhaltsverzeichnis)
- `{{INC:datei.html}}` → Inhalt der Datei (zuerst ersetzt)

## Farbsystem „Kante“ (seit 2.5)
Die Seite ist immer dunkel, Aurora-Theme „Kante“. Es gibt keinen Hell/Dunkel-Schalter mehr, kein `data-theme`, kein localStorage „wb-theme“. Werte (in head.html, `:root`):

```
--bg:#1B1C1E; --surface:#232427; --surface2:#2A2B2E; --panel:#2E2F33;
--ink:#C9CBD0; --muted:#8B8E95; --line:#303135;
--audio:#4F9DB5; --cv:#D39B57; --gate:#6FB08A; --trig:#C77DA6;
--audio-soft:#1C2D33; --cv-soft:#33291C; --gate-soft:#1D2B22; --trig-soft:#31202A;
--warn:#D8C24A; --warn-soft:#2E2A16; color-scheme:dark;
```

Regeln: Farben nur über diese Variablen, keine festen Hex-Werte in SVG, Inline-Styles oder Script (Stand 2.5: keine vorhanden). SVG-Text erbt `fill:var(--ink)`. Auf kräftigen Signalfarben-Flächen dunkle Schrift `var(--bg)` (Kabelnummern, Formleisten-Teile ab Energie 4). Prüfung 2.5: alle 3.792 SVG-Texte gegen ihren Untergrund ≥ 3:1, HTML-Text ≥ 3,5:1 (ohne die absichtlich ausgeblendeten späteren Stufen der Patchpläne).

## Konventionen
- Kapitel: `<section class="part chapter" id="kN">`; B2-Seiten: `<article class="sample" id="b2-x0n">`; Modulporträts `mp-…`; B3 `b3-0n`; KWP `kwp-NN`
- Bausteine 00–13, Kontrollpunkt nach jeder Stufe, Kabel durchnummeriert; Klassen `n audio|cv|gate|trig|zero`
- Signalfarben im Fließtext: `<span class="a|c|g|t">`
- Prüfmarken: `tag-h` Hersteller · `tag-ok` verifiziert · `tag-p` am Gerät prüfen · `tag-d` offen
- Signalfarben: Audio blau, CV orange, Gate grün, Trigger magenta, MIDI grau gestrichelt (Kabeltyp `midi`)
- Collagé und andere disting-NT-Algorithmen erst ins Workbook, wenn der disting NT im Pult ist
- Neue Fassung: Titelzeile und Lede in body1.html, Inhaltsverzeichnis-Eintrag „Was sich geändert hat · Fassung …“, Eintrag `aend-NN`, Fußzeile in anhang.html

## Offene Punkte
Maßgeblich ist Teil VI der Seite („Am Pult prüfen · alle offenen Marken“, pruefen.html). Die Listen aus Bausatz 1.11 sind darin aufgegangen.

## Am Pult verifiziert (Stand 1.11, Weiteres in den Kapiteln mit `tag-ok`)
A-106-5 LP = 7 Uhr · A-124 LP = 7 Uhr · A-130-8 Lötbrücken offen · CatSynth Attenuverter: OFFSET ohne Eingang = Spannungsquelle · 281t-Modusschalter links unter CYCLE · µYarns 1M, GATE 1 oben links, CV 1 daneben · Big-O F.IN, FOLD, Fold-CV · Surges schwingt selbst · L6: 8 CatSynth-Passivfader vor den Eingängen
