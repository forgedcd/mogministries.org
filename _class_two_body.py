def _cards(n=13):
    out=[]
    for i in range(1,n+1):
        out.append(f'''            <figure class="honor-card reveal">
              <div class="honor-card__frame">
                <img src="./assets/img/class-two/grad-{i:02d}-600.webp" srcset="./assets/img/class-two/grad-{i:02d}-600.webp 600w, ./assets/img/class-two/grad-{i:02d}-1200.webp 1200w" sizes="(max-width: 640px) 45vw, (max-width: 1100px) 45vw, 30vw" alt="A Road to Damascus Class Two graduate standing with the MOG Ministries family" width="600" height="800" loading="lazy" decoding="async" />
              </div>
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
            <img src="./assets/img/class-two/class-1000.webp" srcset="./assets/img/class-two/class-1000.webp 1000w, ./assets/img/class-two/class-2000.webp 2000w" sizes="(max-width: 1200px) 94vw, 1180px" alt="The Road to Damascus Class Two graduates together in the chapel at Suwannee Correctional Institution, with the MOG Ministries team and Lt. Harris" width="1000" height="462" fetchpriority="high" />
          </div>
          <figcaption>Brothers. Family. Class Two of the Road to Damascus Program.</figcaption>
        </figure>
      </section>

      <section class="section" aria-labelledby="honor-title">
        <div class="shell">
          <div class="grad-intro">
            <div>
              <p class="eyebrow">Where they started</p>
              <h2 class="h-section reveal" id="honor-title">They came in<br />broken.</h2>
            </div>
            <div class="prose reveal">
              <p>When these men first walked into our classroom, they were broken. Some were still running with gangs. All of them were carrying wounds nobody could see, and most of them felt completely unseen.</p>
              <p>So we started with the message at the heart of everything we teach:</p>
              <p class="grad-pull">God isn&rsquo;t looking to change you. He&rsquo;s looking to love you.</p>
              <p>That&rsquo;s what the Road to Damascus Program is built on: receiving the love of God, and being transformed by the renewing of the mind. The change follows the love. Never the other way around.</p>
            </div>
          </div>

          <blockquote class="grad-verse reveal">
            <p>&ldquo;Do not be conformed to this world, but be transformed by the renewal of your mind.&rdquo;</p>
            <cite>Romans 12:2</cite>
          </blockquote>
        </div>
      </section>

      <section class="section" aria-labelledby="family-title">
        <div class="shell">
          <div class="grad-letter reveal">
            <p class="eyebrow">A word from Frank</p>
            <h2 class="h-section" id="family-title">They became family.</h2>
            <div class="prose mt-10">
              <p>Somewhere along the way, these men stopped being a class. They became family.</p>
              <p>I understand now why Paul wrote his letters the way he did. I understand why, when Paul left, the people wept, embraced him, and kissed him on the cheek as he went. Because that&rsquo;s exactly what graduating these men felt like.</p>
              <p>Josh, the Sullivan family, and I are so proud of each and every one of these men. If we sat down to tell you their stories, we&rsquo;d need about a month straight just to fill you in on everything God did.</p>
            </div>
            <p class="grad-letter__sign">&mdash; Frank Ortega</p>
          </div>

          <blockquote class="grad-verse reveal">
            <p>&ldquo;And there was much weeping on the part of all; they embraced Paul and kissed him.&rdquo;</p>
            <cite>Acts 20:37</cite>
          </blockquote>
        </div>
      </section>

      <section class="section honor-roll" aria-labelledby="roll-title">
        <div class="shell">
          <div class="honor-roll__head">
            <p class="eyebrow">Our brothers</p>
            <h2 class="h-section reveal" id="roll-title">Every one of them seen.<br />Every one of them loved.</h2>
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
          <p class="muted mt-8" style="max-width:52ch;margin-inline:auto">This isn&rsquo;t the end of their story. It&rsquo;s the beginning of what God is writing next.</p>
          <div class="btn-row mt-10" style="justify-content: center">
            <a class="btn btn--gold btn--lg" href="./testimony.html">Read a Testimony From Behind the Walls</a>
            <a class="btn btn--outline btn--lg" href="./vision.html">The 2027 vision</a>
            <a class="btn btn--ghost btn--lg" href="./index.html#rtd-title">About the RTD Program</a>
          </div>
        </div>
      </section>
'''
