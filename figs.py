import math

def f(x):
    return f"{x:.1f}".rstrip('0').rstrip('.')

# ---------- Vier Signalarten ----------
def fig_signals():
    W, H = 760, 400
    x0, x1 = 210, 740
    rows = [("Audio", "audio", "±5 V · 20 Hz–20 kHz"), ("CV", "cv", "fließend, langsam"),
            ("Gate", "gate", "0 / +5 V, mit Dauer"), ("Trigger", "trig", "Impuls, 1–10 ms")]
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Vier Signalarten im Zeitverlauf: Audio schwingt schnell um 0 V, CV wandert langsam, Gate hält ein Plateau, Trigger ist ein kurzer Impuls.">']
    rh = 90
    for i, (name, cls, sub) in enumerate(rows):
        top = 15 + i * rh
        mid = top + rh / 2 - 5
        amp = 30  # px for 5 V
        out.append(f'<text x="10" y="{f(mid-6)}" class="t-lab">{name}</text>')
        out.append(f'<text x="10" y="{f(mid+10)}" class="t-sub">{sub}</text>')
        # zero line
        out.append(f'<line x1="{x0}" y1="{f(mid)}" x2="{x1}" y2="{f(mid)}" class="t-zero"/>')
        out.append(f'<text x="{x0-6}" y="{f(mid+4)}" class="t-ax" text-anchor="end">0 V</text>')
        out.append(f'<text x="{x0-6}" y="{f(mid-amp+4)}" class="t-ax" text-anchor="end">+5</text>')
        out.append(f'<line x1="{x0}" y1="{f(mid-amp)}" x2="{x1}" y2="{f(mid-amp)}" class="t-grid"/>')
        if cls in ("audio", "cv"):
            out.append(f'<text x="{x0-6}" y="{f(mid+amp+4)}" class="t-ax" text-anchor="end">−5</text>')
            out.append(f'<line x1="{x0}" y1="{f(mid+amp)}" x2="{x1}" y2="{f(mid+amp)}" class="t-grid"/>')
        pts = []
        N = 600
        for k in range(N + 1):
            t = k / N
            x = x0 + t * (x1 - x0)
            if cls == "audio":
                ph = (t * 24) % 1
                v = 1 - 2 * ph  # saw
                y = mid - v * amp
            elif cls == "cv":
                v = 0.55 * math.sin(2 * math.pi * t * 1.3 - 0.6) + 0.35 * math.sin(2 * math.pi * t * 0.45)
                y = mid - v * amp
            elif cls == "gate":
                on = (0.06 < t < 0.30) or (0.42 < t < 0.48) or (0.62 < t < 0.90)
                y = mid - (amp if on else 0)
            else:
                on = any(abs(t - c) < 0.006 for c in (0.06, 0.24, 0.42, 0.60, 0.78, 0.96))
                y = mid - (amp if on else 0)
            pts.append(f"{f(x)},{f(y)}")
        out.append(f'<polyline points="{" ".join(pts)}" class="sig sig-{cls}"/>')
        if cls == "gate":
            out.append(f'<text x="{f(x0+0.06*(x1-x0))}" y="{f(mid-amp-6)}" class="t-ax">steigende Flanke</text>')
            out.append(f'<text x="{f(x0+0.30*(x1-x0)+4)}" y="{f(mid+14)}" class="t-ax">fallende Flanke</text>')
            out.append(f'<text x="{f(x0+0.70*(x1-x0))}" y="{f(mid-amp-6)}" class="t-ax" text-anchor="middle">Plateau = Dauer</text>')
        if cls == "trig":
            out.append(f'<text x="{f(x0+0.06*(x1-x0)+8)}" y="{f(mid-amp-6)}" class="t-ax">„Jetzt!“ – keine Dauer</text>')
    out.append(f'<text x="{x1}" y="{H-4}" class="t-ax" text-anchor="end">Zeit →</text>')
    out.append('</svg>')
    return "\n".join(out)


# ---------- Signalarchitektur ----------
def fig_arch():
    W, H = 760, 230
    boxes = [("Quelle", "VCO · 258t", 20), ("Klangformung", "VCF · A-106-5", 210), ("Dynamik", "VCA · A-130-8", 400), ("Ausgang", "L6 · Abhören", 590)]
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Signalarchitektur: Audio fließt von Quelle über Klangformung und Dynamik zum Ausgang; Modulation greift von oben per CV in jede Stufe ein.">']
    o.append('<defs><marker id="arA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fill-audio"/></marker>'
             '<marker id="arC" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fill-cv"/></marker></defs>')
    # modulation band
    o.append('<rect x="20" y="14" width="720" height="44" rx="3" class="box-mod"/>')
    o.append('<text x="36" y="34" class="t-lab">Modulation</text><text x="36" y="50" class="t-sub">281t · LFO · Sequencer · Hüllkurven</text>')
    for i, (t, s, x) in enumerate(boxes):
        o.append(f'<rect x="{x}" y="120" width="150" height="64" rx="3" class="box"/>')
        o.append(f'<text x="{x+75}" y="146" class="t-lab" text-anchor="middle">{t}</text>')
        o.append(f'<text x="{x+75}" y="166" class="t-sub" text-anchor="middle">{s}</text>')
        if i < 3:
            o.append(f'<line x1="{x+150}" y1="152" x2="{x+188}" y2="152" class="wire-audio" marker-end="url(#arA)"/>')
            o.append(f'<text x="{x+170}" y="143" class="t-ax" text-anchor="middle">Audio</text>')
        if i < 3:
            o.append(f'<line x1="{x+75}" y1="58" x2="{x+75}" y2="118" class="wire-cv" marker-end="url(#arC)"/>')
    o.append('<text x="95" y="94" class="t-ax" text-anchor="start" dx="6">CV: Tonhöhe, Form</text>')
    o.append('<text x="285" y="94" class="t-ax" dx="6">CV: Cutoff</text>')
    o.append('<text x="475" y="94" class="t-ax" dx="6">CV: Pegel</text>')
    o.append('<text x="20" y="215" class="t-sub">Lesrichtung im Patch: von links nach rechts. Audio waagerecht, Steuerspannung von oben.</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------- Pegelvergleich ----------
def fig_levels():
    rows = [
        ("Consumer-Line (−10 dBV)", 0.447, "line"),
        ("L6 XLR-Eingang 1/2, max. +4 dBu", 1.74, "lim"),
        ("L6 Line-Eingang 3–6, max. +9 dBu", 3.08, "lim"),
        ("Eurorack-Audio, 10 Vpp", 5.0, "euro"),
        ("L6 Klinke an Kombibuchse 1/2, max. +24 dBu", 17.4, "lim"),
    ]
    W, H = 760, 290
    x0, x1 = 300, 730
    vmax = 18
    sx = lambda v: x0 + v / vmax * (x1 - x0)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Spitzenspannungen im Vergleich: Eurorack-Audio mit 5 V Spitze übersteigt die Line-Eingänge 3 bis 6 des L6 (3,1 V) und den XLR-Eingang (1,7 V), liegt aber weit unter der Grenze der Klinkeneingänge 1 und 2 (17,4 V).">']
    for v in range(0, 19, 2):
        x = sx(v)
        o.append(f'<line x1="{f(x)}" y1="20" x2="{f(x)}" y2="{H-40}" class="t-grid"/>')
        o.append(f'<text x="{f(x)}" y="{H-24}" class="t-ax" text-anchor="middle">{v}</text>')
    o.append(f'<text x="{x1}" y="{H-6}" class="t-ax" text-anchor="end">Spitzenspannung in Volt</text>')
    for i, (lab, v, kind) in enumerate(rows):
        y = 30 + i * 44
        o.append(f'<text x="{x0-10}" y="{y+16}" class="t-sub" text-anchor="end">{lab}</text>')
        cls = {"line": "bar-mute", "lim": "bar-lim", "euro": "bar-euro"}[kind]
        o.append(f'<rect x="{x0}" y="{y}" width="{f(sx(v)-x0)}" height="22" class="{cls}"/>')
        o.append(f'<text x="{f(sx(v)+6)}" y="{y+16}" class="t-ax">{str(v).replace(".", ",")} V</text>')
    xe = sx(5.0)
    o.append(f'<line x1="{f(xe)}" y1="20" x2="{f(xe)}" y2="{H-40}" class="mark-euro"/>')
    o.append('</svg>')
    return "\n".join(o)


# ---------- 1V/Oct ----------
def fig_voct():
    W, H = 760, 330
    x0, x1, y0, y1 = 70, 720, 280, 30  # V 0..3 ; Hz 55..440
    sx = lambda v: x0 + v / 3 * (x1 - x0)
    sy = lambda hz: y0 - (math.log2(hz / 55) / 3) * (y0 - y1)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="1 Volt pro Oktave: jedes zusätzliche Volt verdoppelt die Frequenz. Ohne Quantizer gleitet die Tonhöhe stufenlos, mit Quantizer springt sie in Halbtonstufen von einem Zwölftel Volt.">']
    for v in (0, 1, 2, 3):
        o.append(f'<line x1="{f(sx(v))}" y1="{y1}" x2="{f(sx(v))}" y2="{y0}" class="t-grid"/>')
        o.append(f'<text x="{f(sx(v))}" y="{y0+18}" class="t-ax" text-anchor="middle">{v} V</text>')
    for hz, n in ((55, "A1 · 55 Hz"), (110, "A2 · 110 Hz"), (220, "A3 · 220 Hz"), (440, "A4 · 440 Hz")):
        o.append(f'<line x1="{x0}" y1="{f(sy(hz))}" x2="{x1}" y2="{f(sy(hz))}" class="t-grid"/>')
        o.append(f'<text x="{x0-6}" y="{f(sy(hz)+4)}" class="t-ax" text-anchor="end">{n.split(" · ")[0]}</text>')
        o.append(f'<text x="{x1+4}" y="{f(sy(hz)+4)}" class="t-ax">{n.split(" · ")[1]}</text>')
    # continuous
    o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" class="sig sig-cv" />')
    # quantized steps
    pts = []
    for k in range(36):
        v = k / 12
        hz = 55 * 2 ** v
        pts += [f"{f(sx(v))},{f(sy(hz))}", f"{f(sx(v + 1/12))},{f(sy(hz))}"]
    o.append(f'<polyline points="{" ".join(pts)}" class="sig sig-step"/>')
    # zoom annotation for one semitone
    v = 1.0; xa = sx(v); xb = sx(v + 1/12)
    o.append(f'<line x1="{f(xa)}" y1="{y0-4}" x2="{f(xb)}" y2="{y0-4}" class="anno"/>')
    o.append(f'<text x="{f(xa)}" y="{y0-12}" class="t-ax">1 Halbton = 1/12 V ≈ 83,3 mV</text>')
    o.append(f'<text x="{f(sx(2.15))}" y="{f(sy(55*2**2.15)-14)}" class="t-ax lab-cv" text-anchor="end">ohne Quantizer: gleitet</text>')
    o.append(f'<text x="{f(sx(2.25))}" y="{f(sy(55*2**2.25)+22)}" class="t-ax lab-step">mit Quantizer: Stufen</text>')
    o.append(f'<text x="{x0}" y="{H-4}" class="t-ax">Annahme: FREQ so gestimmt, dass 0 V am 1V/Oct-Eingang A1 ergibt.</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------- Knob ----------
def knob(hour, label, sub, bip=False, w=120):
    # hour: 7..12..5 ; may be float, use 17 for 5 o'clock
    h = hour if hour >= 7 else hour + 12
    ang = (h - 12) * 30  # -150..150
    cx, cy, r = w / 2, 40, 22
    o = [f'<svg viewBox="0 0 {w} 118" class="knob" role="img" aria-label="{label}: {sub}">']
    for k in range(11):
        a = math.radians(-150 + k * 30)
        xa, ya = cx + (r + 5) * math.sin(a), cy - (r + 5) * math.cos(a)
        xb, yb = cx + (r + 10) * math.sin(a), cy - (r + 10) * math.cos(a)
        cls = "tick tick-c" if (bip and k == 5) else "tick"
        o.append(f'<line x1="{f(xa)}" y1="{f(ya)}" x2="{f(xb)}" y2="{f(yb)}" class="{cls}"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" class="kn"/>')
    a = math.radians(ang)
    o.append(f'<line x1="{cx}" y1="{cy}" x2="{f(cx+(r-3)*math.sin(a))}" y2="{f(cy-(r-3)*math.cos(a))}" class="kp"/>')
    o.append(f'<text x="{cx}" y="92" text-anchor="middle" class="k-lab">{label}</text>')
    o.append(f'<text x="{cx}" y="108" text-anchor="middle" class="k-sub">{sub}</text>')
    o.append('</svg>')
    return "".join(o)


# ---------- Kompositions-Zeitleiste ----------
def fig_timeline():
    W, H = 760, 300
    x0, x1 = 150, 740
    sx = lambda s: x0 + s / 120 * (x1 - x0)
    lanes = [
        ("Oszillator 2", "audio", [(0, 0), (30, 0), (75, .8), (100, .8), (120, .2)]),
        ("Resonanz", "cv", [(0, .1), (30, .15), (75, .7), (95, .75), (120, .1)]),
        ("281t-Tiefe", "cv", [(0, .12), (30, .15), (75, .85), (100, .7), (120, .05)]),
        ("281t-Tempo", "trig", [(0, .25), (75, .3), (80, .9), (95, .9), (102, .25), (120, .2)]),
        ("VCA-Pegel", "gate", [(0, 0), (6, .7), (110, .7), (120, 0)]),
    ]
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Formverlauf der Zwei-Minuten-Drone: Ursprung bis 0:30, Aufbau bis 1:15 mit steigender Resonanz und Modulationstiefe, Rückzug bis 2:00 mit kurzem schnellen Höhepunkt.">']
    secs = [(0, 30, "Ursprung"), (30, 75, "Aufbau & Verdichtung"), (75, 120, "Rückzug")]
    for i, (a, b, n) in enumerate(secs):
        o.append(f'<rect x="{f(sx(a))}" y="10" width="{f(sx(b)-sx(a))}" height="{H-50}" class="{"sec-a" if i%2==0 else "sec-b"}"/>')
        o.append(f'<text x="{f((sx(a)+sx(b))/2)}" y="26" class="t-lab" text-anchor="middle">{n}</text>')
    lh = 44
    for i, (n, cls, pts) in enumerate(lanes):
        top = 40 + i * lh
        base = top + lh - 8
        o.append(f'<text x="{x0-10}" y="{base-8}" class="t-sub" text-anchor="end">{n}</text>')
        o.append(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" class="t-grid"/>')
        p = " ".join(f"{f(sx(s))},{f(base - v*(lh-14))}" for s, v in pts)
        o.append(f'<polyline points="{p}" class="sig sig-{cls}"/>')
    for s in (0, 30, 60, 75, 90, 120):
        o.append(f'<text x="{f(sx(s))}" y="{H-24}" class="t-ax" text-anchor="middle">{s//60}:{s%60:02d}</text>')
    o.append(f'<text x="{x0}" y="{H-6}" class="t-ax">Höhe der Linie = wie weit der Regler offen ist (relativ, nicht in Volt).</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------- 281t Modi (B2-Muster) ----------
def fig_modes():
    W, H = 760, 230
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Die drei Modi des 281t: Attack/Decay läuft nach einem Trigger einmal ganz durch, Attack/Hold/Decay hält 10 V solange das Gate anliegt, Loop startet sich am Ende des Decays selbst neu.">']
    panels = [("TRANSIENT", 20), ("SUSTAINED", 270), ("CYCLIC", 520)]
    for n, x in panels:
        w = 220
        o.append(f'<text x="{x}" y="20" class="t-lab">{dict(TRANSIENT="ATTACK/DECAY",SUSTAINED="ATTACK/HOLD/DECAY",CYCLIC="LOOP")[n]}</text>')
        top, base = 36, 130
        o.append(f'<line x1="{x}" y1="{base}" x2="{x+w}" y2="{base}" class="t-grid"/>')
        o.append(f'<text x="{x+w}" y="{top+8}" class="t-ax" text-anchor="end">10 V</text>')
        if n == "TRANSIENT":
            p = [(0, 0), (20, 0), (60, 1), (150, 0), (w, 0)]
            gate = [(20, 1), (24, 0)]
        elif n == "SUSTAINED":
            p = [(0, 0), (20, 0), (60, 1), (140, 1), (200, 0), (w, 0)]
            gate = [(20, 1), (140, 0)]
        else:
            p = [(0, 0), (10, 0)]
            t = 10
            while t + 80 <= w:
                p += [(t + 30, 1), (t + 80, 0)]
                t += 80
            gate = None
        pts = " ".join(f"{f(x+a)},{f(base - v*(base-top-6))}" for a, v in p)
        o.append(f'<polyline points="{pts}" class="sig sig-cv"/>')
        gy = 190
        o.append(f'<line x1="{x}" y1="{gy}" x2="{x+w}" y2="{gy}" class="t-grid"/>')
        if gate:
            a, b = gate[0][0], gate[1][0]
            cls = "sig-trig" if b - a < 10 else "sig-gate"
            o.append(f'<polyline points="{x},{gy} {x+a},{gy} {x+a},{gy-22} {x+b},{gy-22} {x+b},{gy} {x+w},{gy}" class="sig {cls}"/>')
            o.append(f'<text x="{x}" y="{gy+20}" class="t-ax">{"Trigger genügt" if cls=="sig-trig" else "Gate bestimmt die Haltezeit"}</text>')
        else:
            for k in (90, 170):
                o.append(f'<line x1="{x+k}" y1="{gy}" x2="{x+k}" y2="{gy-22}" class="sig sig-trig"/>')
            o.append(f'<text x="{x}" y="{gy+20}" class="t-ax">PULSE OUT am Ende jedes Decays</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------- Werk-Architektur ----------
def fig_werk():
    W, H = 760, 330
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Wie die Teile des 3F4-Lab Workbooks zusammenhängen: Band 1 ist der Lernpfad, schlägt Techniken in Band 2 nach, führt zu den Stilübungen in Band 3 und nutzt die Patchkarten der Bibliothek.">']
    o.append('<defs><marker id="arK" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fill-ink"/></marker></defs>')
    def box(x, y, w, h, t, s, cls="box"):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" class="{cls}"/>')
        o.append(f'<text x="{x+14}" y="{y+26}" class="t-lab">{t}</text>')
        o.append(f'<text x="{x+14}" y="{y+46}" class="t-sub">{s}</text>')
    box(20, 120, 230, 76, "B1 · Lernpfad", "10 Kapitel, der Reihe nach", "box box-strong")
    box(510, 20, 230, 76, "B2 · Nachschlagewerk", "Techniken A–F, beliebig")
    box(510, 228, 230, 76, "B3 · Vom Patch zum Stil", "Grundpatch + 5 Stile")
    box(275, 250, 200, 64, "KWP · Bibliothek", "20 Patchkarten, wachsend")
    box(290, 20, 150, 64, "MOD · Module", "je Modul eine Seite")
    def arr(x1, y1, x2, y2, lab, lx, ly, anchor="middle"):
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="wire-ink" marker-end="url(#arK)"/>')
        o.append(f'<text x="{lx}" y="{ly}" class="t-ax" text-anchor="{anchor}">{lab}</text>')
    arr(250, 136, 506, 66, "schlägt Technik nach", 410, 128)
    arr(250, 180, 506, 256, "führt weiter zu", 395, 205)
    arr(330, 248, 170, 200, "Patchkarte je Kapitel", 210, 240, "end")
    arr(475, 282, 506, 278, "", 0, 0)
    o.append('<text x="490" y="322" class="t-ax" text-anchor="middle">Stil-Varianten</text>')
    o.append('<line x1="506" y1="56" x2="444" y2="52" class="wire-ink" marker-end="url(#arK)"/>')
    o.append('<text x="475" y="44" class="t-ax" text-anchor="middle">Module</text>')
    o.append('</svg>')
    return "\n".join(o)
