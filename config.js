// ===== EDIT EVERYTHING HERE =====
window.SITE = {
  brand: "GaugeLab LA",
  tagline: "Digital instrument cluster upgrades, fitted in Los Angeles",
  email: "hello@example.com",          // TODO: Cheung's contact email
  // Form delivery: set to a FormSubmit/Formspree/your-API URL. Empty = email fallback (mailto).
  formEndpoint: "",
  stripeCheckoutUrl: "",               // TODO: Stripe Payment Link; empty = "we send a secure payment link"
  depositUSD: 200,                     // PLACEHOLDER refundable deposit
  leadTime: "3–5 weeks (estimate)",
  products: [
    { id:"gt86", name:"GT86 / BRZ / FR-S Digital Cluster", make:"Toyota / Subaru / Scion", chassis:"ZN6 / ZC6",
      years:[2013,2020], price:null, plug:"Non-destructive install",
      fit:"Currently for push-button-start trims with dual-zone climate control. Send photos so we can confirm your car.",
      makes:["Toyota","Subaru","Scion"] },
    { id:"ek", name:"Civic EK Digital Cluster", make:"Honda", chassis:"EK / EJ (EK3, EK4, EK9 Type R, EJ6, EJ8)",
      years:[1996,2000], price:null, plug:"Plug-and-play connectors",
      fit:"USDM DX / LX / EX / HX / Si and JDM EK9 chassis — we confirm by VIN and cluster photos before build.",
      makes:["Honda"] },
    { id:"987", name:"Cayman / Boxster Digital Cluster", make:"Porsche", chassis:"987 (2005–2012) · 981 (2013–2016)",
      years:[2005,2016], price:null, plug:"Fitment confirmed per car",
      fit:"987 and 981 generations. Fitment varies by options; we confirm before build.",
      makes:["Porsche"] }
  ],
  comingSoon: ["Porsche 911", "Porsche Panamera", "Porsche Cayenne (2017–2023)", "Honda S2000"]
};
