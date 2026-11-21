import math
from figs import f

# ---------------- Patchplan-Generator ----------------
def patchplan(W, H, modules, cables, default, aria):
    """modules: dict id -> dict(x,y,w,h,title,sub,st,jacks={jid:(label,x,y,kind,lp)})
       kind 'i'/'o'; lp label position 'l','r','b'
       cables: list of (num,type,(mod,jack),(mod,jack),stages)"""
    o = [f'<svg class="pp" viewBox="0 0 {W} {H}" role="img" aria-label="{aria}">']
    for mid, m in modules.items():
        off = "" if default in m["st"].split() else " off"
        o.append(f'<g class="mod{off}" data-st="{m["st"]}">')
        o.append(f'<rect class="m" x="{m["x"]}" y="{m["y"]}" width="{m["w"]}" height="{m["h"]}" rx="3"/>')
        o.append(f'<text class="mt" x="{m["x"]+12}" y="{m["y"]+24}">{m["title"]}</text>')
        if m.get("sub"):
            o.append(f'<text class="ms" x="{m["x"]+12}" y="{m["y"]+40}">{m["sub"]}</text>')
        for jid, (lab, x, y, kind, lp) in m["jacks"].items():
            cls = "jk o" if kind == "o" else "jk"
            o.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="7"/>')
            if lp == "r":
                o.append(f'<text class="jl" x="{x+12}" y="{y+4}">{lab}</text>')
            elif lp == "l":
                o.append(f'<text class="jl" x="{x-12}" y="{y+4}" text-anchor="end">{lab}</text>')
            else:
                o.append(f'<text class="jl" x="{x}" y="{y+22}" text-anchor="middle">{lab}</text>')
        o.append('</g>')
    for num, typ, (ma, ja), (mb, jb), st in cables:
        x0, y0 = modules[ma]["jacks"][ja][1:3]
        x3, y3 = modules[mb]["jacks"][jb][1:3]
        if x3 > x0 + 20:
            dx = max(40, (x3 - x0) * 0.45)
            p1, p2 = (x0 + dx, y0), (x3 - dx, y3)
        else:  # rückwärts: Schleife
            dx = 70
            p1, p2 = (x0 + dx, y0 + (y3 - y0) * 0.15), (x3 - dx, y3 - (y3 - y0) * 0.15)
        bx = .125 * x0 + .375 * p1[0] + .375 * p2[0] + .125 * x3
        by = .125 * y0 + .375 * p1[1] + .375 * p2[1] + .125 * y3
        off = "" if default in st.split() else " off"
        o.append(f'<g class="cg{off}" data-st="{st}"><path class="cab {typ}" d="M{f(x0)},{f(y0)} C{f(p1[0])},{f(p1[1])} {f(p2[0])},{f(p2[1])} {f(x3)},{f(y3)}"/>'
                 f'<g class="badge {typ}"><circle cx="{f(bx)}" cy="{f(by)}" r="11"/><text x="{f(bx)}" y="{f(by+4)}" text-anchor="middle">{num}</text></g></g>')
    o.append('</svg>')
    return "\n".join(o)


def pp_ch2():
    M = {}
    def mod(i, x, y, w, h, t, s, st, jacks):
        M[i] = dict(x=x, y=y, w=w, h=h, title=t, sub=s, st=st, jacks=jacks)
    ALL = "2A 2B 2C"
    mod("yarns", 20, 20, 130, 110, "µYarns", "MIDI → CV", ALL, {"gate": ("GATE 1", 50, 85, "o", "b"), "cv": ("CV 1", 112, 85, "o", "b")})
    mod("f281", 200, 20, 140, 180, "281t", "Kanal 1 und 3", ALL, {"trig": ("TRIG 1", 215, 70, "i", "r"), "o1": ("OUT 1", 330, 110, "o", "l"), "o3": ("OUT 3", 330, 165, "o", "l")})
    mod("vco", 200, 250, 140, 210, "258t", "OSC 1", ALL, {"voct": ("1V/OCT", 215, 295, "i", "r"), "wave": ("WAVE CV", 215, 340, "i", "r"), "o1": ("OUT", 330, 385, "o", "l"), "o2": ("OUT ·2", 330, 430, "o", "l")})
    mod("mult", 390, 20, 130, 140, "Mult", "aktiv", ALL, {"in": ("IN", 405, 95, "i", "r"), "a": ("", 505, 70, "o", "l"), "b": ("", 505, 102, "o", "l"), "c": ("", 505, 134, "o", "l")})
    mod("att", 390, 180, 130, 150, "Attenuverter", "", ALL, {"ina": ("IN A", 405, 235, "i", "r"), "oa": ("OUT A", 505, 250, "o", "b"), "inb": ("IN B", 405, 295, "i", "r"), "ob": ("OUT B", 505, 310, "o", "l")})
    mod("mult2", 390, 360, 130, 110, "2×4 Mult", "aktiv", "2B", {"in": ("IN", 405, 425, "i", "r"), "a": ("", 505, 410, "o", "l"), "b": ("", 505, 445, "o", "l")})
    mod("sem", 560, 20, 150, 150, "A-106-5", "SEM", ALL, {"cv2": ("CV2 IN", 575, 60, "i", "r"), "aud": ("AUDIO IN", 575, 120, "i", "r"), "mix": ("MIX-OUT", 695, 145, "o", "b")})
    mod("wasp", 560, 200, 150, 80, "A-124", "Wasp", "2B", {"aud": ("AUDIO IN", 575, 258, "i", "r"), "out": ("LP/HP", 695, 250, "o", "b")})
    mod("surg", 560, 300, 150, 80, "Surges", "Ripples-Klon", "2B", {"in": ("IN 1", 575, 358, "i", "r"), "lp": ("LP", 695, 350, "o", "b")})
    mod("bigo", 560, 410, 150, 80, "Capt’n Big-O", "Wavefolder", "2C", {"in": ("F.IN", 575, 468, "i", "r"), "out": ("FOLD", 695, 458, "o", "b")})
    mod("lpg", 560, 510, 150, 110, "DPLPG", "Kanal 1", "2C", {"in": ("IN 1", 575, 562, "i", "r"), "trig": ("TRIG 1", 575, 597, "i", "r"), "out": ("OUT 1", 695, 575, "o", "b")})
    mod("mix", 760, 200, 100, 170, "Mixer", "CatSynth 4×", "2B", {"i1": ("IN 1", 775, 240, "i", "r"), "i2": ("IN 2", 775, 280, "i", "r"), "i3": ("IN 3", 775, 320, "i", "r"), "out": ("OUT", 845, 352, "o", "l")})
    mod("vca", 900, 20, 100, 170, "A-130-8", "Kanal 1", ALL, {"in": ("IN 1", 915, 70, "i", "r"), "cv": ("CV 1", 915, 135, "i", "r"), "out": ("OUT 1", 985, 100, "o", "b")})
    mod("l6", 1040, 20, 100, 610, "Fader·L6", "", ALL, {"k1": ("KANAL 1", 1055, 100, "i", "b"), "k2": ("KANAL 2", 1055, 575, "i", "b")})
    C = [
        (1, "cv", ("yarns", "cv"), ("vco", "voct"), ALL),
        (2, "gate", ("yarns", "gate"), ("f281", "trig"), ALL),
        (3, "audio", ("vco", "o1"), ("sem", "aud"), ALL),
        (4, "audio", ("sem", "mix"), ("vca", "in"), "2A 2C"),
        (5, "audio", ("vca", "out"), ("l6", "k1"), ALL),
        (6, "cv", ("f281", "o1"), ("mult", "in"), ALL),
        (7, "cv", ("mult", "a"), ("att", "ina"), ALL),
        (8, "cv", ("att", "oa"), ("vca", "cv"), ALL),
        (9, "cv", ("mult", "b"), ("sem", "cv2"), "2A 2C"),
        (10, "audio", ("vco", "o2"), ("mult2", "in"), "2B"),
        (11, "audio", ("mult2", "a"), ("wasp", "aud"), "2B"),
        (12, "audio", ("mult2", "b"), ("surg", "in"), "2B"),
        (13, "audio", ("sem", "mix"), ("mix", "i1"), "2B"),
        (14, "audio", ("wasp", "out"), ("mix", "i2"), "2B"),
        (15, "audio", ("surg", "lp"), ("mix", "i3"), "2B"),
        (16, "audio", ("mix", "out"), ("vca", "in"), "2B"),
        (17, "audio", ("vco", "o2"), ("bigo", "in"), "2C"),
        (18, "audio", ("bigo", "out"), ("lpg", "in"), "2C"),
        (19, "audio", ("lpg", "out"), ("l6", "k2"), "2C"),
        (20, "cv", ("mult", "c"), ("lpg", "trig"), "2C"),
        (21, "cv", ("f281", "o3"), ("att", "inb"), "2C"),
        (22, "cv", ("att", "ob"), ("vco", "wave"), "2C"),
    ]
    return patchplan(1160, 640, M, C, "2A",
                     "Patchplan Kapitel 02: µYarns spielt den 258t und startet den 281t; der Ton läuft über drei mögliche Wege, klassisch über SEM und A-130-8, im Filtervergleich über SEM, Wasp und Surges, oder West Coast über Wavefolder und DPLPG.")


# ---------------- Ost- und Westküste ----------------
def fig_eastwest():
    W, H = 780, 330
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Zwei Stimmarchitekturen: Ostküste nimmt Obertöne weg und regelt Lautstärke getrennt, Westküste fügt Obertöne hinzu und regelt Helligkeit und Lautstärke in einem Low Pass Gate gemeinsam.">']
    o.append('<defs><marker id="ewA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fill-audio"/></marker>'
             '<marker id="ewC" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fill-cv"/></marker></defs>')
    def spec(x, y, amps):
        for i, a in enumerate(amps):
            o.append(f'<rect x="{x+i*7}" y="{f(y-a*26)}" width="4" height="{f(a*26)}" class="fill-audio"/>')
    rows = [
        (40, "Ostküste · subtraktiv", [("VCO", "obertonreich", [1, .5, .33, .25, .2, .17, .14, .12]),
                                        ("VCF", "nimmt weg", [1, .5, .25, .08, .03, 0, 0, 0]),
                                        ("VCA", "Lautstärke", [1, .5, .25, .08, .03, 0, 0, 0])], ["Hüllkurve 1", "Hüllkurve 2"]),
        (195, "Westküste · formend", [("VCO", "nahe Sinus", [1, 0, 0, 0, 0, 0, 0, 0]),
                                       ("Wavefolder", "fügt hinzu", [1, 0, .45, 0, .3, 0, .18, 0]),
                                       ("LPG", "hell + laut", [1, 0, .3, 0, .1, 0, 0, 0])], ["langsame Mod.", "eine Hüllkurve"]),
    ]
    for y, title, boxes, mods in rows:
        o.append(f'<text x="20" y="{y-14}" class="t-lab">{title}</text>')
        for i, (t, s, amps) in enumerate(boxes):
            x = 150 + i * 220
            o.append(f'<rect x="{x}" y="{y+30}" width="150" height="80" rx="3" class="box"/>')
            o.append(f'<text x="{x+12}" y="{y+52}" class="t-lab">{t}</text>')
            o.append(f'<text x="{x+12}" y="{y+68}" class="t-sub">{s}</text>')
            spec(x + 80, y + 102, amps)
            if i < 2:
                o.append(f'<line x1="{x+150}" y1="{y+70}" x2="{x+218}" y2="{y+70}" class="wire-audio" marker-end="url(#ewA)"/>')
        o.append(f'<text x="20" y="{y+74}" class="t-sub">Audio →</text>')
        # Modulation arrows
        if title.startswith("Ost"):
            for k, bi in enumerate((1, 2)):
                x = 150 + bi * 220 + 75
                o.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+28}" class="wire-cv" marker-end="url(#ewC)"/>')
                o.append(f'<text x="{x+6}" y="{y+8}" class="t-ax">{mods[k]}</text>')
        else:
            x = 150 + 1 * 220 + 75
            o.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+28}" class="wire-cv" marker-end="url(#ewC)"/>')
            o.append(f'<text x="{x+6}" y="{y+8}" class="t-ax">{mods[0]}</text>')
            x = 150 + 2 * 220 + 75
            o.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+28}" class="wire-cv" marker-end="url(#ewC)"/>')
            o.append(f'<text x="{x+6}" y="{y+8}" class="t-ax">{mods[1]}</text>')
    o.append(f'<text x="150" y="{H-6}" class="t-ax">Balken im Kasten: Obertöne nach dieser Stufe (schematisch).</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Wellenformen und Spektren ----------------
def fig_waves():
    W, H = 780, 250
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Vier Grundwellenformen mit ihren Obertönen: Sinus nur Grundton, Dreieck ungerade Obertöne sehr schwach, Rechteck ungerade Obertöne, Sägezahn alle Obertöne.">']
    shapes = [
        ("Sinus", lambda p: math.sin(2 * math.pi * p), lambda n: 1 if n == 1 else 0),
        ("Dreieck", lambda p: 1 - 4 * abs(((p + .25) % 1) - .5), lambda n: (1 / n**2) if n % 2 else 0),
        ("Rechteck", lambda p: 1 if p % 1 < .5 else -1, lambda n: (1 / n) if n % 2 else 0),
        ("Sägezahn", lambda p: 1 - 2 * (p % 1), lambda n: 1 / n),
    ]
    for i, (name, fn, amp) in enumerate(shapes):
        x0 = 20 + i * 190
        w = 160
        o.append(f'<text x="{x0}" y="18" class="t-lab">{name}</text>')
        mid = 70
        o.append(f'<line x1="{x0}" y1="{mid}" x2="{x0+w}" y2="{mid}" class="t-grid"/>')
        pts = " ".join(f"{f(x0 + k / 200 * w)},{f(mid - fn(2 * k / 200) * 34)}" for k in range(201))
        o.append(f'<polyline points="{pts}" class="sig sig-audio"/>')
        base = 205
        o.append(f'<line x1="{x0}" y1="{base}" x2="{x0+w}" y2="{base}" class="t-grid"/>')
        for n in range(1, 11):
            a = amp(n)
            h = a * 80
            bx = x0 + (n - 1) * 16
            if h > 0:
                o.append(f'<rect x="{bx}" y="{f(base-h)}" width="9" height="{f(h)}" class="fill-cv"/>')
            o.append(f'<text x="{bx+4.5}" y="{base+14}" class="t-ax" text-anchor="middle">{n}</text>')
    o.append(f'<text x="20" y="{H-6}" class="t-ax">Obertonnummer 1–10; Höhe = Amplitude relativ zum Grundton.</text>')
    o.append('</svg>')
    return "\n".join(o)


# ---------------- Wavefolding ----------------
def fold(x):
    while abs(x) > 1:
        x = (2 if x > 0 else -2) - x
    return x


def fig_fold():
    W, H = 780, 240
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Wavefolding: Ein Sinus, der lauter wird als die Faltgrenze, wird an ihr zurückgeklappt. Je mehr Verstärkung, desto mehr Falten und Obertöne.">']
    for i, g in enumerate((1, 2.2, 4.5)):
        x0 = 20 + i * 255
        w = 230
        mid = 125
        o.append(f'<text x="{x0}" y="20" class="t-lab">Verstärkung × {str(g).replace(".", ",")}</text>')
        for lim in (-1, 1):
            o.append(f'<line x1="{x0}" y1="{mid - lim*55}" x2="{x0+w}" y2="{mid - lim*55}" class="mark-euro"/>')
        o.append(f'<line x1="{x0}" y1="{mid}" x2="{x0+w}" y2="{mid}" class="t-grid"/>')
        ptsi = " ".join(f"{f(x0 + k/300*w)},{f(mid - max(-1.45, min(1.45, g*math.sin(4*math.pi*k/300)))*55)}" for k in range(301))
        if g > 1:
            o.append(f'<polyline points="{ptsi}" class="sig" style="stroke:var(--muted);stroke-dasharray:3 3;stroke-width:1.2"/>')
        pts = " ".join(f"{f(x0 + k/300*w)},{f(mid - fold(g*math.sin(4*math.pi*k/300))*55)}" for k in range(301))
        o.append(f'<polyline points="{pts}" class="sig sig-audio"/>')
    o.append(f'<text x="20" y="{H-8}" class="t-ax">Orange: Faltgrenze · grau: verstärktes Signal (gekappt) · blau: Ausgang</text>')
    o.append('</svg>')
    return "\n".join(o)
