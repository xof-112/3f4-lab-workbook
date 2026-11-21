from figs import f
from figs2 import patchplan

# Kapitel 10 · Komposition, Performance, Aufnahme und Dokumentation · dazu B2-E-04
# Marker-IDs mit Präfix x10 bzw. e04, damit sie auf der ganzen Seite eindeutig bleiben.


def _defs(p):
    out = '<defs>'
    for k, cls in (("A", "fill-audio"), ("C", "fill-cv"), ("K", "fill-ink"), ("G", "fill-gate"), ("T", "fill-trig")):
        out += (f'<marker id="{p}{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="{cls}"/></marker>')
    return out + '</defs>'


def _box(o, x, y, w, h, t, s=None, cls="box"):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" class="{cls}"/>')
    o.append(f'<text x="{x+10}" y="{y+22}" class="t-lab" style="font-size:15px">{t}</text>')
    if s:
        o.append(f'<text x="{x+10}" y="{y+38}" class="t-sub">{s}</text>')


# ---------------- Motiv und vier Variationen ----------------
MOTIV = [(0, 2, 0), (2, 1, 3), (3, 1, 5), (4, 2, 7), (6, 2, 5)]  # (Start in Achteln, Dauer, Stufe in Halbtönen)


def fig_motiv():
    W, H = 760, 400
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Ein Motiv aus fünf Noten über einen Takt und vier Variationen, die jeweils nur eine Eigenschaft ändern: Transposition um eine Quarte, Umkehrung der Kontur, Augmentation auf doppelte Länge und ein neuer Rhythmus mit denselben Tönen. Die gleich gebliebene Eigenschaft ist jeweils hervorgehoben.">']
    rows = [("Motiv", "Programm Seq.1 · 1 Takt", MOTIV, None),
            ("Transposition", "+5 HT · Kontur bleibt", [(s, d, p + 5) for s, d, p in MOTIV], "Kontur, Rhythmus"),
            ("Umkehrung", "Intervalle gespiegelt", [(s, d, -p + 7) for s, d, p in MOTIV], "Rhythmus"),
            ("Augmentation", "doppelte Dauer · ÷2", [(s * 2, d * 2, p) for s, d, p in MOTIV], "Töne, Kontur"),
            ("Neuer Rhythmus", "Töne bleiben", [(0, 1, 0), (1, 1, 3), (3, 3, 5), (6, 1, 7), (7, 1, 5)], "Töne, Kontur")]
    x0, x1 = 200, 740
    rh = 72
    bw = (x1 - x0) / 16  # 16 Achtel = 2 Takte
    for i, (lab, sub, notes, keep) in enumerate(rows):
        y = 14 + i * rh
        o.append(f'<text x="10" y="{y+22}" class="t-lab" style="font-size:15px">{lab}</text>')
        o.append(f'<text x="10" y="{y+38}" class="t-sub">{sub}</text>')
        if keep:
            o.append(f'<text x="10" y="{y+54}" class="t-ax lab-cv">gleich: {keep}</text>')
        o.append(f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="{rh-12}" class="sec-a" style="stroke:var(--line)"/>')
        for b in range(1, 16):
            cls = "t-zero" if b == 8 else "t-grid"
            o.append(f'<line x1="{f(x0+b*bw)}" y1="{y}" x2="{f(x0+b*bw)}" y2="{y+rh-12}" class="{cls}" style="opacity:{1 if b==8 else .6}"/>')
        pts = []
        for s, d, p in notes:
            yy = y + rh - 18 - (p + 2) * 3.6
            o.append(f'<rect x="{f(x0+s*bw+2)}" y="{f(yy-5)}" width="{f(d*bw-4)}" height="10" rx="2" class="fill-audio" style="opacity:.85"/>')
            pts.append((x0 + s * bw + 2, yy))
        d = " ".join(("M" if k == 0 else "L") + f"{f(px)},{f(py)}" for k, (px, py) in enumerate(pts))
        o.append(f'<path d="{d}" class="sig sig-cv" style="stroke-width:1.4;stroke-dasharray:3 3"/>')
    o.append(f'<text x="{x0}" y="{H-8}" class="t-ax">Takt 1</text>')
    o.append(f'<text x="{f(x0+8*bw+4)}" y="{H-8}" class="t-ax">Takt 2</text>')
    o.append(f'<text x="{x1}" y="{H-8}" class="t-ax lab-cv" text-anchor="end">gestrichelt: Kontur</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Controller über den µYarns ----------------
def fig_ctrl10():
    W, H = 760, 400
    p = "x10c"
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Signalweg der Controller: Intech EN16 und TEK2 hängen magnetisch zusammen an einem USB-Kabel, der Exquis an einem zweiten. Beide gehen über einen USB-Hub in den Host-Anschluss des MIDI-Hosts. Dessen MIDI-Ausgang 1 führt zum µYarns, der aus CC 1 und CC 4 die Spannungen an CV 3 und CV 4 macht; die gehen in die Zeilen der A-138m-Matrix und von dort an Hall, Wellenform und Rings. Ausgang 2 führt zum MIDI-Eingang des L6, wo die Tasten des TEK2 Kanäle stummschalten und Szenen abrufen.">', _defs(p)]
    _box(o, 14, 20, 170, 74, "EN16 + TEK2", "ein USB-Kabel")
    _box(o, 14, 116, 170, 74, "Exquis", "USB · Noten Kanal 2")
    _box(o, 14, 230, 170, 74, "Exquis CV", "MOD = Druck, 0–5 V")
    _box(o, 228, 66, 150, 74, "USB-Hub", "an USB-A des Hosts")
    _box(o, 228, 170, 150, 92, "MIDI-Host", "H4MIDI WC", "box")
    o.append('<text x="238" y="226" class="t-sub">Routing, Filter:</text><text x="238" y="244" class="t-sub">kein Clock zu OUT 1</text>')
    _box(o, 420, 20, 150, 120, "µYarns", "Layout 1M", "box-strong")
    for k, (t, y) in enumerate((("CV 3 ← CC 1", 76), ("CV 4 ← CC 4", 100), ("GATE 3/4 Clock", 124))):
        o.append(f'<text x="430" y="{y}" class="t-ax" style="fill:var(--ink)">{t}</text>')
    _box(o, 420, 170, 150, 92, "L6", "MIDI IN · Kanal 16")
    o.append('<text x="430" y="226" class="t-ax" style="fill:var(--ink)">CC → Mute K1–6</text>')
    o.append('<text x="430" y="244" class="t-ax" style="fill:var(--ink)">PC → Szene A/B/C</text>')
    _box(o, 420, 290, 150, 92, "A-138m", "3 Zeilen × 3 Spalten", "box-mod")
    _box(o, 610, 290, 136, 92, "Ziele", None)
    for k, t in enumerate(("A Hall-Anteil", "B 258t WAVE", "C Rings hell")):
        o.append(f'<text x="620" y="{336+k*16}" class="t-ax" style="fill:var(--ink)">{t}</text>')
    o.append(f'<path d="M184,57 C205,57 205,92 228,92" fill="none" class="wire-ink" style="stroke-dasharray:6 4" marker-end="url(#{p}K)"/>')
    o.append(f'<path d="M184,153 C205,153 205,118 228,118" fill="none" class="wire-ink" style="stroke-dasharray:6 4" marker-end="url(#{p}K)"/>')
    o.append(f'<line x1="303" y1="140" x2="303" y2="168" class="wire-ink" style="stroke-dasharray:6 4" marker-end="url(#{p}K)"/>')
    o.append(f'<path d="M378,196 C398,196 398,80 418,80" fill="none" class="wire-ink" style="stroke-dasharray:6 4" marker-end="url(#{p}K)"/>')
    o.append('<text x="384" y="170" class="t-ax">OUT 1</text>')
    o.append(f'<line x1="378" y1="236" x2="418" y2="236" class="wire-ink" style="stroke-dasharray:6 4" marker-end="url(#{p}K)"/>')
    o.append('<text x="384" y="254" class="t-ax">OUT 2</text>')
    o.append(f'<path d="M570,90 C600,90 600,160 590,200 C585,240 560,280 540,288" fill="none" class="wire-cv" marker-end="url(#{p}C)"/>')
    o.append('<text x="604" y="150" class="t-ax lab-cv">CV 3, CV 4</text>')
    o.append(f'<path d="M184,267 C300,267 330,330 418,330" fill="none" class="wire-cv" marker-end="url(#{p}C)"/>')
    o.append('<text x="250" y="300" class="t-ax lab-cv">Zeile 3</text>')
    o.append(f'<line x1="570" y1="336" x2="608" y2="336" class="wire-cv" marker-end="url(#{p}C)"/>')
    o.append(f'<text x="14" y="{H-14}" class="t-ax">gestrichelt grau: MIDI und USB · orange: Steuerspannung</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Pegel am L6 ----------------
def fig_pegel():
    W, H = 760, 330
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Spitzenspannungen im Vergleich: ein Eurorack-Audiosignal mit plus minus fünf Volt, ein heißes mit plus minus zehn Volt. Die Line-Eingänge der L6-Kanäle 3 bis 6 vertragen plus 9 dBu, das sind etwa 3,1 Volt Spitze; die Klinkeneingänge der Kanäle 1 und 2 vertragen plus 24 dBu, etwa 17 Volt Spitze. Ein Fünf-Volt-Signal liegt also gut 4 dB über der Grenze der Kanäle 3 bis 6 und weit unter der der Kanäle 1 und 2.">']
    x0, x1 = 220, 730
    vmax = 18.0
    sx = lambda v: x0 + v / vmax * (x1 - x0)
    for v in range(0, 19, 2):
        o.append(f'<line x1="{f(sx(v))}" y1="20" x2="{f(sx(v))}" y2="{H-50}" class="t-grid"/>')
        o.append(f'<text x="{f(sx(v))}" y="{H-34}" class="t-ax" text-anchor="middle">{v}</text>')
    o.append(f'<text x="{x1}" y="{H-16}" class="t-ax" text-anchor="end">Spitzenspannung in Volt</text>')
    rows = [("Eurorack-Audio", "typisch ±5 V · 10 Vpp", 5.0, "fill-audio", "+13 dBu"),
            ("heißer Ausgang", "±10 V, etwa Feedback", 10.0, "fill-audio", "+19 dBu"),
            ("L6 Kanal 3–6", "Line, +9 dBu", 3.09, "fill-trig", "Grenze"),
            ("L6 Kanal 1/2", "Klinke TRS, +24 dBu", 17.4, "fill-gate", "Grenze"),
            ("Ziel vor K3–6", "6 dB unter der Grenze", 1.55, "fill-cv", "≈ ±1,5 V")]
    for i, (lab, sub, v, cls, note) in enumerate(rows):
        y = 26 + i * 50
        o.append(f'<text x="10" y="{y+16}" class="t-lab" style="font-size:15px">{lab}</text>')
        o.append(f'<text x="10" y="{y+32}" class="t-sub">{sub}</text>')
        o.append(f'<rect x="{x0}" y="{y+4}" width="{f(sx(v)-x0)}" height="24" rx="2" class="{cls}" style="opacity:.75"/>')
        o.append(f'<text x="{f(sx(v)+8)}" y="{y+21}" class="t-ax" style="fill:var(--ink)">{note}</text>')
    xl = sx(3.09)
    o.append(f'<line x1="{f(xl)}" y1="20" x2="{f(xl)}" y2="{H-50}" style="stroke:var(--trig);stroke-width:2;stroke-dasharray:5 4"/>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Vom Experiment zur Performance ----------------
def fig_weg():
    W, H = 760, 250
    p = "x10w"
    steps = [("Fund", "Recorder läuft", "immer mit"), ("Sichern", "Karte, Fotos,", "Speicher"), ("Reduzieren", "Kern und", "drei Griffe"),
             ("Fixieren", "Form, Szenen,", "Slots"), ("Proben", "drei", "Durchläufe"), ("Rückbau-Test", "neu nur", "nach Karte"), ("Aufführen", "Take mit", "Ordnername")]
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Sieben Schritte vom Experiment zur wiederholbaren Performance: Fund, Sichern, Reduzieren, Fixieren, Proben, Rückbau-Test und Aufführen. Ein Pfeil führt vom Rückbau-Test zurück zum Sichern: Was beim Neuaufbau fehlte, kommt auf die Karte.">', _defs(p)]
    bw, gap = 96, 9
    for i, (t, s, s2) in enumerate(steps):
        x = 10 + i * (bw + gap)
        cls = "box-strong" if t in ("Sichern", "Rückbau-Test") else "box"
        o.append(f'<rect x="{x}" y="70" width="{bw}" height="74" rx="3" class="{cls}"/>')
        o.append(f'<text x="{x+bw/2}" y="98" class="t-lab" style="font-size:13px" text-anchor="middle">{t}</text>')
        o.append(f'<text x="{x+bw/2}" y="116" class="t-sub" text-anchor="middle" style="font-size:10.5px">{s}</text>')
        o.append(f'<text x="{x+bw/2}" y="130" class="t-sub" text-anchor="middle" style="font-size:10.5px">{s2}</text>')
        o.append(f'<text x="{x+bw/2}" y="62" class="t-ax" text-anchor="middle">{i+1}</text>')
        if i:
            o.append(f'<line x1="{x-gap+1}" y1="107" x2="{x-1}" y2="107" class="wire-ink" marker-end="url(#{p}K)"/>')
    xa = 10 + 5 * (bw + gap) + bw / 2
    xb = 10 + 1 * (bw + gap) + bw / 2
    o.append(f'<path d="M{f(xa)},146 C{f(xa)},210 {f(xb)},210 {f(xb)},148" fill="none" class="wire-cv" marker-end="url(#{p}C)"/>')
    o.append(f'<text x="{f((xa+xb)/2)}" y="222" class="t-ax lab-cv" text-anchor="middle">was beim Neuaufbau fehlte, kommt auf die Karte</text>')
    o.append('<text x="10" y="24" class="t-ax">Experiment</text>')
    o.append(f'<text x="{W-10}" y="24" class="t-ax" text-anchor="end">wiederholbare Performance</text>')
    o.append(f'<line x1="90" y1="20" x2="{W-190}" y2="20" class="wire-ink" marker-end="url(#{p}K)" style="opacity:.5"/>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- B2-E-04 · Fehlersuche entlang der Kette ----------------
def fig_suche():
    W, H = 760, 250
    p = "e04"
    chain = [("Quelle", "258t OUT"), ("Formung", "SEM"), ("Dynamik", "A-130-8"), ("Verteilung", "Mult"),
             ("Raum", "Send, Hall"), ("Fader", "passiv"), ("L6", "Kanal-LED")]
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Eine Signalkette aus sieben Stationen von der Quelle bis zum L6. Gemessen wird zuerst in der Mitte, an der Dynamikstufe. Ist das Signal dort richtig, liegt der Fehler dahinter, sonst davor. So halbiert jede Messung den Suchbereich: nach höchstens drei Messungen ist die Station gefunden.">', _defs(p)]
    bw, gap = 92, 15
    for i, (t, s) in enumerate(chain):
        x = 10 + i * (bw + gap)
        o.append(f'<rect x="{x}" y="60" width="{bw}" height="62" rx="3" class="{"box-strong" if i==2 else "box"}"/>')
        o.append(f'<text x="{x+bw/2}" y="86" class="t-lab" style="font-size:13.5px" text-anchor="middle">{t}</text>')
        o.append(f'<text x="{x+bw/2}" y="104" class="t-sub" text-anchor="middle">{s}</text>')
        if i:
            o.append(f'<line x1="{x-gap+1}" y1="91" x2="{x-1}" y2="91" class="wire-audio" marker-end="url(#{p}A)"/>')
    for k, (i, lab, y) in enumerate(((2, "1. Messung", 168), (4, "2. Messung, wenn 1 gut", 196), (0, "2. Messung, wenn 1 schlecht", 224))):
        x = 10 + i * (bw + gap) + bw
        o.append(f'<line x1="{x+gap/2}" y1="124" x2="{x+gap/2}" y2="{y-12}" class="wire-cv" marker-start="url(#{p}C)"/>')
        o.append(f'<circle cx="{x+gap/2}" cy="91" r="5" class="fill-cv"/>')
        o.append(f'<text x="{x+gap/2+8}" y="{y-2}" class="t-ax lab-cv">{lab}</text>')
    o.append('<text x="10" y="30" class="t-ax">Messpunkt mit ZeroScope oder Kopfhörer über einen Abzweig · jede Messung halbiert den Suchbereich</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Patchplan Kapitel 10 ----------------
def pp_ch10():
    M = {}

    def mod(i, x, y, w, h, t, s, st, jacks):
        M[i] = dict(x=x, y=y, w=w, h=h, title=t, sub=s, st=st, jacks=jacks)
    ALL = "10A 10B 10C"
    B = "10B 10C"
    mod("grid", 20, 20, 160, 80, "EN16 + TEK2", "Intech · USB", ALL, {"u": ("USB", 165, 72, "o", "l")})
    mod("exq", 20, 120, 160, 200, "Exquis", "USB · MOD = Druck", ALL, {"u": ("USB", 165, 172, "o", "l"), "mod": ("MOD", 165, 300, "o", "l")})
    mod("host", 220, 20, 150, 250, "MIDI-Host", "über USB-Hub", ALL, {"usb": ("USB-A", 235, 122, "i", "r"),
                                                                       "o1": ("OUT 1", 355, 72, "o", "l"), "o2": ("OUT 2", 355, 232, "o", "l")})
    mod("yarns", 420, 20, 150, 160, "µYarns", "Layout 1M", ALL, {"mi": ("MIDI IN", 435, 72, "i", "r"),
                                                                  "cv3": ("CV 3", 555, 112, "o", "l"), "cv4": ("CV 4", 555, 152, "o", "l")})
    mod("l6m", 420, 200, 150, 70, "L6", "MIDI · Mutes, Szenen", ALL, {"mi": ("MIDI IN", 435, 252, "i", "r")})
    mod("mx", 620, 20, 150, 300, "A-138m", "Makro-Matrix", ALL, {"i1": ("IN 1", 635, 112, "i", "r"), "i2": ("IN 2", 635, 152, "i", "r"), "i3": ("IN 3", 635, 300, "i", "r"),
                                                                   "oa": ("OUT A", 755, 72, "o", "l"), "ob": ("OUT B", 755, 172, "o", "l"), "oc": ("OUT C", 755, 272, "o", "l")})
    mod("mw", 820, 20, 180, 70, "Milky Way", "Hall am Send", ALL, {"cp": ("CABIN PRESSURE CV", 835, 72, "i", "r")})
    mod("vco", 820, 120, 180, 70, "258t", "OSC 1 · Stimme 2A", ALL, {"w": ("WAVE CV", 835, 172, "i", "r")})
    mod("rings", 820, 220, 180, 70, "Rings", "aus Patch 9C", ALL, {"b": ("BRIGHTNESS", 835, 272, "i", "r")})
    mod("mult", 420, 360, 150, 80, "2×4 Mult", "Teil A · Stimme", B, {"o": ("frei", 555, 412, "o", "l")})
    mod("zs", 620, 360, 150, 80, "ZeroScope", "Messkabel", B, {"i": ("IN", 635, 412, "i", "r")})
    mod("samp", 420, 460, 150, 80, "Samples II", "Kick · OUT 1", B, {"k": ("OUT 1", 555, 512, "o", "l")})
    mod("pf", 620, 460, 150, 80, "Passivfader 7", "vor K4 R", B, {"i": ("IN", 635, 512, "i", "r"), "o": ("OUT", 755, 512, "o", "l")})
    mod("l6", 820, 360, 180, 180, "L6", "Audio · MONO an K4", B, {"k4": ("K4 R", 835, 512, "i", "r")})
    Cb = [
        (1, "midi", ("grid", "u"), ("host", "usb"), ALL),
        (2, "midi", ("exq", "u"), ("host", "usb"), ALL),
        (3, "midi", ("host", "o1"), ("yarns", "mi"), ALL),
        (4, "midi", ("host", "o2"), ("l6m", "mi"), ALL),
        (5, "cv", ("yarns", "cv3"), ("mx", "i1"), ALL),
        (6, "cv", ("yarns", "cv4"), ("mx", "i2"), ALL),
        (7, "cv", ("exq", "mod"), ("mx", "i3"), ALL),
        (8, "cv", ("mx", "oa"), ("mw", "cp"), ALL),
        (9, "cv", ("mx", "ob"), ("vco", "w"), ALL),
        (10, "cv", ("mx", "oc"), ("rings", "b"), ALL),
        (11, "audio", ("samp", "k"), ("pf", "i"), B),
        (12, "audio", ("pf", "o"), ("l6", "k4"), B),
        (13, "audio", ("mult", "o"), ("zs", "i"), B),
    ]
    return patchplan(1020, 560, M, Cb, "10A",
                     "Patchplan Kapitel 10, aufbauend auf Patch 9C: In Stufe 10A hängen EN16, TEK2 und Exquis über einen USB-Hub am MIDI-Host. Ausgang 1 geht zum µYarns, dessen CV 3 und CV 4 zusammen mit der MOD-Spannung des Exquis in drei Zeilen der A-138m laufen; deren Spalten steuern den Hall-Anteil am Milky Way, die Wellenform des 258t und die Helligkeit von Rings. Ausgang 2 geht zum MIDI-Eingang des L6 für Mutes und Szenen. In Stufe 10B kommt die Kick einzeln über einen Passivfader auf Kanal 4 rechts des L6, und ein Messkabel führt die Stimme zum ZeroScope.")
