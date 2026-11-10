# Impact Capital VC — website

Static, multilingual (16 languages) website for Impact Capital VC.

- `src/` — generator (`build.py`), translations (`src/i18n/*.json`), CSS and JS.
- `dist/` — the built site. Deploy this folder as the web root.

## Build

```bash
pip install babel
cd src && BASE_URL=https://impactcapital.vc python3 build.py
```

Set `BASE_URL` to the production domain before building — it is used for canonical URLs,
hreflang alternates, Open Graph tags, JSON-LD, `sitemap.xml`, `robots.txt` and `llms.txt`.

## SEO / GEO / AEO

- 16 locales with `hreflang` + `x-default`, localized `<html lang>` and RTL for Arabic and Urdu
- JSON-LD: Organization, WebSite, ItemList, FAQPage, NewsArticle/BlogPosting, BreadcrumbList, Speakable
- `sitemap.xml` with xhtml alternates, per-language RSS feeds
- `robots.txt` explicitly allows AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, …)
- `llms.txt` and `llms-full.txt` for generative engines
- Google Tag Manager container `GTM-PH9PW3JR` on every page

Visuals generated with SOMIN image generation.
