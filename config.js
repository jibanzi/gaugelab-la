// ===== EDIT EVERYTHING HERE =====
window.SITE = {
  brand: "Tachi Club",
  tagline: "Digital cluster swaps for JDM + Euro chassis. Fitted in Los Angeles.",
  email: "hello@example.com",          // TODO: Cheung's contact email
  formEndpoint: "",                    // FormSubmit/Formspree URL; empty = mailto fallback
  stripeCheckoutUrl: "",               // TODO: Stripe Payment Link
  depositUSD: 200,                     // PLACEHOLDER refundable deposit
  leadTime: "3–5 weeks (estimate)",
  gallery: {"gt86": ["gt86-223835832", "gt86-223835833", "gt86-223835834", "gt86-224046690", "gt86-224046691", "gt86-224046692", "brz-224046741", "brz-224046742", "brz-224046743"], "ek": ["ek3-224729425", "ek3-224729426", "ek3-224729428", "ek3-224729429", "ek3-224729430", "ek3-224729431", "ek3-224785198", "ek3-224785199", "ek3-224785200", "ek3-224785201", "ek3-224785202", "ek3-224785203"], "987": ["987-223565096", "987-223565097", "987-223565098", "987-223565099", "987-223565100", "987-224046840", "987-224046842", "987-224046844", "981-223824245", "981-223824272", "981-223824273", "981-223824274", "981-223824275", "981-223824276", "981-224046831", "981-224046832", "981-224046833", "718-224046792"], "991": ["991-223632459", "991-223632460", "991-223632461", "991-223632462", "991-223632463", "991-223632466", "991-224046775", "991-224046776", "991-224046777", "991-224046778"], "pc": ["panamera-cayenne-223599723", "panamera-cayenne-223599724", "panamera-cayenne-223599725", "panamera-cayenne-223599726", "panamera-cayenne-223599727", "panamera-cayenne-223599728", "panamera-cayenne-223599729", "panamera-cayenne-223599730", "panamera-cayenne-223599732", "panamera-cayenne-223599733", "panamera-cayenne-223599734", "panamera-cayenne-223601049", "panamera-cayenne-223601051"]},
  chassis: ["ZN6","ZC6","EK9","EK4","EK3","EJ8","987","981","991","971","9Y0","AP1","AP2"],
  products: [
    { id:"gt86", code:"ZN6 / ZC6", name:"GT86 / BRZ / FR-S Digital Cluster", make:"Toyota / Subaru / Scion",
      years:[2013,2020], price:null, plug:"Non-destructive install", gal:"gt86", hero:"gt86-224046692",
      video:"gt86-toyota-gt-86-digital-gauge-cluster",
      fit:"Currently for push-button-start trims with dual-zone climate control. Send photos so we can confirm your car.",
      specs:["12.3-inch LCD, 2970×720 resolution (manufacturer spec)","3000:1 contrast, up to 1000 nits peak brightness","~178° viewing angles, warm color tone for night driving","Temperature-tested from −30°C to 75°C by the manufacturer","No need to open the factory cluster board — typical install around 30 min per manufacturer"],
      makes:["Toyota","Subaru","Scion"] },
    { id:"ek", code:"EK9 / EK4 / EK3", name:"Civic EK Digital Cluster", make:"Honda",
      years:[1996,2000], price:null, plug:"Plug-and-play into factory harness", gal:"ek", hero:"ek3-224729429",
      video:"ek3-honda-ek3-instrument-cluster",
      fit:"EK / EJ chassis (EK3, EK4, EK9 Type R, EJ6, EJ8). We confirm by VIN and cluster photos before build.",
      specs:["Drops into the factory cluster slot — no brackets, shims or harness cutting","Reads the stock OBD-1 signals: speedo cable, ignition pulse RPM, resistive fuel and coolant","Segmented shift light for high-rev B-series builds (yellow → orange → red)","Can show extra data such as boost, AFR and intake temp with compatible add-on modules","Aftermarket ECUs, cams or sensors may need a matching calibration/signal module — tell us your build"],
      makes:["Honda"] },
    { id:"987", code:"987 / 981", name:"Cayman / Boxster Digital Cluster", make:"Porsche",
      years:[2005,2016], price:null, plug:"Non-destructive, plug-in harness", gal:"987", hero:"981-224046832",
      video:"987-modernize-your-porsche-987-dashboard",
      fit:"987 (2005–2012) and 981 (2013–2016). Fitment varies by options; we confirm before build.",
      specs:["4-inch main screen + dual 3.4-inch side screens","17 selectable UI themes, Linux-based system with quick startup","3000:1 contrast, up to 1000 nits, 800+ PPI (manufacturer spec)","Shows speed, RPM, fuel, coolant temp, drive time and mileage; switch pages from the wheel buttons","Install, plug in the harness, power on — no coding required per manufacturer"],
      makes:["Porsche"] }
  ],
  comingSoon: [
    {code:"991", name:"Porsche 911 (991)", img:"991-224046776", note:"Two 7.1\" + two 4\" screens"},
    {code:"971 / 9Y0", name:"Panamera 2016–23 · Cayenne 2018–23", img:"panamera-cayenne-223601049", note:"Center-dial LCD, 11 color themes"},
    {code:"AP1 / AP2", name:"Honda S2000", img:"", note:"In testing"}
  ],
  ig: [{v:"ig-ek-De6mRsgB47G",code:"EK3"},{v:"ig-gt86-DX0aabLBDOG",code:"ZN6"},{v:"ig-ek-DWbEjeMAX5y",code:"EK9"},{v:"ig-987-DK7WayAyHrJ",code:"987"},{v:"ig-981-DT4hNhwDy_S",code:"981"},{v:"ig-s2000-DY4k_fEIDI9",code:"AP2 · soon"},{v:"ig-panamera-cayenne-C945HPey8FI",code:"971 · soon"}]
};
