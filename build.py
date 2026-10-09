#!/usr/bin/env python3
"""Build the static site from content/site.json.

    python3 build.py

Writes index.html, resume.html and works/<slug>.html. Standard library only.
Content strings are trusted HTML written by the site owner.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
C = json.loads((ROOT / "content" / "site.json").read_text(encoding="utf-8"))
P = C["person"]
FONTS = ("https://fonts.googleapis.com/css2?family=Anton&family=Archivo:ital,wght@0,400;0,500;0,600;1,400"
         "&family=JetBrains+Mono:wght@400;500&family=Noto+Sans+SC:wght@400;500;700&display=swap")
VER = "3"


def bi(v):
    """Bilingual value -> two spans; plain string -> as is."""
    if isinstance(v, dict):
        return f'<span lang="en">{v["en"]}</span><span lang="zh">{v["zh"]}</span>'
    return v


def nn(i):
    return f"{i:02d}"


def head(title, desc, base, og_img="assets/img/og.png"):
    return f"""<!doctype html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://kaihuan-huang.github.io/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f4f0e8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#14120f" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{base}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/css/folio.css?v={VER}">
<script src="{base}assets/js/folio.js?v={VER}"></script>
</head>
<body>
<a class="skip" href="#main"><span lang="en">Skip to content</span><span lang="zh">跳到正文</span></a>
"""


def all_items():
    return [("w", w) for w in C["works"]] + [("d", d) for d in C["deep"]]


def nav(base):
    rows = [f'<li><a href="{base}index.html#top"><span class="m-num">00</span><span class="m-title">{bi({"en": "Home", "zh": "首页"})}</span><span class="m-tag">Start</span></a></li>']
    for i, (_, w) in enumerate(all_items(), 1):
        rows.append(f'<li><a href="{base}works/{w["slug"]}.html"><span class="m-num">{nn(i)}</span><span class="m-title">{w["title"]}</span><span class="m-tag">{bi(w["type"])}</span></a></li>')
    n = len(all_items())
    rows.append(f'<li><a href="{base}resume.html"><span class="m-num">{nn(n + 1)}</span><span class="m-title">{bi({"en": "Résumé", "zh": "简历"})}</span><span class="m-tag">Web · print</span></a></li>')
    rows.append(f'<li><a href="{base}archive.html"><span class="m-num">A</span><span class="m-title">{bi({"en": "Learning Archive", "zh": "学习档案"})}</span><span class="m-tag">2023 — 2025</span></a></li>')
    rows.append(f'<li><a href="{base}notes/"><span class="m-num">{nn(n + 2)}</span><span class="m-title">{bi({"en": "Notes", "zh": "笔记"})}</span><span class="m-tag">Writing</span></a></li>')
    rows.append(f'<li><a href="{base}index.html#contact"><span class="m-num">{nn(n + 3)}</span><span class="m-title">{bi({"en": "Contact", "zh": "联系"})}</span><span class="m-tag">Say hi</span></a></li>')
    return f"""<nav class="nav" id="nav" aria-label="Main">
  <div class="wrap">
    <a class="brand" href="{base}index.html"><span class="stamp">KH</span><span class="b-txt">{P['name_first']} {P['name_last']} — Folio</span></a>
    <div class="nav-r">
      <a class="pill hide-sm" href="{base}resume.html">{bi({"en": "Résumé", "zh": "简历"})}</a>
      <button class="pill" id="lang-btn" type="button" aria-label="Switch language / 切换语言">中</button>
      <button class="pill" id="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{bi({"en": "Menu", "zh": "目录"})}</button>
    </div>
  </div>
</nav>
<div class="menu" id="menu" aria-hidden="true">
  <button class="pill menu-close" id="menu-close" type="button">{bi({"en": "Close", "zh": "关闭"})}</button>
  <div class="wrap">
    <ol>
      {chr(10).join(rows)}
    </ol>
    <div class="m-foot"><span>{bi(P['location'])}</span><a href="mailto:{P['email']}">{P['email']}</a><a href="{P['github']}">GitHub</a></div>
  </div>
</div>
"""


def footer(base):
    idx = "".join(f'<li><a href="{base}works/{w["slug"]}.html">{nn(i)} {w["title"]}</a></li>' for i, (_, w) in enumerate(all_items(), 1))
    return f"""<footer class="foot wrap">
  <div class="cols">
    <div>
      <div class="sign">{P['name_first']} {P['name_last']}</div>
      <div class="motto">{bi({"en": "Measure first. Ship second. Keep the receipts.", "zh": "先测量，再上线，留好凭据。"})}</div>
    </div>
    <div><h4>Index</h4><ul>{idx}</ul></div>
    <div><h4>{bi({"en": "Elsewhere", "zh": "其他"})}</h4><ul>
      <li><a href="{P['github']}">GitHub</a></li>
      <li><a href="{P['linkedin']}">LinkedIn</a></li>
      <li><a href="{base}resume.html">{bi({"en": "Résumé", "zh": "简历"})}</a></li>
      <li><a href="{base}archive.html">{bi({"en": "Learning Archive", "zh": "学习档案"})}</a></li>
      <li><a href="{base}notes/">{bi({"en": "Notes", "zh": "笔记"})}</a></li>
    </ul></div>
    <div><h4>{bi({"en": "Contact", "zh": "联系"})}</h4><ul>
      <li><a href="mailto:{P['email']}">{P['email']}</a></li>
      <li>{bi(P['location'])}</li>
    </ul></div>
  </div>
  <div class="base mono"><span>© <span id="year">2026</span> {P['name_first']} {P['name_last']}</span><span>{P['coords']}</span></div>
</footer>
</body>
</html>
"""


def flow(steps, big=False):
    lis = []
    for s in steps:
        cls = "step gate" if s.get("gate") else "step"
        lis.append(f'<li class="{cls}"><span>{bi(s)}</span></li>')
    return f'<ol class="flow{" big" if big else ""}" aria-label="Flow">{"".join(lis)}</ol>'


def metric(m):
    src = m["src"]
    s = f'<a href="{m["url"]}">{src}</a>' if m.get("url") else f'<span title="Private source">{src}</span>'
    return f'<div class="metric"><div class="mv">{m["v"]}</div><div class="ml">{bi(m["l"])}</div><div class="ms mono">src · {s}</div></div>'


# ---------------- index ----------------

def wall_card(i, w):
    return f"""      <article class="work reveal">
        <a href="works/{w['slug']}.html">
          <div class="w-label mono"><span>Nº{nn(i)}</span><span>{w['tag']}</span></div>
          <div class="frame"><img src="assets/img/works/{w['img']}" alt="{w['alt']}" loading="lazy" width="960" height="750"><span class="v-dim"></span></div>
          <div class="dim mono"><span class="d-line"></span><span class="d-txt">{w['dim']}</span></div>
          <div class="w-cap">
            <span class="num">{nn(i)}</span><h3>{w['title']}</h3>
            <span class="type">{bi(w['type'])}</span>
            <p>{bi(w['pitch'])}</p>
          </div>
        </a>
      </article>"""


def deep_card(i, d):
    return f"""      <article class="deep reveal">
        <a href="works/{d['slug']}.html">
          <div class="w-label mono"><span>Nº{nn(i)}</span><span>{bi(d['kicker'])}</span></div>
          <h3>{d['title']}</h3>
          <span class="type">{bi(d['type'])}</span>
          <p>{bi(d['pitch'])}</p>
          {flow(d['flow'])}
          <span class="go mono">{bi({"en": "Read the case →", "zh": "阅读案例 →"})}</span>
        </a>
      </article>"""


def build_index():
    works = C["works"]
    nw = len(works)
    cards = "\n".join(wall_card(i, w) for i, w in enumerate(works, 1))
    deeps = "\n".join(deep_card(nw + i, d) for i, d in enumerate(C["deep"], 1))
    stats = "".join(f'<div class="stat"><div class="st-num">{s["v"]}</div><div class="st-lab">{bi(s["l"])}</div></div>' for s in C["stats"])
    roles = ""
    for r in C["roles"]:
        items = "".join(f"<li>{bi(x)}</li>" for x in r["items"])
        roles += f'<li><span class="when mono">{r["when"]}</span><div><b>{r["title"]}</b><span class="at">{bi(r["at"])}</span>{f"<ul>{items}</ul>" if items else ""}</div></li>'
    skills = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in C["skills"])
    mq_words = ["Eval in CI", "Approval gates", "PII masking", "Audit trails", "Idempotent writes", "Bilingual LLM", "FastAPI · Postgres", "Row locks · outbox"]
    mq = "".join(f'<span class="mq-item">{x}</span>' for x in mq_words) * 2

    html = head(f"{P['name_first']} {P['name_last']} · AI Engineer",
                "Kaihuan Huang, AI engineer: production Python services and evaluated LLM applications. Live demos with source, tests and measured results.", "")
    html += f"""
<div class="intro" id="intro" aria-hidden="true">
  <div class="in-stage">
    <div class="kicker">Selected work · 2025–2026</div>
    <div class="in-name">{P['name_first']} <span class="red">{P['name_last']}</span></div>
    <div class="in-term" data-line="$ run evals --held-out  →  33/39 fully correct · 0 invented values"></div>
    <div class="in-hint">{bi({"en": "Click to enter", "zh": "点击进入"})}</div>
  </div>
</div>
{nav("")}
<main id="main">
  <header class="hero wrap" id="top">
    <div class="hero-top mono">
      <span>Section A–A · {bi({"en": "Selected work", "zh": "作品选"})}</span>
      <span>{P['coords']}</span>
    </div>
    <h1>{P['name_first']} <span class="red">{P['name_last']}</span></h1>
    <div class="hero-row">
      <div>
        <p class="role-line">{bi(P['role_line'])}</p>
        <p class="dek">{bi(P['dek'])}</p>
        <p class="avail mono"><span class="dot"></span>{bi({"en": "Open to AI / backend engineering roles · US permanent resident", "zh": "正在看 AI / 后端工程岗位 · 美国永久居民"})}</p>
      </div>
      <div class="cta">
        <a class="btn solid" href="mailto:{P['email']}?subject=Intro%20call">{bi({"en": "Email me →", "zh": "发邮件 →"})}</a>
        <a class="btn" href="resume.html">{bi({"en": "Résumé", "zh": "简历"})}</a>
      </div>
    </div>
  </header>

  <section class="wall wrap" id="works" aria-labelledby="works-h">
    <div class="wall-head">
      <h2 id="works-h">{bi({"en": "Six works on the wall", "zh": "墙上的六件作品"})}</h2>
      <span class="mono muted">{bi({"en": "Live · independent reimplementations · synthetic data · source &amp; tests", "zh": "在线 · 独立重写 · 合成数据 · 附源码与测试"})}</span>
    </div>
    <div class="works">
{cards}
    </div>
    <div class="wall-foot mono">
      <span>AI systems · 2025 — 2026 · {P['name_first']} {P['name_last']}</span>
      <span>{bi({"en": "Hover to measure · click to enter", "zh": "悬停测量 · 点击进入"})}</span>
    </div>
  </section>

  <div class="mq" aria-hidden="true"><div class="mq-track">{mq}</div></div>

  <section class="sec wrap" id="deep" aria-labelledby="deep-h">
    <div class="sec-head"><span class="n">01</span><h2 id="deep-h">— {bi({"en": "Behind the wall", "zh": "墙后的工作"})}</h2><span class="sec-note mono">{bi({"en": "Production &amp; private code · design and results only", "zh": "生产与私有代码 · 只展示设计与结果"})}</span></div>
    <div class="deeps">
{deeps}
    </div>
  </section>

  <section class="sec wrap" id="archive" aria-labelledby="archive-h">
    <div class="sec-head"><span class="n">02</span><h2 id="archive-h">— {bi({"en": "Learning Archive", "zh": "学习档案"})}</h2><span class="sec-note mono">{bi({"en": "2023 — 2025 · what each early project taught me", "zh": "2023 — 2025 · 每个早期项目教会我的事"})}</span></div>
    <p class="arch-intro">{bi(C['archive_intro'])}</p>
    {archive_register("")}
    <div class="cta left"><a class="btn" href="archive.html">{bi({"en": "Open the archive →", "zh": "打开学习档案 →"})}</a></div>
  </section>

  <section class="sec wrap" id="about" aria-labelledby="about-h">
    <div class="sec-head"><span class="n">03</span><h2 id="about-h">— {bi({"en": "The Engineer", "zh": "工程师"})}</h2></div>
    <div class="study">
      <figure class="fig reveal">
        <div class="plate" id="plate">{PLATE_SVG}</div>
        <figcaption class="mono"><span>FIG. 01 — {bi({"en": "The model proposes; the system decides", "zh": "模型提议，系统决定"})}</span><span>York · MSc</span></figcaption>
      </figure>
      <div class="reveal">
        <span class="kicker">{bi({"en": "Profile", "zh": "简介"})}</span>
        <h3>{bi({"en": "Measured before it ships", "zh": "上线之前，先量清楚"})}</h3>
        <p class="quote">{bi({"en": "“A model's answer is a proposal. What runs is decided by rules, tests and an explicit yes.”", "zh": "“模型的回答只是提议。真正执行什么，由规则、测试和一句明确的‘是’来决定。”"})}</p>
        <p>{bi({"en": "I build production Python services and evaluated LLM applications. At <b>Jackson Ventures</b> I shipped a reservation service real guests use, led the IPOT POS backend, rebuilt <b>Nalu</b> after its LLM pilot invented booking values, and built loan-draw review controls for <b>BloomFrontier</b>. Before that, at <b>Polygraf.ai</b>, I built PII detection and policy enforcement for text sent to AI tools.", "zh": "我做生产级 Python 服务和经过评估的 LLM 应用。在 <b>Jackson Ventures</b>，我上线了真实客人在用的预订服务，主导 IPOT 的 POS 后端，在 LLM 试点编造预订字段后重建了 <b>Nalu</b>，并为 <b>BloomFrontier</b> 构建提款审核控制。此前在 <b>Polygraf.ai</b>，我为发往 AI 工具的文本构建 PII 检测与策略执行。"})}</p>
        <p>{bi({"en": "Every number on this site names where it was measured. Where the code is private, the case page says so.", "zh": "本站每个数字都注明测量来源；代码不公开的，案例页会直接说明。"})}</p>
        <div class="stats">{stats}</div>
        <ul class="roles">{roles}</ul>
        <dl class="skills">{skills}</dl>
      </div>
    </div>
  </section>

  <section class="sec wrap" id="contact" aria-labelledby="contact-h">
    <div class="sec-head"><span class="n">04</span><h2 id="contact-h">— {bi({"en": "The Invitation", "zh": "邀请"})}</h2></div>
    <div class="invite reveal">
      <span class="kicker">{bi({"en": "Hiring for AI or backend engineering?", "zh": "在招 AI 或后端工程师？"})}</span>
      <div class="big">{bi({"en": "Let's build<br>what <span class=\"red\">ships</span>", "zh": "一起做<br>能<span class=\"red\">上线</span>的东西"})}</div>
      <a class="mail" href="mailto:{P['email']}">{P['email']}</a>
      <div class="cta">
        <a class="btn solid" href="mailto:{P['email']}?subject=20-minute%20intro%20call">{bi({"en": "Book a 20-min intro →", "zh": "约 20 分钟聊聊 →"})}</a>
        <a class="btn" href="resume.html">{bi({"en": "Résumé", "zh": "简历"})}</a>
        <a class="btn" href="{P['github']}">GitHub</a>
      </div>
      <p>{bi({"en": "San Francisco Bay Area · US permanent resident, no sponsorship needed.", "zh": "旧金山湾区 · 美国永久居民，无需工作签证担保。"})}</p>
    </div>
  </section>
</main>
"""
    html += footer("")
    (ROOT / "index.html").write_text(html, encoding="utf-8")


# ---------------- case pages ----------------

def build_case(i, kind, w, prev, nxt):
    spec = "".join(f"<dt>{k}</dt><dd>{bi(v)}</dd>" for k, v in w["spec"])
    approach = "".join(f"<li>{bi(a)}</li>" for a in w["approach"])
    metrics = "".join(metric(m) for m in w["metrics"])
    limits = "".join(f"<li>{bi(x)}</li>" for x in w["limits"])
    if kind == "w":
        hero = f"""<figure class="case-hero">
      <div class="frame"><img src="../assets/img/works/{w['img']}" alt="{w['alt']}" width="960" height="750"><span class="v-dim"></span></div>
      <div class="dim mono on"><span class="d-line"></span><span class="d-txt">{w['dim']}</span></div>
    </figure>"""
        btns = f'<a class="btn solid" href="{w["demo"]}">{bi({"en": "Open live demo →", "zh": "打开在线演示 →"})}</a>'
        if w.get("repo"):
            btns += f'<a class="btn" href="{w["repo"]}">{bi({"en": "Source", "zh": "源码"})}</a>'
        for t, u in w.get("extra_links", []):
            btns += f'<a class="btn" href="{u}">{t}</a>'
        kicker = w["tag"]
    else:
        hero = f'<figure class="case-hero plate-flow"><div class="sheet">{flow(w["flow"], big=True)}<div class="sheet-foot mono"><span>SECTION · {w["title"].upper()}</span><span>{bi({"en": "Design view · code private", "zh": "设计视图 · 代码私有"})}</span></div></div></figure>'
        btns = ""
        if w.get("link"):
            btns = f'<a class="btn solid" href="{w["link"][1]}">{w["link"][0]} →</a>'
        kicker = bi(w["kicker"])
    pager = f"""<nav class="pager wrap mono" aria-label="More work">
    <a href="{prev['slug']}.html">← {prev['title']}</a>
    <a href="../index.html#works">{bi({"en": "All work", "zh": "全部作品"})}</a>
    <a href="{nxt['slug']}.html">{nxt['title']} →</a>
  </nav>"""
    secs = [({"en": "Problem", "zh": "问题"}, f'<p class="lead">{bi(w["problem"])}</p>')]
    if kind == "w":
        secs.append(({"en": "Flow", "zh": "流程"}, flow(w["flow"])))
    secs.append(({"en": "What I built", "zh": "我做了什么"}, f'<ul class="approach">{approach}</ul>'))
    if w.get("video"):
        v = w["video"]
        secs.append(({"en": "Watch it run", "zh": "看它运行"}, f'<figure class="case-video"><video src="{v["src"]}" controls muted playsinline preload="none" poster="{v.get("poster", "")}"></video><figcaption class="mono">{bi(v["cap"])}</figcaption></figure>'))
    secs.append(({"en": "Measured", "zh": "测量结果"}, f'<div class="metrics">{metrics}</div>'))
    secs.append(({"en": "Limits, stated plainly", "zh": "局限，直说"}, f'<ul class="limits">{limits}</ul>'))
    body = "".join(f'<section class="case-sec"><h2 class="case-h"><span class="mono">{nn(k)}</span>{bi(h)}</h2>{c}</section>' for k, (h, c) in enumerate(secs, 1))
    html = head(f"{w['title']} · {P['name_first']} {P['name_last']}", w["pitch"]["en"], "../")
    html += nav("../")
    html += f"""<main id="main" class="case">
  <header class="wrap case-head">
    <div class="hero-top mono"><span>Nº{nn(i)} · {kicker}</span><span>{bi(w['type'])}</span></div>
    <h1>{w['title']}</h1>
    <p class="case-pitch">{bi(w['pitch'])}</p>
    <div class="cta left">{btns}</div>
  </header>
  <div class="wrap">{hero}</div>
  <div class="wrap case-body">
    <aside class="titleblock"><dl>{spec}</dl></aside>
    <div class="case-main">
      {body}
    </div>
  </div>
  {pager}
</main>
"""
    html += footer("../")
    out = ROOT / "works" / f"{w['slug']}.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")


# ---------------- learning archive ----------------

def slug_title(slug):
    for _, w in all_items():
        if w["slug"] == slug:
            return w["title"]
    return slug


def archive_register(base):
    rows = ""
    for k, a in enumerate(C["archive"], 1):
        rows += f"""<li class="reg-row reveal"><a href="{base}archive.html#{a['id']}">
          <span class="r-no mono">A{nn(k)}</span>
          <span class="r-yr mono">{a['years']}</span>
          <span class="r-ti"><b>{bi(a['title'])}</b><em>{bi(a['kind'])}</em></span>
          <span class="r-rule">{bi(a['rule'])}</span>
          <span class="r-now mono">→ {slug_title(a['now'])}</span>
        </a></li>"""
    head_row = f"""<li class="reg-head mono" aria-hidden="true"><span>No.</span><span>{bi({"en": "Year", "zh": "年份"})}</span><span>{bi({"en": "Sheet", "zh": "图纸"})}</span><span>{bi({"en": "The rule it left me", "zh": "留下的规则"})}</span><span>{bi({"en": "Shows today in", "zh": "今天体现在"})}</span></li>"""
    return f'<ol class="register">{head_row}{rows}</ol>'


def timeline():
    pts = [("2023", {"en": "First LLM apps · York MSc · hackathons", "zh": "第一批 LLM 应用 · 约克硕士 · 黑客松"}),
           ("2024", {"en": "Rebuilding models · team product", "zh": "拆模型 · 团队产品"}), ("2025", {"en": "Polygraf.ai · PII & policy", "zh": "Polygraf.ai · PII 与策略"}),
           ("2026", {"en": "Production at Jackson Ventures", "zh": "Jackson Ventures 生产环境"})]
    lis = ""
    for i, (y, l) in enumerate(pts):
        cls = ' class="now"' if i == len(pts) - 1 else ""
        lis += f'<li{cls}><span class="t-yr">{y}</span><span class="t-lb">{bi(l)}</span></li>'
    return f'<ol class="timeline" aria-label="Timeline">{lis}</ol>'


def build_archive():
    sheets = ""
    for k, a in enumerate(C["archive"], 1):
        repos = " · ".join(a["repos"])
        sheets += f"""<article class="sheet-a reveal" id="{a['id']}">
      <div class="sa-side mono"><span class="sa-no">A{nn(k)}</span><span>{a['years']}</span><span>{bi(a['kind'])}</span></div>
      <div class="sa-main">
        <h2>{bi(a['title'])}</h2>
        <p class="sa-stack mono">{a['stack']}</p>
        <dl class="sa-dl">
          <dt>{bi({"en": "Then", "zh": "当时"})}</dt><dd>{bi(a['then'])}</dd>
          <dt>{bi({"en": "What it taught me", "zh": "学到的"})}</dt><dd>{bi(a['learned'])}</dd>
          <dt class="red">{bi({"en": "The rule", "zh": "规则"})}</dt><dd class="sa-rule">{bi(a['rule'])}</dd>
        </dl>
        <div class="sa-foot mono"><span>{bi({"en": "Repos", "zh": "仓库"})}: {repos}</span><a href="works/{a['now']}.html">{bi({"en": "Shows today in", "zh": "今天体现在"})} {slug_title(a['now'])} →</a></div>
      </div>
    </article>"""
    html = head(f"Learning Archive · {P['name_first']} {P['name_last']}", "Earlier projects and the engineering rules they left behind.", "")
    html += nav("")
    html += f"""<main id="main" class="case">
  <header class="wrap case-head">
    <div class="hero-top mono"><span>Section C–C · {bi({"en": "Learning archive", "zh": "学习档案"})}</span><span>2023 — 2026</span></div>
    <h1>{bi({"en": "How I got here", "zh": "一路走来"})}</h1>
    <p class="case-pitch">{bi(C['archive_intro'])}</p>
  </header>
  <div class="wrap">{timeline()}</div>
  <div class="wrap sheets">{sheets}</div>
  <nav class="pager wrap mono" aria-label="More"><a href="index.html#archive">← {bi({"en": "Back", "zh": "返回"})}</a><a href="index.html#works">{bi({"en": "All work", "zh": "全部作品"})}</a><a href="resume.html">{bi({"en": "Résumé", "zh": "简历"})} →</a></nav>
</main>
"""
    html += footer("")
    (ROOT / "archive.html").write_text(html, encoding="utf-8")


# ---------------- résumé ----------------

def build_resume():
    roles = ""
    for r in C["roles"]:
        items = "".join(f"<li>{bi(x)}</li>" for x in r["items"])
        roles += f'<div class="r-role"><div class="r-top"><b>{r["title"]}</b><span class="mono">{r["when"]}</span></div><div class="r-at">{bi(r["at"])}</div>{f"<ul>{items}</ul>" if items else ""}</div>'
    proj = ""
    for _, w in all_items():
        url = w.get("demo") or f"https://kaihuan-huang.github.io/works/{w['slug']}.html"
        proj += f'<div class="r-role"><div class="r-top"><b><a href="{url}">{w["title"]}</a></b><span class="mono">{bi(w["type"])}</span></div><div class="r-at">{bi(w["pitch"])}</div></div>'
    skills = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in C["skills"])
    html = head(f"Résumé · {P['name_first']} {P['name_last']}", "Résumé of Kaihuan Huang, AI engineer.", "")
    html += nav("")
    html += f"""<main id="main" class="resume wrap">
  <div class="r-actions no-print"><button class="btn solid" type="button" onclick="window.print()">{bi({"en": "Print / save as PDF", "zh": "打印 / 存为 PDF"})}</button></div>
  <header class="r-head">
    <h1>{P['name_first']} {P['name_last']}</h1>
    <p>{bi(P['role_line'])}</p>
    <p class="mono">{bi(P['location'])} · US permanent resident · <a href="mailto:{P['email']}">{P['email']}</a> · <a href="{P['github']}">github.com/kaihuan-huang</a> · <a href="https://kaihuan-huang.github.io/">kaihuan-huang.github.io</a></p>
  </header>
  <section><h2>{bi({"en": "Experience", "zh": "经历"})}</h2>{roles}</section>
  <section><h2>{bi({"en": "Selected work", "zh": "作品"})}</h2>{proj}</section>
  <section><h2>{bi({"en": "Skills", "zh": "技能"})}</h2><dl class="skills">{skills}</dl></section>
</main>
"""
    html += footer("")
    (ROOT / "resume.html").write_text(html, encoding="utf-8")


PLATE_SVG = (ROOT / "assets" / "img" / "plate.svg").read_text(encoding="utf-8")

if __name__ == "__main__":
    build_index()
    items = all_items()
    for i, (kind, w) in enumerate(items, 1):
        prev = items[i - 2][1]
        nxt = items[i % len(items)][1]
        build_case(i, kind, w, prev, nxt)
    build_resume()
    build_archive()
    print(f"built index.html, resume.html and {len(items)} case pages")
