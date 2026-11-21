import math
from figs import f

# B2-A-01, A-02, A-03 · Marker-Präfix a0…, damit die IDs auf der ganzen Seite eindeutig bleiben.


def _defs(p):
    out = '<defs>'
    for k, cls in (("A", "fill-audio"), ("C", "fill-cv"), ("K", "fill-ink"), ("G", "fill-gate"), ("T", "fill-trig")):
        out += (f'<marker id="{p}{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="{cls}"/></marker>')
    return out + '</defs>'


def _pl(pts, cls, extra=""):
    return f'<polyline points="{" ".join(f"{f(x)},{f(y)}" for x, y in pts)}" class="sig {cls}"{extra}/>'


# ---------------- A-01 · Wie ein Eingang ein Gate liest ----------------
def fig_a01():
    W, H = 760, 360
    x0, x1 = 150, 740
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Eine langsame Hüllkurve steigt über eine Schaltschwelle von etwa 2,5 Volt und fällt wieder darunter. Darunter das Gate, das ein Eingang daraus liest: hoch, solange die Spannung über der Schwelle liegt. Ganz unten der Trigger, den eine Flankenerkennung aus der steigenden Flanke macht. Eine zweite, abgeschwächte Hüllkurve bleibt unter der Schwelle und löst nichts aus.">']
    # Zeile 1: CV mit Schwelle
    y0, sc = 120, 9.0  # 0 V bei y0, 9 px pro Volt
    o.append('<text x="10" y="40" class="t-lab" style="font-size:15px">Spannung</text><text x="10" y="56" class="t-sub">Hüllkurve 0–10 V</text>')
    for v in (0, 5, 10):
        o.append(f'<line x1="{x0}" y1="{f(y0-v*sc)}" x2="{x1}" y2="{f(y0-v*sc)}" class="{"t-zero" if v==0 else "t-grid"}"/>')
        o.append(f'<text x="{x0-6}" y="{f(y0-v*sc+4)}" class="t-ax" text-anchor="end">{v} V</text>')
    thr = 2.5
    o.append(f'<line x1="{x0}" y1="{f(y0-thr*sc)}" x2="{x1}" y2="{f(y0-thr*sc)}" style="stroke:var(--gate);stroke-width:1.5;stroke-dasharray:6 4"/>')
    o.append(f'<text x="{x1}" y="{f(y0-thr*sc-5)}" class="t-ax" text-anchor="end" style="fill:var(--gate)">Schwelle ≈ 2,5 V</text>')

    def env(t, a, d, peak):
        if t < 0:
            return 0
        if t < a:
            return peak * t / a
        return peak * math.exp(-(t - a) / d)
    span = x1 - x0
    pts, pts2 = [], []
    for i in range(0, 241):
        x = x0 + span * i / 240
        t = i / 240
        v = env(t - 0.05, 0.12, 0.13, 10)
        v2 = env(t - 0.62, 0.08, 0.1, 2.0)
        pts.append((x, y0 - v * sc))
        pts2.append((x, y0 - v2 * sc))
    o.append(_pl(pts, "sig-cv"))
    o.append(_pl(pts2, "sig-cv", ' style="stroke-dasharray:4 3"'))
    o.append(f'<text x="{x1}" y="{y0+15}" class="t-ax lab-cv" text-anchor="end">gestrichelt: abgeschwächt, bleibt unter der Schwelle</text>')
    # Schwellen-Zeitpunkte
    on = off = None
    for i in range(1, len(pts)):
        v_prev = (y0 - pts[i - 1][1]) / sc
        v = (y0 - pts[i][1]) / sc
        if on is None and v_prev < thr <= v:
            on = pts[i][0]
        if on is not None and off is None and v_prev >= thr > v:
            off = pts[i][0]
    # Zeile 2: Gate
    yg = 220
    o.append('<text x="10" y="196" class="t-lab" style="font-size:15px">Gate</text><text x="10" y="212" class="t-sub">so liest es ein Eingang</text>')
    o.append(f'<line x1="{x0}" y1="{yg}" x2="{x1}" y2="{yg}" class="t-zero"/>')
    o.append(_pl([(x0, yg), (on, yg), (on, yg - 40), (off, yg - 40), (off, yg), (x1, yg)], "sig-gate"))
    o.append(f'<text x="{f((on+off)/2)}" y="{yg-48}" class="t-ax" text-anchor="middle" style="fill:var(--gate)">hoch, solange über der Schwelle</text>')
    for xx in (on, off):
        o.append(f'<line x1="{f(xx)}" y1="{f(y0-thr*sc)}" x2="{f(xx)}" y2="{yg}" class="t-grid" style="stroke-dasharray:2 3"/>')
    # Zeile 3: Trigger
    yt = 310
    o.append('<text x="10" y="286" class="t-lab" style="font-size:15px">Trigger</text><text x="10" y="302" class="t-sub">aus der steigenden Flanke</text>')
    o.append(f'<line x1="{x0}" y1="{yt}" x2="{x1}" y2="{yt}" class="t-zero"/>')
    o.append(_pl([(x0, yt), (on, yt), (on, yt - 40), (on + 6, yt - 40), (on + 6, yt), (x1, yt)], "sig-trig"))
    o.append(f'<text x="{f(on+14)}" y="{yt-28}" class="t-ax" style="fill:var(--trig)">ein paar Millisekunden</text>')
    o.append(f'<text x="{x1}" y="{H-8}" class="t-ax" text-anchor="end">Zeit →</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- A-02 · Hart und weich begrenzen ----------------
def fig_a02clip():
    W, H = 760, 300
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Drei Fassungen desselben Sinus. Links unverändert mit plus minus fünf Volt. In der Mitte zu stark verstärkt und hart abgeschnitten, wie an einer Versorgungsgrenze oder am Wandler: oben und unten flach, mit scharfen Ecken. Rechts weich begrenzt, wie an einem übersteuerten Filtereingang: die Spitzen werden rund gedrückt.">']
    panels = [("Nennpegel", "±5 V, sauber", lambda s: 5 * s),
              ("hart begrenzt", "Wandler oder Versorgung", lambda s: max(-6.5, min(6.5, 9.5 * s))),
              ("weich begrenzt", "übersteuerte Eingangsstufe", lambda s: 7.2 * math.tanh(1.6 * s))]
    pw, gap, y0, sc = 228, 18, 150, 10.5
    for k, (t, sub, fn) in enumerate(panels):
        x = 14 + k * (pw + gap)
        o.append(f'<text x="{x}" y="24" class="t-lab" style="font-size:15px">{t}</text><text x="{x}" y="40" class="t-sub">{sub}</text>')
        o.append(f'<rect x="{x}" y="{f(y0-6.5*sc)}" width="{pw}" height="{f(13*sc)}" class="sec-a" style="stroke:var(--line)"/>')
        for v in (-5, 0, 5):
            o.append(f'<line x1="{x}" y1="{f(y0-v*sc)}" x2="{x+pw}" y2="{f(y0-v*sc)}" class="{"t-zero" if v==0 else "t-grid"}"/>')
        pts = []
        for i in range(0, 201):
            ph = i / 200 * 2 * math.pi * 2
            pts.append((x + pw * i / 200, y0 - fn(math.sin(ph)) * sc))
        o.append(_pl(pts, "sig-audio"))
        if k == 1:
            o.append(f'<line x1="{x}" y1="{f(y0-6.5*sc)}" x2="{x+pw}" y2="{f(y0-6.5*sc)}" style="stroke:var(--trig);stroke-width:2;stroke-dasharray:5 4"/>')
            o.append(f'<text x="{x+pw-4}" y="{f(y0-6.5*sc-6)}" class="t-ax" text-anchor="end" style="fill:var(--trig)">Grenze</text>')
    o.append(f'<text x="18" y="{f(y0-5*sc-4)}" class="t-ax">+5 V</text>')
    o.append(f'<text x="18" y="{f(y0+5*sc+13)}" class="t-ax">−5 V</text>')
    o.append(f'<text x="14" y="{H-12}" class="t-ax">Hart: neue, scharfe Obertöne, klingt kaputt und steckt in der Aufnahme. Weich: dichter, wärmer, oft gewollt.</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- A-02 · Kanalplan zum L6 ----------------
def fig_a02route():
    W, H = 760, 380
    p = "a02r"
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Kanalplan aus Kapitel 10: Milky Way OUT 1 und 2 als Hall-Return über zwei Passivfader auf die Kanäle 1 und 2 des L6, die viel Reserve haben. Die trockene Stimme über Mult A und einen Passivfader auf Kanal 3. Samples II mit Summe und einzelner Kick auf Kanal 4 links und rechts. Elements mit Riser auf Kanal 5, Rings über den FOUR PLAY auf Kanal 6. Die Kanäle 3 bis 6 sind Line-Eingänge mit plus 9 dBu.">', _defs(p)]
    src = [("Milky Way OUT 1", "Hall-Return L"), ("Milky Way OUT 2", "Hall-Return R"), ("Stimme 2A", "trocken, Mult A"),
           ("Samples II OUT 5", "Summe ohne Kick"), ("Samples II OUT 1", "Kick einzeln"), ("Elements", "mit Riser"), ("Rings", "über FOUR PLAY")]
    dst = [("K1", "TRS +24 dBu"), ("K2", "TRS +24 dBu"), ("K3 L", "Line +9 dBu"), ("K4 L", "Line +9 dBu"), ("K4 R", "Line +9 dBu"),
           ("K5 L", "Line +9 dBu"), ("K6 L", "Line +9 dBu")]
    rh = 46
    for i, ((s, ss), (d, ds)) in enumerate(zip(src, dst)):
        y = 30 + i * rh
        o.append(f'<rect x="14" y="{y}" width="200" height="36" rx="3" class="box"/>')
        o.append(f'<text x="24" y="{y+16}" class="t-lab" style="font-size:13.5px">{s}</text><text x="24" y="{y+30}" class="t-sub">{ss}</text>')
        o.append(f'<rect x="318" y="{y+4}" width="96" height="28" rx="3" class="box-mod"/>')
        o.append(f'<text x="366" y="{y+23}" class="t-ax" text-anchor="middle" style="fill:var(--ink)">Passivfader</text>')
        o.append(f'<line x1="214" y1="{y+18}" x2="316" y2="{y+18}" class="wire-audio" marker-end="url(#{p}A)"/>')
        o.append(f'<line x1="414" y1="{y+18}" x2="526" y2="{y+18}" class="wire-audio" marker-end="url(#{p}A)"/>')
        cls = "box-strong" if i < 2 else "box"
        o.append(f'<rect x="528" y="{y}" width="110" height="36" rx="3" class="{cls}"/>')
        o.append(f'<text x="540" y="{y+16}" class="t-lab" style="font-size:14px">{d}</text><text x="540" y="{y+30}" class="t-sub">{ds}</text>')
    yL = 30
    o.append(f'<rect x="652" y="{yL}" width="94" height="{7*rh-10}" rx="3" class="box"/>')
    o.append(f'<text x="699" y="{yL+24}" class="t-lab" text-anchor="middle">L6</text>')
    o.append(f'<text x="699" y="{yL+44}" class="t-sub" text-anchor="middle">Recorder</text>')
    o.append(f'<text x="699" y="{yL+60}" class="t-sub" text-anchor="middle">32-Bit-Float</text>')
    o.append(f'<text x="699" y="{yL+150}" class="t-sub" text-anchor="middle">MASTER</text>')
    o.append(f'<text x="699" y="{yL+166}" class="t-sub" text-anchor="middle">stereo</text>')
    o.append(f'<text x="14" y="{H-18}" class="t-ax">Kanalplan aus Kapitel 10 · K1/K2: Klinke an der Kombibuchse, doppelte Wandler · K3–K6: Line, je ein Stereopaar</text>')
    o.append(f'<text x="14" y="{H-4}" class="t-ax">K5 und K6 nur links gesteckt (MONO): eine Stereodatei mit L = R</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- A-03 · Quantisieren frei und im Takt ----------------
NOTES = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "H", "C"]


def fig_a03():
    W, H = 760, 450
    x0, x1 = 70, 740
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Eine langsam wandernde Steuerspannung zwischen 0 und 1 Volt, also über eine Oktave. Oben quantisiert ein Quantizer frei auf Halbtöne: der Ausgang springt, sobald die Eingangsspannung die Mitte zwischen zwei Halbtönen überschreitet. Unten mit Tonleiter C-Dur und Trigger am Takteingang: der Ausgang ändert sich nur bei jedem Taktimpuls und nur auf Töne der Tonleiter. Am Trigger-Ausgang erscheint bei jedem neuen Ton ein Impuls.">']
    def cv(t):
        return 0.5 + 0.38 * math.sin(2 * math.pi * (t * 1.15 + 0.05)) + 0.08 * math.sin(2 * math.pi * t * 4.3)
    N = 400
    span = x1 - x0
    rows = [("frei, chromatisch", "Trig. In leer: folgt sofort", 44, list(range(13)), None),
            ("im Takt, C-Dur", "Trig. In mit Clock · Penrose: 7 Tasten an", 248, [0, 2, 4, 5, 7, 9, 11, 12], 12)]
    hh = 150
    for lab, sub, yt, scale, clk in rows:
        yb = yt + hh
        sc = hh / 1.0
        o.append(f'<text x="{x0}" y="{yt-16}" class="t-lab" style="font-size:15px">{lab}</text>')
        o.append(f'<text x="{x0+180}" y="{yt-16}" class="t-sub">{sub}</text>')
        for n in range(13):
            y = yb - n / 12 * sc
            on = n in scale
            o.append(f'<line x1="{x0}" y1="{f(y)}" x2="{x1}" y2="{f(y)}" class="t-grid" style="opacity:{1 if on else .35}"/>')
            o.append(f'<text x="{x0-8}" y="{f(y+4)}" class="t-ax" text-anchor="end" style="{"" if on else "opacity:.45"}">{NOTES[n]}</text>')
        o.append(f'<text x="{x0-36}" y="{f(yb+4)}" class="t-ax" text-anchor="end">0 V</text>')
        o.append(f'<text x="{x0-36}" y="{f(yt+4)}" class="t-ax" text-anchor="end">1 V</text>')
        pts = [(x0 + span * i / N, yb - cv(i / N) * sc) for i in range(N + 1)]
        o.append(_pl(pts, "sig-cv", ' style="stroke-width:1.6"'))

        def q(v):
            return min(scale, key=lambda n: abs(n / 12 - v)) / 12
        out, cur, trig = [], None, []
        ticks = [round(N * k / clk) for k in range(clk)] if clk else None
        for i in range(N + 1):
            v = cv(i / N)
            if ticks is None or i in ticks or cur is None:
                nv = q(v)
                if nv != cur:
                    trig.append(x0 + span * i / N)
                cur = nv
            x = x0 + span * i / N
            if out and abs(out[-1][1] - (yb - cur * sc)) > 0.01:
                out.append((x, out[-1][1]))
            out.append((x, yb - cur * sc))
        o.append(_pl(out, "sig-step"))
        if ticks:
            for k in ticks:
                x = x0 + span * k / N
                o.append(f'<line x1="{f(x)}" y1="{yb+6}" x2="{f(x)}" y2="{yb+16}" style="stroke:var(--trig);stroke-width:2"/>')
            o.append(f'<text x="{x1}" y="{yb+30}" class="t-ax" text-anchor="end" style="fill:var(--trig)">Takt am Trig. In</text>')
        for x in trig[1:]:
            o.append(f'<circle cx="{f(x)}" cy="{yt-5}" r="3" class="fill-gate"/>')
    o.append(f'<text x="{x0}" y="{H-6}" class="t-ax"><tspan class="lab-cv">orange: Eingang</tspan> · <tspan class="lab-step">blau: Ausgang</tspan> · <tspan style="fill:var(--gate)">Punkte: Impuls am Trig. Out (A-156) bzw. Gate Out (Penrose)</tspan></text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- F-03 · Das Pult als Karte ----------------
CAT = {  # Kategorie wie im Rack-Schema
    "seq": ("Takt, Sequencing", "var(--trig-soft)", "var(--trig)"),
    "mod": ("Modulation, Werkzeuge", "var(--cv-soft)", "var(--cv)"),
    "src": ("Klangquellen", "var(--audio-soft)", "var(--audio)"),
    "fx": ("Filter, VCA, Effekte", "var(--gate-soft)", "var(--gate)"),
    "mix": ("Routing, Strom", "var(--panel)", "var(--muted)"),
}
MODCAT = {"MOD-µYarns": "seq", "MOD-LeoLeo": "seq", "MOD-Swarm": "src", "MOD-µTuring": "seq", "MOD-Volts": "seq", "MOD-Voltages": "seq",
          "MOD-Bode": "fx", "MOD-Skies": "fx", "MOD-Mult": "mix", "MOD-A-160-2": "seq", "MOD-A-118-2": "mod", "MOD-Mult-1x8": "mix",
          "MOD-Attenuverter": "mod", "MOD-281t": "mod", "MOD-Volcan": "mod", "MOD-SERRA": "mod", "MOD-ADSR": "mod", "MOD-FOUR LFO": "mod",
          "MOD-EuroPi": "mod", "MOD-Mixer": "mix", "MOD-XDR": "fx", "MOD-Arythmatik": "seq", "MOD-mGrids": "seq", "MOD-A-166": "seq",
          "MOD-Mitch": "mix", "MOD-CHAOS": "mod", "MOD-ZeroScope": "mix", "MOD-A-151": "seq", "MOD-A-156": "seq", "MOD-Penrose": "seq",
          "MOD-A-185-2": "seq", "MOD-Logic": "seq", "MOD-258t": "src", "MOD-Cali": "src", "MOD-Big-O": "src", "MOD-A-115": "src",
          "MOD-Blck_Noir": "src", "MOD-Samples-II": "src", "MOD-FOUR PLAY": "fx", "MOD-Lyra8-FX": "fx", "MOD-Muxlicer": "seq",
          "MOD-Rings": "src", "MOD-Elements": "src", "MOD-A-106-5": "fx", "MOD-A-124": "fx", "MOD-DPLPG": "fx", "MOD-Surges": "fx",
          "MOD-A-130-8": "fx", "MOD-Slew": "mod", "MOD-A-138f": "mix", "MOD-Morphor Echo": "fx", "MOD-Roboto": "fx", "MOD-Milky Way": "fx",
          "MOD-8x8": "mix", "MOD-Programm": "seq", "MOD-A-138m": "mix", "MOD-Ears": "src", "MOD-Straw": "mix", "MOD-L6": "mix"}
# Reihenfolge links → rechts laut Rack-Schema v12; Mehrfachmodule einzeln
LAYOUT = {
    1: [("MOD-µYarns", 6), ("MOD-LeoLeo", 42), ("MOD-Swarm", 41), ("MOD-µTuring", 4), ("MOD-µTuring", 6), ("MOD-Volts", 4), ("MOD-Volts", 4),
        ("MOD-Voltages", 8), ("MOD-Bode", 14), ("MOD-Skies", 18)],
    2: [("MOD-Mult", 2), ("MOD-A-160-2", 4), ("MOD-A-118-2", 4), ("MOD-Mult-1x8", 2), ("MOD-Attenuverter", 2), ("MOD-281t", 28), ("MOD-Volcan", 10),
        ("MOD-SERRA", 10), ("MOD-ADSR", 2), ("MOD-FOUR LFO", 14), ("MOD-EuroPi", 8), ("MOD-Mixer", 2), ("MOD-XDR", 4), ("MOD-Arythmatik", 6),
        ("MOD-mGrids", 8), ("MOD-Mixer", 2), ("MOD-A-166", 8), ("MOD-Mitch", 6), ("MOD-CHAOS", 18), ("MOD-ZeroScope", 6)],
    3: [("MOD-A-151", 4), ("MOD-A-151", 4), ("MOD-A-156", 8), ("MOD-Penrose", 6), ("MOD-A-185-2", 6), ("MOD-Logic", 2), ("MOD-258t", 18),
        ("MOD-Cali", 12), ("MOD-Big-O", 14), ("MOD-A-115", 8), ("MOD-Blck_Noir", 30), ("MOD-Samples-II", 4), ("MOD-FOUR PLAY", 12), ("MOD-Lyra8-FX", 20)],
    4: [("MOD-Muxlicer", 16), ("MOD-Rings", 14), ("MOD-Elements", 34), ("MOD-Attenuverter", 2), ("MOD-A-106-5", 8), ("MOD-A-124", 8), ("MOD-DPLPG", 2),
        ("MOD-Surges", 8), ("MOD-Surges", 8), ("MOD-Mult", 2), ("MOD-A-130-8", 6), ("MOD-Slew", 2), ("MOD-A-138f", 4), ("MOD-Morphor Echo", 20),
        ("MOD-Roboto", 6), ("MOD-Milky Way", 6)],
    5: [("MOD-8x8", 30), ("MOD-Programm", 40), ("MOD-A-138m", 20), ("MOD-Ears", 4), ("MOD-Straw", 3), ("MOD-L6", 50)],
}


def fig_pult():
    import register
    short = {r[1]: r[5] for r in register.MODS}
    slug = register._slug
    W, H = 760, 470
    x0, px = 10, 740 / 148
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Das Pult als Karte: fünf Reihen mit je 148 HP, jedes Modul als Feld in seiner Breite und nach Aufgabe eingefärbt. Reihe 1 Sequencing und Effekte oben, Reihe 2 Takt und Modulation, Reihe 3 Quantizer, Stimmen und Drums, Reihe 4 Resonatoren, Filter, VCAs und Effekte, Reihe 5 Matrix, Programm und L6. Jedes Feld springt zur Zeile in der Modultabelle.">']
    rh = 78
    for r in range(1, 6):
        y = 14 + (r - 1) * rh
        o.append(f'<text x="{x0}" y="{y+9}" class="t-ax">{register.ROWS[r]}</text>')
        o.append(f'<rect x="{x0}" y="{y+14}" width="{f(148*px)}" height="52" class="sec-a" style="stroke:var(--line)"/>')
        x = x0
        used = 0
        for mid, hp in LAYOUT[r]:
            w = hp * px
            lab, fill, stroke = CAT[MODCAT[mid]]
            o.append(f'<a href="#{slug(mid)}"><rect x="{f(x+.5)}" y="{y+15}" width="{f(w-1)}" height="50" style="fill:{fill};stroke:{stroke};stroke-width:1"/>')
            t = short[mid]
            if w >= len(t) * 6.2 + 6:
                o.append(f'<text x="{f(x+w/2)}" y="{y+44}" class="t-ax" text-anchor="middle" style="fill:var(--ink);font-size:10.5px">{t}</text>')
            elif w >= 18:
                o.append(f'<text x="{f(x+w/2+3.5)}" y="{y+62}" class="t-ax" transform="rotate(-90 {f(x+w/2+3.5)} {y+62})" style="fill:var(--ink);font-size:9px">{t[:8]}</text>')
            o.append('</a>')
            x += w
            used += hp
        o.append(f'<text x="{x0+148*px}" y="{y+9}" class="t-ax" text-anchor="end">{used} von 148 HP</text>')
    ly = H - 34
    lx = x0
    for k in ("seq", "mod", "src", "fx", "mix"):
        lab, fill, stroke = CAT[k]
        o.append(f'<rect x="{lx}" y="{ly}" width="14" height="14" style="fill:{fill};stroke:{stroke}"/>')
        o.append(f'<text x="{lx+20}" y="{ly+11}" class="t-ax" style="fill:var(--ink)">{lab}</text>')
        lx += 20 + len(lab) * 6.8 + 22
    o.append(f'<text x="{x0}" y="{H-6}" class="t-ax">Stand Rack-Schema v12 nach dem Umbau vom Oktober 2026 · schmale Module ohne Beschriftung: in der Tabelle unten</text>')
    o.append('</svg>')
    return "\n".join(o)
