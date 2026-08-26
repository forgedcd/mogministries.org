#!/usr/bin/env python3
"""Generate the interior pages of the MOG Ministries site from a shared shell."""
import pathlib

ROOT = pathlib.Path(__file__).parent

GIVING = "https://mog-ministries-518429.churchcenter.com/giving"
GIVING_BOOKS = "https://mog-ministries-518429.churchcenter.com/giving/to/books"
LOGIN = "https://mog-ministries-518429.churchcenter.com/login"
SPOTIFY = "https://open.spotify.com/show/6ksbkht4V8t94FUHcdaVnK"
CC = "https://mog-ministries-518429.churchcenter.com"
SHOP = "https://menofgodshop.bigcartel.com/"
AMZ_REAL = "https://www.amazon.com/Real-Prayer-B-S-Guide-Powerful/dp/B0FHQPR7SX/"
AMZ_FATHER = "https://www.amazon.com/Father-Wounds-Steps-Heal-Relationship/dp/B0DWRJ88T7/"
AMZ_UNFOR = "https://www.amazon.com/unForgiveness-Forgive-When-They-Deserve/dp/B0FV3M7MX8/"

NAV = [
    ("index.html", "Home"),
    ("audio-books.html", "Audio Books"),
    ("give.html", "Give"),
    ("merch.html", "MOG Merch"),
]

HEAD = """<!doctype html>
<html lang="en" data-theme="dark">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content="{desc}" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:image" content="./assets/img/{og}" />
    <meta property="og:type" content="website" />
    <link rel="icon" href="./assets/img/mog-shield.png" />
    <link rel="preconnect" href="https://api.fontshare.com" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://api.fontshare.com/v2/css?f[]=clash-display@500,600&f[]=satoshi@400,500,700&display=swap" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="./base.css" />
    <link rel="stylesheet" href="./style.css" />
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>

    <header class="site-header">
      <div class="header-inner">
        <a class="brand" href="./index.html" aria-label="MOG Ministries — home">
          <img src="./assets/img/mog-logo.png" alt="MOG Ministries" width="1400" height="411" />
        </a>
        <nav class="nav" id="primary-nav" aria-label="Primary">
{navlinks}
          <a href="{login}" target="_blank" rel="noopener noreferrer">Log in</a>
        </nav>
        <div class="header-actions">
          <button class="icon-btn" type="button" data-theme-toggle aria-label="Switch colour theme"></button>
          <button class="icon-btn nav-toggle" type="button" data-nav-toggle aria-controls="primary-nav" aria-expanded="false" aria-label="Open menu"></button>
        </div>
      </div>
    </header>

    <main id="main">
"""

FOOTER = """    </main>

    <footer class="site-footer">
      <div class="shell">
        <div class="footer-top">
          <div class="footer-brand">
            <img src="./assets/img/mog-logo.png" alt="MOG Ministries" width="1400" height="411" />
            <p>
              Ministering to the heart of God by going out to the least of these. Prisons. Jails.
              The overlooked. The youth of this generation.
            </p>
          </div>
          <div class="footer-col">
            <h2>Explore</h2>
            <ul role="list">
              <li><a href="./index.html">Home</a></li>
              <li><a href="./audio-books.html">Audio Books</a></li>
              <li><a href="./give.html">Give</a></li>
              <li><a href="./merch.html">MOG Merch</a></li>
              <li><a href="./sow.html">Sow a Seed</a></li>
            </ul>
          </div>
          <div class="footer-col">
            <h2>Connect</h2>
            <ul role="list">
              <li><a href="mailto:Support@mogministries.org">Support@mogministries.org</a></li>
              <li><a href="tel:9723694638">972-369-4638</a></li>
              <li><a href="{giving}" target="_blank" rel="noopener noreferrer">Give Now</a></li>
              <li><a href="{login}" target="_blank" rel="noopener noreferrer">Log in</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <span>© 2026 MOG Ministries</span>
          <a href="https://planning.center/terms/" target="_blank" rel="noopener noreferrer">Terms of Service</a>
          <a href="https://planning.center/privacy/" target="_blank" rel="noopener noreferrer">Privacy Policy</a>
          <span class="spacer">Matthew 25:40</span>
        </div>
      </div>
    </footer>

    <script src="./app.js" defer></script>
  </body>
</html>
""".replace("{giving}", GIVING).replace("{login}", LOGIN)


def pagehead(img, alt, w, h, eyebrow, title, sub="", actions=""):
    sub_html = f'\n          <p class="hero__sub">{sub}</p>' if sub else ""
    act_html = f'\n          <div class="btn-row mt-10">{actions}</div>' if actions else ""
    return f"""      <section class="pagehead">
        <div class="pagehead__media">
          <img src="./assets/img/{img}" alt="{alt}" width="{w}" height="{h}" fetchpriority="high" />
        </div>
        <div class="hero__bars" aria-hidden="true"></div>
        <div class="pagehead__inner">
          <p class="eyebrow">{eyebrow}</p>
          <h1>{title}</h1>{sub_html}{act_html}
        </div>
      </section>
"""


def build(slug, title, desc, og, body):
    navlinks = "\n".join(
        '          <a href="./{h}"{cur}>{lbl}</a>'.format(
            h=h, lbl=lbl, cur=' aria-current="page"' if h == slug else ""
        )
        for h, lbl in NAV
    )
    html = (
        HEAD.format(title=title, desc=desc, og=og, navlinks=navlinks, login=LOGIN)
        + body
        + FOOTER
    )
    (ROOT / slug).write_text(html, encoding="utf-8")
    print("wrote", slug, len(html))


# ==========================================================================
# GIVE
# ==========================================================================
give_body = pagehead(
    "yard-teaching-1600.webp",
    "Frank Ortega teaching a group of young men seated under a pavilion in a prison yard",
    1600,
    894,
    "Give — Partnership",
    'Hope <span class="gold-text">Dealers</span>',
    "This is the Hope Dealers Partnership Program. ($87 Monthly)",
) + f"""
      <section class="section bars-motif" aria-labelledby="hd-title">
        <div class="shell">
          <div class="split split--wide-left">
            <div>
              <p class="eyebrow">01 — The invitation</p>
              <h2 class="h-section reveal" id="hd-title">
                You're not just supporting a ministry — you're stepping into an identity.
              </h2>
              <div class="prose mt-10 reveal">
                <p>
                  When you partner with M.O.G., you're not just supporting a ministry— you're
                  stepping into an identity.
                </p>
                <p>
                  You become a <strong>Hope Dealer</strong> — bringing the light of Jesus into places
                  most people avoid.
                </p>
                <ul class="stack-lines" role="list">
                  <li>This isn't for passive believers.</li>
                </ul>
                <p>
                  This is for those who refuse to sit back and wait— who want to take the Gospel into
                  prisons, jails, and broken places where it's needed most.
                </p>
                <p>
                  If you care more about souls than comfort… if you believe the church should be
                  sent, not sheltered… this is for you.
                </p>
                <p>
                  Jesus made it clear: when we serve "the least of these," we're serving Him
                  (Matthew 25:40).
                </p>
                <p>This is the mission of M.O.G.</p>
              </div>
              <div class="btn-row mt-10 reveal">
                <a class="btn btn--gold btn--lg" href="{GIVING}" target="_blank" rel="noopener noreferrer">Partner Now</a>
              </div>
            </div>
            <figure class="split__media reveal">
              <img src="./assets/img/chapel-group-800.webp" alt="A chapel filled with incarcerated men gathered after a MOG Ministries service" width="800" height="353" loading="lazy" decoding="async" />
              <span class="bracket-frame" aria-hidden="true"></span>
              <figcaption>$87 monthly. One steady yes.</figcaption>
            </figure>
          </div>
        </div>
      </section>

      <section class="section section--panel" aria-labelledby="incl-title">
        <div class="shell">
          <p class="eyebrow">02 — What partnership does</p>
          <h2 class="h-section reveal" id="incl-title">Real transformation—inside prisons and beyond</h2>
          <div class="grid grid--3 mt-12">
            <article class="card card--cut reveal">
              <h3 class="h-card">A free Hope Dealers tee</h3>
              <p>
                When you become a monthly partner, you're helping bring real transformation—inside
                prisons and beyond. As a thank you, you'll receive a free official Hope Dealers
                t-shirt.
              </p>
            </article>
            <article class="card card--cut reveal">
              <h3 class="h-card">Check your email</h3>
              <p>
                After setting up your recurring gift, be sure to check your email (and spam) to fill
                out the form.
              </p>
            </article>
            <article class="card card--cut reveal">
              <h3 class="h-card">The weekly Post-Prison call</h3>
              <p>
                We're also launching a weekly Post-Prison call—where you'll have access to connect
                with men we've ministered to, help pour into them, and hear powerful testimonies as
                they stay free and walk with Jesus.
              </p>
            </article>
          </div>
          <div class="bigline mt-12 reveal">
            <p>This is more than donating.</p>
            <p class="gold-text">This is impact. This is Kingdom work.</p>
          </div>
        </div>
      </section>

      <section class="section" aria-labelledby="heart-title">
        <div class="shell">
          <div class="split split--wide-right">
            <figure class="split__media reveal">
              <img src="./assets/img/yard-circle-800.webp" alt="Ministry team praying with a circle of young men in a prison yard" width="800" height="480" loading="lazy" decoding="async" />
              <span class="bracket-frame" aria-hidden="true"></span>
              <figcaption>Men like Josh and Guy.</figcaption>
            </figure>
            <div>
              <p class="eyebrow">03 — Our heart</p>
              <h2 class="h-section reveal" id="heart-title">People matter—especially the ones the world has written off</h2>
              <div class="prose mt-10 reveal">
                <p>
                  M.O.G. Ministries exists because people matter—especially the ones the world has
                  written off. This vision was forged through real relationships with men living
                  behind concrete walls and steel gates. Men like Josh and Guy—men God raised up
                  where most people only saw failure.
                </p>
                <p>
                  We do not go behind the walls to run events or play church. We show up
                  consistently, speak truth, meet practical needs, and walk with men long enough to
                  see real transformation take root.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--panel" aria-labelledby="b2026-title">
        <div class="shell">
          <p class="eyebrow">04 — The build</p>
          <h2 class="h-section reveal" id="b2026-title">What we are building in 2026</h2>
          <div class="ledger mt-12">
            <article class="ledger__row reveal">
              <p class="ledger__stat">01</p>
              <h3 class="ledger__title">Consistent Presence</h3>
              <p class="ledger__desc">
                We are committed to returning to the same facilities consistently—building trust,
                accountability, and discipleship over time.
              </p>
            </article>
            <article class="ledger__row reveal">
              <p class="ledger__stat">02</p>
              <h3 class="ledger__title">Discipleship &amp; Identity</h3>
              <p class="ledger__desc">
                Through in-person ministry inside facilities, we will disciple men in identity,
                leadership, prayer, generosity, responsibility, and vision.
              </p>
            </article>
            <article class="ledger__row reveal">
              <p class="ledger__stat">03</p>
              <h3 class="ledger__title">Meeting Practical Needs</h3>
              <p class="ledger__desc">
                Where approved, we will feed inmates, give away discipleship resources, and create
                space for baptisms. Generosity is not a tactic—it is the Gospel in action.
              </p>
            </article>
          </div>
        </div>
      </section>

      <section class="section" aria-labelledby="goal-title">
        <div class="shell">
          <p class="eyebrow">04 — The end goal</p>
          <h2 class="h-section reveal" id="goal-title">Not behavior modification. Heart transformation.</h2>
          <div class="prose mt-10 reveal">
            <p>
              Our goal is not behavior modification—it is heart transformation. Even men serving life
              sentences still carry purpose, influence, and the ability to change their family's
              future.
            </p>
            <p>
              We believe prisons can become mission fields and leadership training grounds. Hope does
              not stop at a sentence, a gate, or a wall.
            </p>
          </div>
        </div>
      </section>

      <section class="cta-band">
        <div class="cta-band__inner reveal">
          <p class="eyebrow eyebrow--center">1,000 in 2026</p>
          <h2 class="h-section">We're believing for 1,000 monthly Hope Dealers in 2026.</h2>
          <p class="lede muted mt-8">Let's reach them together.</p>
          <div class="btn-row mt-10" style="justify-content: center">
            <a class="btn btn--gold btn--lg" href="{GIVING}" target="_blank" rel="noopener noreferrer">Partner Now</a>
            <a class="btn btn--outline btn--lg" href="./sow.html">Other ways to sow</a>
          </div>
        </div>
      </section>
"""

# ==========================================================================
# SOW
# ==========================================================================
sow_body = pagehead(
    "baptism-water-1600.webp",
    "Frank Ortega baptizing an inmate inside a prison chapel baptistry",
    1600,
    2133,
    "Sow a Seed",
    'Sow into <span class="gold-text">M.O.G.</span> Ministries',
    "Three Ways to Sow Into the Least of These",
) + f"""
      <section class="section section--flush-top bars-motif">
        <div class="shell">
          <div class="stack-lines stack-lines--lg reveal" role="list">
            <p role="listitem">We don't wait for the darkness to come to us.</p>
            <p role="listitem">We take the light of Jesus into dark places.</p>
            <p role="listitem">Prisons. Jails. The overlooked. The youth of this generation.</p>
            <p role="listitem">This is where we go.</p>
          </div>
          <p class="lede mt-10 reveal">
            And when you give, you're not just "supporting." You're helping us deal hope to the
            hopeless.
          </p>
        </div>
      </section>

      <section class="section" aria-labelledby="sow1-title">
        <div class="shell">
          <div class="split split--wide-left">
            <div>
              <p class="eyebrow">01 — The Hope Dealers Partners Program</p>
              <h2 class="h-section reveal" id="sow1-title">Not a one-time moment. A steady yes.</h2>
              <div class="prose mt-10 reveal">
                <p>This is for the person who wants to be consistent.</p>
                <p>
                  When you become a Partner, you're joining the mission in a real way. Your monthly
                  partnership helps us keep showing up behind the walls and in discipleship
                  follow-ups.
                </p>
                <p>
                  This isn't about building a platform. It's about taking Jesus where He's taken the
                  least and needed the most.
                </p>
              </div>
              <div class="btn-row mt-10 reveal">
                <a class="btn btn--gold" href="./give.html">Join Partners Program</a>
              </div>
            </div>
            <div class="reveal">
              <p class="eyebrow">Promises you can read for yourself</p>
              <div class="stack-8 mt-8">
                <blockquote class="scripture">
                  <p>
                    "Truly, I say to you, as you did it to one of the least of these my brothers, you
                    did it to me."
                  </p>
                  <cite>Matthew 25:40</cite>
                </blockquote>
                <blockquote class="scripture">
                  <p>
                    "Whoever is generous to the poor lends to the Lord, and he will repay him for his
                    deed."
                  </p>
                  <cite>Proverbs 19:17</cite>
                </blockquote>
                <blockquote class="scripture">
                  <p>
                    "If you pour yourself out for the hungry and satisfy the desire of the afflicted,
                    then shall your light rise in the darkness… and the Lord will guide you
                    continually…"
                  </p>
                  <cite>Isaiah 58:10–11</cite>
                </blockquote>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--panel" aria-labelledby="sow2-title">
        <div class="shell">
          <p class="eyebrow">02 — Sow a Book</p>
          <h2 class="h-section reveal" id="sow2-title">Put a book in an inmate's hands</h2>
          <div class="split split--wide-left mt-12">
            <div class="prose reveal">
              <p>
                This is for the person who says, "I don't just want to give. I want to KNOW an inmate
                is holding what I sow."
              </p>
              <p>
                When you sow a book, you're covering the print cost of one of Frank Ortega's titles —
                <em>Father Wounds</em>, <em>Real Prayer</em>, or <em>unForgiveness</em> — and putting
                it directly into the hands of a man behind the walls. Free to him. Purchased by you.
              </p>
              <p>Here's the simple math:</p>
              <div class="bigline"><p class="gold-text">$11 = 1 book sown.</p></div>
              <p>That $11 covers printing AND getting the book distributed inside the facility.</p>
              <p>
                It's about half the Amazon retail price. And when you give, choose the
                <strong>“Books”</strong> designation — not general giving — so every dollar goes
                straight to book distribution.
              </p>
              <div class="btn-row mt-10">
                <a class="btn btn--gold btn--lg" href="{GIVING_BOOKS}" target="_blank" rel="noopener noreferrer">Sow a Book</a>
              </div>
            </div>
            <div class="reveal">
              <p class="eyebrow">Books going into inmates' hands</p>
              <ol class="book-list mt-8" role="list">
                <li class="book-row">
                  <span class="book-row__no">01</span>
                  <a class="book-row__title" href="{AMZ_FATHER}" target="_blank" rel="noopener noreferrer">
                    Father Wounds <span>8 Steps to Heal Your Relationship with your Dad</span>
                  </a>
                </li>
                <li class="book-row">
                  <span class="book-row__no">02</span>
                  <a class="book-row__title" href="{AMZ_REAL}" target="_blank" rel="noopener noreferrer">
                    Real Prayer <span>A No B.S Guide to a Powerful Prayer Life</span>
                  </a>
                </li>
                <li class="book-row">
                  <span class="book-row__no">03</span>
                  <a class="book-row__title" href="{AMZ_UNFOR}" target="_blank" rel="noopener noreferrer">
                    unForgiveness <span>How to Forgive When They Don't Deserve It</span>
                  </a>
                </li>
              </ol>
              <figure class="mt-12">
                <img
                  src="./assets/img/chapel-teaching-800.webp"
                  srcset="./assets/img/chapel-teaching-800.webp 800w, ./assets/img/chapel-teaching-1600.webp 1600w"
                  sizes="(max-width: 900px) 100vw, 40vw"
                  alt="Frank Ortega teaching from a pulpit inside a Florida prison chapel filled with inmates in blue uniforms"
                  width="800"
                  height="1066"
                  loading="lazy"
                  decoding="async"
                />
              </figure>
            </div>
          </div>
        </div>
      </section>

      <section class="section" aria-labelledby="sow3-title">
        <div class="shell">
          <p class="eyebrow">03 — General Sowing</p>
          <h2 class="h-section reveal" id="sow3-title">Fuel the mission wherever it's needed most</h2>
          <div class="prose mt-10 reveal">
            <p>
              General sowing is for the person who simply wants to say, "Put my seed wherever the
              need is greatest right now."
            </p>
            <p>This helps us stay flexible and respond in real time to what's in front of us.</p>
            <p>This is the kind of giving that keeps the whole engine running.</p>
          </div>
        </div>
      </section>

      <section class="section section--panel" aria-labelledby="sowdoes-title">
        <div class="shell">
          <p class="eyebrow">04 — What your giving does</p>
          <h2 class="h-section reveal" id="sowdoes-title">
            Whether you partner, sow books, or give generally, your giving helps us:
          </h2>
          <ul class="checklist mt-12 grid grid--2" role="list">
            <li class="reveal">Bring hope to inmates behind the walls</li>
            <li class="reveal">Put free physical books — <em>Father Wounds</em>, <em>Real Prayer</em>, <em>unForgiveness</em> — into inmates' hands</li>
            <li class="reveal">Reach the youth of this generation with engaging, Scripture-rooted content</li>
            <li class="reveal">Fund the RTD (Road to Damascus) 12-week discipleship program inside the walls</li>
            <li class="reveal">Sow back into the places and organizations we minister with</li>
          </ul>
          <div class="btn-row mt-12 reveal">
            <a class="btn btn--gold btn--lg" href="{GIVING}" target="_blank" rel="noopener noreferrer">Give Here</a>
          </div>
        </div>
      </section>
"""

# ==========================================================================
# AUDIO BOOKS
# ==========================================================================
ab_body = pagehead(
    "tex-bars.webp",
    "Gold light falling through the bars of a cell window onto a concrete wall",
    1024,
    1536,
    "Audio Books — January 3–16, 2026",
    "Audio <span class=\"gold-text\">Books</span>",
    "Full-length books, read aloud and released free — enjoy them yourself, then sow a paperback into the hands of a man behind the walls.",
) + f"""
      <section class="section" aria-label="Audio book releases">
        <div class="shell">
          <div class="grid grid--2">
            <article class="card card--cut reveal">
              <p class="media-card__date">February 2, 2026 · Audio Books</p>
              <h2 class="h-card">Watch Your Mouth</h2>
              <p>Frank Ortega's Newest Book Release</p>
              <div class="btn-row mt-8">
                <a class="btn btn--gold" href="{CC}/episodes/609323" target="_blank" rel="noopener noreferrer">Listen</a>
              </div>
            </article>

            <article class="card card--cut reveal">
              <p class="media-card__date">January 16, 2026 · Audio Books</p>
              <h2 class="h-card">Real Prayer</h2>
              <p>Full Audio Book of "Real Prayer" A no B.S guide to a powerful prayer life.</p>
              <div class="btn-row mt-8">
                <a class="btn btn--gold" href="{CC}/episodes/591502" target="_blank" rel="noopener noreferrer">Listen</a>
                <a class="btn btn--ghost" href="{AMZ_REAL}" target="_blank" rel="noopener noreferrer">Paperback Copy</a>
              </div>
            </article>

            <article class="card card--cut reveal">
              <p class="media-card__date">January 3, 2026 · Audio Books</p>
              <h2 class="h-card">Coming soon…</h2>
              <p>Father Wounds — 8 Steps to Heal Your Relationship with your Dad.</p>
              <div class="btn-row mt-8">
                <a class="btn btn--outline" href="{CC}/episodes/591493" target="_blank" rel="noopener noreferrer">Details</a>
                <a class="btn btn--ghost" href="{AMZ_FATHER}" target="_blank" rel="noopener noreferrer">Paperback Copy</a>
              </div>
            </article>

            <article class="card card--cut reveal">
              <p class="media-card__date">January 3, 2026 · Audio Books</p>
              <h2 class="h-card">Coming soon…</h2>
              <p>unForgiveness — How to Forgive When They Don't Deserve It.</p>
              <div class="btn-row mt-8">
                <a class="btn btn--outline" href="{CC}/episodes/591503" target="_blank" rel="noopener noreferrer">Details</a>
                <a class="btn btn--ghost" href="{AMZ_UNFOR}" target="_blank" rel="noopener noreferrer">Paperback Copy</a>
              </div>
            </article>
          </div>
        </div>
      </section>

      <section class="section section--panel section--tight">
        <div class="shell pullquote reveal">
          <blockquote>$11 = 1 book sown — printed and placed directly into someone's hands.</blockquote>
          <cite>Sowing Books</cite>
        </div>
      </section>

      <section class="cta-band">
        <div class="cta-band__inner reveal">
          <p class="eyebrow eyebrow--center">Put it in their hands</p>
          <h2 class="h-section">Sow a paperback behind the walls</h2>
          <p class="lede muted mt-8">
            Enjoy the audio books yourself, then sow a physical copy of <em>Father Wounds</em>,
            <em>Real Prayer</em>, or <em>unForgiveness</em> into an inmate's hands for $11. Tap Sow
            a Seed and choose the “Books” designation.
          </p>
          <div class="btn-row mt-10" style="justify-content: center">
            <a class="btn btn--gold btn--lg" href="./sow.html">Sow a Book</a>
          </div>
        </div>
      </section>
"""

# ==========================================================================
# PODCAST
# ==========================================================================
pod_body = pagehead(
    "tex-razorwire.webp",
    "Razor wire coiled along the top of a perimeter fence at dusk",
    1983,
    793,
    "MOG Podcast",
    'MOG <span class="gold-text">Podcast</span>',
    "Teaching, prayer and discipleship — released for the church and delivered to inmate tablets behind the walls.",
    actions=f'<a class="btn btn--gold btn--lg" href="{SPOTIFY}" target="_blank" rel="noopener noreferrer">Listen on Spotify</a>',
) + f"""

      <section class="section section--flush-top" aria-labelledby="ep-title">
        <div class="shell">
          <p class="eyebrow">Episodes</p>
          <h2 class="h-section reveal" id="ep-title">Recent from the feed</h2>
          <div class="grid grid--3 mt-12">
            <a class="media-card reveal" href="{CC}/episodes/611551" target="_blank" rel="noopener noreferrer">
              <div class="media-card__art media-card__art--type">
                <span class="media-card__badge">Watch</span>
                <div>
                  <span class="t">Tongues and<br />The Holy Spirit</span>
                  <span class="s">Virtual Discipleship</span>
                </div>
              </div>
              <div class="media-card__body">
                <p class="media-card__date">February 6, 2026 · MOG Teachings</p>
                <h3 class="h-card">Tongues and The Holy Spirit</h3>
                <p>
                  Speaking in tongues in the Bible. Praying in the Spirit vs public tongues. Why
                  spiritual gifts are meant to edify the church. Why chaos is not a sign of the Holy
                  Spirit.
                </p>
              </div>
            </a>
            <a class="media-card reveal" href="{CC}/episodes/613735" target="_blank" rel="noopener noreferrer">
              <div class="media-card__art media-card__art--type">
                <span class="media-card__badge">Pray</span>
                <div>
                  <span class="t">Prayers<br />For Miracles</span>
                  <span class="s">Pray Along With Us</span>
                </div>
              </div>
              <div class="media-card__body">
                <p class="media-card__date">February 13, 2026 · Prayer</p>
                <h3 class="h-card">Prayers For Miracles</h3>
                <p>Financial testimony &amp; desperate prayer.</p>
              </div>
            </a>
            <a class="media-card reveal" href="{CC}/episodes/610964" target="_blank" rel="noopener noreferrer">
              <div class="media-card__art media-card__art--type">
                <span class="media-card__badge">Listen</span>
                <div>
                  <span class="t">Porque Dios<br />No nos escucha</span>
                  <span class="s">Contenido en Español</span>
                </div>
              </div>
              <div class="media-card__body">
                <p class="media-card__date">February 4, 2026 · Animo Para Hoy</p>
                <h3 class="h-card">Porque Dios No nos escucha</h3>
                <p>Programa en español sobre el poder del perdon.</p>
              </div>
            </a>
            <a class="media-card reveal" href="{CC}/episodes/591502" target="_blank" rel="noopener noreferrer">
              <div class="media-card__art media-card__art--type">
                <span class="media-card__badge">Audio Book</span>
                <div>
                  <span class="t">Real<br />Prayer</span>
                  <span class="s">Frank Ortega</span>
                </div>
              </div>
              <div class="media-card__body">
                <p class="media-card__date">January 16, 2026 · Audio Books</p>
                <h3 class="h-card">Real Prayer</h3>
                <p>Full audio book — a no B.S guide to a powerful prayer life.</p>
              </div>
            </a>
            <a class="media-card reveal" href="{CC}/episodes/591493" target="_blank" rel="noopener noreferrer">
              <div class="media-card__art media-card__art--type">
                <span class="media-card__badge">Soon</span>
                <div>
                  <span class="t">Father<br />Wounds</span>
                  <span class="s">Coming soon…</span>
                </div>
              </div>
              <div class="media-card__body">
                <p class="media-card__date">January 3, 2026 · Audio Books</p>
                <h3 class="h-card">Coming soon…</h3>
                <p>8 Steps to Heal Your Relationship with your Dad.</p>
              </div>
            </a>
            <a class="media-card reveal" href="{CC}/episodes/591503" target="_blank" rel="noopener noreferrer">
              <div class="media-card__art media-card__art--type">
                <span class="media-card__badge">Soon</span>
                <div>
                  <span class="t">un<br />Forgiveness</span>
                  <span class="s">Coming soon…</span>
                </div>
              </div>
              <div class="media-card__body">
                <p class="media-card__date">January 3, 2026 · Audio Books</p>
                <h3 class="h-card">Coming soon…</h3>
                <p>How to Forgive When They Don't Deserve It.</p>
              </div>
            </a>
          </div>
        </div>
      </section>

      <section class="section section--panel" aria-labelledby="tab-title">
        <div class="shell">
          <div class="split split--wide-right">
            <figure class="split__media reveal">
              <img src="./assets/img/rtd-graduation-800.webp" alt="RTD program graduates holding certificates of completion inside a prison chapel" width="800" height="527" loading="lazy" decoding="async" />
              <span class="bracket-frame" aria-hidden="true"></span>
              <figcaption>Discipleship that keeps going after we leave.</figcaption>
            </figure>
            <div>
              <p class="eyebrow">On inmate tablets</p>
              <h2 class="h-section reveal" id="tab-title">The Hope Dealers Podcast goes where we can't stay</h2>
              <div class="prose mt-10 reveal">
                <p>
                  Through in-person ministry and the Hope Dealers Podcast delivered to inmate
                  tablets, we will disciple men in identity, leadership, prayer, generosity,
                  responsibility, and vision.
                </p>
              </div>
              <div class="btn-row mt-10 reveal">
                <a class="btn btn--gold" href="{SPOTIFY}" target="_blank" rel="noopener noreferrer">Listen on Spotify</a>
                <a class="btn btn--ghost" href="./give.html">Help fund it</a>
              </div>
            </div>
          </div>
        </div>
      </section>
"""

# ==========================================================================
# MERCH
# ==========================================================================
merch_body = pagehead(
    "baptism-certs-1600.webp",
    "Men in blue prison uniforms holding up certificates of baptism",
    1600,
    856,
    "MOG Merch",
    'MOG Merch <span class="gold-text">Available Now</span>',
    "All Proceeds go to Prison Ministry",
    actions=f'<a class="btn btn--gold btn--lg" href="{SHOP}" target="_blank" rel="noopener noreferrer">Shop Now</a>',
) + f"""

      <section class="section bars-motif" aria-labelledby="tee-title">
        <div class="shell">
          <div class="split split--wide-right">
            <div class="reveal">
              <div class="tee">
                <div>
                  <span class="tee__shield" aria-hidden="true">
                    <img src="./assets/img/mog-shield.png" alt="" width="120" height="120" />
                  </span>
                  <span class="tee__mark">
                    <span class="l1">Hope</span>
                    <span class="l2 gold-text">Dealer</span>
                  </span>
                  <span class="tee__sub">M.O.G. Ministries · Monthly Partners</span>
                </div>
              </div>
            </div>
            <div>
              <p class="eyebrow">Partners only</p>
              <h2 class="h-section reveal" id="tee-title">The Official HOPE DEALER T-Shirt</h2>
              <div class="prose mt-10 reveal">
                <p>This Shirt is Exclusive for our Monthly Supporters Only.</p>
                <p>
                  Join the Hope Dealers Partner's Program to receive your Hope Dealer T-Shirt.
                </p>
              </div>
              <div class="btn-row mt-10 reveal">
                <a class="btn btn--gold btn--lg" href="./give.html">Partner With Us Here</a>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--tight" aria-label="Photos from the field">
        <div class="strip">
          <figure>
            <img src="./assets/img/yard-circle-800.webp" alt="Ministry team praying with a circle of young men in a prison yard" width="800" height="480" loading="lazy" decoding="async" />
          </figure>
          <figure>
            <img src="./assets/img/yard-teaching-800.webp" alt="Frank Ortega teaching a group of young men seated under a pavilion in a prison yard" width="800" height="447" loading="lazy" decoding="async" />
          </figure>
          <figure>
            <img src="./assets/img/chapel-group-800.webp" alt="A chapel filled with incarcerated men gathered after a MOG Ministries service" width="800" height="353" loading="lazy" decoding="async" />
          </figure>
          <figure>
            <img src="./assets/img/rtd-graduation-800.webp" alt="RTD program graduates holding certificates of completion" width="800" height="527" loading="lazy" decoding="async" />
          </figure>
        </div>
      </section>

      <section class="cta-band">
        <div class="cta-band__inner reveal">
          <p class="eyebrow eyebrow--center">Every dollar goes out</p>
          <h2 class="h-section">All Proceeds go to Prison Ministry</h2>
          <div class="btn-row mt-10" style="justify-content: center">
            <a class="btn btn--gold btn--lg" href="{SHOP}" target="_blank" rel="noopener noreferrer">Shop Now</a>
            <a class="btn btn--outline btn--lg" href="./give.html">Partner With Us Here</a>
          </div>
        </div>
      </section>
"""

build(
    "give.html",
    "Give — Hope Dealers Partnership | MOG Ministries",
    "Become a Hope Dealer. $87 monthly partnership funding prison ministry, discipleship and practical needs behind the walls.",
    "yard-teaching-1600.webp",
    give_body,
)
build(
    "sow.html",
    "Sow a Seed | MOG Ministries",
    "Three ways to sow into the least of these: the Hope Dealers Partners Program, sowing books at $11 each, or general sowing.",
    "yard-circle-1600.webp",
    sow_body,
)
build(
    "audio-books.html",
    "Audio Books | MOG Ministries",
    "Free full-length audio books from MOG Ministries: Watch Your Mouth, Real Prayer, Father Wounds and unForgiveness.",
    "tex-bars.webp",
    ab_body,
)
build(
    "merch.html",
    "MOG Merch | MOG Ministries",
    "MOG Merch available now. All proceeds go to prison ministry. The official Hope Dealer t-shirt is exclusive to monthly partners.",
    "baptism-certs-1600.webp",
    merch_body,
)
