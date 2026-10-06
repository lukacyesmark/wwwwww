/* wwwwww.cz — bez knihoven, bez závislostí */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(pointer: fine)').matches;
  window.dataLayer = window.dataLayer || [];
  const track = (event, data = {}) => window.dataLayer.push({ event, ...data });

  /* ---------- header, menu, mobile bar ---------- */
  const header = $('.header');
  const mbar = $('#mbar');
  const hero = $('.hero, .phero');
  const onScroll = () => {
    const y = scrollY;
    header && header.classList.toggle('is-scrolled', y > 10);
    if (mbar) {
      const limit = hero ? hero.offsetHeight * 0.6 : 300;
      const nearForm = $('#poptavka') && $('#poptavka').getBoundingClientRect().top < innerHeight * 0.8;
      mbar.classList.toggle('is-on', y > limit && !nearForm);
    }
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const burger = $('.burger');
  if (burger) {
    const setMenu = (open) => {
      document.body.classList.toggle('menu-open', open);
      burger.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    };
    burger.addEventListener('click', () => setMenu(!document.body.classList.contains('menu-open')));
    $$('.nav a').forEach(a => a.addEventListener('click', () => setMenu(false)));
    addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
  }

  /* ---------- reveal on scroll ---------- */
  const rvEls = $$('.rv, .step');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rvEls.forEach(el => io.observe(el));
  } else rvEls.forEach(el => el.classList.add('is-in'));

  /* ---------- hero canvas: signal of w-waves ---------- */
  const cv = $('#wave');
  if (cv) {
    const ctx = cv.getContext('2d');
    let w, h, dpr, t = 0, raf = 0, visible = true;
    const mouse = { x: -9999, y: -9999, tx: -9999, ty: -9999 };
    const LINES = 9;
    const resize = () => {
      dpr = Math.min(devicePixelRatio || 1, 2);
      w = cv.clientWidth; h = cv.clientHeight;
      cv.width = w * dpr; cv.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    const draw = () => {
      ctx.clearRect(0, 0, w, h);
      mouse.x += (mouse.tx - mouse.x) * 0.08;
      mouse.y += (mouse.ty - mouse.y) * 0.08;
      const step = Math.max(26, w / 46);
      for (let i = 0; i < LINES; i++) {
        const baseY = h * (0.18 + i * 0.085);
        const isAccent = i === 5;
        ctx.beginPath();
        let k = 0;
        for (let x = -step; x <= w + step; x += step / 4, k++) {
          // W-tvar: horní, dolní, střední, dolní …
          const phase = k % 4;
          const shape = phase === 0 ? -1 : phase === 2 ? -0.35 : 1;
          const env = Math.sin(x * 0.004 + t * 0.6 + i * 0.7) * 0.5 + 0.5;
          const dx = x - mouse.x, dy = baseY - mouse.y;
          const near = Math.exp(-(dx * dx + dy * dy) / 26000);
          const amp = 2 + env * 7 + near * 34;
          const y = baseY + shape * amp + Math.sin(x * 0.002 + t * 0.3 + i) * 10;
          k === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.lineJoin = 'round';
        ctx.lineWidth = isAccent ? 1.6 : 1;
        ctx.strokeStyle = isAccent ? 'rgba(200,255,0,.75)' : `rgba(242,242,242,${0.05 + (i % 3) * 0.025})`;
        ctx.stroke();
      }
      t += 0.012;
      if (!reduce && visible) raf = requestAnimationFrame(draw);
    };
    resize();
    addEventListener('resize', () => { resize(); if (reduce) draw(); });
    if (fine) addEventListener('pointermove', e => {
      const r = cv.getBoundingClientRect();
      mouse.tx = e.clientX - r.left; mouse.ty = e.clientY - r.top;
    }, { passive: true });
    new IntersectionObserver(([en]) => {
      visible = en.isIntersecting;
      cancelAnimationFrame(raf);
      if (visible) draw();
    }).observe(cv);
  }

  /* ---------- scramble words ---------- */
  const scr = $('.scramble');
  if (scr && !reduce) {
    const words = scr.dataset.words.split('|');
    const chars = 'wWvV/\\_-<>01';
    let wi = 0;
    const swap = () => {
      const from = scr.textContent, to = words[(wi = (wi + 1) % words.length)];
      const len = Math.max(from.length, to.length);
      let f = 0;
      const tick = () => {
        let out = '';
        for (let i = 0; i < len; i++) {
          const reveal = f / 1.6 - i;
          out += reveal > 1 ? (to[i] || '') : reveal > 0 ? chars[(Math.random() * chars.length) | 0] : (from[i] || '');
        }
        scr.textContent = out;
        if (f++ < len * 1.6 + 2) requestAnimationFrame(tick); else scr.textContent = to;
      };
      tick();
    };
    setInterval(() => { if (!document.hidden) swap(); }, 2800);
  }

  /* ---------- live page metrics + terminal ---------- */
  const measure = () => {
    const nav = performance.getEntriesByType('navigation')[0];
    const res = performance.getEntriesByType('resource');
    let load = nav ? (nav.loadEventEnd || nav.domContentLoadedEventEnd) : performance.now();
    let bytes = 0;
    [nav, ...res].forEach(r => { if (r) bytes += r.transferSize || r.encodedBodySize || 0; });
    return { load: Math.max(1, Math.round(load)), kb: Math.max(1, Math.round(bytes / 1024)), req: res.length + 1 };
  };
  const countUp = (el, to) => {
    if (!el) return;
    if (reduce) { el.textContent = to; return; }
    const t0 = performance.now(), dur = 1100;
    const f = now => {
      const p = Math.min(1, (now - t0) / dur);
      el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(f);
    };
    requestAnimationFrame(f);
  };
  const runTerm = (m) => {
    countUp($('#s-load'), m.load);
    countUp($('#s-weight'), m.kb);
    const term = $('#term');
    if (!term) return;
    const lines = [
      `<span class="c">// výsledky z vašeho prohlížeče</span>`,
      `načtení stránky <span class="v">${m.load} ms</span> <span class="ok">✓</span>`,
      `váha stránky &nbsp;&nbsp;<span class="v">${m.kb} kB</span> <span class="ok">✓</span>`,
      `požadavky &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="v">${m.req}</span> <span class="ok">✓</span>`,
      `jQuery, pluginy <span class="v">0</span> <span class="ok">✓</span>`,
      `lokální SEO &nbsp;&nbsp;&nbsp;<span class="v">Jeseník</span> <span class="ok">✓</span>`,
      `<span class="p">❯</span> <span class="v">váš web může být další</span> <span class="cursor"></span>`
    ];
    let i = 0;
    const next = () => {
      if (i >= lines.length) return;
      const d = document.createElement('div');
      d.innerHTML = lines[i++];
      const last = term.querySelector('.cursor'); if (last) last.remove();
      term.appendChild(d);
      setTimeout(next, reduce ? 0 : 260);
    };
    setTimeout(next, reduce ? 0 : 500);
  };
  const startMetrics = () => setTimeout(() => runTerm(measure()), 60);
  if (document.readyState === 'complete') startMetrics(); else addEventListener('load', startMetrics);

  /* ---------- card spotlight ---------- */
  if (fine) $$('.card').forEach(c => c.addEventListener('pointermove', e => {
    const r = c.getBoundingClientRect();
    c.style.setProperty('--mx', `${e.clientX - r.left}px`);
    c.style.setProperty('--my', `${e.clientY - r.top}px`);
  }));

  /* ---------- magnetic accent buttons ---------- */
  if (fine && !reduce) $$('.btn--accent').forEach(b => {
    b.addEventListener('pointermove', e => {
      const r = b.getBoundingClientRect();
      b.style.setProperty('--bx', `${(e.clientX - r.left - r.width / 2) * 0.18}px`);
      b.style.setProperty('--by', `${(e.clientY - r.top - r.height / 2) * 0.28}px`);
    });
    b.addEventListener('pointerleave', () => { b.style.setProperty('--bx', '0px'); b.style.setProperty('--by', '0px'); });
  });

  /* ---------- configurator ---------- */
  const cfg = $('#cfg');
  const brief = $('#cfg-brief');
  let briefText = '';
  if (cfg && brief) {
    const pages = $('#c-pages'), pagesOut = $('#c-pages-out');
    const update = () => {
      const type = (cfg.querySelector('[name=c-type]:checked') || {}).value || '';
      const field = (cfg.querySelector('[name=c-field]:checked') || {}).value || '';
      const extras = $$('[name=c-extra]:checked', cfg).map(i => i.value);
      const n = +pages.value;
      pagesOut.textContent = n === 20 ? '20+' : n;
      const pg = n === 1 ? '1 stránka' : n < 5 ? `${n} stránky` : `${n === 20 ? '20+' : n} stránek`;
      briefText = `Typ: ${type}\nObor: ${field}\nRozsah: ${pg}\nNavíc: ${extras.length ? extras.join(', ') : '—'}`;
      brief.innerHTML = briefText.split('\n').map(l => { const [k, ...v] = l.split(': '); return `<b>${k}:</b> ${v.join(': ')}`; }).join('\n');
    };
    cfg.addEventListener('input', update);
    update();
    $('#cfg-send').addEventListener('click', () => {
      const msg = $('#f-msg');
      if (msg) {
        msg.value = `Dobrý den, posílám zadání z konfigurátoru:\n\n${briefText}\n\n`;
        const type = (cfg.querySelector('[name=c-type]:checked') || {}).value;
        const map = { 'Nový web': 'Nový web', 'Redesign webu': 'Redesign', 'E-shop': 'E-shop', 'Landing page': 'Nový web' };
        $$('[name="interest[]"]').forEach(i => { i.checked = i.value === map[type] || (i.value === 'SEO' && /SEO/.test(briefText)) || (i.value === 'Správa webu' && /Správa/.test(briefText)); });
        setTimeout(() => { msg.focus({ preventScroll: true }); msg.setSelectionRange(msg.value.length, msg.value.length); }, 700);
      }
      track('configurator_send');
    });
  }

  /* ---------- attribution (first touch UTM + referrer) ---------- */
  let attribution = '';
  try {
    const p = new URLSearchParams(location.search);
    const utm = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'fbclid'].filter(k => p.get(k)).map(k => `${k}=${p.get(k)}`).join('&');
    const stored = localStorage.getItem('ww_attr');
    if (!stored) {
      const ref = document.referrer && !document.referrer.includes(location.host) ? document.referrer : 'direct';
      attribution = `${utm || 'no-utm'} | ref=${ref} | landing=${location.pathname}`;
      localStorage.setItem('ww_attr', attribution);
    } else attribution = stored;
  } catch (e) { attribution = document.referrer || 'direct'; }

  /* ---------- forms ---------- */
  const started = Date.now();
  $$('form[data-form]').forEach(form => {
    const msgBox = $('.form__msg', form);
    const show = (cls, html) => { msgBox.className = `form__msg ${cls}`; msgBox.innerHTML = html; };
    form.addEventListener('submit', async e => {
      e.preventDefault();
      form.elements.attribution.value = attribution;
      form.elements.ts.value = String(Math.round((Date.now() - started) / 1000));
      const req = $$('[required]', form);
      const bad = req.find(f => !f.value.trim() || (f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value)));
      if (bad) {
        show('is-err', bad.type === 'email' ? 'Zkontrolujte prosím e-mail.' : 'Vyplňte prosím jméno, e-mail a pár slov o projektu.');
        bad.focus();
        return;
      }
      form.classList.add('is-sending');
      try {
        const fd = new FormData(form);
        const cf7 = form.dataset.cf7; // WordPress: odeslání přes Contact Form 7
        if (cf7 && fd.get('website')) { form.classList.add('is-done'); show('is-ok', 'Díky!'); return; }
        if (cf7) {
          fd.append('_wpcf7', cf7);
          fd.append('_wpcf7_unit_tag', `wpcf7-f${cf7}-o1`);
          fd.append('_wpcf7_locale', 'cs_CZ');
          fd.append('_wpcf7_container_post', '0');
        }
        const url = cf7 ? `/wp-json/contact-form-7/v1/contact-forms/${cf7}/feedback` : form.action;
        const r = await fetch(url, { method: 'POST', body: fd, headers: { Accept: 'application/json' } });
        const j = await r.json().catch(() => ({}));
        if (!r.ok || !(cf7 ? j.status === 'mail_sent' : j.ok)) throw new Error(j.status || j.error || 'send');
        form.classList.add('is-done');
        show('is-ok', '<strong>Díky, poptávka dorazila.</strong><br>Ozveme se obvykle do jednoho pracovního dne. Spěcháte? Volejte <a href="tel:+420731842606">731 842 606</a>.');
        track('generate_lead', { form: form.elements.page.value });
      } catch (err) {
        show('is-err', 'Odeslání se nepovedlo. Napište prosím přímo na <a href="mailto:lukac@yesmark.eu">lukac@yesmark.eu</a> nebo volejte <a href="tel:+420731842606">731 842 606</a>.');
      } finally {
        form.classList.remove('is-sending');
      }
    });
  });

  /* ---------- click tracking (dataLayer pro GA4 / GTM) ---------- */
  document.addEventListener('click', e => {
    const a = e.target.closest('[data-track]');
    if (a) track('cta_click', { cta: a.dataset.track });
  });

  /* ---------- misc ---------- */
  $$('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
  if (new URLSearchParams(location.search).get('odeslano') === '1') {
    const f = $('form[data-form]');
    if (f) { f.classList.add('is-done'); const m = $('.form__msg', f); m.className = 'form__msg is-ok'; m.innerHTML = '<strong>Díky, poptávka dorazila.</strong> Ozveme se obvykle do jednoho pracovního dne.'; }
  }
})();
