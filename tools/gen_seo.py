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
POLD = re.search(r"POLD=\(\)=>T\('([^']*)'", app).group(1)
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
                q.append((f"How much is the {p['name']}?", f"${p['price']:,} USD, paid in full at checkout (in stock, no deposit). " + POLD) if p.get("direct") else (f"How much is the {p['name']}?", f"${p['price']:,} USD, with a ${p.get('deposit', cfg['depositUSD']):,} deposit to place the order."))
        else:
            q.append((f"How much is the {p['name']}?", f"Final pricing is confirmed after the fitment check and before build. A ${cfg['depositUSD']} deposit starts the order."))
    q += [
        ("Are these items in stock?", "No. All items are custom / made to order (or sourced to order) for your car after fitment is confirmed."),
        ("How long does it take?", f"Current estimate: {LEAD} after you approve the order. Some large items (e.g. the 718 rear diffuser) are estimated at 4–6 weeks. We will update you if this changes."),
        ("Do you ship outside the US?", f"No. We ship only to street addresses in the 50 US states and Washington, D.C. We do not ship to PO Boxes, APO/FPO/DPO, Puerto Rico or other US territories, or outside the US. US shipping is calculated at checkout based on your ZIP and package size; free local pickup at our Los Angeles warehouse. See {BASE}/shipping-policy/"),
        ("How much is shipping?", "US shipping is calculated at checkout based on your ZIP and package size; free local pickup at our Los Angeles warehouse. The shipping amount is shown as its own line before you pay (dadan carrier quote from Los Angeles to your ZIP). Deposit orders pay shipping with the balance; pay-in-full orders pay it at checkout. In-stock items that ship directly from our supplier include shipping in the price."),
        ("Is the deposit refundable? How do I cancel?", "Deposit & cancellation policy: " + POL),
    ]
    if p and p.get("direct"):  # in-stock AE item: pay in full, no deposit
        q = q[:-5] + [("Is it in stock?", "Yes. This is an in-stock item from our supplier: you pay the full price at checkout (no deposit) and it ships directly to your US address, est. 2–3 weeks."),
                      ("Do you ship outside the US?", f"No. We ship only to street addresses in the 50 US states and Washington, D.C. We do not ship to PO Boxes, APO/FPO/DPO, Puerto Rico or other US territories, or outside the US. Prices include shipping to the US. See {BASE}/shipping-policy/"),
                      ("Can I cancel? What is the refund policy?", POLD)]
    if (p and p.get("payFull") and p.get("allowPayFull")) or (not p and any(x.get("payFull") and x.get("allowPayFull") for x in cfg["products"])):
        q.append(("Can I pay in full instead of a deposit? What is the refund policy?", "Yes, on the digital cluster pages you can choose Pay deposit or Pay in full. " + POLF))
    return q

def faq_ld(q): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in q]}

def page(path, title, desc, image, body, ld):
    url = BASE + path
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<base href="/">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="{'product' if '/p/' in path else 'website'}"><meta property="og:site_name" content="Tachi Club"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{image}">
<meta name="theme-color" content="#0E0F11"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css?v=20261101i"><script src="/config.js?v=20261101i"></script><script src="https://js.stripe.com/v3" async></script>
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
    if p.get("direct"): summary = f"{p['name']} for {p['make']} {p['code']} ({yrs}). {p['plug']}. In stock; pay in full at checkout (no deposit); ships direct from our supplier, est. 2–3 weeks. {price_txt}."
    title = f"{p['name']} ({p['code']}, {yrs}) | Tachi Club" if p.get("acc") else f"{p['name']} – Digital LCD Gauge Cluster Swap ({p['code']}, {yrs}) | Tachi Club"
    desc = (f"{p['name']} for {p['make']} {p['code']} {yrs}. {p['plug']}. {price_txt}. " + ("In stock; ships directly from our supplier to US addresses, shipping included." if p.get("direct") else "Made to order, ships in the US from Los Angeles; shipping calculated at checkout, free LA pickup."))[:300]
    if p.get("seoTitle"): title = f"{p['seoTitle']} | Tachi Club"
    if p.get("seoDesc"): desc = p["seoDesc"][:300]
    q = gen_faq(p)
    prod = {"@type": "Product", "@id": BASE + path + "#product", "name": p["name"], "sku": pid, "category": "Automotive " + kind,
            "brand": {"@type": "Brand", "name": "Tachi Club"}, "description": f"{p['fit']} " + " ".join(p["specs"]),
            "image": [img(p["hero"])] + [img(n) for n in g if n != p["hero"]][:5], "url": BASE + path}
    if p.get("price"):
        avail = "https://schema.org/InStock" if p.get("direct") else "https://schema.org/PreOrder"
        seller = {"@id": BASE + "/#org"}
        if p.get("priceV"):
            prod["offers"] = [{"@type": "Offer", "name": k.title(), "price": str(v), "priceCurrency": "USD", "availability": avail,
                               "url": BASE + path, "seller": seller} for k, v in p["priceV"].items()]
        else:
            prod["offers"] = {"@type": "Offer", "price": str(p["price"]), "priceCurrency": "USD", "availability": avail, "url": BASE + path, "seller": seller}
    ld = [ORG, SITE, prod, crumbs([("Home", "/"), (p["name"], path)]), faq_ld(q)]
    gal = "".join(f'<img loading="lazy" src="/media/img/{n}-s.webp" alt="{E((p.get("alts") or [])[i] if i < len(p.get("alts") or []) else p["name"] + " – " + p["code"] + " photo " + str(i + 1))}">' for i, n in enumerate(g))
    body = f"""<article class="pgrid"><div class="pm"><img class="main-media" src="/media/img/{p['hero']}.webp" alt="{E(p['name'])} installed – {E(p['make'])} {E(p['code'])}"><div class="gal" style="margin-top:8px">{gal}</div></div>
<div><nav aria-label="Breadcrumb"><a href="/">Home</a> › {E(p['name'])}</nav><h1>{E(p['name'])}</h1>
<p class="lead"><b>Summary:</b> {E(summary)}</p>
<h2>Fitment</h2><p>{E(p['fit'])}</p><p>Chassis: {E(p['code'])} · Years: {yrs} · Make: {E(p['make'])}</p>
<h2>Price</h2><p>{E(price_txt)}</p>{"" if p.get("direct") else "<p class=\"note shipnote\"><b>Shipping:</b> US shipping is calculated at checkout based on your ZIP and package size; free local pickup at our Los Angeles warehouse.</p>"}
<h2>Specs</h2><ul>{''.join(f'<li>{E(s)}</li>' for s in p['specs'])}</ul>
{'' if p.get('direct') else '<h2>Deposit &amp; cancellation policy</h2><p class="note">' + E(POL) + '</p>'}{('<h2>' + ('Refund policy (in-stock item)' if p.get('direct') else 'Pay-in-full refund policy') + '</h2><p class="note">' + E(POLD if p.get('direct') else POLF) + '</p>') if (p.get('payFull') and p.get('allowPayFull')) or p.get('direct') else ''}{xl(p)}
<p><a class="btn" href="/#/p/{pid}">{"Buy now – pay in full" if p.get("direct") else "Order / pre-order this item"}</a></p>
<p class="note">US customers only (50 states + DC). <a href="/shipping-policy/">Shipping Policy</a> · <a href="/returns-refund-policy/">Returns &amp; Refund Policy</a> · <a href="/terms/">Terms of Service</a></p>
<h2>FAQ</h2>{faq_html(q)}</div></article>"""
    os.makedirs(f"p/{pid}", exist_ok=True)
    out = page(path, title, desc, img(p["hero"]), body, ld)
    # humans: jump into the interactive SPA product view (order form w/ required policy checkbox)
    # humans: same URL, but switch the SPA to this product (order form incl. required policy checkbox)
    out = out.replace("<script>/* boot", "<script>if(!location.hash)history.replaceState(null,'',location.pathname+location.search+'#/p/%s');</script><script src=\"/app.js?v=20261101i\"></script><script>/* boot" % pid)
    open(f"p/{pid}/index.html", "w", encoding="utf-8").write(out)
    urls.append((path, "0.9"))
    llms_products.append(f"- [{p['name']}]({BASE + path}): {summary} Fitment: {p['fit']}")


# ---- Policy pages (2026-11-01, Cheung decisions). Support email per Cheung; no phone/extra address invented.
SUP = "support@oliandcece.com"
DMG = f"If your item arrives damaged, is the wrong item, or is missing parts, email {SUP} with your order number and photos within 7 days of delivery. We send a replacement first, or refund you if a replacement is not possible. This is the only exception to the no-returns rule for shipped orders."
POLICIES = {
 "shipping-policy": ("Shipping Policy", "Tachi Club ships only to street addresses in the 50 US states and Washington, D.C. Shipping times, tracking, lost packages and address rules.", [
  ("Where do you ship?", "We ship only to street addresses in the 50 US states and Washington, D.C. (including Alaska and Hawaii)."),
  ("Where don't you ship?", "We do not ship to PO Boxes, APO/FPO/DPO military or diplomatic addresses, Puerto Rico or other US territories, or any address outside the United States. Orders with these addresses are refused at checkout."),
  ("How much is shipping?", "US shipping is calculated at checkout based on your ZIP and package size; free local pickup at our Los Angeles warehouse. Items that ship from our Los Angeles warehouse (digital clusters and made-to-order parts): enter your ZIP on the order form and we show the shipping amount as its own line before you pay; it is based on the actual packed size and weight and a live carrier rate from Los Angeles. Deposit orders pay shipping together with the balance; pay-in-full orders pay it at checkout. Choose \"Local pickup at our LA warehouse\" for $0 shipping; pickup details are emailed after you order. In-stock items that ship directly from our supplier (marked \"In stock · pay in full\") include US shipping in the price."),
  ("When will my order ship? (in-stock items)", "In-stock accessories (marked \"In stock · pay in full\") ship directly from our supplier, usually within 2–5 business days after your order. Transit is usually about 7–15 business days."),
  ("When will my order ship? (custom items)", "Custom / made-to-order items ship after production, per the lead time shown on each product page: digital clusters are estimated at 3–5 weeks, and other custom parts at about 2–6 weeks (large items such as the 718 rear diffuser 4–6 weeks). We email you if the estimate changes."),
  ("Signature confirmation", "Orders with a goods value of $500 or more ship with signature confirmation required on delivery (adult signature where the carrier offers it). Please make sure someone can sign for the package."),
  ("Tracking and delivery confirmation", "When your order ships we email you the carrier and tracking number. When the carrier shows it delivered, we email you a delivery confirmation."),
  ("Late or lost packages", f"If tracking has not updated or your package has not arrived, email {SUP} with your order number and we will open a trace with the carrier. If there is still no delivery scan 30 days after shipment, we treat the package as lost and send a replacement or a refund."),
  ("Wrong address", f"Please check your address at checkout; you are responsible for a correct, complete address. Before shipment, email {SUP} and we will try to update it. After shipment we cannot change it. If a package is returned or lost because of an incorrect address, reshipping may cost extra."),
  ("Damaged, wrong or missing items", DMG),
  ("Contact", f"Email {SUP} with your order number.")]),
 "returns-refund-policy": ("Returns & Refund Policy", "Cancellation and refund rules for Tachi Club custom orders (full refund before you confirm production start; after that, refund minus actual costs incurred, capped at the deposit) and in-stock items (full refund before shipment); 7-day damaged/wrong item cover.", [
  ("Production-start confirmation (custom items)", "After you pay for a custom item, we email you a summary of your order (vehicle, VIN, options, lead time) with a Confirm production start link. We do not order parts or start production until you click it. The time, IP address and policy version of your confirmation are recorded with your order."),
  ("Deposit pre-orders (custom items)", POL),
  ("Paid-in-full custom items", POLF),
  ("In-stock items (paid in full, ship direct from our supplier)", POLD),
  ("After shipment", "Once an order has shipped, we do not accept returns, refunds or exchanges, except for the damaged, wrong or missing item cover below."),
  ("Damaged, wrong or missing items (7 days)", DMG),
  ("Lost packages", "No delivery scan 30 days after shipment: we send a replacement or a refund. See the Shipping Policy."),
  ("How refunds are paid", "Approved refunds go back to the original payment method. They usually appear within 5–10 business days, depending on your bank."),
  ("Cost breakdown after production starts", "If you cancel a custom order after confirming production start, we deduct only the costs we have actually incurred for your order (materials/parts, machining/production, freight) and send you an itemized breakdown. The deduction is never more than the deposit amount for that item; the rest is refunded."),
  ("How to cancel or claim", f"Email {SUP} with your order number (and photos for damaged/wrong items). Whether production had started is determined by your recorded Confirm production start click.")]),
 "terms": ("Terms of Service", "Terms of sale for orders placed on Tachi Club (tachiclub.oliandcece.com), operated by Oli&CeCe Inc.", [
  ("Who we are", "Tachi Club is operated by Oli&CeCe Inc., Commerce, California, USA. Contact: " + SUP + "."),
  ("US customers only", "We sell and ship only to customers with street addresses in the 50 US states and Washington, D.C. See the Shipping Policy."),
  ("Orders and payment", "Prices are in USD. For items that ship from our Los Angeles warehouse, US shipping is calculated at checkout from your ZIP and package size and shown as a separate line before you pay (free local pickup in LA); in-stock items shipped directly by our supplier include shipping. Custom items are ordered with a deposit (balance due before shipping); in-stock items are paid in full at checkout. Payments are processed by Stripe. Your order is accepted when we send the order confirmation email."),
  ("Payment verification and order review", "Card payments may require 3D Secure authentication with your bank. Payments that fail card security checks (CVC or billing ZIP) may be declined. Orders over $500 from first-time customers are reviewed before we order parts; we may contact you to verify the order, or cancel it with a full refund."),
  ("Production-start confirmation", "For custom items we order parts or start production only after you confirm the order specifications by clicking the Confirm production start link we email you."),
  ("Policies you agree to", "By checking the box on the order form you agree to these Terms, the Returns & Refund Policy and the Shipping Policy that apply to your payment option. The exact policy text shown to you, with the time of acceptance, is kept with your order and repeated in your confirmation email."),
  ("Fitment", "Fitment information is provided per our suppliers. Tell us your car, year and trim; for custom items we confirm fitment from your VIN/photos before ordering. Installation is your responsibility; professional installation is recommended where noted."),
  ("Mileage", "Digital clusters are programmed to match your vehicle's original odometer reading. We never alter mileage."),
  ("Cancellations, refunds, returns", "As set out in the Returns & Refund Policy, including the 7-day damaged/wrong/missing item cover."),
  ("Payment disputes", f"If there is a problem with your order, please contact {SUP} first so we can fix it quickly. We keep records of your order, policy acceptance, payment verification, emails and shipping to respond to card disputes."),
  ("Trademarks", "Not affiliated with Toyota, Subaru, Honda, Mazda or Porsche. Brand names are used for fitment reference only."),
  ("Changes", "We may update these terms; the version shown at the time of your order applies to that order.")])}
for slug, (t, d, secs) in POLICIES.items():
    path = f"/{slug}/"; urls.append((path, "0.5"))
    body = f"<article><div class=\"wrap\"><h1>{E(t)}</h1><p class=\"lead\">{E(d)}</p><p class=\"note\">Last updated {TODAY}.</p>" + "".join(f"<h2>{E(a)}</h2><p>{E(b)}</p>" for a, b in secs) + \
        '<p class="note"><a href="/shipping-policy/">Shipping Policy</a> · <a href="/returns-refund-policy/">Returns &amp; Refund Policy</a> · <a href="/terms/">Terms of Service</a> · <a href="/faq/">FAQ</a></p></div></article>'
    ld = [ORG, SITE, {"@type": "WebPage", "@id": BASE + path, "name": t, "url": BASE + path, "description": d, "dateModified": TODAY, "isPartOf": {"@id": BASE + "/#website"}, "publisher": {"@id": BASE + "/#org"}},
          crumbs([("Home", "/"), (t, path)])]
    if slug == "returns-refund-policy":
        ld.append({"@type": "MerchantReturnPolicy", "@id": BASE + path + "#policy", "name": t, "url": BASE + path, "applicableCountry": "US", "returnPolicyCountry": "US",
                   "returnPolicyCategory": "https://schema.org/MerchantReturnNotPermitted", "refundType": "https://schema.org/FullRefund", "returnFees": "https://schema.org/FreeReturn", "itemCondition": "https://schema.org/NewCondition", "description": "No returns or exchanges after shipment, except damaged, wrong or missing items reported with photos within 7 days of delivery (replacement first, else refund). Cancellation: custom items, full refund before the customer confirms production start, afterwards refund minus actual costs incurred (capped at the deposit); in-stock items, full refund any time before shipment. Refunds in 5-10 business days to the original payment method."})
    os.makedirs(slug, exist_ok=True)
    out = page(path, f"{t} | Tachi Club", d, img("981-224046832"), body, ld).replace('<script>/* boot the interactive SPA view for humans; crawlers read the static content above */</script>', '<script src="/app.js?v=20261101i"></script>' if False else '')
    open(f"{slug}/index.html", "w", encoding="utf-8").write(out)

# FAQ page
q = gen_faq() + [("What about my mileage (digital clusters)?", "Federal law requires the replacement cluster to show the vehicle’s true mileage. We program each cluster to match your original odometer reading, which is why we ask for an odometer photo and VIN. We never alter mileage."),
                 ("Will it fit my exact car?", "We check your VIN, trim and photos of your current part before ordering or building.")]
body = f"<h1>FAQ</h1><p class=\"lead\">Tachi Club sells made-to-order digital instrument clusters and carbon fiber parts for JDM and Porsche chassis, operated from Los Angeles (Commerce, CA).</p>{faq_html(q)}"
os.makedirs("faq", exist_ok=True)
open("faq/index.html", "w", encoding="utf-8").write(
    page("/faq/", "FAQ – Fitment, Lead Time, Shipping & Deposit Policy | Tachi Club",
         "Answers on fitment, lead time, US shipping, and Tachi Club's deposit & cancellation policy for made-to-order car parts.",
         img("981-224046832"), body, [ORG, SITE, crumbs([("Home", "/"), ("FAQ", "/faq/")]), faq_ld(q)]).replace("<script>/* boot", "<script>if(!location.hash)history.replaceState(null,'',location.pathname+location.search+'#/faq');</script><script src=\"/app.js?v=20261101i\"></script><script>/* boot"))

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
{"- Pay-in-full refund policy (digital clusters, full payment): " + POLF if any(x.get("allowPayFull") for x in cfg["products"]) else "- Digital clusters: deposit pre-order only for now."}
- Fitment is confirmed from VIN/photos before ordering or building.

## Pages
- [FAQ]({BASE}/faq/)
- [Shipping Policy]({BASE}/shipping-policy/): US only — 50 states + DC; no PO Boxes, APO/FPO/DPO, PR/territories; LA-warehouse items: US shipping calculated at checkout by ZIP + package size, free local pickup in Los Angeles; direct-ship in-stock items include shipping; in-stock items ship in 2–5 business days + ~7–15 transit.
- [Returns & Refund Policy]({BASE}/returns-refund-policy/)
- [Terms of Service]({BASE}/terms/)
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
ix = re.sub(r'<main id="app">.*?</main>', f'<main id="app"><h1>Tachi Club — digital LCD gauge clusters, Los Angeles</h1><p>{E(DESC)}</p><h2>Digital clusters</h2><ul>{li(HERO)}</ul><h2>Accessories</h2><ul>{li(ACC)}</ul><p><a href="/faq/">FAQ</a> · <a href="/shipping-policy/">Shipping Policy</a> · <a href="/returns-refund-policy/">Returns &amp; Refund Policy</a> · <a href="/terms/">Terms of Service</a></p></main>', ix, flags=re.S)
open("index.html", "w", encoding="utf-8").write(ix)
