// ===== EDIT EVERYTHING HERE =====
window.SITE = {
  brand: "Tachi Club",
  tagline: "Digital cluster swaps for JDM + Euro chassis. Fitted in Los Angeles.",
  email: "hello@example.com",          // TODO: Cheung's contact email
  formEndpoint: "",                    // FormSubmit/Formspree URL; empty = mailto fallback
  stripeCheckoutUrl: "",               // TODO: Stripe Payment Link (deposit)
  stripeMode: "live",                  // LIVE (HECCEI LTD) approved by Cheung t306u 2026-11-01; all payments via orderApi backend Checkout
  stripePublishableKey: "pk_live_51H9kpZAcpVACF0U1IBf0EN1mN4V32JSgKmfYiuiotM1NjmphZA0HynM7mR1fA9JwL3lk4C4Oba8t6skNQ2uncq9k00l1Cdb9la",            // pk_live_ (publishable only; NEVER sk_/rk_ here)
  paymentLinks: {                      // option keys only; links intentionally empty — all payments go through orderApi Checkout (deposit/shipping/policy logic)
    gt86: { standard: "", premium: "" },   // $899 / $1049
    ek:   { standard: "" },                   // $899 single version (t331u)
    "987":{ standard: "", premium: "" },   // $1299 / $1549
    gr86tl: { standard: "" },               // $649
    p987sw: { standard: "", premium: "" },  // $1499 / $2099
    c9ymc: { standard: "" },                // $339
    p718mc: { standard: "" },               // $299
    p718dl: { standard: "" },               // $799
    sbshb: { standard: "" },                // $49
    mxtray: { standard: "" }                // $109 (direct pay in full via order service)
  },
  orderApi: "https://orders.oliandcece.com/api/order", // order service on VPS; empty = hide order form
  telegramBot: "TachiClubBot",                    // Telegram bot username (no @); empty = hide chat button
  depositUSD: 200,                     // default deposit (clusters); see POL in app.js for policy
  leadTime: "3–5 weeks (estimate)",
  gallery: {"gt86": ["gt86-223835832", "gt86-223835833", "gt86-223835834", "gt86-224046690", "gt86-224046691", "gt86-224046692", "brz-224046741", "brz-224046742", "brz-224046743"], "ek": ["ek3-224729425", "ek3-224729426", "ek3-224729428", "ek3-224729429", "ek3-224729430", "ek3-224729431", "ek3-224785198", "ek3-224785199", "ek3-224785200", "ek3-224785201", "ek3-224785202", "ek3-224785203"], "987": ["987-223565096", "987-223565097", "987-223565098", "987-223565099", "987-223565100", "987-224046840", "987-224046842", "987-224046844", "981-223824245", "981-223824272", "981-223824273", "981-223824274", "981-223824275", "981-223824276", "981-224046831", "981-224046832", "981-224046833", "718-224046792"], "991": ["991-223632459", "991-223632460", "991-223632461", "991-223632462", "991-223632463", "991-223632466", "991-224046775", "991-224046776", "991-224046777", "991-224046778"], "gr86tl": ["gr86tl-1", "gr86tl-2", "gr86tl-3", "gr86tl-4"], "p987sw": ["p987sw-1", "p987sw-2", "p987sw-3", "p987sw-4"], "c9ymc": ["c9ymc-1", "c9ymc-2", "c9ymc-3", "c9ymc-4"], "p718mc": ["p718mc-1", "p718mc-2", "p718mc-3", "p718mc-4"], "p718dl": ["p718dl-1", "p718dl-2", "p718dl-3", "p718dl-4"], "sbshb": ["sbshb-1", "sbshb-2", "sbshb-3", "sbshb-4"], "mxtray": ["mxtray-1", "mxtray-2", "mxtray-3", "mxtray-4"], "pc": ["panamera-cayenne-223599723", "panamera-cayenne-223599724", "panamera-cayenne-223599725", "panamera-cayenne-223599726", "panamera-cayenne-223599727", "panamera-cayenne-223599728", "panamera-cayenne-223599729", "panamera-cayenne-223599730", "panamera-cayenne-223599732", "panamera-cayenne-223599733", "panamera-cayenne-223599734", "panamera-cayenne-223601049", "panamera-cayenne-223601051"]},
  chassis: ["ZN6","ZC6","EK9","EK4","EK3","EJ8","987","981","991","971","9Y0","AP1","AP2","ZN8","ZD8","997"],
  products: [
    { id:"gt86", payFull:true, allowPayFull:false /* t285u: pay-in-full hidden until cost is final; set true to re-enable */, priceV:{standard:899,premium:1049}, code:"ZN6 / ZC6", name:"GT86 / BRZ / FR-S Digital Cluster", make:"Toyota / Subaru / Scion",
      years:[2013,2020], price:899, plug:"Non-destructive install", gal:"gt86", hero:"gt86-224046692",
      video:"gt86-toyota-gt-86-digital-gauge-cluster",
      fit:"Currently for push-button-start trims with dual-zone climate control. Send photos so we can confirm your car.",
      specs:["12.3-inch LCD, 2970×720 resolution (manufacturer spec)","3000:1 contrast, up to 1000 nits peak brightness","~178° viewing angles, warm color tone for night driving","Temperature-tested from −30°C to 75°C by the manufacturer","No need to open the factory cluster board — typical install around 30 min per manufacturer"],
      makes:["Toyota","Subaru","Scion"] },
    { id:"ek", payFull:true, allowPayFull:false /* t285u: pay-in-full hidden until cost is final; set true to re-enable */, code:"EK9 / EK4 / EK3", name:"Civic EK Digital Cluster", make:"Honda",
      years:[1996,2000], price:899, plug:"Plug-and-play into factory harness", gal:"ek", hero:"ek3-224729429",
      video:"ek3-honda-ek3-instrument-cluster",
      fit:"1996–2000 Honda Civic EK3, EK4, EK9, EJ6, EJ8, EJ9. We confirm by VIN and cluster photos before build.",
      specs:["Plug and play — drops into the factory cluster slot","12.3-inch Japan JDI LCD, 1920×720 resolution (manufacturer spec)","6 switchable UI themes","Selectable tach redline: 8,000 / 9,000 / 10,000 / 11,000 rpm","Selectable max speedometer scale: 180 / 220 / 240","Configurable RPM shift light","Configurable service interval reminder","13 selectable startup logos","Aftermarket ECUs, cams or sensors may need a matching calibration/signal module — tell us your build"],
      makes:["Honda"] },
    { id:"987", payFull:true, allowPayFull:false /* t285u: pay-in-full hidden until cost is final; set true to re-enable */, priceV:{standard:1299,premium:1549}, code:"987 / 981", name:"Cayman / Boxster Digital Cluster", make:"Porsche",
      years:[2005,2016], price:1299, plug:"Non-destructive, plug-in harness", gal:"987", hero:"981-224046832",
      video:"987-modernize-your-porsche-987-dashboard",
      fit:"987 (2005–2012) and 981 (2013–2016). Fitment varies by options; we confirm before build.",
      specs:["4-inch main screen + dual 3.4-inch side screens","17 selectable UI themes, Linux-based system with quick startup","3000:1 contrast, up to 1000 nits, 800+ PPI (manufacturer spec)","Shows speed, RPM, fuel, coolant temp, drive time and mileage; switch pages from the wheel buttons","Install, plug in the harness, power on — no coding required per manufacturer"],
      makes:["Porsche"] },
    { id:"gr86tl", acc:true, deposit:435, code:"ZN8 / ZD8", name:"GR86 / BRZ RGB Sequential Tail Lights", make:"Toyota / Subaru",
      years:[2022,2025], price:649, plug:"Plug-and-play, no cutting", gal:"gr86tl", hero:"gr86tl-1",
      fit:"2nd-gen GR86 (ZN8) and BRZ (ZD8), 2022–2025. Not for 1st-gen 86/BRZ/FR-S. Pair (left + right).",
      specs:["Full LED tail lamp assembly, sold as a left/right pair","Sequential turn signal and animated start-up sequence","RGB running light with app-selectable colors","Plugs into the factory connectors — no splicing","Check local lighting laws before road use; colored running lights may be show/off-road only in some states"],
      makes:["Toyota","Subaru"] },
    { id:"p987sw", acc:true, deposit:1014, depositV:{standard:1014,premium:1400}, priceV:{standard:1499,premium:2099}, code:"987 / 997", name:"Cayman / Boxster Carbon Steering Wheel", make:"Porsche",
      years:[2005,2012], price:1499, plug:"Reuses your factory airbag & buttons", gal:"p987sw", hero:"p987sw-1",
      fit:"987 Cayman / Boxster and 997 911 three-spoke wheels (2005–2012). Your original airbag and controls transfer over; we recommend professional install.",
      specs:["Real carbon fiber upper and lower sections","Perforated leather or Alcantara grips, flat-bottom shape","Choice of center-stripe and stitching color","Built to order on your original wheel's mounting","Standard (leather) or Premium (Alcantara + custom stitch)"],
      makes:["Porsche"] },
    { id:"c9ymc", acc:true, deposit:191, code:"9Y0 / 9Y3", name:"Cayenne Carbon Fiber Mirror Covers", make:"Porsche",
      years:[2018,2022], price:339, plug:"Add-on covers, fit over factory caps", gal:"c9ymc", hero:"c9ymc-2",
      fit:"Cayenne 9Y0 SUV and 9Y3 Coupe, 2018–2022 (pre-facelift), left-hand drive. Add-on style: the covers fit over your factory mirror caps. Pair (left + right). Send a photo of your mirrors if unsure.",
      specs:["Real carbon fiber with gloss clear coat (per supplier)","Add-on covers that go over the factory mirror caps — nothing to cut or wire","Sold as a left/right pair","Ships from our partner factory to our LA warehouse, then to you — est. 3–5 weeks","Supplier photos shown; actual weave pattern may vary slightly"],
      makes:["Porsche"] },
    { id:"p718mc", acc:true, deposit:174, code:"982 / 718", name:"718 Cayman / Boxster Carbon Fiber Mirror Caps", make:"Porsche",
      years:[2016,2024], price:299, plug:"Mirror cap shells, no wiring", gal:"p718mc", hero:"p718mc-2",
      fit:"718 Cayman / Boxster (982) incl. S, GTS, Spyder and GT4, 2016+, left-hand drive (US). Pair (left + right). We confirm your car from a mirror photo before ordering.",
      specs:["Carbon fiber mirror cap shells, 3K weave with clear coat (per supplier)","Approx. 10.0 × 6.4 in per cap (supplier measurement)","Sold as a left/right pair","Professional install recommended","Supplier photos shown; actual weave pattern may vary slightly"],
      makes:["Porsche"] },
    { id:"p718dl", acc:true, deposit:469, code:"982 / 718", name:"718 Cayman / Boxster Carbon Rear Diffuser", make:"Porsche",
      years:[2017,2022], price:799, plug:"Bolts to the rear bumper, pro install advised", gal:"p718dl", hero:"p718dl-1",
      fit:"718 Cayman / Boxster (982), 2017–2022 with the standard center-exit exhaust. Not for GT4 / Spyder / GT4 RS rear bumpers. We confirm your car from a rear bumper photo before ordering.",
      specs:["Carbon fiber rear bumper diffuser with center exhaust cut-out (per supplier)","Made to order by our partner factory — est. 4–6 weeks to you","Professional install recommended","Large item: ships to our LA warehouse for inspection before it goes to you","Supplier photos shown; finish and weave may vary slightly"],
      makes:["Porsche"] },
    { id:"sbshb", acc:true, direct:true /* in-stock AE item: pay in full only, no deposit (2026-11-01) */, deposit:17, code:"WRX / STI / 86", name:"Front + Rear Shifter Bushing Kit (Polyurethane)", make:"Subaru / Toyota / Scion",
      years:[2002,2021], price:49, plug:"Bolt-in, replaces the factory rubber shifter bushings", gal:"sbshb", hero:"sbshb-1",
      fit:"Manual-transmission Subaru and Toyota 86 platform shifters: Subaru BRZ, Scion FR-S and Toyota GT86 / 86 (2013–2021, 6-speed manual), WRX STI 6-speed (2004–2021) and WRX (2002–2014). Not for automatic/CVT cars or the 2022+ WRX / GR86 / BRZ. Fitment is per the supplier; tell us your car and gearbox and we confirm before ordering.",
      specs:["Front shifter stabilizer bushings + rear shifter bushing with metal sleeve and bolts (per supplier photos)","Red polyurethane — firmer than the factory rubber for a tighter, less sloppy shift; may pass a little more vibration","Generic aftermarket part, not a Kartboy / Whiteline / Perrin product","Ships directly from the supplier to your address (not via our LA warehouse) — est. 2–3 weeks","Supplier photos shown; supplier stock is limited, we confirm availability before charging the balance"],
      makes:["Subaru","Toyota","Scion"] },
    { id:"mxtray", acc:true, direct:true /* in-stock AE item: pay in full only, no deposit */, code:"ND", name:"MX-5 Miata ND Center Armrest Storage Tray", make:"Mazda",
      years:[2016,2025], price:109, plug:"Drop-in tray for the center armrest box, no tools", gal:"mxtray", hero:"mxtray-1",
      seoTitle:"Mazda MX-5 Miata ND Center Armrest Storage Tray (2016+) – Console Organizer",
      alts:["Mazda MX-5 Miata ND center armrest storage tray installed in the console box","ND Miata armrest tray close-up with cup well","Black ABS MX-5 ND console organizer tray held in hand","MX-5 Miata ND armrest compartment tray fitted, top view"],
      seoDesc:"Drop-in center armrest storage tray / console organizer for the Mazda MX-5 Miata ND and RF (2016+). Black ABS, no tools. In stock, $109, pay in full, ships direct to US addresses in about 2–3 weeks.",
      fit:"Mazda MX-5 Miata ND (2016+), soft top and RF, left-hand drive. Sits inside the factory center armrest compartment behind the seats. Fitment is per the supplier; tell us your year in the note and if it does not fit we cancel and refund before ordering.",
      specs:["Layered organizer tray with a small cup/coin well (per supplier photos)","Black ABS, 3D-printed by the supplier — visible print layer lines are normal","Drop-in fit, no drilling or tools","Generic aftermarket part, not a Mazda product","In stock — ships directly from the supplier to your address (not via our LA warehouse), est. 2–3 weeks","Supplier photos shown; pay in full at checkout, no deposit"],
      makes:["Mazda"] }
  ],
  comingSoon: [
    {code:"991", name:"Porsche 911 (991)", img:"991-224046776", note:"Two 7.1\" + two 4\" screens"},
    {code:"971 / 9Y0", name:"Panamera 2016–23 · Cayenne 2018–23", img:"panamera-cayenne-223601049", note:"Center-dial LCD, 11 color themes"},
    {code:"AP1 / AP2", name:"Honda S2000", img:"", note:"In testing"}
  ],
  ig: [{v:"ig-ek-De6mRsgB47G",code:"EK3"},{v:"ig-gt86-DX0aabLBDOG",code:"ZN6"},{v:"ig-ek-DWbEjeMAX5y",code:"EK9"},{v:"ig-987-DK7WayAyHrJ",code:"987"},{v:"ig-981-DT4hNhwDy_S",code:"981"},{v:"ig-s2000-DY4k_fEIDI9",code:"AP2 · soon"},{v:"ig-panamera-cayenne-C945HPey8FI",code:"971 · soon"}]
};
