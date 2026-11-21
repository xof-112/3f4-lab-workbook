from figs import f

def fig_leopanel():
    W, H = 900, 470
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Panelkarte des Leo Leo: links die 4×4-Reglermatrix mit Mute-Schaltern, rechts Zeilen-CV-Ausgänge, Stufen-Trigger-Eingänge, Gate-Ausgänge, zwei Reihen Regelschalter, Handtaster, die Takteingänge DOWN, RIGHT, LEFT, RESET, der Ausgang /2, die Mischausgänge ABCD und DCBA und der Kaskadenschalter.">']
    o.append(f'<rect x="4" y="4" width="{W-8}" height="{H-8}" rx="4" class="panel-bg"/>')
    # Matrix
    xs = [70, 150, 230, 310]; ys = [80, 160, 240, 320]
    for r, lab in enumerate("ABCD"):
        o.append(f'<text x="28" y="{ys[r]+5}" class="t-lab">{lab}</text>')
        for c in range(4):
            o.append(f'<circle cx="{xs[c]}" cy="{ys[r]}" r="22" class="kn2"/>')
            o.append(f'<line x1="{xs[c]}" y1="{ys[r]}" x2="{xs[c]}" y2="{ys[r]-16}" class="kp2"/>')
    for c in range(4):
        o.append(f'<text x="{xs[c]}" y="{ys[0]-38}" class="t-lab" text-anchor="middle">{c+1}</text>')
        o.append(f'<rect x="{xs[c]-7}" y="370" width="14" height="24" rx="2" class="sw"/>')
    o.append('<text x="28" y="388" class="t-ax">MUTE</text>')
    o.append('<text x="190" y="440" class="t-sub" text-anchor="middle">Spalten 1–4 = Stufen (Zeit) · Zeilen A–D = Spuren</text>')
    def jack(x, y, lab, out):
        o.append(f'<circle cx="{x}" cy="{y}" r="9" class="{"jo" if out else "ji"}"/>')
        o.append(f'<text x="{x}" y="{y+24}" class="t-ax" text-anchor="middle">{lab}</text>')
    def title(x, y, t):
        o.append(f'<text x="{x}" y="{y}" class="t-sub" text-anchor="middle" style="font-weight:600">{t}</text>')
    title(430, 50, "ROW CV OUT"); [jack(x, y, l, True) for x, y, l in ((400, 80, "A"), (460, 80, "B"), (400, 140, "C"), (460, 140, "D"))]
    title(560, 50, "STAGE TRIGGER"); [jack(x, y, l, False) for x, y, l in ((530, 80, "1"), (590, 80, "2"), (530, 140, "3"), (590, 140, "4"))]
    title(720, 50, "GATE OUT"); [jack(x, y, l, True) for x, y, l in ((660, 80, "1"), (720, 80, "2"), (790, 80, "ALL"), (660, 140, "3"), (720, 140, "4"), (790, 140, "COMMON"))]
    for row, y, lab in ((0, 225, "Regeln für Lauf →"), (1, 295, "Regeln für Lauf ←")):
        for x in (400, 460, 520, 580):
            o.append(f'<rect x="{x-7}" y="{y-12}" width="14" height="24" rx="2" class="sw"/>')
        o.append(f'<text x="370" y="{y+4}" class="t-ax" text-anchor="end">{"→" if row == 0 else "←"}</text>')
        o.append(f'<text x="490" y="{y+30}" class="t-ax" text-anchor="middle">{lab} · PLAY / SKIP / STOP</text>')
    for x in (400, 460, 520, 580):
        o.append(f'<circle cx="{x}" cy="375" r="13" class="btn-c"/>')
    o.append('<text x="490" y="410" class="t-ax" text-anchor="middle">MANUAL STAGE TRIGGER</text>')
    jack(660, 225, "DOWN", False); jack(660, 300, "/2", True); jack(660, 375, "RESET", False)
    title(760, 200, "MIX CV OUT"); jack(730, 225, "DCBA", True); jack(800, 225, "ABCD", True)
    title(760, 278, "DIRECTION"); jack(730, 300, "RIGHT", False); jack(800, 300, "LEFT", False)
    o.append('<rect x="790" y="363" width="14" height="24" rx="2" class="sw"/>')
    o.append('<text x="797" y="410" class="t-ax" text-anchor="middle">∞ Kaskade</text>')
    o.append(f'<text x="{W-16}" y="{H-14}" class="t-ax" text-anchor="end">○ Eingang · ● Ausgang · ▭ Schalter · ◯ Taster</text>')
    o.append('</svg>')
    return "\n".join(o)


def fig_readings():
    W, H = 780, 250
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Drei Lesarten der Matrix: vier parallele Spuren zu je vier Schritten, zwei Sequenzen zu je acht Schritten, eine Sequenz mit sechzehn Schritten.">']
    o.append('<defs><marker id="rdA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="fill-audio"/></marker>'
             '<marker id="rdC" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="fill-cv"/></marker></defs>')
    panels = [("4 × 4 · ROW CV OUT A–D", "4x4"), ("2 × 8 · ABCD und DCBA, /2 → RESET", "2x8"), ("1 × 16 · ABCD mit DOWN", "16")]
    for p, (t, mode) in enumerate(panels):
        x0 = 20 + p * 258
        o.append(f'<text x="{x0}" y="20" class="t-sub" style="font-weight:600">{t}</text>')
        g = 44
        for r in range(4):
            for c in range(4):
                cx, cy = x0 + 30 + c * g, 60 + r * g
                if mode == "4x4":
                    n = c + 1; cls = "fill-audio"
                elif mode == "2x8":
                    if r < 2: n = r * 4 + c + 1; cls = "fill-audio"
                    else: n = (3 - r) * 4 + c + 1; cls = "fill-cv"
                else:
                    n = r * 4 + c + 1; cls = "fill-audio"
                o.append(f'<circle cx="{cx}" cy="{cy}" r="14" class="{cls}" opacity=".18"/>')
                o.append(f'<text x="{cx}" y="{cy+4}" class="t-ax" text-anchor="middle" style="fill:var(--ink)">{n}</text>')
            if mode == "4x4":
                o.append(f'<line x1="{x0+30+3*g+18}" y1="{60+r*g}" x2="{x0+30+3*g+44}" y2="{60+r*g}" class="wire-audio" marker-end="url(#rdA)"/>')
                o.append(f'<text x="{x0+30+3*g+50}" y="{64+r*g}" class="t-ax">{"ABCD"[r]}</text>')
        if mode == "2x8":
            o.append(f'<text x="{x0+30+3*g+24}" y="{60+g/2+4}" class="t-ax" style="fill:var(--audio)">ABCD</text>')
            o.append(f'<text x="{x0+30+3*g+24}" y="{60+2.5*g+4}" class="t-ax" style="fill:var(--cv)">DCBA</text>')
        if mode == "16":
            o.append(f'<text x="{x0+30+3*g+24}" y="{60+1.5*g+4}" class="t-ax">ABCD</text>')
    o.append(f'<text x="20" y="{H-10}" class="t-ax">Zahlen = Reihenfolge der Schritte bei Lauf nach rechts. In 2 × 8 läuft DCBA gleichzeitig von unten (orange).</text>')
    o.append('</svg>')
    return "\n".join(o)
