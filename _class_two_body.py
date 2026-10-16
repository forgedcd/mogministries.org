def _cards(n=13):
    out=[]
    for i in range(1,n+1):
        out.append(f'''            <figure class="honor-card reveal">
              <div class="honor-card__frame">
                <img src="./assets/img/class-two/grad-{i:02d}-600.webp" srcset="./assets/img/class-two/grad-{i:02d}-600.webp 600w, ./assets/img/class-two/grad-{i:02d}-1200.webp 1200w" sizes="(max-width: 640px) 90vw, (max-width: 1100px) 45vw, 30vw" alt="Road to Damascus Class Two graduate with the MOG Ministries team, holding his certificate" width="600" height="800" loading="lazy" decoding="async" />
              </div>
              <figcaption><span class="honor-card__no">No. {i:02d}</span><span class="honor-card__label">RTD Graduate &middot; Class Two</span></figcaption>
            </figure>''')
    return "\n".join(out)

def body():
    return f'''      <section class="grad-hero">
        <div class="grad-hero__inner shell">
          <p class="eyebrow">Road to Damascus &mdash; Class Two</p>
          <h1 class="grad-hero__title">Class Two.<br /><span class="gold-text">Graduated.</span></h1>
          <p class="grad-hero__date">Wednesday &middot; October 14, 2026 &middot; Suwannee Correctional Institution, Florida</p>
        </div>
        <figure class="grad-class shell reveal">
          <div class="grad-class__frame">
            <img src="./assets/img/class-two/class-1000.webp" srcset="./assets/img/class-two/class-1000.webp 1000w, ./assets/img/class-two/class-2000.webp 2000w" sizes="(max-width: 1200px) 94vw, 1180px" alt="The Road to Damascus Class Two graduates holding their certificates in the chapel at Suwannee Correctional Institution, with the MOG Ministries team and Lt. Harris" width="1000" height="462" fetchpriority="high" />
          </div>
          <figcaption>The second graduating class of the RTD Program, certificates in hand. Tap to view full size.</figcaption>
        </figure>
      </section>

      <section class="section" aria-labelledby="honor-title">
        <div class="shell">
          <div class="grad-intro">
            <div>
              <p class="eyebrow">Why we honor them</p>
              <h2 class="h-section reveal" id="honor-title">Twelve weeks.<br />New men.</h2>
            </div>
            <div class="prose reveal">
              <p>For twelve weeks, these men showed up. Week after week, they sat in a prison classroom and did the hard work most people spend a lifetime avoiding: facing what shaped them, getting honest about what they've done, and letting God heal what they could never fix on their own.</p>
              <p>They walked in carrying anger, shame, and years of hurt. They walked out with certificates in their hands, and more importantly, with new hearts.</p>
              <p>We don't celebrate what we taught them. We celebrate what Jesus did in them.</p>
            </div>
          </div>

          <blockquote class="grad-verse reveal">
            <p>&ldquo;Therefore, if anyone is in Christ, he is a new creation. The old has passed away; behold, the new has come.&rdquo;</p>
            <cite>2 Corinthians 5:17</cite>
          </blockquote>
        </div>
      </section>

      <section class="section honor-roll" aria-labelledby="roll-title">
        <div class="shell">
          <div class="honor-roll__head">
            <p class="eyebrow">The honor roll</p>
            <h2 class="h-section reveal" id="roll-title">Every man. Every certificate.</h2>
            <p class="muted mt-8 max-52">Each graduate stood with our team to receive his certificate. Tap any photo to see it full size.</p>
          </div>
          <div class="honor-grid mt-12">
{_cards()}
          </div>
        </div>
      </section>

      <section class="section" aria-labelledby="thanks-title">
        <div class="shell">
          <div class="grad-thanks reveal">
            <p class="eyebrow eyebrow--center">With gratitude</p>
            <h2 class="h-section" id="thanks-title">To Lt. Harris and the staff of Suwannee CI.</h2>
            <p>None of this happens without the leaders who open the doors. Thank you for believing these men deserve a real shot at healing and a real relationship with Jesus Christ.</p>
          </div>
        </div>
      </section>

      <section class="cta-band">
        <div class="cta-band__inner reveal">
          <p class="eyebrow eyebrow--center">Philippians 1:6</p>
          <h2 class="h-section">He who began a good work in you will carry it on to completion.</h2>
          <p class="muted mt-8" style="max-width:52ch;margin-inline:auto">Graduation isn't the finish line. It's the first page of what God is writing next.</p>
          <div class="btn-row mt-10" style="justify-content: center">
            <a class="btn btn--gold btn--lg" href="./testimony.html">Read a Testimony From Behind the Walls</a>
            <a class="btn btn--outline btn--lg" href="./index.html#rtd-title">About the RTD Program</a>
          </div>
        </div>
      </section>
'''
