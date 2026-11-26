#!/usr/bin/env python3
"""Собирает сайт: content/*.html + tools/figures*.py -> notes/*.html и index.html.

    python3 tools/build.py
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from figures import F  # noqa: E402
import figures2  # noqa: E402,F401

SITE = "Конспекты по физике"
HEAD = (ROOT / "template/head.html").read_text()
TAIL = (ROOT / "template/tail.html").read_text()

SOLID = "".join(f'html[data-theme] svg .solid[fill="{c}"]{{fill:var(--f-{n})}}' for c, n in (
    ("#58c4dd", "blue"), ("#83c167", "green"), ("#ffff00", "yellow"), ("#fc6255", "red"),
    ("#ff8c1a", "orange"), ("#c78bff", "purple"), ("#9aa4b2", "muted"), ("#dfe7f1", "text")))

EXTRA = """<style id="physics">
html[data-theme] .wrap th{text-transform:none;letter-spacing:0}
.wrap table{border-collapse:collapse;width:100%;margin:1em 0;font-size:.92rem;display:block;overflow-x:auto}
.wrap th,.wrap td{border:1px solid var(--line);padding:6px 10px;text-align:left}
.wrap figure.viz{margin:1.4em 0}
.wrap figure.viz svg{display:block;width:100%;height:auto}
.wrap .katex-display{overflow-x:auto;overflow-y:hidden;padding:4px 0}
</style>
"""


def read(path):
    s = path.read_text()
    m = re.match(r"<!--(.*?)-->\s*", s, re.S)
    meta = dict(l.split(": ", 1) for l in m.group(1).strip().split("\n"))
    meta["body"] = s[m.end():]
    meta["file"] = path.name
    return meta


def plain(s):
    return html.unescape(re.sub(r"<[^>]+>|\$", "", s)).strip()


def lesson(i, L, lessons, used):
    def sub(m):
        used.add(m.group(1))
        return f'<figure class="viz">{F[m.group(1)]()}</figure>'

    body = re.sub(r"§(\w+)§", sub, L["body"])
    toc = "".join(f'<li><a href="#{a}">{re.sub(r"^[0-9]+[.] ", "", t)}</a></li>'
                  for a, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body))
    chips = "".join(f'<span class="chip">{c.strip()}</span>' for c in L["chips"].replace("&amp;", "\0").split(";")).replace("\0", "&amp;")
    pager = ""
    if i > 0:
        p = lessons[i - 1]
        pager += f'<a class="prev" href="{p["file"]}"><small>← тема {i}</small><b>{p["title"]}</b></a>'
    if i + 1 < len(lessons):
        n = lessons[i + 1]
        pager += f'<a class="next" href="{n["file"]}"><small>тема {i+2} →</small><b>{n["title"]}</b></a>'
    title = f'{i+1}. {L["title"]}'
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/png" href="../favicon.png">
<title>{title} — {SITE}</title>
<meta name="description" content="{html.escape(plain(L["sub"]), quote=True)}">
{HEAD}
{EXTRA}<style>{SOLID}</style>
</head>
<body>
<div class="wrap">
<div class="top"><a class="sitelink" href="../index.html">← Все темы</a><a class="back dl" href="{L["file"]}" download="{L["file"]}" title="Скачать конспект одним HTML-файлом, откроется без интернета">⬇ Скачать конспект</a><button type="button" id="theme-toggle" class="theme-toggle" aria-label="Переключить тему">тёмная тема</button></div>

<header class="hero">
  <h1>{title}</h1>
  <div class="sub">{L["sub"]}</div>
  <div class="meta">{chips}</div>
</header>

<nav class="toc">
  <h2>Содержание</h2>
  <ol>{toc}</ol>
</nav>
{body}

<footer>
  Конспект составлен по рукописным записям занятий. Чертежи перерисованы; дополнения и исправления отмечены в тексте.
</footer>
<nav class="pager" aria-label="Соседние темы">{pager}</nav>
</div>
<button class="toplink" id="topBtn">↑ наверх</button>
{TAIL}
</body>
</html>
"""


def index(lessons):
    cards, noscript = [], []
    colors = ["--ic-purple", "--ic-pink", "--ic-green", "--ic-blue", "--ic-yellow"]
    for i, L in enumerate(lessons):
        items = "".join(f"<li>{c.strip()}</li>" for c in L["cards"].split("|"))
        key = plain(" ".join([L["title"], L["sub"], L["chips"], L["cards"], " ".join(re.findall(r"<h[23][^>]*>(.*?)</h[23]>", L["body"]))])).lower()
        cards.append(f'<a class="pcard" href="notes/{L["file"]}" data-k="{html.escape(key, quote=True)}"><div class="ph">'
                     f'<span class="badge" style="background:var({colors[i % 5]})">{i+1}</span><h3>{L["title"]}</h3></div>'
                     f'<ul class="tl">{items}</ul><div class="pf"><span>чертежей: {L["body"].count("§") // 2}</span><em>→</em></div></a>')
    drawings = sum(L["body"].count("§") // 2 for L in lessons)
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{SITE} — механика</title>
<meta name="description" content="Конспекты по механике с формулами, чертежами и разбором задач: векторы, кинематика, законы Ньютона, блоки, закон Гука, трение, статика, импульс.">
<link rel="icon" type="image/png" href="favicon.png">
<script>(function(){{try{{var t=localStorage.getItem("conspectusTheme");document.documentElement.setAttribute("data-theme",t||(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"))}}catch(e){{document.documentElement.setAttribute("data-theme","light")}}}})();</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<style>.pcard[hidden]{{display:none}}</style>
</head>
<body>
<div class="page">
<header class="nav"><div style="display:flex;align-items:center;gap:4px"><a class="brand" href="index.html">физика<i>.</i></a><nav class="links"><a href="#pick">Темы</a><a href="https://vmaiorov-collab.github.io/conspectus/">Конспекты по программированию</a></nav></div><div class="navr"><button type="button" id="theme-toggle" class="theme-toggle" aria-label="Переключить тему">тёмная тема</button></div></header>

<section class="hero2">
  <div class="hl">
    <div class="hmain">
      <span class="chip">Механика</span>
      <h1>Конспекты по <span class="hi">физике</span></h1>
      <p>Определения, выводы формул, чертежи и разобранные задачи. Все рисунки нарисованы заново в SVG.</p>
      <div class="cta"><a class="btn1" href="#pick">Выбрать тему</a></div>
      <div class="sbox"><div class="search"><input id="q" type="search" placeholder="Поиск по темам: блоки, момент, пружина…" autocomplete="off" aria-label="Поиск по темам"></div></div>
    </div>
    <div class="hstats"><div><b>{len(lessons)}</b><span>тем</span></div><div><b>{drawings}</b><span>чертежей к темам и задачам</span></div><div><b>1</b><span>файл на тему — читается офлайн</span></div></div>
  </div>
</section>

<div class="nores" id="nores" hidden>Ничего не найдено.</div>
<div id="pick">
<h2 class="big">Темы</h2>
<nav class="pgrid">{"".join(cards)}</nav>
</div>
<footer class="foot"><a href="https://github.com/vmaiorov-collab/physics-conspectus">исходники на GitHub</a></footer>
</div>
<script>
(function(){{var q=document.getElementById("q"),cards=[].slice.call(document.querySelectorAll(".pcard")),no=document.getElementById("nores");
q.addEventListener("input",function(){{var words=q.value.toLowerCase().split(/\\s+/).filter(Boolean),n=0;
cards.forEach(function(c){{var ok=words.every(function(w){{return c.dataset.k.indexOf(w)>=0}});c.hidden=!ok;if(ok)n++}});no.hidden=n>0}});}})();
(function(){{var root=document.documentElement,btn=document.getElementById("theme-toggle");
function label(){{btn.textContent=root.getAttribute("data-theme")==="dark"?"светлая тема":"тёмная тема"}}label();
btn.addEventListener("click",function(){{var next=root.getAttribute("data-theme")==="dark"?"light":"dark";root.setAttribute("data-theme",next);label();try{{localStorage.setItem("conspectusTheme",next)}}catch(e){{}}}});}})();
</script>
</body>
</html>
"""


def main():
    lessons = [read(p) for p in sorted((ROOT / "content").glob("*.html"))]
    (ROOT / "notes").mkdir(exist_ok=True)
    used = set()
    for i, L in enumerate(lessons):
        out = lesson(i, L, lessons, used)
        (ROOT / "notes" / L["file"]).write_text(out)
        print(f'{L["file"]}: {len(out)//1024} КБ')
    (ROOT / "index.html").write_text(index(lessons))
    print("фигуры без места:", sorted(set(F) - used))


if __name__ == "__main__":
    main()
