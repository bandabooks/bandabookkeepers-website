#!/usr/bin/env python3
"""Banda Bookkeepers static site generator.

Run from the repository root:  python3 _src/build.py
Writes every page as <path>/index.html at the repository root (the web root).
contact.php, assets/ and .htaccess are hand-edited and not touched here.
"""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://bandabookkeepers.com"
TMB = "https://www.thinkmybiz.co.za"
REF = "?ref=bandabookkeepers"
UPDATED = "2026-11-21"
PHONE, PHONE_INTL, CELL = "066 210 5631", "27662105631", "072 104 1051"
EMAIL = "accounts@thinkmybiz.co.za"
ADDRESS = "No 48 Rabe Street, Havenga Building, Mokopane, Limpopo, 0600"
WA = f"https://wa.me/{PHONE_INTL}?text=" + "Hi%20Banda%20Bookkeepers%2C%20I%27d%20like%20a%20quote%20for%20monthly%20bookkeeping."

def tmb(path=""):
    return f"{TMB}/{path}{REF}" if path else f"{TMB}/{REF}"

MARK = ('<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="{bg}"/>'
        '<path d="M14 14V50M14 14H28A8 8 0 0 1 28 30H14M14 30H30A10 10 0 0 1 30 50H14" fill="none" stroke="#fff" '
        'stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/><path d="M42 20L45 23L51.5 15.5" fill="none" '
        'stroke="{tick}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def icon(d):
    return (f'<div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="#1F5FD6" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg></div>')

I = {
 "ledger": '<path d="M4 4h12a4 4 0 0 1 4 4v12H8a4 4 0 0 1-4-4z"/><path d="M8 9h8M8 13h8M8 17h5"/>',
 "bank": '<path d="M3 10l9-6 9 6"/><path d="M5 10v8M9 10v8M15 10v8M19 10v8M3 20h18"/>',
 "people": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/>',
 "receipt": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
 "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
 "broom": '<path d="M14 4l6 6M12 6l6 6-7 7H5v-6z"/><path d="M5 19l4-4"/>',
 "cloud": '<path d="M7 18a5 5 0 1 1 1-9.9A6 6 0 0 1 19.5 10 4 4 0 0 1 18 18z"/>',
 "folder": '<path d="M3 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 13l2 2 4-4"/>',
 "in": '<path d="M12 3v12M7 10l5 5 5-5"/><path d="M4 19h16"/>',
 "out": '<path d="M12 21V9M7 14l5-5 5 5"/><path d="M4 5h16"/>',
}

NAV = [("/", "Home"), ("/services/", "Services & packages"), ("/bookkeeping-advice/", "Bookkeeping advice"),
       ("/about/", "About"), ("/contact/", "Contact")]

ORG_LD = {
  "@context": "https://schema.org", "@type": "AccountingService", "name": "Banda Bookkeepers",
  "url": SITE + "/", "logo": SITE + "/assets/img/favicon.svg", "telephone": "+27 66 210 5631", "email": EMAIL,
  "description": "Monthly bookkeeping, bank reconciliations, payroll records and VAT-ready books for South African small businesses.",
  "address": {"@type": "PostalAddress", "streetAddress": "No 48 Rabe Street, Havenga Building", "addressLocality": "Mokopane",
              "addressRegion": "Limpopo", "postalCode": "0600", "addressCountry": "ZA"},
  "areaServed": ["Mokopane", "Polokwane", "Pretoria", "Centurion", "Johannesburg", "Midrand", "South Africa"],
  "parentOrganization": {"@type": "AccountingService", "name": "Think Mybiz Accountants and Tax Practitioners (Pty) Ltd", "url": TMB + "/"},
}

def head(title, desc, path, extra_ld=None, noindex=False):
    lds = [ORG_LD] + ([extra_ld] if extra_ld else [])
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{robots}<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Banda Bookkeepers">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta name="theme-color" content="#0B2545">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v=1">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="strip"><div class="wrap">
<span>Bookkeeping desk of <a href="{tmb()}">Think Mybiz Accountants &amp; Tax Practitioners</a></span>
<span class="hide-sm">Call or WhatsApp <a href="tel:+{PHONE_INTL}">{PHONE}</a></span>
</div></div>
<header class="site-head"><div class="wrap">
<a class="brand" href="/" aria-label="Banda Bookkeepers home">{MARK.format(bg="#0B2545", tick="#5B9BFF")}<span class="brand-text"><b>BANDA</b><span>BOOKKEEPERS</span></span></a>
<nav aria-label="Main">
<button class="menu-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Open menu"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0B2545" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
<ul class="nav-links" id="nav-links">
""" + "\n".join(
        f'<li><a href="{h}"{" aria-current=page" if h == path else ""}>{t}</a></li>' for h, t in NAV) + """
<li><a class="btn btn-primary nav-cta" href="/contact/">Free consultation</a></li>
</ul>
</nav>
</div></header>
<main id="main">
"""

def tmb_band(title="Need more than bookkeeping? Think Mybiz takes it from here."):
    items = [("services/individual-tax/", "Income &amp; provisional tax"), ("services/business-tax/", "Company &amp; trust tax returns"),
             ("services/vat/", "VAT201 submissions to SARS"), ("services/payroll/", "EMP201 / EMP501 payroll submissions"),
             ("services/accounting/", "Annual financial statements"), ("services/sars-disputes/", "SARS letters, audits &amp; disputes"),
             ("services/business-compliance/", "CIPC, licences &amp; tenders"), ("services/business-advisory/", "Business advisory &amp; growth")]
    lis = "\n".join(f'<li><a href="{tmb(p)}">{t} <span aria-hidden="true">→</span></a></li>' for p, t in items)
    return f"""<section><div class="wrap"><div class="tmb">
<span class="eyebrow" style="color:#9DBDF5">Our main firm</span>
<h2>{title}</h2>
<p>Banda Bookkeepers is the bookkeeping desk of Think Mybiz Accountants and Tax Practitioners. Your reconciled books flow straight into tax, financial statements and compliance at the same practice — one client record, no documents sent twice.</p>
<ul class="tmb-list">
{lis}
</ul>
<a class="btn btn-light" href="{tmb()}">Visit thinkmybiz.co.za</a>
</div></div></section>
"""

def cta_band():
    return f"""<section class="cta-band"><div class="wrap">
<div><h2>Get your books under control this month.</h2>
<p>Free consultation. Fixed monthly fee. Reconciled books and a report you can read.</p></div>
<div class="actions"><a class="btn btn-light" href="/contact/">Book a free consultation</a>
<a class="btn btn-ghost-light" href="{WA}">WhatsApp {PHONE}</a></div>
</div></section>
"""

FOOT = f"""</main>
<footer class="site-foot"><div class="wrap">
<div class="foot-grid">
<div class="foot-brand">
<a class="brand" href="/" aria-label="Banda Bookkeepers home">{MARK.format(bg="#1F5FD6", tick="#BFD6FF")}<span class="brand-text"><b>BANDA</b><span>BOOKKEEPERS</span></span></a>
<p style="margin-top:14px">Monthly bookkeeping for South African small businesses. Part of Think Mybiz Accountants and Tax Practitioners (Pty) Ltd.</p>
</div>
<div><h4>Bookkeeping</h4><ul>
<li><a href="/services/">Services &amp; packages</a></li>
<li><a href="/bookkeeping-advice/">Bookkeeping advice</a></li>
<li><a href="/bookkeeping-advice/monthly-bookkeeping-checklist/">Monthly checklist</a></li>
<li><a href="/about/">About us</a></li>
<li><a href="/contact/">Free consultation</a></li>
</ul></div>
<div><h4>At Think Mybiz</h4><ul>
<li><a href="{tmb('services/business-tax/')}">Tax returns</a></li>
<li><a href="{tmb('services/vat/')}">VAT submissions</a></li>
<li><a href="{tmb('services/accounting/')}">Financial statements</a></li>
<li><a href="{tmb('services/sars-disputes/')}">SARS disputes</a></li>
<li><a href="{tmb('services/')}">All services</a></li>
</ul></div>
<div><h4>Contact</h4><ul>
<li><a href="tel:+{PHONE_INTL}">{PHONE}</a> (call / WhatsApp)</li>
<li><a href="tel:+27721041051">{CELL}</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li>{ADDRESS}</li>
</ul></div>
</div>
<div class="foot-base">
<span>© <span id="year">2026</span> Think Mybiz Accountants and Tax Practitioners (Pty) Ltd · CIPC 2021/819201/07 · SARS registered tax practitioner PR-0034776</span>
<span><a href="/privacy/">Privacy (POPIA)</a></span>
</div>
</div></footer>
<script src="/assets/js/site.js?v=1" defer></script>
</body>
</html>
"""

def page_head(eyebrow, h1, lead, crumbs=None):
    c = ""
    if crumbs:
        c = '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(
            f'<a href="{h}">{t}</a>' if h else t for h, t in crumbs) + "</nav>"
    return f"""<div class="page-head"><div class="wrap">{c}
<span class="eyebrow">{eyebrow}</span>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
</div></div>
"""

PAGES = {}

def write(path, title, desc, body, ld=None, noindex=False):
    PAGES[path] = noindex
    out = head(title, desc, path, ld, noindex) + body + FOOT
    fp = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    if path == "/404/":
        fp = os.path.join(ROOT, "404.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(out)

# ---------------------------------------------------------------- content
SERVICES = [
 ("ledger", "Monthly bookkeeping", "Every bank, card and cash transaction captured and coded to the right account — monthly, not in a year-end rush."),
 ("bank", "Bank &amp; card reconciliations", "Each account reconciled to its statement every month, with differences found and explained."),
 ("in", "Debtors (money owed to you)", "Invoices tracked and an age analysis showing who is overdue, so you know who to follow up."),
 ("out", "Creditors (money you owe)", "Supplier invoices captured and supplier statements reconciled, with a clear payment schedule."),
 ("people", "Payroll records", "Monthly payslips, payroll journals and the figures your EMP201 needs, kept in one place."),
 ("receipt", "VAT-ready books", "VAT coded on every transaction and VAT201 working papers prepared each period."),
 ("chart", "Monthly management reports", "Income statement, balance sheet and a cash summary in plain language — what came in, what went out, what is left."),
 ("broom", "Catch-up &amp; clean-up", "Months or years of backlog captured and reconciled, so you start again from clean opening balances."),
 ("cloud", "Cloud software setup", "Set-up or migration onto cloud accounting software, with bank feeds connected so less is typed by hand."),
 ("folder", "Year-end pack", "A reconciled trial balance and supporting schedules, ready for financial statements and tax at Think Mybiz."),
]

def service_cards(n=None):
    s = SERVICES[:n] if n else SERVICES
    return "\n".join(f'<div class="card">{icon(I[i])}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in s)

PACKAGES = [
 ("Starter", "Sole traders · under about 100 transactions a month", False,
  ["Transactions captured and coded", "One bank account reconciled monthly", "Quarterly management report", "Year-end pack for tax"]),
 ("Business", "Small businesses and VAT vendors", True,
  ["All bank and card accounts reconciled", "Debtors and creditors kept up to date", "VAT201 working papers each period", "Monthly management report"]),
 ("Business + Payroll", "Employers with staff", False,
  ["Everything in Business", "Monthly payslips and payroll journals", "EMP201 support figures", "Leave and payroll records kept"]),
 ("Clean-up (once-off)", "Businesses behind on their books", False,
  ["Backlog captured and reconciled", "Opening balances confirmed", "Problem items listed for you", "Then onto a monthly package"]),
]

def package_cards():
    out = []
    for name, who, feat, items in PACKAGES:
        slug = name
        badge = '<span class="badge">Most chosen</span>' if feat else ""
        lis = "".join(f"<li>{x}</li>" for x in items)
        out.append(f'<div class="card pkg{" featured" if feat else ""}">{badge}<h3>{name}</h3><span class="who">{who}</span>'
                   f'<ul>{lis}</ul><p style="margin-top:auto;padding-top:14px"><a class="btn {"btn-primary" if feat else "btn-outline"}" '
                   f'href="/contact/?package={html.escape(slug)}">Get a quote</a></p></div>')
    return "\n".join(out)

STEPS = [("Free consultation", "A short call or meeting about your business, volumes and the state of your books."),
         ("Quote &amp; engagement letter", "A fixed monthly fee and a signed letter setting out the scope and deadlines."),
         ("Onboarding", "FICA documents, bank statements or feeds, prior records and software access collected."),
         ("Catch-up, if needed", "Any backlog captured and reconciled to clean opening balances."),
         ("Monthly cycle", "Documents in by an agreed date; books closed and your report delivered on time.")]

def steps():
    return '<ol class="steps">' + "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in STEPS) + "</ol>"

ARTICLES = [
 ("what-does-a-bookkeeper-do", "What does a bookkeeper actually do each month?",
  "A month-by-month look at the work behind clean books: capturing, reconciling, debtors, creditors, payroll records and the monthly report."),
 ("bookkeeper-vs-accountant", "Bookkeeper vs accountant: who does what?",
  "Bookkeeping keeps the records; accounting turns them into financial statements, tax returns and advice. Here is where the line sits."),
 ("signs-your-books-are-behind", "7 signs your books are behind — and how to catch up",
  "Unreconciled bank accounts, guessed VAT and a shoebox of slips. How to tell your books need attention, and what a clean-up involves."),
 ("how-long-to-keep-business-records", "How long must you keep business records in South Africa?",
  "SARS expects records to be kept for five years in most cases. What to keep, how long, and how to store it safely."),
 ("monthly-bookkeeping-checklist", "The monthly bookkeeping checklist for small business owners",
  "A practical month-end checklist you can print: what to collect, what to reconcile and what to review before the month closes."),
]

def article_cards(exclude=None, n=None):
    a = [x for x in ARTICLES if x[0] != exclude][: n or 99]
    return "\n".join(f'<a class="card card-link" href="/bookkeeping-advice/{s}/"><h3>{t}</h3><p>{d}</p><span class="more">Read the guide →</span></a>' for s, t, d in a)

FAQ = [
 ("What does monthly bookkeeping cost?", "We quote a fixed monthly fee after a free consultation. The fee depends mainly on how many transactions you have each month, how many bank and card accounts you use, and whether you need payroll records or VAT working papers."),
 ("Do I need a bookkeeper if I already have an accountant?", "Your accountant prepares financial statements and tax returns from your records. A bookkeeper keeps those records accurate every month. At Banda Bookkeepers both sit in the same practice: we keep the books, and Think Mybiz Accountants handles tax and financial statements."),
 ("Can you catch up books that are months or years behind?", "Yes. A clean-up captures and reconciles the backlog, confirms opening balances and lists anything that needs your input. Once the books are current, we move you onto a monthly package."),
 ("Do you submit my VAT and tax returns?", "Bookkeeping prepares VAT-ready books and VAT201 working papers. Submissions to SARS, tax returns and financial statements are handled by our main firm, Think Mybiz Accountants and Tax Practitioners."),
 ("Do I need to visit your office?", "No. Most clients send documents electronically and we work remotely across South Africa. You are welcome to meet us at our Mokopane office or arrange a meeting in Polokwane, Pretoria, Centurion, Johannesburg or Midrand."),
 ("Which accounting software do you work with?", "We work with the cloud accounting software you already use, or help you choose and set one up, with bank feeds connected where your bank supports it."),
]

def faq_block(items):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>"

FAQ_LD = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

# ---------------------------------------------------------------- home
home = f"""<section class="hero">
<svg class="hero-mark" viewBox="0 0 64 64" aria-hidden="true"><path d="M14 14V50M14 14H28A8 8 0 0 1 28 30H14M14 30H30A10 10 0 0 1 30 50H14" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/><path d="M42 20L45 23L51.5 15.5" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
<div class="wrap hero-grid">
<div>
<span class="eyebrow">Monthly bookkeeping · South Africa</span>
<h1>Your books, done right, every month.</h1>
<p class="lead">We capture, reconcile and report on your business transactions every month — so you always know where your money went, and your books are ready for VAT, payroll and SARS.</p>
<div class="actions"><a class="btn btn-primary" href="/contact/">Book a free bookkeeping consultation</a>
<a class="btn btn-ghost-light" href="{WA}">WhatsApp {PHONE}</a></div>
<div class="trust"><span><b>Registered practice</b> · SARS tax practitioner PR-0034776</span><span><b>Remote</b> across South Africa</span></div>
</div>
<div class="hero-card">
<h2>Every month, you get:</h2>
<ul class="checks">
<li>All bank and card accounts reconciled to the statement</li>
<li>Debtors and creditors up to date</li>
<li>VAT coded and VAT201 working papers ready</li>
<li>Payroll records and EMP201 figures</li>
<li>A plain-language report: income, expenses, cash</li>
</ul>
<p class="small muted" style="margin:16px 0 0">Fixed monthly fee, quoted after a free consultation.</p>
</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">What we do</span><h2>Bookkeeping is all we focus on here</h2>
<p class="lead">Accurate records are the foundation for every tax return, VAT submission, loan application and business decision. We keep them right, month after month.</p></div>
<div class="grid g3">{service_cards(6)}</div>
<p style="margin-top:24px"><a class="btn btn-outline" href="/services/">See all services and packages</a></p>
</div></section>

<section class="alt"><div class="wrap">
<div class="grid g2" style="align-items:center;gap:48px">
<div><span class="eyebrow">Why monthly matters</span><h2>Year-end bookkeeping is expensive bookkeeping</h2>
<p>When books are left until year-end, missing slips are harder to find, bank differences pile up and VAT returns are prepared from guesses. Fixing twelve months at once costs more than keeping one month right.</p>
<p>Monthly bookkeeping means problems surface while they are small, VAT is supported by real records, and you can see your cash position before you make a decision — not after.</p>
<p><a href="/bookkeeping-advice/signs-your-books-are-behind/">7 signs your books are behind →</a></p></div>
<div class="card"><h3>Who we work with</h3>
<ul class="checks" style="margin-top:12px">
<li>(Pty) Ltd companies and CCs with regular monthly transactions</li>
<li>VAT vendors who need records behind every VAT return</li>
<li>Employers running payroll for 1 to 50 staff</li>
<li>Sole traders moving from spreadsheets to proper books</li>
<li>Businesses behind on their books after a SARS letter, loan request or tender requirement</li>
<li>Startups that want clean books from day one</li>
</ul></div>
</div></div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">Packages</span><h2>Pick the level of help you need</h2>
<p class="lead">Every package includes captured transactions, reconciled bank accounts and a report. Fees are fixed monthly and quoted after a free consultation.</p></div>
<div class="grid g4">{package_cards()}</div>
</div></section>

<section class="alt"><div class="wrap">
<div class="sec-head"><span class="eyebrow">How we work</span><h2>From first call to your first monthly report</h2></div>
{steps()}
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">Bookkeeping advice</span><h2>Learn what good books look like</h2>
<p class="lead">Plain-language guides for business owners. No jargon, no sales pitch.</p></div>
<div class="grid g3">{article_cards(n=3)}</div>
<p style="margin-top:24px"><a href="/bookkeeping-advice/">All bookkeeping guides →</a></p>
</div></section>

{tmb_band()}

<section class="alt"><div class="wrap" style="max-width:860px">
<div class="sec-head"><span class="eyebrow">Questions</span><h2>Bookkeeping FAQs</h2></div>
{faq_block(FAQ)}
</div></section>
{cta_band()}"""
write("/", "Banda Bookkeepers | Monthly Bookkeeping for South African Small Businesses",
      "Monthly bookkeeping, bank reconciliations, payroll records and VAT-ready books for South African small businesses. Free consultation. Part of Think Mybiz Accountants.",
      home, FAQ_LD)

# ---------------------------------------------------------------- services
services = page_head("Services &amp; packages", "Bookkeeping services and packages",
    "Everything that keeps your records accurate, current and ready for SARS — delivered every month at a fixed fee.") + f"""
<section><div class="wrap">
<div class="sec-head"><h2>Bookkeeping services</h2><p class="lead">Choose a package below, or tell us what you need and we will build the right mix.</p></div>
<div class="grid g3">{service_cards()}</div>
</div></section>

<section class="alt" id="packages"><div class="wrap">
<div class="sec-head"><h2>Packages</h2><p class="lead">Fixed monthly fees, quoted after a free consultation, based on your monthly transactions and number of accounts.</p></div>
<div class="grid g4">{package_cards()}</div>
</div></section>

<section><div class="wrap grid g2" style="gap:48px">
<div><h2>What you send us</h2>
<ul class="checks">
<li>Bank and card statements, or access to bank feeds</li>
<li>Sales invoices and supplier invoices for the month</li>
<li>Cash slips and petty-cash records</li>
<li>Payroll changes: new staff, leave, overtime, terminations</li>
<li>Anything unusual: loans, asset purchases, owner payments</li>
</ul></div>
<div><h2>What you get back</h2>
<ul class="checks">
<li>Reconciled bank and card accounts</li>
<li>An up-to-date debtors and creditors list</li>
<li>VAT201 working papers (VAT vendors)</li>
<li>Payroll records and EMP201 figures (employers)</li>
<li>A monthly report with questions for you, if any</li>
</ul></div>
</div></section>

<section class="paper"><div class="wrap" style="max-width:860px">
<h2>Not sure which package fits?</h2>
<p>Tell us your business type, roughly how many transactions you have a month and whether you are VAT registered. We will recommend a package and quote a fixed monthly fee.</p>
<a class="btn btn-primary" href="/contact/">Get a bookkeeping quote</a>
</div></section>
{tmb_band("Tax, VAT submissions and financial statements are handled by Think Mybiz")}
{cta_band()}"""
write("/services/", "Bookkeeping Services & Packages | Banda Bookkeepers",
      "Monthly bookkeeping, bank reconciliations, debtors and creditors, payroll records, VAT-ready books, clean-ups and cloud setup. Fixed monthly packages.",
      services)

# ---------------------------------------------------------------- advice hub
hub = page_head("Bookkeeping advice", "Bookkeeping guides for business owners",
    "Practical, plain-language advice on keeping your records right — written by a registered South African practice.") + f"""
<section><div class="wrap">
<div class="grid g3">{article_cards()}</div>
</div></section>
<section class="paper"><div class="wrap" style="max-width:860px">
<h2>Free: the monthly bookkeeping checklist</h2>
<p>A one-page month-end routine for small business owners — what to collect, reconcile and review. Print it and keep it next to your desk.</p>
<a class="btn btn-primary" href="/bookkeeping-advice/monthly-bookkeeping-checklist/">Open the checklist</a>
</div></section>
{cta_band()}"""
write("/bookkeeping-advice/", "Bookkeeping Advice & Guides | Banda Bookkeepers",
      "Plain-language bookkeeping guides for South African small business owners: what a bookkeeper does, record keeping for SARS, catching up on books and a monthly checklist.",
      hub)

def article(slug, h1, desc, body, extra_ld=None):
    a_ld = {"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc,
            "datePublished": UPDATED, "dateModified": UPDATED,
            "author": {"@type": "Organization", "name": "Banda Bookkeepers"},
            "publisher": {"@type": "Organization", "name": "Banda Bookkeepers", "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/favicon.svg"}},
            "mainEntityOfPage": f"{SITE}/bookkeeping-advice/{slug}/"}
    content = f"""<div class="page-head"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/bookkeeping-advice/">Bookkeeping advice</a></nav>
<h1 style="max-width:22ch">{h1}</h1>
<p class="lead">{desc}</p>
<p class="meta">Banda Bookkeepers · Updated 21 November 2026</p>
</div></div>
<section><div class="wrap article">
{body}
<div class="callout"><h3>Want your books done for you?</h3>
<p>Banda Bookkeepers keeps your records reconciled and VAT-ready every month, for a fixed fee.</p>
<div class="actions"><a class="btn btn-primary" href="/contact/">Book a free consultation</a><a class="btn btn-outline" href="/services/">See packages</a></div></div>
</div></section>
<section class="alt"><div class="wrap"><h2>More bookkeeping guides</h2><div class="grid g3">{article_cards(exclude=slug, n=3)}</div></div></section>
"""
    write(f"/bookkeeping-advice/{slug}/", f"{h1} | Banda Bookkeepers", desc, content, extra_ld or a_ld)

A = {x[0]: x for x in ARTICLES}

s, t, d = A["what-does-a-bookkeeper-do"]
article(s, t, d, """
<p>Bookkeeping is the routine work of recording every financial transaction in your business and checking that the records agree with reality. Done monthly, it keeps your numbers usable all year — not just at tax time.</p>
<h2>1. Capturing and coding transactions</h2>
<p>Every payment in and out of your bank accounts, credit cards and petty cash is recorded and allocated to the right account: sales, rent, fuel, stock, salaries, loan repayments and so on. Correct coding is what makes your income statement meaningful and your VAT figures defensible.</p>
<h2>2. Reconciling bank and card accounts</h2>
<p>A reconciliation compares the balance in your books with the balance on your bank statement and explains every difference. It catches duplicated entries, missing transactions, bank charges you did not expect and payments that were never recorded. An unreconciled account is the most common reason books cannot be trusted.</p>
<h2>3. Keeping debtors and creditors up to date</h2>
<p>Your debtors list shows who owes you money and for how long. Your creditors list shows what you owe suppliers and when it is due. Kept current, they protect your cash flow: you chase overdue invoices on time and avoid paying a supplier twice.</p>
<h2>4. Payroll records</h2>
<p>For employers, the bookkeeper keeps payslips, payroll journals, leave records and the monthly figures needed for employer returns, so salaries in your books match what was actually paid.</p>
<h2>5. VAT-ready records</h2>
<p>For VAT vendors, each transaction carries the right VAT treatment, and the bookkeeper prepares working papers that support the VAT return. When SARS asks for support, the invoices and reconciliations are already there.</p>
<h2>6. The monthly report</h2>
<p>At month-end you receive a short report: income, expenses, profit, cash position and anything that needs your input. This is where bookkeeping stops being admin and starts being useful for decisions.</p>
<h2>What a bookkeeper does not do</h2>
<p>Bookkeeping produces the records. Preparing annual financial statements, completing tax returns and giving tax advice is accounting and tax work. At our practice that work is done by our main firm, <a href="https://www.thinkmybiz.co.za/?ref=bandabookkeepers">Think Mybiz Accountants and Tax Practitioners</a>, using the books we keep. See <a href="/bookkeeping-advice/bookkeeper-vs-accountant/">bookkeeper vs accountant</a> for where the line sits.</p>
""")

s, t, d = A["bookkeeper-vs-accountant"]
article(s, t, d, """
<p>Business owners often use “bookkeeper” and “accountant” for the same job. They are two stages of one process: the bookkeeper builds accurate records; the accountant uses those records to report, comply and advise.</p>
<h2>The bookkeeper: accurate records, every month</h2>
<ul>
<li>Captures and codes all transactions</li>
<li>Reconciles bank, card and loan accounts</li>
<li>Maintains debtors, creditors and payroll records</li>
<li>Prepares VAT working papers and monthly reports</li>
<li>Hands over a reconciled trial balance at year-end</li>
</ul>
<h2>The accountant and tax practitioner: reporting, compliance and advice</h2>
<ul>
<li>Prepares annual financial statements</li>
<li>Completes and submits income tax, provisional tax and company tax returns</li>
<li>Submits VAT and employer returns and deals with SARS queries</li>
<li>Advises on tax planning, structure and growth</li>
</ul>
<h2>Why the split matters</h2>
<p>If the bookkeeping is weak, the accountant spends time — your money — fixing records before any real accounting can start. If the records are clean, year-end becomes a review instead of a rebuild.</p>
<h2>How it works at our practice</h2>
<p>Banda Bookkeepers keeps your books every month. When the year closes, the reconciled records pass to <a href="https://www.thinkmybiz.co.za/services/accounting/?ref=bandabookkeepers">Think Mybiz Accountants</a> for financial statements and tax. It is one practice and one client record, so nothing is lost in a hand-over and you never send the same documents twice.</p>
<div class="callout"><p><b>Need tax or financial statements now?</b> Go straight to <a href="https://www.thinkmybiz.co.za/services/?ref=bandabookkeepers">Think Mybiz services</a>.</p></div>
""")

s, t, d = A["signs-your-books-are-behind"]
article(s, t, d, """
<p>Books rarely fall behind all at once. A busy month becomes a busy quarter, and suddenly nobody is sure what the real bank balance is. Here are the warning signs.</p>
<ol>
<li><b>Your bank accounts have not been reconciled for more than a month.</b> Without reconciliations you cannot be sure the books are complete.</li>
<li><b>VAT returns are prepared from bank statements alone.</b> VAT should be supported by valid invoices, not estimated from what left the account.</li>
<li><b>Slips and invoices live in a box, a car or a WhatsApp chat.</b> If documents are not filed as you go, they go missing.</li>
<li><b>You do not know who owes you money.</b> An out-of-date debtors list means late payers are not chased.</li>
<li><b>Your accountant asks the same questions every year.</b> Recurring year-end queries usually point to month-end gaps.</li>
<li><b>You cannot answer a bank or funder quickly.</b> Loan applications and tenders ask for recent management accounts.</li>
<li><b>A SARS letter has arrived and the support is hard to find.</b> Records you cannot produce are records you do not have.</li>
</ol>
<h2>How a clean-up works</h2>
<p>A catch-up or clean-up project brings the books back to a reliable position:</p>
<ol>
<li>Collect bank statements and available documents for the backlog period.</li>
<li>Capture and code every transaction.</li>
<li>Reconcile every bank and card account, month by month.</li>
<li>Confirm opening balances and list items that need your input.</li>
<li>Move onto a monthly package so it does not happen again.</li>
</ol>
<p>If a SARS letter is part of the picture, the tax side is handled by our main firm — see <a href="https://www.thinkmybiz.co.za/services/sars-disputes/?ref=bandabookkeepers">SARS letters and disputes at Think Mybiz</a>.</p>
""")

s, t, d = A["how-long-to-keep-business-records"]
article(s, t, d, """
<p>Good bookkeeping is not only about getting this month right. It is also about being able to produce the records behind a return years later, if SARS asks.</p>
<h2>The general rule: five years</h2>
<p>Under the Tax Administration Act, a person who has submitted a return must keep the records, books of account and documents for five years from the date the return was submitted. A person who should have submitted a return but did not must keep records until it is submitted. Records relevant to an audit, investigation, objection or appeal must be kept until that matter is finalised. Source: <a href="https://www.sars.gov.za/client-segments/record-keeping/">SARS — Record keeping</a> (checked 21 November 2026).</p>
<p>Employers must also keep employee tax records for at least five years following the submission of the related return (<a href="https://www.sars.gov.za/guide-for-employers-in-respect-of-employees-tax-2027/">SARS Guide for Employers in respect of Employees' Tax</a>).</p>
<h2>What to keep</h2>
<ul>
<li>Bank, card and loan statements</li>
<li>Sales invoices, credit notes and receipts issued</li>
<li>Supplier tax invoices and receipts</li>
<li>Payroll records: payslips, registers, leave and employee tax certificates</li>
<li>Asset purchase and sale documents</li>
<li>Contracts, leases and loan agreements</li>
<li>Your general ledger, reconciliations and year-end working papers</li>
</ul>
<h2>Keeping records safely</h2>
<p>SARS accepts records in their original form or in an acceptable electronic form. A simple, consistent digital filing system — one folder per month, scanned slips named by date and supplier, statements stored as PDFs — makes records easy to find and protects against loss. Because records contain personal information, store them securely and in line with POPIA.</p>
<div class="callout"><p>This guide is general information, not tax advice for your situation. For advice on a specific matter, speak to a registered tax practitioner at <a href="https://www.thinkmybiz.co.za/?ref=bandabookkeepers">Think Mybiz Accountants</a>.</p></div>
""")

s, t, d = A["monthly-bookkeeping-checklist"]
article(s, t, d, """
<p>Use this checklist in the first week of every month for the month that has just closed. If we keep your books, the items marked <b>(we do this)</b> are done for you.</p>
<h2>Collect</h2>
<ul>
<li>☐ Bank, card and loan statements for every account</li>
<li>☐ All sales invoices and credit notes issued</li>
<li>☐ All supplier invoices and receipts, including cash slips</li>
<li>☐ Payroll changes: new staff, leave, overtime, terminations</li>
<li>☐ Notes on anything unusual: loans, asset purchases, owner withdrawals</li>
</ul>
<h2>Record and reconcile</h2>
<ul>
<li>☐ Capture and code all transactions <b>(we do this)</b></li>
<li>☐ Reconcile every bank and card account to its statement <b>(we do this)</b></li>
<li>☐ Update debtors and creditors <b>(we do this)</b></li>
<li>☐ Process payroll journals <b>(we do this)</b></li>
<li>☐ Check VAT on every invoice; prepare VAT working papers <b>(we do this)</b></li>
</ul>
<h2>Review</h2>
<ul>
<li>☐ Who owes you money for more than 30 days? Follow up.</li>
<li>☐ Which supplier payments are due this month?</li>
<li>☐ Did income and expenses match what you expected?</li>
<li>☐ Is cash enough for salaries, VAT and suppliers next month?</li>
<li>☐ File this month's documents in one dated folder.</li>
</ul>
<p>Tip: print this page (Ctrl + P) and keep it next to your desk.</p>
""")

# ---------------------------------------------------------------- about
about = page_head("About us", "Bookkeeping you can rely on, inside a registered practice",
    "Banda Bookkeepers is the bookkeeping desk of Think Mybiz Accountants and Tax Practitioners — one practice, one team, one point of accountability.") + f"""
<section><div class="wrap grid g2" style="gap:48px">
<div>
<h2>Who we are</h2>
<p>We keep small-business books clean, current and reconciled — every month, not just at year-end. We capture transactions, reconcile bank accounts, track who owes you and who you owe, and keep your records ready for VAT, payroll and SARS.</p>
<p>Because we are part of <a href="{tmb()}">Think Mybiz Accountants and Tax Practitioners</a>, your books flow straight into tax returns, financial statements and compliance at the same practice. Nothing is lost between a bookkeeper and an accountant.</p>
<p><b>Mission:</b> give every small business owner books they can trust and understand, closed off every month.</p>
<p><b>Vision:</b> to be the bookkeeping partner South African small businesses recommend first.</p>
</div>
<div class="card">
<h3>Our values</h3>
<ul class="checks" style="margin-top:12px">
<li><span><b>Accuracy first</b> — every account reconciled, every balance explained.</span></li>
<li><span><b>On time, every month</b> — fixed monthly deadlines, not year-end catch-ups.</span></li>
<li><span><b>Plain language</b> — reports owners can read without an accountant beside them.</span></li>
<li><span><b>Confidentiality</b> — records handled privately and in line with POPIA.</span></li>
<li><span><b>Evidence-based</b> — every entry supported by a statement, invoice or slip.</span></li>
</ul></div>
</div></section>

<section class="alt"><div class="wrap">
<h2>Registrations</h2>
<div class="grid g4">
<div class="card"><h3>Legal entity</h3><p>Think Mybiz Accountants and Tax Practitioners (Pty) Ltd</p></div>
<div class="card"><h3>CIPC registration</h3><p>2021/819201/07</p></div>
<div class="card"><h3>SARS tax practitioner</h3><p>PR-0034776</p></div>
<div class="card"><h3>Affiliations</h3><p>SAIT Tax Technician (SA) · CIBA · ICBA</p></div>
</div>
</div></section>

<section><div class="wrap">
<h2>Where we work</h2>
<p class="lead">Head office in Mokopane, Limpopo, also serving Polokwane, Pretoria &amp; Centurion and Johannesburg &amp; Midrand — and remote clients across South Africa.</p>
</div></section>
{tmb_band()}
{cta_band()}"""
write("/about/", "About Banda Bookkeepers | Part of Think Mybiz Accountants",
      "Banda Bookkeepers is the bookkeeping desk of Think Mybiz Accountants and Tax Practitioners (Pty) Ltd. Monthly bookkeeping from a registered South African practice.",
      about)

# ---------------------------------------------------------------- contact
def opts(name, values, required=True, placeholder="Select…"):
    o = f'<option value="">{placeholder}</option>' + "".join(f'<option>{html.escape(v)}</option>' for v in values)
    return f'<select id="f-{name}" name="{name}"{" required" if required else ""}>{o}</select>'

contact = page_head("Free consultation", "Get a bookkeeping quote",
    "Answer a few quick questions and we will recommend a package and quote a fixed monthly fee. No obligation.") + f"""
<section><div class="wrap grid contact-grid">
<div>
<form id="enquiry" class="form" action="/contact.php" method="post" novalidate>
<div class="row">
<div><label for="f-name">Your name *</label><input id="f-name" name="name" autocomplete="name" required maxlength="120"></div>
<div><label for="f-business">Business name</label><input id="f-business" name="business" autocomplete="organization" maxlength="160"></div>
</div>
<div class="row">
<div><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required maxlength="160"></div>
<div><label for="f-phone">Phone / WhatsApp *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required maxlength="40"></div>
</div>
<div class="row">
<div><label for="f-entity">Business type *</label>{opts("entity", ["Sole trader", "(Pty) Ltd", "Close corporation (CC)", "Trust", "NPO / NPC", "Partnership", "Not registered yet"])}</div>
<div><label for="f-town">Town or city</label><input id="f-town" name="town" autocomplete="address-level2" maxlength="80"></div>
</div>
<div class="row">
<div><label for="f-volume">Transactions per month *</label>{opts("volume", ["Under 100", "100 to 300", "Over 300", "Not sure"])}</div>
<div><label for="f-accounts">Bank and card accounts</label>{opts("accounts", ["1", "2 to 3", "4 or more"], False)}</div>
</div>
<div class="row">
<div><label for="f-vat">VAT registered?</label>{opts("vat", ["Yes", "No", "Not sure"], False)}</div>
<div><label for="f-staff">Employees on payroll</label>{opts("staff", ["None", "1 to 5", "6 to 20", "21 to 50", "Over 50"], False)}</div>
</div>
<div class="row">
<div><label for="f-status">Are your books up to date? *</label>{opts("status", ["Up to date", "Behind by a few months", "Behind by a year or more", "No books kept yet"])}</div>
<div><label for="f-software">Accounting software used</label><input id="f-software" name="software" maxlength="80" placeholder="e.g. none, spreadsheets, cloud software"></div>
</div>
<div><label for="f-package">Package of interest</label>
<select id="f-package" name="package"><option>Not sure yet</option><option>Starter</option><option>Business</option><option>Business + Payroll</option><option>Clean-up (once-off)</option></select></div>
<div><label for="f-message">Anything else we should know?</label><textarea id="f-message" name="message" maxlength="5000" placeholder="e.g. why you are looking now — a SARS letter, a loan application, growth…"></textarea></div>
<div class="hp" aria-hidden="true"><label for="f-hp">Leave this empty</label><input id="f-hp" name="hp_check" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="ts" value="">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree that Banda Bookkeepers / Think Mybiz may use these details to respond to my enquiry, as set out in the <a href="/privacy/">privacy notice</a>. *</span></label>
<div id="enquiry-err" class="notice err" role="alert" hidden></div>
<div><button class="btn btn-primary" type="submit">Send my enquiry</button></div>
</form>
</div>
<aside>
<div class="card" style="position:sticky;top:96px">
<h3>Prefer to talk?</h3>
<ul class="contact-list" style="margin-top:14px">
<li><b>Call or WhatsApp</b><a href="tel:+{PHONE_INTL}">{PHONE}</a> · <a href="tel:+27721041051">{CELL}</a></li>
<li><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><b>Head office</b>{ADDRESS}</li>
<li><b>Also serving</b>Polokwane · Pretoria &amp; Centurion · Johannesburg &amp; Midrand · remote nationwide</li>
</ul>
<p style="margin:18px 0 0"><a class="btn btn-wa" href="{WA}">Chat on WhatsApp</a></p>
<hr style="border:0;border-top:1px solid var(--rule);margin:22px 0">
<p class="small muted" style="margin:0">Looking for tax returns, VAT submissions, financial statements or help with a SARS letter? <a href="{tmb('contact/')}">Contact Think Mybiz Accountants →</a></p>
</div>
</aside>
</div></section>
"""
write("/contact/", "Free Bookkeeping Consultation & Quote | Banda Bookkeepers",
      "Get a fixed monthly bookkeeping quote. Tell us about your business and we will recommend the right package. Call or WhatsApp 066 210 5631.",
      contact)

# ---------------------------------------------------------------- thank you
thanks = page_head("Enquiry received", "Thank you — we have your enquiry",
    "We will contact you to arrange your free bookkeeping consultation. A confirmation email is on its way.") + f"""
<section><div class="wrap" style="max-width:860px">
<h2>While you wait</h2>
<ul class="checks">
<li>Have your latest bank statement period ready.</li>
<li>Note which accounting software you use, if any.</li>
<li>Please ask us for a secure route before sending identity numbers or full statements.</li>
</ul>
<div class="actions" style="margin-top:24px"><a class="btn btn-primary" href="/bookkeeping-advice/monthly-bookkeeping-checklist/">Read the monthly checklist</a>
<a class="btn btn-outline" href="/">Back to home</a></div>
</div></section>
"""
write("/thank-you/", "Thank You | Banda Bookkeepers", "Your bookkeeping enquiry has been received.", thanks, noindex=True)

# ---------------------------------------------------------------- privacy
privacy = page_head("Privacy", "Privacy notice (POPIA)",
    "How Banda Bookkeepers, part of Think Mybiz Accountants and Tax Practitioners (Pty) Ltd, handles the personal information you send us.") + f"""
<section><div class="wrap article">
<h2>Who is responsible</h2>
<p>The responsible party is Think Mybiz Accountants and Tax Practitioners (Pty) Ltd (CIPC 2021/819201/07), {ADDRESS}. Contact: <a href="mailto:{EMAIL}">{EMAIL}</a>, {PHONE}.</p>
<h2>What we collect through this website</h2>
<p>When you submit the enquiry form we receive the details you enter: your name, email address, phone number, business name and town, and your answers about your business and bookkeeping needs. This website does not use advertising cookies or analytics trackers.</p>
<h2>Why we use it</h2>
<p>Only to respond to your enquiry, prepare a quote and, if you become a client, to provide the services you engage us for. We do not sell your information or use it for marketing without your consent.</p>
<h2>Where it goes</h2>
<p>Form submissions are emailed to the practice mailbox and are not stored on the web server. If you become a client, your records are kept as required by law and our professional obligations.</p>
<h2>Your rights</h2>
<p>You may ask to see, correct or delete the personal information we hold about you, or object to its use, by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>. You may also lodge a complaint with the Information Regulator (South Africa).</p>
</div></section>
"""
write("/privacy/", "Privacy Notice (POPIA) | Banda Bookkeepers",
      "How Banda Bookkeepers and Think Mybiz Accountants handle personal information submitted through bandabookkeepers.com.", privacy)

# ---------------------------------------------------------------- 404
nf = page_head("Page not found", "We could not find that page",
    "The page may have moved. Try one of these instead.") + """
<section><div class="wrap"><div class="actions">
<a class="btn btn-primary" href="/">Home</a><a class="btn btn-outline" href="/services/">Services &amp; packages</a>
<a class="btn btn-outline" href="/bookkeeping-advice/">Bookkeeping advice</a><a class="btn btn-outline" href="/contact/">Contact</a>
</div></div></section>
"""
write("/404/", "Page Not Found | Banda Bookkeepers", "Page not found.", nf, noindex=True)

# ---------------------------------------------------------------- sitemap + robots
urls = [p for p, noidx in PAGES.items() if not noidx]
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for p in urls:
        f.write(f"<url><loc>{SITE}{p}</loc><lastmod>{UPDATED}</lastmod></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\n\nSitemap: {SITE}/sitemap.xml\n")
print("Built", len(PAGES), "pages")
