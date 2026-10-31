#!/usr/bin/env python3
"""Generate crawlable SEO/AEO static pages from config.js (run from repo root).
Outputs: p/<id>/index.html, faq/index.html, sitemap.xml, robots.txt, llms.txt.
Static pages show real content to crawlers and then boot the same SPA (app.js)."""
import json, subprocess, html, datetime, os, re
BASE = "https://tachiclub.oliandcece.com"
cfg = json.loads(subprocess.check_output(["node", "-e",
  "global.window={};require('./config.js');console.log(JSON.stringify(window.SITE))"], cwd="."))
app = open("app.js", encoding="utf-8").read()
POL = re.search(r"POL=\(\)=>T\('([^']*)'", app).group(1)
POLF = re.search(r"POLF=\(\)=>T\('([^']*)'", app).group(1)
DESC = "Tachi Club makes plug-in digital LCD gauge clusters (instrument cluster swaps) for Toyota GT86 / Subaru BRZ / Scion FR-S, Honda Civic EK and Porsche 987/981 Cayman & Boxster, plus supporting carbon accessories. Made to order, US customers, Los Angeles."
HERO = [p for p in cfg["products"] if not p.get("acc")]
ACC = [p for p in cfg["products"] if p.get("acc")]
XL = {"Porsche": "987", "Toyota": "gt86", "Subaru": "gt86", "Scion": "gt86", "Honda": "ek"}
LEAD = cfg.get("leadTime", "3–5 weeks (estimate)")
E = html.escape
TODAY = datetime.date.today().isoformat()
ORG = {"@type": "Organization", "@id": BASE + "/#org", "name": "Tachi Club", "url": BASE + "/",
       "logo": BASE + "/favicon.svg", "description": DESC,
       "parentOrganization": {"@type": "Organization", "name": "Oli&CeCe Inc.", "url": "https://oliandcece.com"},
       "address": {"@type": "PostalAddress", "streetAddress": "5631 Ferguson Dr, Dock 1&2", "addressLocality": "Commerce",
                   "addressRegion": "CA", "postalCode": "90022", "addressCountry": "US"}}
SITE = {"@type": "WebSite", "@id": BASE + "/#website", "name": "Tachi Club", "description": DESC, "url": BASE + "/", "publisher": {"@id": BASE + "/#org"}}

def img(n): return f"{BASE}/media/img/{n}.webp"

def gen_faq(p=None):
    q = []
    if p:
        q.append((f"Will the {p['name']} fit my car?", f"{p['fit']} Fitment years listed: {p['years'][0]}–{p['years'][1]} ({p['code']})."))
        if p.get("price"):
            if p.get("priceV"):
                pv = p["priceV"]; dv = p.get("depositV", {})
                q.append((f"How much is the {p['name']}?", "Standard: $%s (deposit $%s). Premium: $%s (deposit $%s). Prices in USD." % (
                    f"{pv['standard']:,}", f"{dv.get('standard', p.get('deposit') or cfg['depositUSD']):,}", f"{pv['premium']:,}", f"{dv.get('premium', p.get('deposit') or cfg['depositUSD']):,}")))
            else:
                q.append((f"How much is the {p['name']}?", f"${p['price']:,} USD, with a ${p.get('deposit', cfg['depositUSD']):,} deposit to place the order."))
        else:
            q.append((f"How much is the {p['name']}?", f"Final pricing is confirmed after the fitment check and before build. A ${cfg['depositUSD']} deposit starts the order."))
    q += [
        ("Are these items in stock?", "No. All items are custom / made to order (or sourced to order) for your car after fitment is confirmed."),
        ("How long does it take?", f"Current estimate: {LEAD} after you approve the order. Some large items (e.g. the 718 rear diffuser) are estimated at 4–6 weeks. We will update you if this changes."),
        ("Do you ship outside the US?", "Currently we focus on US customers."),
        ("Is the deposit refundable? How do I cancel?", "Deposit & cancellation policy: " + POL),
    ]
    if not p or p.get("payFull"):
        q.append(("Can I pay in full instead of a deposit? What is the refund policy?", "Yes, on the digital cluster pages you can choose Pay deposit or Pay in full. " + POLF))
    return q

def faq_ld(q): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in q]}

def page(path, title, desc, image, body, ld):
    url = BASE + path
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<base href="/">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="{'product' if '/p/' in path else 'website'}"><meta property="og:site_name" content="Tachi Club"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{image}">
<meta name="theme-color" content="#090909"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css"><script src="/config.js"></script><script src="https://js.stripe.com/v3" async></script>
</head>
<body><div class="grain"></div><header><a href="/" class="logo" id="logo" aria-label="Tachi Club home"></a><nav><a href="/#/models">Clusters</a><a href="/#/acc">Accessories</a><a href="/#/how">Process</a><a href="/faq/">FAQ</a><a href="/#/request">Request</a><a href="/#/about">About</a></nav></header>
<div class="kanji" aria-hidden="true" style="display:none"></div><main id="app">{body}</main><footer id="foot"></footer>
<script>/* boot the interactive SPA view for humans; crawlers read the static content above */</script>
</body></html>
"""

def faq_html(q): return "".join(f"<details open><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in q)

def crumbs(items): return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(items)]}

def xl(p):
    if not p.get("acc"): return ""
    c = next((x for x in HERO if x["id"] == next((XL[m] for m in p.get("makes", []) if m in XL), None)), None)
    return f'<p>Pair it with our hero product: <a href="/p/{c["id"]}/">{E(c["name"])} ({E(c["code"])})</a></p>' if c else ""

urls = [("/", "1.0"), ("/faq/", "0.7")]
llms_products = []
for p in HERO + ACC:
    pid = p["id"]; path = f"/p/{pid}/"
    g = cfg["gallery"].get(p["gal"], [])
    kind = "accessory" if p.get("acc") else "digital instrument cluster"
    yrs = f"{p['years'][0]}–{p['years'][1]}"
    if p.get("priceV"):
        price_txt = f"Standard ${p['priceV']['standard']:,} / Premium ${p['priceV']['premium']:,}"
    elif p.get("price"):
        price_txt = f"${p['price']:,}"
    else:
        price_txt = f"Quoted after fitment check (${cfg['depositUSD']} deposit)"
    summary = f"{p['name']} for {p['make']} {p['code']} ({yrs}). {p['plug']}. Made to order; {LEAD}. {price_txt}."
    title = f"{p['name']} ({p['code']}, {yrs}) | Tachi Club" if p.get("acc") else f"{p['name']} – Digital LCD Gauge Cluster Swap ({p['code']}, {yrs}) | Tachi Club"
    desc = (f"{p['name']} for {p['make']} {p['code']} {yrs}. {p['plug']}. {price_txt}. Made to order, ships in the US from Los Angeles.")[:300]
    q = gen_faq(p)
    prod = {"@type": "Product", "@id": BASE + path + "#product", "name": p["name"], "sku": pid, "category": "Automotive " + kind,
            "brand": {"@type": "Brand", "name": "Tachi Club"}, "description": f"{p['fit']} " + " ".join(p["specs"]),
            "image": [img(p["hero"])] + [img(n) for n in g if n != p["hero"]][:5], "url": BASE + path}
    if p.get("price"):
        avail = "https://schema.org/PreOrder"
        seller = {"@id": BASE + "/#org"}
        if p.get("priceV"):
            prod["offers"] = [{"@type": "Offer", "name": k.title(), "price": str(v), "priceCurrency": "USD", "availability": avail,
                               "url": BASE + path, "seller": seller} for k, v in p["priceV"].items()]
        else:
            prod["offers"] = {"@type": "Offer", "price": str(p["price"]), "priceCurrency": "USD", "availability": avail, "url": BASE + path, "seller": seller}
    ld = [ORG, SITE, prod, crumbs([("Home", "/"), (p["name"], path)]), faq_ld(q)]
    gal = "".join(f'<img loading="lazy" src="/media/img/{n}-s.webp" alt="{E(p["name"])} – {E(p["code"])} photo {i + 1}">' for i, n in enumerate(g))
    body = f"""<article class="pgrid"><div class="pm"><img class="main-media" src="/media/img/{p['hero']}.webp" alt="{E(p['name'])} installed – {E(p['make'])} {E(p['code'])}"><div class="gal" style="margin-top:8px">{gal}</div></div>
<div><nav aria-label="Breadcrumb"><a href="/">Home</a> › {E(p['name'])}</nav><h1>{E(p['name'])}</h1>
<p class="lead"><b>Summary:</b> {E(summary)}</p>
<h2>Fitment</h2><p>{E(p['fit'])}</p><p>Chassis: {E(p['code'])} · Years: {yrs} · Make: {E(p['make'])}</p>
<h2>Price</h2><p>{E(price_txt)}</p>
<h2>Specs</h2><ul>{''.join(f'<li>{E(s)}</li>' for s in p['specs'])}</ul>
<h2>Deposit &amp; cancellation policy</h2><p class="note">{E(POL)}</p>{('<h2>Pay-in-full refund policy</h2><p class="note">' + E(POLF) + '</p>') if p.get('payFull') else ''}{xl(p)}
<p><a class="btn" href="/#/p/{pid}">Order / pre-order this item</a></p>
<h2>FAQ</h2>{faq_html(q)}</div></article>"""
    os.makedirs(f"p/{pid}", exist_ok=True)
    out = page(path, title, desc, img(p["hero"]), body, ld)
    # humans: jump into the interactive SPA product view (order form w/ required policy checkbox)
    # humans: same URL, but switch the SPA to this product (order form incl. required policy checkbox)
    out = out.replace("<script>/* boot", "<script>if(!location.hash)history.replaceState(null,'',location.pathname+location.search+'#/p/%s');</script><script src=\"/app.js\"></script><script>/* boot" % pid)
    open(f"p/{pid}/index.html", "w", encoding="utf-8").write(out)
    urls.append((path, "0.9"))
    llms_products.append(f"- [{p['name']}]({BASE + path}): {summary} Fitment: {p['fit']}")

# FAQ page
q = gen_faq() + [("What about my mileage (digital clusters)?", "Federal law requires the replacement cluster to show the vehicle’s true mileage. We program each cluster to match your original odometer reading, which is why we ask for an odometer photo and VIN. We never alter mileage."),
                 ("Will it fit my exact car?", "We check your VIN, trim and photos of your current part before ordering or building.")]
body = f"<h1>FAQ</h1><p class=\"lead\">Tachi Club sells made-to-order digital instrument clusters and carbon fiber parts for JDM and Porsche chassis, operated from Los Angeles (Commerce, CA).</p>{faq_html(q)}"
os.makedirs("faq", exist_ok=True)
open("faq/index.html", "w", encoding="utf-8").write(
    page("/faq/", "FAQ – Fitment, Lead Time, Shipping & Deposit Policy | Tachi Club",
         "Answers on fitment, lead time, US shipping, and Tachi Club's deposit & cancellation policy for made-to-order car parts.",
         img("981-224046832"), body, [ORG, SITE, crumbs([("Home", "/"), ("FAQ", "/faq/")]), faq_ld(q)]).replace("<script>/* boot", "<script>if(!location.hash)history.replaceState(null,'',location.pathname+location.search+'#/faq');</script><script src=\"/app.js\"></script><script>/* boot"))

open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls) + "</urlset>\n")
open("robots.txt", "w").write("User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in
    ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "Googlebot", "Bingbot", "ClaudeBot", "Claude-SearchBot", "Claude-User", "anthropic-ai", "Applebot", "Applebot-Extended", "CCBot"]) +
    f"Sitemap: {BASE}/sitemap.xml\n")
open("llms.txt", "w", encoding="utf-8").write(f"""# Tachi Club

> {DESC} Operated by Oli&CeCe Inc. in Commerce (Los Angeles), California. Prices in USD.

## Hero products: digital LCD gauge clusters
{chr(10).join(llms_products[:len(HERO)])}

## Accessories (supporting items)
{chr(10).join(llms_products[len(HERO):])}

## Policies
- Lead time: {LEAD}; large items such as the 718 rear diffuser 4–6 weeks.
- Deposit & cancellation policy (deposit orders): {POL}
- Pay-in-full refund policy (digital clusters, full payment): {POLF}
- Fitment is confirmed from VIN/photos before ordering or building.

## Pages
- [FAQ]({BASE}/faq/)
- [Sitemap]({BASE}/sitemap.xml)
""")
print("ok", len(urls), "urls")

# ---- index.html: canonical, OG domain, JSON-LD graph, crawlable product links (replaced by SPA on load)
ix = open("index.html", encoding="utf-8").read()
if not os.path.exists("tools/index.html.bak-pre-seo"): open("tools/index.html.bak-pre-seo", "w", encoding="utf-8").write(ix)
ix = re.sub(r"<title>.*?</title>", "<title>Tachi Club — Digital LCD Gauge Clusters for GT86/BRZ, Civic EK &amp; Porsche 987/981 · Los Angeles</title>", ix)
ix = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + E(DESC) + '">', ix)
ix = ix.replace("https://jibanzi.github.io/gaugelab-la/media/img/", BASE + "/media/img/")
ix = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": [ORG, SITE, {"@type": "Store", "name": "Tachi Club", "url": BASE + "/", "parentOrganization": {"@id": BASE + "/#org"}, "address": ORG["address"]}]}, ensure_ascii=False) + "</script>", ix, flags=re.S)
ix = re.sub(r'\n?<link rel="canonical"[^>]*>', '', ix)
ix = re.sub(r'<meta property="og:url"[^>]*>', '', ix)
ix = ix.replace('<link rel="icon"', f'<link rel="canonical" href="{BASE}/"><meta property="og:url" content="{BASE}/">\n<link rel="icon"', 1)
li = lambda L: "".join(f'<li><a href="/p/{p["id"]}/">{E(p["name"])} ({E(p["code"])}, {p["years"][0]}–{p["years"][1]})</a></li>' for p in L)
ix = re.sub(r'<main id="app">.*?</main>', f'<main id="app"><h1>Tachi Club — digital LCD gauge clusters, Los Angeles</h1><p>{E(DESC)}</p><h2>Digital clusters</h2><ul>{li(HERO)}</ul><h2>Accessories</h2><ul>{li(ACC)}</ul><p><a href="/faq/">FAQ</a></p></main>', ix, flags=re.S)
open("index.html", "w", encoding="utf-8").write(ix)
