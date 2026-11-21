from figs import f
from figs2 import patchplan

# Kapitel 09 · Arrangement und Songform

def _defs(p):
    return ('<defs>'
            '<marker id="' + p + 'C" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fill-cv"/></marker>'
            '<marker id="' + p + 'K" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fill-ink"/></marker>'
            '<marker id="' + p + 'G" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fill-gate"/></marker>'
            '</defs>')


# ---------------- Zeitebenen ----------------
def fig_zeitebenen():
    W, H = 760, 330
    x0, x1 = 190, 744
    bars = 64
    bw = (x1 - x0) / bars
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Fünf Zeitebenen über 64 Takte: Takt, 4 Takte, 8 Takte als Phrase, 16 Takte und die ganze Form. Jede Ebene wird von einem anderen Teil des Pults gezählt. An jeder Phrasengrenze beginnt eine Bewegung schon vor dem Wechsel.">', _defs('z9')]
    rows = [("Takt", "Programm · 16 Steps", 1),
            ("4 Takte", "Arythmatik OUT 4", 4),
            ("8 Takte · Phrase", "PHRASE-Spur · Muxlicer", 8),
            ("16 Takte", "Flip · Speed /2", 16),
            ("64 Takte · Form", "Muxlicer, 8 Teile", 64)]
    y = 24
    for i, (lab, sub, n) in enumerate(rows):
        h = 30
        o.append(f'<text x="10" y="{y+14}" class="t-lab" style="font-size:15px">{lab}</text>')
        o.append(f'<text x="10" y="{y+29}" class="t-sub">{sub}</text>')
        k = 0
        for b in range(0, bars, n):
            cls = "sec-a" if k % 2 == 0 else "sec-b"
            o.append(f'<rect x="{f(x0+b*bw)}" y="{y}" width="{f(n*bw-1)}" height="{h}" class="{cls}" style="stroke:var(--line)"/>')
            k += 1
        if n == 8:
            for b in range(8, bars, 8):
                xb = x0 + b * bw
                o.append(f'<path d="M{f(xb-2*bw)},{y+h-3} L{f(xb)},{y+4}" class="sig sig-cv" style="stroke-width:2.2"/>')
        if n == 64:
            names = ["Intro", "Groove", "Thema", "Thema+", "Break", "Aufbau", "Peak", "Outro"]
            for j, nm in enumerate(names):
                o.append(f'<text x="{f(x0+(j*8+4)*bw)}" y="{y+20}" class="t-ax" text-anchor="middle">{nm}</text>')
                if j:
                    o.append(f'<line x1="{f(x0+j*8*bw)}" y1="{y}" x2="{f(x0+j*8*bw)}" y2="{y+h}" class="t-zero"/>')
        y += 52
    for b in range(0, bars + 1, 8):
        o.append(f'<text x="{f(x0+b*bw)}" y="{y+6}" class="t-ax" text-anchor="middle">{b+1 if b<bars else ""}</text>')
    o.append(f'<text x="{x0}" y="{y+24}" class="t-ax">Takt</text>')
    o.append(f'<text x="{x1}" y="{y+24}" class="t-ax lab-cv" text-anchor="end">orange: Bewegung, die vor der Phrasengrenze beginnt</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Matrix als Sequencer ----------------
SONG = [  # BD SD HH Stimme Rings Hall Hell Chaos, Energie
    ("Intro", [0, 0, 2, 0, 3, 4, 1, 0], 1),
    ("Groove", [3, 0, 2, 0, 3, 3, 2, 0], 2),
    ("Thema", [3, 0, 3, 4, 2, 2, 2, 1], 3),
    ("Thema+", [4, 2, 3, 4, 3, 2, 3, 2], 4),
    ("Break", [0, 0, 1, 0, 4, 5, 1, 0], 1),
    ("Aufbau", [1, 3, 4, 3, 3, 3, 3, 4], 4),
    ("Peak", [5, 3, 4, 5, 4, 2, 5, 1], 5),
    ("Outro", [3, 0, 4, 0, 2, 4, 1, 0], 1),
]
COLS = ["BD", "SD", "HH", "Stimme", "Rings", "Hall", "Hell", "Chaos"]


def fig_matrix9():
    W, H = 760, 470
    act = 3  # Teil 4 läuft
    gx, gy, cw, ch = 250, 70, 52, 38
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Der Muxlicer hebt das Gate des laufenden Teils, hier Teil 4. Dieses Gate liegt an Zeile 4 der 8×8-Matrix. Jede Spalte gibt nur den Regler der aktiven Zeile aus, so wird jede Spalte zu einem Sequencer mit acht Werten, einem pro Songteil.">', _defs('m9')]
    o.append('<text x="20" y="40" class="t-lab">Muxlicer</text>')
    o.append('<text x="20" y="56" class="t-sub">ein Gate pro Teil</text>')
    o.append(f'<text x="{gx}" y="40" class="t-lab">8×8 Matrix · Regler = Wert pro Teil</text>')
    for r, (nm, vals, e) in enumerate(SONG):
        y = gy + r * ch
        on = r == act
        o.append(f'<rect x="20" y="{y+4}" width="58" height="{ch-8}" rx="2" class="{"box-strong" if on else "box"}"/>')
        o.append(f'<text x="49" y="{y+ch/2+4}" class="t-ax" text-anchor="middle" style="fill:var(--ink)">Gate {r+1}</text>')
        o.append(f'<text x="92" y="{y+ch/2+4}" class="t-ax">{nm}</text>')
        o.append(f'<line x1="160" y1="{y+ch/2}" x2="{gx-6}" y2="{y+ch/2}" class="{"wire-gate" if on else "t-grid"}"' + (f' marker-end="url(#m9G)"' if on else '') + '/>')
        if on:
            o.append(f'<rect x="{gx-4}" y="{y+2}" width="{len(COLS)*cw+8}" height="{ch-4}" rx="3" style="fill:var(--gate-soft);stroke:var(--gate);stroke-width:1.5"/>')
        for c, v in enumerate(vals):
            cx = gx + c * cw + cw / 2
            cy = y + ch / 2
            o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="12" class="kn2"/>')
            ang = -135 + v / 5 * 270
            import math
            a = math.radians(ang - 90)
            o.append(f'<line x1="{f(cx)}" y1="{f(cy)}" x2="{f(cx+10*math.cos(a))}" y2="{f(cy+10*math.sin(a))}" class="kp2" style="stroke-width:2.4{";opacity:.45" if not on else ""}"/>')
    yb = gy + 8 * ch + 8
    for c, nm in enumerate(COLS):
        cx = gx + c * cw + cw / 2
        o.append(f'<line x1="{f(cx)}" y1="{yb}" x2="{f(cx)}" y2="{yb+30}" class="wire-cv" marker-end="url(#m9C)"/>')
        o.append(f'<text x="{f(cx)}" y="{yb+48}" class="t-ax" text-anchor="middle" style="fill:var(--ink)">{nm}</text>')
        o.append(f'<text x="{f(cx)}" y="{yb+64}" class="t-ax lab-cv" text-anchor="middle">{SONG[act][1][c]}</text>')
    o.append(f'<text x="{gx-14}" y="{yb+48}" class="t-ax" text-anchor="end">Spalte</text>')
    o.append(f'<text x="{gx-14}" y="{yb+64}" class="t-ax lab-cv" text-anchor="end">Ausgang jetzt</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Riser und andere Ankündigungen ----------------
def fig_riser():
    W, H = 760, 420
    x0, x1 = 200, 744
    bars = 6  # 4 vor, 2 nach der Grenze
    bw = (x1 - x0) / bars
    xb = x0 + 4 * bw
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Sechs Arten, eine Teilgrenze anzukündigen, über vier Takte davor und zwei danach: ein Rausch-Riser mit langem Anstieg und schnellem Abfall auf der Eins, ein Ratchet-Wirbel mit immer dichteren Schlägen, ein Swell auf Filter oder Hall-Send, eine Lücke im letzten Takt, ein Becken auf der Eins und ein Downlifter danach.">', _defs('r9')]
    for b in range(bars + 1):
        x = x0 + b * bw
        o.append(f'<line x1="{f(x)}" y1="16" x2="{f(x)}" y2="{H-40}" class="t-grid"/>')
    o.append(f'<rect x="{f(xb-1.5)}" y="12" width="3" height="{H-48}" class="fill-ink"/>')
    o.append(f'<text x="{f(xb)}" y="{H-14}" class="t-ax" text-anchor="middle" style="fill:var(--ink);font-weight:600">die Eins des neuen Teils</text>')
    for b, t in enumerate(["Takt 5", "Takt 6", "Takt 7", "Takt 8", "Takt 1", "Takt 2"]):
        o.append(f'<text x="{f(x0+b*bw+bw/2)}" y="{H-28}" class="t-ax" text-anchor="middle">{t}</text>')
    rows = [("Rausch-Riser", "Hüllkurve → VCA → Elements"),
            ("Ratchet-Wirbel", "Programm, letzter Takt"),
            ("Swell", "Cutoff oder Hall-Send"),
            ("Lücke", "alles stumm bis auf eins"),
            ("Becken auf der Eins", "PHRASE-Spur → Samples II"),
            ("Downlifter", "fallende Hüllkurve danach")]
    rh = 56
    for i, (lab, sub) in enumerate(rows):
        y = 22 + i * rh
        base = y + 40
        top = y + 6
        o.append(f'<text x="10" y="{y+20}" class="t-lab" style="font-size:15px">{lab}</text>')
        o.append(f'<text x="10" y="{y+36}" class="t-sub">{sub}</text>')
        if i == 0:
            xs = xb - 2 * bw
            d = f"M{f(x0)},{base} L{f(xs)},{base} "
            n = 24
            for k in range(1, n + 1):
                t = k / n
                d += f"L{f(xs+t*2*bw)},{f(base-(base-top)*t**2)} "
            d += f"L{f(xb+0.12*bw)},{base} L{f(x1)},{base}"
            o.append(f'<path d="{d}" class="sig sig-cv"/>')
        elif i == 1:
            hits = [0, 1, 2, 3, 4, 5, 6, 7] + [8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5] + [12 + k / 4 for k in range(16)]
            for hpos in hits:
                if hpos >= 16:
                    continue
                x = x0 + (hpos / 16) * 4 * bw
                o.append(f'<line x1="{f(x)}" y1="{base}" x2="{f(x)}" y2="{top+8}" class="sig sig-trig" style="stroke-width:1.6"/>')
            for hpos in [0, 4, 8, 12]:
                x = xb + hpos / 16 * 2 * bw
                o.append(f'<line x1="{f(x)}" y1="{base}" x2="{f(x)}" y2="{top+8}" class="sig sig-trig" style="stroke-width:1.6"/>')
        elif i == 2:
            xs = xb - 2 * bw
            d = f"M{f(x0)},{base-6} L{f(xs)},{base-6} L{f(xb)},{top} "
            n = 16
            for k in range(1, n + 1):
                t = k / n
                d += f"L{f(xb+t*1.2*bw)},{f(top+(base-6-top)*(1-(1-t)**2))} "
            d += f"L{f(x1)},{base-6}"
            o.append(f'<path d="{d}" class="sig sig-cv"/>')
        elif i == 3:
            for b in range(bars):
                if b == 3:
                    o.append(f'<rect x="{f(x0+b*bw+bw*0.75)}" y="{top+6}" width="{f(bw*0.22)}" height="{base-top-6}" rx="2" class="fill-audio" style="opacity:.8"/>')
                    continue
                o.append(f'<rect x="{f(x0+b*bw+3)}" y="{top+6}" width="{f(bw-6)}" height="{base-top-6}" rx="2" class="fill-audio" style="opacity:{.35 if b<3 else .8}"/>')
        elif i == 4:
            for b in range(4):
                x = x0 + b * bw
                o.append(f'<line x1="{f(x)}" y1="{base}" x2="{f(x)}" y2="{top+20}" class="sig sig-trig" style="stroke-width:1.3;opacity:.4"/>')
            o.append(f'<line x1="{f(xb)}" y1="{base}" x2="{f(xb)}" y2="{top}" class="sig sig-trig" style="stroke-width:3"/>')
        elif i == 5:
            d = f"M{f(x0)},{base} L{f(xb)},{base} L{f(xb+2)},{top} "
            n = 16
            for k in range(1, n + 1):
                t = k / n
                d += f"L{f(xb+2+t*1.6*bw)},{f(top+(base-top)*(1-(1-t)**3))} "
            d += f"L{f(x1)},{base}"
            o.append(f'<path d="{d}" class="sig sig-cv"/>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Spannungsbögen ----------------
def fig_boegen():
    W, H = 760, 230
    pw, gap = 236, 26
    curves = [("Bogen", "ein Höhepunkt im letzten Drittel", [1, 2, 3, 3, 4, 4, 5, 2]),
              ("Treppe mit Bruch", "jeder Teil etwas mehr, dann ein Break", [1, 2, 3, 4, 1, 4, 5, 1]),
              ("Zwei Wellen", "Höhepunkt, Ruhe, größerer Höhepunkt", [1, 3, 4, 2, 1, 3, 5, 1])]
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Drei typische Energieverläufe über acht Songteile: ein Bogen mit Höhepunkt im letzten Drittel, eine Treppe mit Break und eine Form mit zwei Wellen, deren zweite höher ist.">']
    for i, (t, s, v) in enumerate(curves):
        x0 = 12 + i * (pw + gap)
        y0, h = 54, 130
        o.append(f'<text x="{x0}" y="20" class="t-lab">{t}</text>')
        o.append(f'<text x="{x0}" y="38" class="t-sub">{s}</text>')
        o.append(f'<rect x="{x0}" y="{y0}" width="{pw}" height="{h}" class="sec-a" style="stroke:var(--line)"/>')
        sw = pw / 8
        for k in range(1, 8):
            o.append(f'<line x1="{f(x0+k*sw)}" y1="{y0}" x2="{f(x0+k*sw)}" y2="{y0+h}" class="t-grid"/>')
        d = ""
        for k, e in enumerate(v):
            yy = y0 + h - e / 5 * (h - 12) - 4
            d += (f"M{f(x0+k*sw)},{f(yy)}" if k == 0 else f" L{f(x0+k*sw)},{f(yy)}") + f" L{f(x0+(k+1)*sw)},{f(yy)}"
            o.append(f'<rect x="{f(x0+k*sw+2)}" y="{f(yy)}" width="{f(sw-4)}" height="{f(y0+h-yy)}" class="fill-cv" style="opacity:.16"/>')
        o.append(f'<path d="{d}" class="sig sig-cv" style="stroke-width:2.4"/>')
        for k in range(8):
            o.append(f'<text x="{f(x0+k*sw+sw/2)}" y="{y0+h+16}" class="t-ax" text-anchor="middle">{k+1}</text>')
    o.append(f'<text x="12" y="{H-6}" class="t-ax">Teil 1–8 · Höhe = Energie, also der Fader am Muxlicer</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Patchplan Kapitel 09 ----------------
def pp_ch9():
    M = {}

    def mod(i, x, y, w, h, t, s, st, jacks):
        M[i] = dict(x=x, y=y, w=w, h=h, title=t, sub=s, st=st, jacks=jacks)
    ALL = "9A 9B 9C"
    B = "9B 9C"
    C = "9C"
    mod("exq", 20, 20, 150, 80, "Exquis", "MIDI-Controller", C, {"o": ("MIDI OUT", 155, 72, "o", "l")})
    mod("prog", 20, 120, 150, 360, "Programm", "Spuren 3, 4 · Seq.2", ALL, {
        "midi": ("MIDI IN", 35, 172, "i", "r"), "chance": ("CHANCE IN", 35, 212, "i", "r"),
        "d3": ("DRUM 3", 155, 260, "o", "l"), "d4": ("DRUM 4", 155, 300, "o", "l"), "rst": ("RESET OUT", 155, 340, "o", "l"),
        "s2p": ("SEQ.2 PITCH", 155, 400, "o", "l"), "s2g": ("SEQ.2 GATE", 155, 440, "o", "l")})
    mod("noise", 20, 510, 150, 80, "A-118-2", "Rauschen", ALL, {"o": ("C NOISE", 155, 562, "o", "l")})
    mod("f281", 215, 20, 130, 110, "281t", "Kanal 3 · Riser", ALL, {"t": ("TRIG 3", 230, 72, "i", "r"), "o": ("OUT 3", 330, 102, "o", "l")})
    mod("multb", 215, 200, 130, 130, "2×4 Mult", "Teil B", B, {"in": ("IN", 230, 252, "i", "r"), "a": ("", 330, 266, "o", "l"), "b": ("", 330, 300, "o", "l")})
    mod("logic", 215, 350, 130, 130, "Logic", "auf OR", B, {"ina": ("IN A", 230, 402, "i", "r"), "inb": ("IN B", 230, 442, "i", "r"), "o": ("OUT", 330, 422, "o", "l")})
    mod("att", 395, 20, 140, 110, "Attenuverter", "Reihe 4 · A", ALL, {"in": ("IN A", 410, 72, "i", "r"), "o": ("OUT A", 520, 102, "o", "l")})
    mod("mux", 395, 230, 140, 260, "Muxlicer", "Songpult", B, {"clk": ("CLOCK IN", 410, 282, "i", "r"), "rst": ("RESET", 410, 342, "i", "r"),
                                                                "eoc": ("EOC", 520, 312, "o", "l"), "g": ("GATE 1–8", 520, 372, "o", "l"), "com": ("COM I/O", 520, 452, "o", "l")})
    mod("vca", 585, 20, 150, 180, "A-130-8", "Kanal 3 · Kanal 1", ALL, {"in3": ("IN 3", 600, 72, "i", "r"), "cv3": ("CV 3", 600, 112, "i", "r"),
                                                                       "o3": ("OUT 3", 720, 92, "o", "l"), "o1": ("OUT 1", 720, 172, "o", "l")})
    mxj = {"in": ("IN 1–8", 600, 372, "i", "r")}
    for k in range(8):
        mxj["o%d" % (k + 1)] = ("OUT %d" % (k + 1), 720, 282 + 36 * k, "o", "l")
    mod("mx", 585, 230, 150, 340, "8×8 Matrix", "Zeile = Teil", B, mxj)
    mod("rings", 585, 600, 150, 130, "Rings", "Arp vom Exquis", C, {"v": ("V/OCT", 600, 652, "i", "r"), "s": ("STRUM", 600, 700, "i", "r"), "o": ("ODD", 720, 676, "o", "l")})
    mod("elem", 785, 20, 150, 95, "Elements", "Resonator", ALL, {"in": ("STRIKE IN", 800, 72, "i", "r"), "o": ("OUT R", 920, 90, "o", "l")})
    mod("samp", 785, 125, 150, 70, "Samples II", "Kanal 5 · Becken", ALL, {"t": ("TRIG 5", 800, 177, "i", "r")})
    mod("grids", 785, 210, 150, 180, "mGrids", "Fill und Chaos", B, {"bd": ("FILL BD", 800, 262, "i", "r"), "sd": ("FILL SD", 800, 296, "i", "r"),
                                                                    "hh": ("FILL HH", 800, 330, "i", "r"), "ch": ("CHAOS", 800, 364, "i", "r")})
    mod("fp3", 785, 405, 150, 200, "FOUR PLAY", "Reihe 3 · Stimmen", B, {"in1": ("IN 1", 800, 457, "i", "r"), "cv1": ("CV 1", 800, 492, "i", "r"), "o1": ("OUT 1", 920, 474, "o", "l"),
                                                                        "in2": ("IN 2", 800, 532, "i", "r"), "cv2": ("CV 2", 800, 567, "i", "r"), "o2": ("OUT 2", 920, 550, "o", "l")})
    mod("fp4", 785, 620, 150, 70, "FOUR PLAY", "Reihe 4 · Hall-Send", B, {"cv": ("CV 1", 800, 672, "i", "r")})
    mod("sem", 785, 705, 150, 70, "A-106-5 SEM", "Helligkeit", B, {"cv": ("CV1 IN", 800, 757, "i", "r")})
    mod("multa", 965, 430, 105, 80, "2×4 Mult", "Teil A", B, {"in": ("IN", 980, 482, "i", "r")})
    mod("l6", 1100, 20, 100, 760, "L6", "über Fader", ALL, {"k5": ("K5", 1115, 82, "i", "r"), "k6": ("K6", 1115, 550, "i", "r")})
    Cb = [
        (1, "trig", ("prog", "d4"), ("f281", "t"), ALL),
        (2, "cv", ("f281", "o"), ("att", "in"), ALL),
        (3, "cv", ("att", "o"), ("vca", "cv3"), ALL),
        (4, "audio", ("noise", "o"), ("vca", "in3"), ALL),
        (5, "audio", ("vca", "o3"), ("elem", "in"), ALL),
        (6, "audio", ("elem", "o"), ("l6", "k5"), ALL),
        (7, "trig", ("prog", "d3"), ("samp", "t"), "9A"),
        (8, "trig", ("prog", "d3"), ("multb", "in"), B),
        (9, "trig", ("multb", "a"), ("samp", "t"), B),
        (10, "trig", ("multb", "b"), ("mux", "clk"), B),
        (11, "trig", ("prog", "rst"), ("logic", "ina"), B),
        (12, "trig", ("mux", "eoc"), ("logic", "inb"), B),
        (13, "trig", ("logic", "o"), ("mux", "rst"), B),
        (14, "gate", ("mux", "g"), ("mx", "in"), B),
        (15, "cv", ("mx", "o1"), ("grids", "bd"), B),
        (16, "cv", ("mx", "o2"), ("grids", "sd"), B),
        (17, "cv", ("mx", "o3"), ("grids", "hh"), B),
        (18, "audio", ("vca", "o1"), ("fp3", "in1"), B),
        (19, "audio", ("fp3", "o1"), ("multa", "in"), B),
        (20, "cv", ("mx", "o4"), ("fp3", "cv1"), B),
        (21, "cv", ("mx", "o6"), ("fp4", "cv"), B),
        (22, "cv", ("mx", "o7"), ("sem", "cv"), B),
        (23, "cv", ("mx", "o8"), ("grids", "ch"), B),
        (24, "cv", ("mux", "com"), ("prog", "chance"), B),
        (25, "midi", ("exq", "o"), ("prog", "midi"), C),
        (26, "cv", ("prog", "s2p"), ("rings", "v"), C),
        (27, "gate", ("prog", "s2g"), ("rings", "s"), C),
        (28, "audio", ("rings", "o"), ("fp3", "in2"), C),
        (29, "audio", ("fp3", "o2"), ("l6", "k6"), C),
        (30, "cv", ("mx", "o5"), ("fp3", "cv2"), C),
    ]
    return patchplan(1240, 795, M, Cb, "9A",
                     "Patchplan Kapitel 09: In Stufe 9A startet Programm-Spur 4 kurz vor jeder Phrasengrenze den 281t, dessen langsamer Anstieg über einen Attenuverter einen A-130-8-Kanal öffnet, der Rauschen in Elements schickt. Spur 3 schlägt auf jeder Eins ein Becken an. In Stufe 9B taktet Spur 3 den Muxlicer, seine acht Gates laufen in die 8×8-Matrix, deren Spalten Grids-Fills, Chaos, zwei FOUR-PLAY-Kanäle und das SEM-Filter pro Songteil einstellen; die Fader gehen in Chance In. In Stufe 9C spielt der Exquis über MIDI den Arpeggiator von Seq.2, der Rings anstößt; Matrix-Spalte 5 blendet Rings ein und aus.")
