#!/usr/bin/env python3
"""Static site generator for Impact Capital VC. Run: python3 build.py"""
import json, os, shutil, html, datetime
from babel.dates import format_date

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "..", "dist")
BASE_URL = os.environ.get("BASE_URL", "https://impactcapital.vc").rstrip("/")
GTM_ID = "GTM-PH9PW3JR"
BRAND = "Impact Capital VC"
CONTACT = "mailto:hello@impactcapital.vc"
LINKEDIN = "https://www.linkedin.com/"
X_URL = "https://x.com/"

LANGS = [  # code, hreflang, native name, babel locale, dir
    ("en", "en", "English", "en", "ltr"), ("zh", "zh-Hans", "简体中文", "zh_Hans", "ltr"),
    ("es", "es", "Español", "es", "ltr"), ("hi", "hi", "हिन्दी", "hi", "ltr"),
    ("ar", "ar", "العربية", "ar", "rtl"), ("fr", "fr", "Français", "fr", "ltr"),
    ("pt", "pt", "Português", "pt", "ltr"), ("ru", "ru", "Русский", "ru", "ltr"),
    ("ja", "ja", "日本語", "ja", "ltr"), ("de", "de", "Deutsch", "de", "ltr"),
    ("id", "id", "Bahasa Indonesia", "id", "ltr"), ("bn", "bn", "বাংলা", "bn", "ltr"),
    ("ur", "ur", "اردو", "ur", "rtl"), ("tr", "tr", "Türkçe", "tr", "ltr"),
    ("ko", "ko", "한국어", "ko", "ltr"), ("vi", "vi", "Tiếng Việt", "vi", "ltr"),
]

COMPANIES = [  # slug, name, url, image, investment-note date (newest first)
    ("defy", "Defy", "https://www.defygroup.ai/", "defy", "2026-08-25"),
    ("touchigh", "ToucHigh", "https://touchigh.ai/", "touchigh", "2026-03-17"),
    ("somonitor", "Somonitor", "https://somonitor.ai/", "somonitor", "2025-09-03"),
    ("matrex", "Matrex Analytica", "https://matrexanalytica.com/", "matrex", "2025-02-11"),
    ("mindfuse", "Mindfuse", "https://mindfuse.sg/", "mindfuse", "2024-06-20"),
    ("snmrush", "SNMRush", "https://snmrush.com/", "snmrush", "2023-12-05"),
]
COMPANY_SLUGS = {"defy": "defy", "touchigh": "touchigh", "somonitor": "somonitor",
                 "matrex": "matrex-analytica", "mindfuse": "mindfuse", "snmrush": "snmrush"}

ARTICLES = [  # id, slug, date, type
    ("a01", "nvidia-ceo-investigation-ai-industry-impact", "2026-11-09", "NewsArticle"),
    ("a02", "ai-capital-supercycle-venture-funding", "2026-10-14", "BlogPosting"),
    ("a03", "why-agentic-ai-is-the-next-venture-frontier", "2026-09-02", "BlogPosting"),
    ("a04", "application-layer-moats-beyond-foundation-models", "2026-07-21", "BlogPosting"),
    ("a05", "compute-economics-ai-startups", "2026-06-10", "BlogPosting"),
    ("a06", "from-search-to-answers-geo-aeo-venture-opportunity", "2026-04-28", "BlogPosting"),
    ("a07", "valuation-discipline-in-the-ai-boom", "2026-03-17", "BlogPosting"),
    ("a08", "singapore-asia-ai-corridor-venture", "2026-02-03", "BlogPosting"),
    ("a09", "scientist-founders-agentic-ai", "2025-12-09", "BlogPosting"),
    ("a10", "agentic-ai-smes-cross-border-commerce", "2025-10-21", "BlogPosting"),
    ("a11", "responsible-ai-governance-investment-criterion", "2025-09-16", "BlogPosting"),
]
SOURCES = {"a01": [
    ("Al Jazeera / Reuters — Nvidia investigates CEO Jensen Huang (8 Nov 2026)", "https://www.aljazeera.com/news/2026/11/8/us-chipmaker-nvidia-investigates-ceo-jensen-huang-over-affair"),
    ("Yahoo Finance — Nvidia's board launches investigation (8 Nov 2026)", "https://finance.yahoo.com/markets/article/nvidias-jensen-huang-admits-to-affair-after-allegations-of-romance-with-chinese-spy-report-205122263.html"),
    ("CNBC — Huang affair and Nvidia succession (9 Nov 2026)", "https://www.cnbc.com/2026/11/09/jensen-huang-affair-nvidia-succession.html"),
    ("Bloomberg — Nvidia board to probe spying case (8 Nov 2026)", "https://www.bloomberg.com/news/articles/2026-11-08/nvidia-board-to-probe-spying-case-after-ceo-jensen-huang-admits-infidelity"),
    ("Axios — Huang's letter to staff (8 Nov 2026)", "https://www.axios.com/2026/11/08/nvidia-ceo-jensen-huang-affair-email-to-company"),
]}

T = {}
for code, *_ in LANGS:
    with open(os.path.join(ROOT, "i18n", f"{code}.json"), encoding="utf-8") as f:
        T[code] = json.load(f)

e = html.escape
def ja(s):  # JSON for script tags
    return json.dumps(s, ensure_ascii=False).replace("</", "<\\/")

def fdate(d, loc):
    return format_date(datetime.date.fromisoformat(d), "long", locale=loc)

def write(rel, content):
    p = os.path.join(DIST, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

def page_url(lang, path):  # path like "" or "portfolio/defy/"
    return f"{BASE_URL}/{lang}/{path}"

GTM_HEAD = f"""<!-- Google Tag Manager -->
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());
(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->"""
GTM_BODY = f"""<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>"""

LOGO = """<svg viewBox="0 0 40 40" width="40" height="40" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5B5BF7"/><stop offset=".55" stop-color="#19D3C5"/><stop offset="1" stop-color="#FFB547"/></linearGradient></defs><circle cx="20" cy="20" r="19" fill="url(#lg)"/><path d="M14 11v18M20 29V11l7 9-7 9" stroke="#070A1F" stroke-width="3.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>"""

def head(lang, title, desc, path, depth, img="og.jpg", jsonld=(), og_type="website", extra=""):
    L = dict((c, (h, n, b, d)) for c, h, n, b, d in LANGS)
    rp = "../" * depth
    alts = "\n".join(f'<link rel="alternate" hreflang="{h}" href="{page_url(c, path)}">' for c, h, *_ in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{page_url("en", path)}">'
    ld = "\n".join(f'<script type="application/ld+json">{ja(x)}</script>' for x in jsonld)
    ogloc = "\n".join(f'<meta property="og:locale:alternate" content="{b}">' for c, h, n, b, d in LANGS if c != lang)
    return f"""<!doctype html>
<html lang="{L[lang][0]}" dir="{L[lang][3]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{GTM_HEAD}
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<link rel="canonical" href="{page_url(lang, path)}">
{alts}
<meta property="og:site_name" content="{BRAND}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{page_url(lang, path)}">
<meta property="og:image" content="{BASE_URL}/assets/img/{img}">
<meta property="og:locale" content="{L[lang][2]}">
{ogloc}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{BASE_URL}/assets/img/{img}">
<meta name="theme-color" content="#070A1F">
<link rel="icon" href="{rp}assets/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{rp}site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="{BRAND} — AI Perspectives" href="{BASE_URL}/{lang}/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rp}assets/style.css">
{extra}
{ld}
</head>"""

def nav(lang, path, depth):
    u = T[lang]["ui"]; rp = "../" * depth
    opts = "".join(
        f'<li><a href="{rp}{c}/{path}" hreflang="{h}" lang="{h}"{" aria-current=\"true\"" if c == lang else ""}>{n}</a></li>'
        for c, h, n, *_ in LANGS)
    cur = dict((c, n) for c, h, n, *_ in LANGS)[lang]
    return f"""<body>
{GTM_BODY}
<a class="skip" href="#main">{e(u['skip'])}</a>
<header class="nav"><div class="wrap nav-in">
<a class="brand" href="{rp}{lang}/" aria-label="{BRAND}">{LOGO}<span>Impact Capital <b>VC</b></span></a>
<nav aria-label="Main"><ul class="menu">
<li><a href="{rp}{lang}/#portfolio">{e(u['nav_portfolio'])}</a></li>
<li><a href="{rp}{lang}/#collective">{e(u['nav_collective'])}</a></li>
<li><a href="{rp}{lang}/perspectives/">{e(u['nav_perspectives'])}</a></li>
<li><a href="{CONTACT}">{e(u['nav_contact'])}</a></li>
</ul></nav>
<details class="lang"><summary aria-label="{e(u['language'])}"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18" fill="none" stroke="currentColor" stroke-width="1.6"/></svg><span>{cur}</span></summary><ul>{opts}</ul></details>
</div></header>
<main id="main">"""

def footer(lang, depth):
    u = T[lang]["ui"]; rp = "../" * depth
    return f"""</main>
<footer class="foot"><div class="wrap foot-in">
<div><a class="brand" href="{rp}{lang}/">{LOGO}<span>Impact Capital <b>VC</b></span></a><p class="muted">{e(u['footer_tag'])}</p></div>
<div><h2>{e(u['connect'])}</h2><ul><li><a href="{X_URL}" rel="noopener">X</a></li><li><a href="{LINKEDIN}" rel="noopener">LinkedIn</a></li><li><a href="{CONTACT}">{e(u['careers'])}</a></li><li><a href="{CONTACT}">{e(u['nav_contact'])}</a></li></ul></div>
<div><h2>{e(u['nav_perspectives'])}</h2><ul><li><a href="{rp}{lang}/perspectives/">{e(u['perspectives_title'])}</a></li><li><a href="{rp}{lang}/#portfolio">{e(u['nav_portfolio'])}</a></li><li><a href="{rp}{lang}/feed.xml">RSS</a></li></ul></div>
<div><h2>{e(u['legal'])}</h2><ul><li><a href="{rp}{lang}/privacy/">{e(u['privacy'])}</a></li></ul></div>
</div><div class="wrap copy">© {datetime.date.today().year} {BRAND}. {e(u['rights'])}</div></footer>
<script src="{rp}assets/site.js" defer></script>
</body></html>"""

def org_ld():
    return {"@context": "https://schema.org", "@type": ["Organization", "FinancialService"], "@id": f"{BASE_URL}/#org",
            "name": BRAND, "alternateName": "Impact Capital", "url": BASE_URL + "/",
            "logo": f"{BASE_URL}/assets/favicon.svg", "image": f"{BASE_URL}/assets/img/og.jpg",
            "description": T["en"]["ui"]["site_desc"],
            "knowsAbout": ["Venture capital", "Agentic AI", "Artificial intelligence", "Generative engine optimization", "AI startups"],
            "sameAs": [LINKEDIN, X_URL]}

def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

def faq_ld(pairs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}

def img(name, alt, cls="", eager=False, sizes="100vw", rp=""):
    return (f'<img class="{cls}" src="{rp}assets/img/{name}.webp" srcset="{rp}assets/img/{name}-sm.webp 640w, {rp}assets/img/{name}.webp 1536w" '
            f'sizes="{sizes}" width="1536" height="1024" alt="{e(alt)}" {"fetchpriority=\"high\"" if eager else "loading=\"lazy\""} decoding="async">')

ARROW = '<span class="arr" aria-hidden="true">→</span>'

def build_home(lang):
    t = T[lang]; u, h, C, A = t["ui"], t["home"], t["companies"], t["articles"]
    rp = "../"; L = dict((c, b) for c, hh, n, b, d in LANGS)[lang]
    slides = [f"""<article class="slide is-on" data-i="0">{img('hero', h['hero_title'], 'bg', True, rp=rp)}
<div class="wrap slide-in"><p class="kicker">{e(h['hero_kicker'])}</p><h1>{e(h['hero_title'])}</h1><p class="lead">{e(h['hero_sub'])}</p>
<a class="btn" href="#portfolio">{e(u['nav_portfolio'])} {ARROW}</a></div></article>"""]
    for i, (k, name, url, im, d) in enumerate(COMPANIES, 1):
        slides.append(f"""<article class="slide" data-i="{i}">{img(im, name + ' — ' + C[k]['tagline'], 'bg', rp=rp)}
<div class="wrap slide-in"><p class="kicker">{e(name)}</p><h2 class="h1">{e(C[k]['tagline'])}</h2><p class="lead">{e(C[k]['summary'])}</p>
<a class="btn" href="portfolio/{COMPANY_SLUGS[k]}/">{e(u['learn_more'])} {ARROW}</a></div></article>""")
    dots = "".join(f'<button aria-label="{i+1}" data-go="{i}"{" class=\"on\"" if i == 0 else ""}></button>' for i in range(len(slides)))
    grid = "".join(f"""<a class="tile" href="portfolio/{COMPANY_SLUGS[k]}/">{img(im, name, 'tile-img', sizes='(max-width:700px) 100vw, 33vw', rp=rp)}
<span class="tile-body"><span class="tile-sector">{e(C[k]['sector'])}</span><strong>{e(name)}</strong><span class="tile-tag">{e(C[k]['tagline'])}</span></span></a>""" for k, name, url, im, d in COMPANIES)
    pillars = "".join(f'<div class="pillar"><span class="num">0{i}</span><h3>{e(h[f"p{i}_t"])}</h3><p>{e(h[f"p{i}_d"])}</p></div>' for i in (1, 2, 3))
    coll = "".join(f'<div class="card"><h3>{e(h[f"c{i}_t"])}</h3><p>{e(h[f"c{i}_d"])}</p></div>' for i in (1, 2, 3, 4))
    arts = "".join(article_card(lang, a, rp, "perspectives/") for a in ARTICLES[:3])
    faqs = [(h[f"faq{i}_q"], h[f"faq{i}_a"]) for i in (1, 2, 3, 4)]
    faqh = "".join(f"<details class=\"qa\"><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs)
    ld = [org_ld(),
          {"@context": "https://schema.org", "@type": "WebSite", "@id": f"{BASE_URL}/#web", "name": BRAND, "url": BASE_URL + "/",
           "inLanguage": [x[1] for x in LANGS], "publisher": {"@id": f"{BASE_URL}/#org"}},
          {"@context": "https://schema.org", "@type": "ItemList", "name": f"{BRAND} portfolio",
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": page_url(lang, f"portfolio/{COMPANY_SLUGS[k]}/")} for i, (k, n, *_r) in enumerate(COMPANIES)]},
          faq_ld(faqs)]
    body = f"""<section class="hero" aria-roledescription="carousel">{''.join(slides)}<div class="dots wrap">{dots}</div></section>
<section class="statement wrap"><p class="kicker">{e(h['statement_kicker'])}</p><h2 class="display">{h['statement_title']}</h2><p class="lead">{e(h['statement_text'])}</p></section>
<section class="wrap block"><p class="kicker">{e(h['thesis_kicker'])}</p><h2 class="display sm">{e(h['thesis_title'])}</h2><div class="pillars">{pillars}</div></section>
<section id="portfolio" class="wrap block"><p class="kicker">{e(h['portfolio_kicker'])}</p><h2 class="display">{h['portfolio_title']}</h2><div class="grid">{grid}</div></section>
<section id="collective" class="wrap block"><p class="kicker">{e(h['collective_kicker'])}</p><h2 class="display">{h['collective_title']}</h2><div class="cards">{coll}</div></section>
<section class="wrap block"><p class="kicker">{e(h['perspectives_kicker'])}</p><h2 class="display">{h['perspectives_title']}</h2><div class="arts">{arts}</div>
<p><a class="btn ghost" href="perspectives/">{e(h['all_articles'])} {ARROW}</a></p></section>
<section class="wrap block"><h2 class="display sm">{e(u['faq'])}</h2><div class="faq">{faqh}</div></section>
<section class="wrap cta"><h2 class="display">{h['cta_title']}</h2><p class="lead">{e(h['cta_text'])}</p><a class="btn" href="{CONTACT}">{e(h['cta_btn'])} {ARROW}</a></section>"""
    write(f"{lang}/index.html", head(lang, u["site_title"], u["site_desc"], "", 1, jsonld=ld) + nav(lang, "", 1) + body + footer(lang, 1))

def article_card(lang, a, rp, base):
    aid, slug, d, _ = a; A = T[lang]["articles"][aid]; loc = dict((c, b) for c, h, n, b, dd in LANGS)[lang]
    return f"""<a class="art" href="{base}{slug}/">{img(aid, A['title'], 'art-img', sizes='(max-width:700px) 100vw, 33vw', rp=rp)}
<span class="art-body"><time datetime="{d}">{fdate(d, loc)}</time><strong>{e(A['title'])}</strong><span class="muted">{e(A['desc'])}</span></span></a>"""

def build_perspectives(lang):
    u = T[lang]["ui"]; rp = "../../"
    cards = "".join(article_card(lang, a, rp, "") for a in ARTICLES)
    ld = [org_ld(), crumbs([(BRAND, page_url(lang, "")), (u["perspectives_title"], page_url(lang, "perspectives/"))]),
          {"@context": "https://schema.org", "@type": "CollectionPage", "name": u["perspectives_title"], "description": u["perspectives_desc"],
           "inLanguage": dict((c, h) for c, h, *_ in LANGS)[lang], "url": page_url(lang, "perspectives/"),
           "hasPart": [{"@type": a[3], "headline": T[lang]["articles"][a[0]]["title"], "url": page_url(lang, f"perspectives/{a[1]}/"), "datePublished": a[2]} for a in ARTICLES]}]
    body = f"""<section class="wrap page-head"><p class="kicker">{BRAND}</p><h1 class="display">{e(u['perspectives_title'])}</h1><p class="lead">{e(u['perspectives_desc'])}</p></section>
<section class="wrap block"><div class="arts">{cards}</div></section>"""
    write(f"{lang}/perspectives/index.html", head(lang, f"{u['perspectives_title']} | {BRAND}", u["perspectives_desc"], "perspectives/", 2, jsonld=ld) + nav(lang, "perspectives/", 2) + body + footer(lang, 2))

def build_article(lang, idx):
    aid, slug, d, typ = ARTICLES[idx]; u = T[lang]["ui"]; A = T[lang]["articles"][aid]; rp = "../../../"
    loc = dict((c, b) for c, h, n, b, dd in LANGS)[lang]; hl = dict((c, h) for c, h, *_ in LANGS)[lang]
    path = f"perspectives/{slug}/"
    paras = "".join(f"<p>{e(p)}</p>" for p in A["body"])
    tk = "".join(f"<li>{e(x)}</li>" for x in A["takeaways"])
    src = ""
    if aid in SOURCES:
        src = f'<section class="sources"><h2>{e(u["sources"])}</h2><ol>' + "".join(f'<li><a href="{s}" rel="noopener nofollow">{e(n)}</a></li>' for n, s in SOURCES[aid]) + "</ol></section>"
    related = [a for a in ARTICLES if a[0] != aid][:3] if idx else ARTICLES[1:4]
    rel = "".join(article_card(lang, a, rp, "../") for a in related)
    ld = [{"@context": "https://schema.org", "@type": typ, "headline": A["title"], "description": A["desc"],
           "image": [f"{BASE_URL}/assets/img/{aid}.webp"], "datePublished": d, "dateModified": d, "inLanguage": hl,
           "author": {"@type": "Organization", "name": u["author"], "url": BASE_URL + "/"},
           "publisher": {"@id": f"{BASE_URL}/#org", "@type": "Organization", "name": BRAND, "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/assets/favicon.svg"}},
           "mainEntityOfPage": page_url(lang, path), "articleBody": " ".join(A["body"]),
           "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".article-desc", ".takeaways"]},
           **({"citation": [s for n, s in SOURCES[aid]]} if aid in SOURCES else {})},
          crumbs([(BRAND, page_url(lang, "")), (u["perspectives_title"], page_url(lang, "perspectives/")), (A["title"], page_url(lang, path))]),
          faq_ld([(A["faq_q"], A["faq_a"])]), org_ld()]
    extra = f'<meta property="article:published_time" content="{d}">'
    body = f"""<article class="wrap article">
<nav class="crumbs" aria-label="Breadcrumb"><a href="../../">{BRAND}</a> / <a href="../">{e(u['perspectives_title'])}</a></nav>
<header><p class="kicker">{e(u['nav_perspectives'])}</p><h1 class="display sm">{e(A['title'])}</h1>
<p class="meta">{e(u['published'])} <time datetime="{d}">{fdate(d, loc)}</time> · {e(u['by'])} {e(u['author'])}</p></header>
<figure class="art-hero">{img(aid, A['title'], '', True, rp=rp)}</figure>
<p class="lead article-desc">{e(A['desc'])}</p>
<aside class="takeaways"><h2>{e(u['takeaways'])}</h2><ul>{tk}</ul></aside>
<div class="prose">{paras}</div>
<section class="faq"><h2>{e(u['faq'])}</h2><details class="qa" open><summary>{e(A['faq_q'])}</summary><p>{e(A['faq_a'])}</p></details></section>
{src}
<p><a class="btn ghost" href="../">← {e(u['back_perspectives'])}</a></p>
</article>
<section class="wrap block"><div class="arts">{rel}</div></section>"""
    write(f"{lang}/{path}index.html", head(lang, f"{A['title']} | {BRAND}", A["desc"], path, 3, img=f"{aid}.webp", jsonld=ld, og_type="article", extra=extra) + nav(lang, path, 3) + body + footer(lang, 3))

def build_company(lang, idx):
    k, name, url, im, d = COMPANIES[idx]; u = T[lang]["ui"]; C = T[lang]["companies"][k]; rp = "../../../"
    loc = dict((c, b) for c, h, n, b, dd in LANGS)[lang]; hl = dict((c, h) for c, h, *_ in LANGS)[lang]
    path = f"portfolio/{COMPANY_SLUGS[k]}/"
    note = "".join(f"<p>{e(p)}</p>" for p in C["note"])
    others = "".join(f'<a class="chip" href="../{COMPANY_SLUGS[kk]}/">{e(nn)}</a>' for kk, nn, *_r in COMPANIES if kk != k)
    ld = [{"@context": "https://schema.org", "@type": "Organization", "name": name, "url": url, "description": C["summary"],
           "funder": {"@id": f"{BASE_URL}/#org", "@type": "Organization", "name": BRAND}},
          {"@context": "https://schema.org", "@type": "Article", "headline": C["note_title"], "datePublished": d, "inLanguage": hl,
           "about": {"@type": "Organization", "name": name, "url": url}, "image": f"{BASE_URL}/assets/img/{im}.webp",
           "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@id": f"{BASE_URL}/#org", "@type": "Organization", "name": BRAND},
           "mainEntityOfPage": page_url(lang, path), "articleBody": " ".join(C["note"])},
          crumbs([(BRAND, page_url(lang, "")), (u["portfolio_title"], page_url(lang, "#portfolio")), (name, page_url(lang, path))])]
    body = f"""<section class="co-hero">{img(im, name + ' — ' + C['tagline'], 'bg', True, rp=rp)}
<div class="wrap slide-in"><nav class="crumbs" aria-label="Breadcrumb"><a href="../../">{BRAND}</a> / <a href="../../#portfolio">{e(u['portfolio_title'])}</a></nav>
<p class="kicker">{e(C['sector'])}</p><h1 class="h1">{e(name)}</h1><p class="lead">{e(C['tagline'])}</p></div></section>
<div class="wrap co">
<div class="co-main"><p class="lead">{e(C['summary'])}</p>
<article class="note"><p class="kicker">{e(u['investment_note'])} · <time datetime="{d}">{fdate(d, loc)}</time></p><h2 class="display sm">{e(C['note_title'])}</h2><div class="prose">{note}</div></article></div>
<aside class="facts"><dl><dt>{e(u['sector'])}</dt><dd>{e(C['sector'])}</dd><dt>{e(u['hq'])}</dt><dd>{e(C['hq'])}</dd>
<dt>{e(u['invested'])}</dt><dd><time datetime="{d}">{fdate(d, loc)}</time></dd></dl>
<a class="btn" href="{url}" rel="noopener" target="_blank">{e(u['visit_site'])} ↗</a></aside></div>
<section class="wrap block"><p class="kicker">{e(u['portfolio_title'])}</p><div class="chips">{others}</div></section>"""
    write(f"{lang}/{path}index.html", head(lang, f"{name} — {C['tagline']} | {BRAND}", C["summary"], path, 3, img=f"{im}.webp", jsonld=ld) + nav(lang, path, 3) + body + footer(lang, 3))

def build_privacy(lang):
    u = T[lang]["ui"]; path = "privacy/"
    txt = T[lang].get("privacy_text", T["en"].get("privacy_text", ""))
    body = f"""<section class="wrap page-head article"><h1 class="display sm">{e(u['privacy'])}</h1><div class="prose"><p>{e(txt)}</p></div></section>"""
    write(f"{lang}/{path}index.html", head(lang, f"{u['privacy']} | {BRAND}", u["privacy"] + " — " + BRAND, path, 2) .replace('index,follow', 'noindex,follow') + nav(lang, path, 2) + body + footer(lang, 2))

def build_feed(lang):
    hl = dict((c, h) for c, h, *_ in LANGS)[lang]; u = T[lang]["ui"]
    items = "".join(f"""<item><title>{e(T[lang]['articles'][a]['title'])}</title><link>{page_url(lang, f'perspectives/{s}/')}</link><guid>{page_url(lang, f'perspectives/{s}/')}</guid><pubDate>{datetime.date.fromisoformat(d).strftime('%a, %d %b %Y 08:00:00 +0000')}</pubDate><description>{e(T[lang]['articles'][a]['desc'])}</description></item>""" for a, s, d, _ in ARTICLES)
    write(f"{lang}/feed.xml", f"""<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{BRAND} — {e(u['perspectives_title'])}</title><link>{page_url(lang, 'perspectives/')}</link><description>{e(u['perspectives_desc'])}</description><language>{hl}</language>{items}</channel></rss>""")

def build_root():
    links = "".join(f'<li><a href="{c}/" hreflang="{h}" lang="{h}">{n}</a></li>' for c, h, n, *_ in LANGS)
    alts = "\n".join(f'<link rel="alternate" hreflang="{h}" href="{BASE_URL}/{c}/">' for c, h, *_ in LANGS)
    codes = ja([c for c, *_ in LANGS])
    write("index.html", f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
{GTM_HEAD}
<title>{e(T['en']['ui']['site_title'])}</title><meta name="description" content="{e(T['en']['ui']['site_desc'])}">
<link rel="canonical" href="{BASE_URL}/">{alts}
<link rel="alternate" hreflang="x-default" href="{BASE_URL}/">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css">
<script type="application/ld+json">{ja(org_ld())}</script>
<script>(function(){{var s={codes};var p=(navigator.languages||[navigator.language||'en']);for(var i=0;i<p.length;i++){{var c=(p[i]||'').slice(0,2).toLowerCase();if(s.indexOf(c)>-1){{location.replace(c+'/');return;}}}}location.replace('en/');}})();</script>
</head><body>{GTM_BODY}<main class="wrap page-head"><a class="brand" href="en/">{LOGO}<span>Impact Capital <b>VC</b></span></a>
<h1 class="display sm">{e(T['en']['home']['hero_title'])}</h1><p class="lead">{e(T['en']['ui']['site_desc'])}</p><ul class="chips">{links}</ul></main></body></html>""")

def build_meta():
    urls = []
    paths = [""] + ["perspectives/"] + [f"perspectives/{a[1]}/" for a in ARTICLES] + [f"portfolio/{COMPANY_SLUGS[c[0]]}/" for c in COMPANIES]
    lastmod = {"": ARTICLES[0][2], "perspectives/": ARTICLES[0][2]}
    for a in ARTICLES: lastmod[f"perspectives/{a[1]}/"] = a[2]
    for c in COMPANIES: lastmod[f"portfolio/{COMPANY_SLUGS[c[0]]}/"] = c[4]
    for p in paths:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{page_url(c, p)}"/>' for c, h, *_ in LANGS) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{page_url("en", p)}"/>'
        for c, *_ in LANGS:
            urls.append(f"<url><loc>{page_url(c, p)}</loc><lastmod>{lastmod[p]}</lastmod>{alts}</url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot", "Googlebot", "CCBot", "meta-externalagent", "Bytespider", "DuckAssistBot", "YouBot", "Amazonbot"]
    write("robots.txt", "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"User-agent: *\nAllow: /\nDisallow: /*/privacy/\n\nSitemap: {BASE_URL}/sitemap.xml\n")
    en = T["en"]
    llms = [f"# {BRAND}\n", f"> {en['ui']['site_desc']}\n",
            "Impact Capital VC invests in non-standard, unconventional agentic AI companies. Content is available in 16 languages: " + ", ".join(n for c, h, n, *_ in LANGS) + f". English pages live under {BASE_URL}/en/.\n",
            "## Portfolio\n"] + [f"- [{n}]({page_url('en', 'portfolio/' + COMPANY_SLUGS[k] + '/')}): {en['companies'][k]['tagline']}. Investment note dated {d}. Website: {u}" for k, n, u, im, d in COMPANIES] + \
           ["\n## AI Perspectives\n"] + [f"- [{en['articles'][a]['title']}]({page_url('en', 'perspectives/' + s + '/')}) ({d}): {en['articles'][a]['desc']}" for a, s, d, _ in ARTICLES] + \
           ["\n## Optional\n", f"- [Full text for LLMs]({BASE_URL}/llms-full.txt)", f"- [Sitemap]({BASE_URL}/sitemap.xml)"]
    write("llms.txt", "\n".join(llms) + "\n")
    full = [f"# {BRAND} — full content (English)\n", en["ui"]["site_desc"], "\n" + en["home"]["statement_text"].replace("<em>", "").replace("</em>", "") + "\n"]
    full += ["## FAQ\n"] + [f"**{en['home'][f'faq{i}_q']}** {en['home'][f'faq{i}_a']}\n" for i in (1, 2, 3, 4)]
    full += ["## Portfolio and investment notes\n"]
    for k, n, u, im, d in COMPANIES:
        c = en["companies"][k]
        full += [f"### {n} ({u})\n", f"{c['tagline']}. {c['summary']}\n", f"Investment note ({d}) — {c['note_title']}:\n", "\n\n".join(c["note"]) + "\n"]
    full += ["## AI Perspectives\n"]
    for a, s, d, _ in ARTICLES:
        A = en["articles"][a]
        full += [f"### {A['title']}\n", f"Published {d}. URL: {page_url('en', 'perspectives/' + s + '/')}\n", "\n\n".join(A["body"]) + "\n", "Key takeaways: " + " ".join(A["takeaways"]) + "\n", f"Q: {A['faq_q']} A: {A['faq_a']}\n"]
        if a in SOURCES: full += ["Sources: " + "; ".join(f"{n} {s}" for n, s in SOURCES[a]) + "\n"]
    write("llms-full.txt", "\n".join(full))
    write("site.webmanifest", ja({"name": BRAND, "short_name": "Impact Capital", "start_url": "/en/", "display": "standalone", "background_color": "#070A1F", "theme_color": "#070A1F", "icons": [{"src": "/assets/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}))
    write("assets/favicon.svg", LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))
    write("404.html", f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{GTM_HEAD}<title>404 | {BRAND}</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/style.css"></head><body>{GTM_BODY}<main class="wrap page-head"><h1 class="display">404</h1><p class="lead"><a href="/en/">{BRAND}</a></p></main></body></html>')

if __name__ == "__main__":
    for d in ("index.html",):
        pass
    for code, *_ in LANGS:
        shutil.rmtree(os.path.join(DIST, code), ignore_errors=True)
    for code, *_ in LANGS:
        build_home(code); build_perspectives(code); build_privacy(code); build_feed(code)
        for i in range(len(ARTICLES)): build_article(code, i)
        for i in range(len(COMPANIES)): build_company(code, i)
    build_root(); build_meta()
    shutil.copy(os.path.join(ROOT, "style.css"), os.path.join(DIST, "assets", "style.css"))
    shutil.copy(os.path.join(ROOT, "site.js"), os.path.join(DIST, "assets", "site.js"))
    n = sum(len(f) for _, _, f in os.walk(DIST))
    print("built", n, "files")
