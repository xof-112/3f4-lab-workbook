import math
from figs import f
from figs2 import patchplan

# Kapitel 08 · FX, Feedback und räumlicher Klang

PFX = ['e8']
def ARROWS_(p):
    PFX[0] = p
    return ('<defs>'
          '<marker id="'+p+'A" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fill-audio"/></marker>'
          '<marker id="'+p+'C" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fill-cv"/></marker>'
          '<marker id="'+p+'K" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fill-ink"/></marker>'
          '</defs>')


def _box(o, x, y, w, h, t, s=None, cls="box"):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" class="{cls}"/>')
    o.append(f'<text x="{x+10}" y="{y+22}" class="t-lab">{t}</text>')
    if s:
        o.append(f'<text x="{x+10}" y="{y+38}" class="t-sub">{s}</text>')


def _arr(o, x1, y1, x2, y2, kind="audio"):
    m = PFX[0] + {"audio": "A", "cv": "C", "ink": "K"}[kind]
    cls = {"audio": "wire-audio", "cv": "wire-cv", "ink": "wire-ink"}[kind]
    o.append(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" class="{cls}" marker-end="url(#{m})"/>')


def _path(o, d, kind="audio", arrow=True):
    m = PFX[0] + {"audio": "A", "cv": "C", "ink": "K"}[kind]
    cls = {"audio": "wire-audio", "cv": "wire-cv", "ink": "wire-ink"}[kind]
    mk = f' marker-end="url(#{m})"' if arrow else ""
    o.append(f'<path d="{d}" fill="none" class="{cls}"{mk}/>')


# ---------------- Insert, Send/Return, Parallel ----------------
def fig_fxroute():
    W, H = 760, 400
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Drei Arten, einen Effekt einzubinden: Insert in Reihe mit Dry/Wet am Effekt, Send/Return mit einem Abzweig über einen VCA und 100 Prozent nassem Effekt, der am Mischpult zum trockenen Signal kommt, und die Rückkopplung, bei der ein Teil des Ausgangs wieder in den Eingang läuft.">', ARROWS_('e8x')]
    # Reihe 1: Insert
    y = 30
    o.append(f'<text x="20" y="{y}" class="t-lab">Insert</text>')
    o.append(f'<text x="20" y="{y+16}" class="t-sub">in Reihe</text>')
    _box(o, 130, y - 18, 120, 52, "Quelle")
    _box(o, 330, y - 18, 160, 52, "Effekt", "Dry/Wet am Effekt")
    _box(o, 570, y - 18, 150, 52, "L6", "ein Kanal")
    _arr(o, 250, y + 8, 326, y + 8)
    _arr(o, 490, y + 8, 566, y + 8)
    # Reihe 2: Send/Return
    y = 150
    o.append(f'<text x="20" y="{y}" class="t-lab">Send</text>')
    o.append(f'<text x="20" y="{y+16}" class="t-sub">parallel</text>')
    _box(o, 130, y - 18, 120, 52, "Quelle")
    o.append(f'<circle cx="290" cy="{y+8}" r="5" class="fill-audio"/>')
    o.append(f'<text x="290" y="{y-6}" class="t-ax" text-anchor="middle">Mult</text>')
    o.append(f'<line x1="250" y1="{y+8}" x2="290" y2="{y+8}" class="wire-audio"/>')
    _arr(o, 290, y + 8, 566, y + 8)
    o.append(f'<text x="430" y="{y}" class="t-ax" text-anchor="middle">trocken</text>')
    _box(o, 330, y + 50, 100, 52, "VCA", "Send")
    _box(o, 450, y + 50, 100, 52, "Effekt", "100 % nass", "box box-strong")
    _path(o, f"M290,{y+8} L290,{y+76} L326,{y+76}")
    _arr(o, 430, y + 76, 446, y + 76)
    _path(o, f"M550,{y+76} L600,{y+76} L600,{y+38}")
    _box(o, 570, y - 18, 150, 52, "L6", "trocken + Return")
    o.append(f'<text x="608" y="{y+70}" class="t-ax">Return</text>')
    _arr(o, 380, y + 140, 380, y + 106, "cv")
    o.append(f'<text x="388" y="{y+136}" class="t-ax">Throw: Hüllkurve, Gate</text>')
    # Reihe 3: Rückkopplung
    y = 330
    o.append(f'<text x="20" y="{y}" class="t-lab">Schleife</text>')
    o.append(f'<text x="20" y="{y+16}" class="t-sub">Rückkopplung</text>')
    _box(o, 130, y - 18, 120, 52, "Quelle")
    o.append(f'<circle cx="300" cy="{y+8}" r="12" class="box"/><text x="300" y="{y+13}" class="t-ax" text-anchor="middle" style="fill:var(--ink)">+</text>')
    _arr(o, 250, y + 8, 286, y + 8)
    _box(o, 340, y - 18, 130, 52, "Delay", "Zeit")
    _arr(o, 312, y + 8, 336, y + 8)
    _arr(o, 470, y + 8, 566, y + 8)
    _box(o, 570, y - 18, 150, 52, "L6")
    _path(o, f"M520,{y+8} L520,{y+52} L470,{y+52}")
    _box(o, 360, y + 36, 110, 30, "")
    o.append(f'<text x="415" y="{y+56}" class="t-ax" text-anchor="middle" style="fill:var(--ink)">Filter · VCA = g</text>')
    _path(o, f"M360,{y+52} L300,{y+52} L300,{y+22}")
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Echos über der Zeit, Taps ----------------
def fig_echoes():
    W, H = 760, 330
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Zwei Echoreihen über vier Sekunden. Oben ein einfaches Delay mit Rückkopplung 0,6: jede Wiederholung kommt nach derselben Zeit und ist um denselben Faktor leiser. Unten die vier Taps des Morphor Echo bei einem Viertel, der Hälfte, drei Vierteln und der vollen Zeit; mit Rückkopplung über Tap 4 wiederholt sich das ganze Muster leiser.">']
    x0, x1 = 70, 740
    T = 4.0
    sx = lambda t: x0 + t / T * (x1 - x0)
    for k in range(0, 9):
        t = k * 0.5
        o.append(f'<line x1="{f(sx(t))}" y1="20" x2="{f(sx(t))}" y2="290" class="t-grid"/>')
        o.append(f'<text x="{f(sx(t))}" y="306" class="t-ax" text-anchor="middle">{str(t).replace(".", ",")} s</text>')
    # oben: einfaches Delay
    base = 135
    o.append(f'<text x="10" y="40" class="t-lab">Delay</text>')
    o.append(f'<text x="10" y="56" class="t-sub">T 0,5 s</text>')
    o.append(f'<text x="10" y="70" class="t-sub">g 0,6</text>')
    o.append(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" class="t-zero"/>')
    for n in range(0, 9):
        a = 0.6 ** n
        h = a * 100
        cls = "fill-ink" if n == 0 else "fill-audio"
        o.append(f'<rect x="{f(sx(n*0.5)-4)}" y="{f(base-h)}" width="8" height="{f(h)}" class="{cls}"/>')
        if n in (1, 2, 4):
            db = 20 * math.log10(a)
            o.append(f'<text x="{f(sx(n*0.5)+8)}" y="{f(base-h-4)}" class="t-ax">{f(db).replace(".", ",")} dB</text>')
    # unten: Taps
    base = 280
    o.append(f'<text x="10" y="185" class="t-lab">Taps</text>')
    o.append(f'<text x="10" y="201" class="t-sub">Zeit 2 s</text>')
    o.append(f'<text x="10" y="215" class="t-sub">g 0,5</text>')
    o.append(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" class="t-zero"/>')
    o.append(f'<rect x="{f(sx(0)-4)}" y="{base-100}" width="8" height="100" class="fill-ink"/>')
    lv = [0.8, 0.65, 0.5, 0.9]
    for rnd in range(2):
        for i in range(4):
            t = rnd * 2 + (i + 1) * 0.5
            if t > T:
                continue
            a = lv[i] * (0.5 ** rnd)
            h = a * 100
            cls = "fill-cv" if i == 3 else "fill-audio"
            o.append(f'<rect x="{f(sx(t)-4)}" y="{f(base-h)}" width="8" height="{f(h)}" class="{cls}"/>')
            if rnd == 0:
                o.append(f'<text x="{f(sx(t))}" y="{f(base-h-6)}" class="t-ax" text-anchor="middle">Tap {i+1}</text>')
    o.append(f'<text x="{f(sx(2.5)+10)}" y="{base-62}" class="t-ax">ab hier: Tap 4 zurück, Muster × 0,5</text>')
    o.append(f'<text x="{x0}" y="{H-4}" class="t-ax">Schwarz: Anschlag · blau: Wiederholung · orange: Tap 4, der zurückgeführt wird</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Phaser und Flanger ----------------
def fig_comb():
    W, H = 760, 300
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Frequenzgang auf logarithmischer Achse. Oben ein Flanger mit 2 Millisekunden Verzögerung: Kerben im gleichen Abstand von 500 Hertz, die nach oben immer dichter wirken. Unten ein Phaser mit vier Allpass-Stufen: nur zwei Kerben, unregelmäßig verteilt.">']
    x0, x1 = 60, 740
    lo, hi = math.log10(50), math.log10(16000)
    sx = lambda fr: x0 + (math.log10(fr) - lo) / (hi - lo) * (x1 - x0)
    for fr, lab in ((100, "100"), (300, "300"), (1000, "1k"), (3000, "3k"), (10000, "10k")):
        o.append(f'<line x1="{f(sx(fr))}" y1="20" x2="{f(sx(fr))}" y2="262" class="t-grid"/>')
        o.append(f'<text x="{f(sx(fr))}" y="278" class="t-ax" text-anchor="middle">{lab} Hz</text>')

    def curve(fn, ytop, h):
        pts = []
        for k in range(0, 601):
            fr = 10 ** (lo + k / 600 * (hi - lo))
            m = fn(fr)
            pts.append(f"{f(sx(fr))},{f(ytop + h - m * h)}")
        o.append(f'<polyline points="{" ".join(pts)}" class="sig sig-audio" style="stroke-width:1.6"/>')
        o.append(f'<line x1="{x0}" y1="{ytop+h}" x2="{x1}" y2="{ytop+h}" class="t-zero"/>')

    tau = 0.002
    curve(lambda fr: abs(math.cos(math.pi * fr * tau)), 30, 95)
    o.append(f'<text x="10" y="50" class="t-lab">Flanger</text>')
    o.append(f'<text x="10" y="66" class="t-sub">2 ms + trocken</text>')
    fc = 700.0

    def phaser(fr):
        ph = 4 * 2 * math.atan(fr / fc)
        return abs(math.cos(ph / 2))
    curve(phaser, 160, 95)
    o.append(f'<text x="10" y="180" class="t-lab">Phaser</text>')
    o.append(f'<text x="10" y="196" class="t-sub">4 Allpässe</text>')
    o.append(f'<text x="{x0}" y="{H-4}" class="t-ax">Die Kerben wandern, wenn ein LFO die Verzögerung (Flanger) oder die Allpass-Frequenz (Phaser) bewegt.</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Frequency Shifting vs. Pitch Shifting ----------------
def fig_shift():
    W, H = 760, 300
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Drei Spektren eines Tons mit 100 Hertz Grundton. Original: Teiltöne bei 100, 200, 300 Hertz und so weiter. Pitch-Shift um eine Quinte: alle mal 1,5, die Abstände wachsen mit, der Ton bleibt harmonisch. Frequency Shift um 50 Hertz: alle plus 50, die Abstände bleiben 100 Hertz, die Teiltöne liegen nicht mehr auf Vielfachen eines Grundtons.">']
    x0, x1 = 150, 740
    fmax = 1300
    sx = lambda fr: x0 + fr / fmax * (x1 - x0)
    rows = [("Original", "100 Hz", lambda n: 100 * n, "fill-ink"),
            ("Pitch-Shift", "× 1,5 · Quinte", lambda n: 150 * n, "fill-audio"),
            ("Frequency Shift", "+ 50 Hz", lambda n: 100 * n + 50, "fill-cv")]
    for r, (t, s, fn, cls) in enumerate(rows):
        base = 80 + r * 80
        o.append(f'<text x="10" y="{base-30}" class="t-lab">{t}</text>')
        o.append(f'<text x="10" y="{base-14}" class="t-sub">{s}</text>')
        o.append(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" class="t-zero"/>')
        for n in range(1, 13):
            fr = fn(n)
            if fr > fmax:
                break
            h = 50 / n ** 0.6
            o.append(f'<rect x="{f(sx(fr)-3)}" y="{f(base-h)}" width="6" height="{f(h)}" class="{cls}"/>')
            if n <= 3:
                o.append(f'<text x="{f(sx(fr))}" y="{base+13}" class="t-ax" text-anchor="middle">{fr}</text>')
    for fr in range(0, fmax + 1, 200):
        o.append(f'<line x1="{f(sx(fr))}" y1="268" x2="{f(sx(fr))}" y2="274" class="t-zero"/>')
        o.append(f'<text x="{f(sx(fr))}" y="288" class="t-ax" text-anchor="middle">{fr}</text>')
    o.append(f'<text x="{x0-8}" y="288" class="t-ax" text-anchor="end">Hz</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Schleifenverstärkung ----------------
def fig_loopgain():
    W, H = 760, 236
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Pegel der Wiederholungen bei vier Schleifenverstärkungen. Bei 0,5 klingt es schnell aus, bei 0,9 lange, bei 1,0 bleibt es stehen, bei 1,1 wächst es, bis eine Stufe begrenzt und es als verzerrte Fläche stehen bleibt.">']
    cases = [(0.5, "g 0,5", "schnell aus"), (0.9, "g 0,9", "lange Fahne"), (1.0, "g 1,0", "steht"), (1.1, "g 1,1", "wächst bis zur Grenze")]
    for i, (g, t, s) in enumerate(cases):
        x0 = 20 + i * 185
        w = 165
        base = 200
        top = 60
        o.append(f'<text x="{x0}" y="22" class="t-lab">{t}</text>')
        o.append(f'<text x="{x0}" y="38" class="t-sub">{s}</text>')
        o.append(f'<line x1="{x0}" y1="{base}" x2="{x0+w}" y2="{base}" class="t-zero"/>')
        lim_y = base - 1.6 * 80
        o.append(f'<line x1="{x0}" y1="{f(lim_y)}" x2="{x0+w}" y2="{f(lim_y)}" class="mark-euro"/>')
        a = 1.0
        for n in range(12):
            h = min(a, 1.6) * 80
            cls = "fill-cv" if a >= 1.6 else "fill-audio"
            o.append(f'<rect x="{f(x0+4+n*13.5)}" y="{f(base-h)}" width="8" height="{f(h)}" class="{cls}"/>')
            a *= g
    o.append(f'<text x="20" y="226" class="t-ax">Orange gestrichelt: Grenze der Schaltung · g = VCA × Filter × Effekt</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Sicherheitskette ----------------
def fig_safety():
    W, H = 760, 234
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Sicherheitskette einer Rückkopplung bis zum L6: Feedback-VCA in der Schleife, Hochpass gegen Bässe und Gleichspannung, ein Begrenzer, danach der Passivfader und der L6-Kanal. Zu jeder Stufe steht, was sie schützt.">', ARROWS_('e8y')]
    items = [("Feedback-VCA", "von null an", "Schleife"), ("Hochpass", "Bass, DC", "Schleife"),
             ("Begrenzer", "Sättigung", "Schleife"), ("Passivfader", "schützt den L6", "Rack → L6"),
             ("L6-Kanal", "nur Abhören", "Pult")]
    for i, (t, s, z) in enumerate(items):
        x = 20 + i * 148
        cls = "box box-strong" if i < 3 else "box"
        _box(o, x, 70, 128, 60, t, s, cls)
        o.append(f'<text x="{x+64}" y="58" class="t-ax" text-anchor="middle">{z}</text>')
        if i < 4:
            _arr(o, x + 128, 100, x + 146, 100)
    _path(o, "M404,130 L404,170 L84,170 L84,134", "audio")
    o.append('<text x="244" y="188" class="t-ax" text-anchor="middle">zurück in den Effekt</text>')
    o.append('<text x="20" y="222" class="t-ax">Orange: regelt die Schleife · grau: schützt nur Aufnahme und Ohren</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Panorama der Taps ----------------
def fig_pan():
    W, H = 760, 230
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Wo die vier Taps des Morphor Echo im Stereobild liegen. Ping-Pong: abwechselnd links und rechts. Traverse: Tap 1 und Tap 4 außen, Tap 2 und 3 dazwischen, die Echos wandern hinüber. Chaos: jeder Tap mit zufälligem Pegel pro Seite.">']
    x0, x1 = 160, 700
    rows = [("Ping-Pong", "abwechselnd", [-1, 1, -0.84, 0.84]), ("Traverse", "wandert", [-1, -1 / 3, 1 / 3, 1]),
            ("Chaos", "zufällig", [0.35, -0.8, 0.6, -0.1])]
    for r, (t, s, pos) in enumerate(rows):
        y = 50 + r * 60
        o.append(f'<text x="10" y="{y}" class="t-lab">{t}</text>')
        o.append(f'<text x="10" y="{y+16}" class="t-sub">{s}</text>')
        o.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" class="t-grid"/>')
        o.append(f'<line x1="{(x0+x1)/2}" y1="{y-8}" x2="{(x0+x1)/2}" y2="{y+8}" class="t-zero"/>')
        for i, p in enumerate(pos):
            x = (x0 + x1) / 2 + p * (x1 - x0) / 2 * 0.92
            cls = "fill-cv" if i == 3 else "fill-audio"
            o.append(f'<circle cx="{f(x)}" cy="{y}" r="11" class="{cls}"/>')
            o.append(f'<text x="{f(x)}" y="{y+4}" class="t-ax" text-anchor="middle" style="fill:var(--surface)">{i+1}</text>')
    o.append(f'<text x="{x0}" y="{H-24}" class="t-ax">L</text><text x="{(x0+x1)/2}" y="{H-24}" class="t-ax" text-anchor="middle">Mitte</text><text x="{x1}" y="{H-24}" class="t-ax" text-anchor="end">R</text>')
    o.append(f'<text x="{x0}" y="{H-6}" class="t-ax">SPREAD: Breite · Mitte = mono · negativ = Reihenfolge umgekehrt</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Patchplan Kapitel 08 ----------------
def pp_ch8():
    M = {}

    def mod(i, x, y, w, h, t, s, st, jacks):
        M[i] = dict(x=x, y=y, w=w, h=h, title=t, sub=s, st=st, jacks=jacks)
    ALL = "8A 8B 8C"
    B = "8B 8C"
    C = "8C"
    mod("v2a", 20, 20, 150, 80, "Stimme 2A", "A-130-8 Kanal 1", ALL, {"o": ("OUT 1", 155, 72, "o", "l")})
    mod("f281", 20, 130, 150, 80, "281t", "Kanal 4 · Throw", ALL, {"o": ("OUT 4", 155, 182, "o", "l")})
    mod("prog", 20, 240, 150, 80, "Programm", "Zählspur", B, {"o": ("DRUM 2", 155, 292, "o", "l")})
    mod("lfo", 20, 540, 150, 80, "FOUR LFO", "langsam", C, {"o": ("OUT 1", 155, 592, "o", "l")})
    mod("multa", 215, 20, 130, 150, "2×4 Mult", "Teil A", ALL, {"in": ("IN", 230, 72, "i", "r"), "a": ("", 330, 72, "o", "l"), "b": ("", 330, 107, "o", "l"), "c": ("", 330, 142, "o", "l")})
    mod("att", 215, 360, 130, 150, "Attenuverter", "Reihe 4", B, {"ina": ("IN A", 230, 410, "i", "r"), "oa": ("OUT A", 330, 425, "o", "l"), "inb": ("IN B", 230, 470, "i", "r"), "ob": ("OUT B", 330, 485, "o", "l")})
    mod("fp4", 395, 20, 140, 150, "FOUR PLAY", "Reihe 4 · Send", ALL, {"in": ("IN 1", 410, 72, "i", "r"), "cv": ("CV 1", 410, 122, "i", "r"), "o": ("OUT 1", 520, 97, "o", "l")})
    mod("vca2", 395, 360, 140, 130, "A-130-8", "Kanal 2 · Feedback", B, {"in": ("IN 2", 410, 410, "i", "r"), "cv": ("CV 2", 410, 455, "i", "r"), "o": ("OUT 2", 520, 432, "o", "l")})
    mod("fp3", 395, 540, 140, 170, "FOUR PLAY", "Reihe 3 · Loop", C, {"in1": ("IN 1", 410, 590, "i", "r"), "in2": ("IN 2", 410, 670, "i", "r"), "o2": ("OUT 2", 520, 630, "o", "l")})
    mod("echo", 585, 20, 150, 230, "Morphor Echo", "Delay", B, {"in": ("IN", 600, 72, "i", "r"), "sync": ("SYNC", 600, 122, "i", "r"), "fb": ("FB IN", 600, 172, "i", "r"),
                                                                "l": ("ALL L", 720, 82, "o", "l"), "r": ("ALL R", 720, 122, "o", "l"), "t4": ("TAP 4", 720, 202, "o", "l")})
    mod("surg", 585, 270, 150, 80, "Surges", "Tiefpass", B, {"in": ("IN 1", 600, 322, "i", "r"), "lp": ("LP", 720, 310, "o", "l")})
    mod("bode", 585, 540, 150, 150, "Bode 1630", "Shifter", C, {"sig": ("SIG IN", 600, 590, "i", "r"), "ctrl": ("CTRL 1", 600, 650, "i", "r"), "oa": ("OUT A", 720, 600, "o", "l"), "ob": ("OUT B", 720, 660, "o", "l")})
    mod("mw", 785, 20, 150, 150, "Milky Way", "Hall", ALL, {"i1": ("IN 1", 800, 72, "i", "r"), "i2": ("IN 2", 800, 122, "i", "r"), "o1": ("OUT 1", 920, 82, "o", "l"), "o2": ("OUT 2", 920, 132, "o", "l")})
    mod("lyra", 785, 400, 150, 80, "Lyra-8 FX", "Delay + Drive", C, {"in": ("IN", 800, 452, "i", "r"), "o": ("OUT", 920, 440, "o", "l")})
    mod("wasp", 785, 510, 150, 80, "Wasp", "Hochpass", C, {"in": ("IN", 800, 562, "i", "r"), "o": ("LP/HP", 920, 550, "o", "l")})
    mod("multb", 965, 520, 105, 120, "2×4 Mult", "Teil B", C, {"in": ("IN", 980, 572, "i", "r"), "a": ("", 1055, 590, "o", "l"), "b": ("", 1055, 622, "o", "l")})
    mod("l6", 1100, 20, 100, 700, "L6", "über Fader", ALL, {"k1": ("K1 · L", 1115, 82, "i", "r"), "k2": ("K2 · R", 1115, 132, "i", "r"), "k3": ("K3 · M", 1115, 230, "i", "r"),
                                                         "k4": ("K4 · L", 1115, 600, "i", "r"), "k5": ("K5 · R", 1115, 670, "i", "r")})
    Cb = [
        (1, "audio", ("v2a", "o"), ("multa", "in"), ALL),
        (2, "audio", ("multa", "a"), ("l6", "k3"), ALL),
        (3, "audio", ("multa", "b"), ("fp4", "in"), ALL),
        (4, "audio", ("fp4", "o"), ("mw", "i1"), "8A"),
        (5, "audio", ("mw", "o1"), ("l6", "k1"), ALL),
        (6, "audio", ("mw", "o2"), ("l6", "k2"), ALL),
        (7, "cv", ("f281", "o"), ("fp4", "cv"), "8A"),
        (8, "audio", ("fp4", "o"), ("echo", "in"), B),
        (9, "audio", ("echo", "l"), ("mw", "i1"), B),
        (10, "audio", ("echo", "r"), ("mw", "i2"), B),
        (11, "trig", ("prog", "o"), ("echo", "sync"), B),
        (12, "audio", ("echo", "t4"), ("surg", "in"), B),
        (13, "audio", ("surg", "lp"), ("vca2", "in"), B),
        (14, "audio", ("vca2", "o"), ("echo", "fb"), B),
        (15, "cv", ("att", "oa"), ("vca2", "cv"), B),
        (16, "cv", ("f281", "o"), ("att", "ina"), B),
        (17, "audio", ("multa", "c"), ("fp3", "in1"), C),
        (18, "audio", ("fp3", "o2"), ("bode", "sig"), C),
        (19, "audio", ("bode", "oa"), ("lyra", "in"), C),
        (20, "audio", ("lyra", "o"), ("wasp", "in"), C),
        (21, "audio", ("wasp", "o"), ("multb", "in"), C),
        (22, "audio", ("multb", "a"), ("fp3", "in2"), C),
        (23, "audio", ("multb", "b"), ("l6", "k4"), C),
        (24, "audio", ("bode", "ob"), ("l6", "k5"), C),
        (25, "cv", ("lfo", "o"), ("att", "inb"), C),
        (26, "cv", ("att", "ob"), ("bode", "ctrl"), C),
    ]
    return patchplan(1240, 730, M, Cb, "8A",
                     "Patchplan Kapitel 08: Die Stimme aus 2A wird über einen Mult verteilt, trocken auf L6 Kanal 3, über einen FOUR PLAY als Send in den Milky Way und stereo zurück auf Kanal 1 und 2. In Stufe 8B sitzt das Morphor Echo vor dem Hall, Tap 4 läuft über Surges und einen VCA-Kanal in den Feedback-Eingang. In Stufe 8C läuft eine zweite Schleife aus FOUR PLAY, Bode 1630, Lyra-8 FX und Wasp, deren zwei Richtungen auf Kanal 4 und 5 liegen.")
