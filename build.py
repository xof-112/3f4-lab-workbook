# 3F4-Lab Workbook · Bausatz – setzt alle Teile zu 3f4-lab-workbook.html zusammen.
# Seit Fassung 2.5 aus der veröffentlichten Seite 2.4 zurückgewonnen: Texte, Tabellen, Register und die meisten
# Grafiken stehen fertig im HTML. Nur die Grafiken im Dict F kommen noch aus Python (figs*.py).
import re, figs, figs2, figs3, figs4, figs5, figs6, figs7
ORDER = ("head.html", "body1.html", "body2.html", "ch02.html", "ch03.html", "ch04.html", "ch05.html",
         "ch06.html", "ch07.html", "ch08.html", "ch09.html", "ch10.html",
         "band2.html", "band3.html", "kwp.html", "pruefen.html", "anhang.html", "script.html")
html = "\n".join(open(p, encoding="utf-8").read() for p in ORDER)
html = re.sub(r"\{\{INC:([\w.]+)\}\}", lambda m: open(m.group(1), encoding="utf-8").read(), html)
F = {"signals": figs.fig_signals, "arch": figs.fig_arch, "levels": figs.fig_levels,
     "timeline": figs.fig_timeline, "modes": figs.fig_modes, "pp_ch2": figs2.pp_ch2,
     "eastwest": figs2.fig_eastwest, "waves": figs2.fig_waves, "fold": figs2.fig_fold,
     "leopanel": figs3.fig_leopanel, "readings": figs3.fig_readings,
     "fxroute": figs4.fig_fxroute, "echoes": figs4.fig_echoes, "comb": figs4.fig_comb, "shift": figs4.fig_shift,
     "loopgain": figs4.fig_loopgain, "safety": figs4.fig_safety, "pan": figs4.fig_pan,
     "zeitebenen": figs5.fig_zeitebenen, "matrix9": figs5.fig_matrix9, "riser": figs5.fig_riser, "boegen": figs5.fig_boegen,
     "motiv": figs6.fig_motiv, "ctrl10": figs6.fig_ctrl10, "pegel": figs6.fig_pegel, "weg": figs6.fig_weg,
     "suche": figs6.fig_suche, "pp_ch10": figs6.pp_ch10,
     "a01": figs7.fig_a01, "a02clip": figs7.fig_a02clip, "a02route": figs7.fig_a02route}
html = re.sub(r"\{\{FIG:(\w+)\}\}", lambda m: F[m.group(1)](), html)
def kn(m):
    return figs.knob(float(m.group(1)), m.group(2), m.group(3), bip=bool(m.group(4)))
html = re.sub(r"\{\{KNOB:([\d.]+)\|([^|]*)\|([^|}]*)(?:\|(b))?\}\}", kn, html)
READER = '<div class="reader" data-reader hidden><button type="button" class="rd-play">▶ Vorlesen</button><button type="button" class="rd-stop">■ Stopp</button><label>Tempo <select class="rd-rate"><option value="0.85">langsam</option><option value="1" selected>normal</option><option value="1.2">schneller</option></select></label><span class="rs" aria-live="polite"></span></div>'
html = html.replace("{{READER}}", READER).replace("{{BACK}}", '<a class="back toc-back" href="#inhalt">↑ zum Inhaltsverzeichnis</a>')
assert "{{" not in html, re.findall(r"\{\{[^}]*\}\}", html)
open("3f4-lab-workbook.html", "w", encoding="utf-8").write(html)
# GitHub Pages (Ordner docs/): dieselbe Seite als vollständiges HTML-Dokument
import os
os.makedirs("docs", exist_ok=True)
open("docs/index.html", "w", encoding="utf-8").write(
    '<!DOCTYPE html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    + html + '\n</html>\n')
open("docs/.nojekyll", "w").close()
print(len(html))
