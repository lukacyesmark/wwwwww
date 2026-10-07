/* wwwwww.cz — interakce (bez knihoven). Vkládá se zakódovaný do HTML widgetu „ww-system“. */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  var $ = function (s, r) { return (r || doc).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); };
  var inEditor = doc.body.classList.contains('elementor-editor-active') || /elementor-preview/.test(location.search);
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(pointer: fine)').matches;
  window.dataLayer = window.dataLayer || [];
  var track = function (ev, data) { var o = { event: ev }; for (var k in data) o[k] = data[k]; window.dataLayer.push(o); };

  /* header + menu + mobilní lišta */
  var wh = $('.wh'), mbar = $('.wmbar'), hero = $('.ww-hero, .ww-phero');
  var onScroll = function () {
    var y = scrollY;
    if (wh) wh.classList.toggle('is-scrolled', y > 10);
    if (mbar) {
      var form = $('#poptavka');
      var nearForm = form ? form.getBoundingClientRect().top < innerHeight * 0.85 && form.getBoundingClientRect().bottom > 0 : false;
      mbar.classList.toggle('is-on', y > (hero ? hero.offsetHeight * 0.5 : 300) && !nearForm);
    }
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var burger = $('.wburger');
  if (burger) {
    var setMenu = function (open) {
      doc.body.classList.toggle('ww-menu-open', open);
      burger.setAttribute('aria-expanded', String(open));
      doc.body.style.overflow = open ? 'hidden' : '';
    };
    burger.addEventListener('click', function () { setMenu(!doc.body.classList.contains('ww-menu-open')); });
    $$('.wnav a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  }
  $$('.wnav a').forEach(function (a) { if (a.getAttribute('href') === location.pathname) a.classList.add('is-active'); });

  /* reveal při scrollu (v editoru Elementoru vypnuto) */
  if (!inEditor && !reduce && 'IntersectionObserver' in window) {
    root.classList.add('ww-js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    $$('.ww-rv').forEach(function (el, i) { io.observe(el); });
  }

  /* hero: parallax vizuálu a záře podle myši */
  var hv = $('.hv__stack'), heroEl = $('.ww-hero');
  if (fine && !reduce && hv && heroEl) {
    heroEl.addEventListener('pointermove', function (e) {
      var r = heroEl.getBoundingClientRect();
      var nx = (e.clientX - r.left) / r.width - 0.5, ny = (e.clientY - r.top) / r.height - 0.5;
      hv.style.setProperty('--px', (nx * 18).toFixed(1) + 'px');
      hv.style.setProperty('--py', (ny * 14).toFixed(1) + 'px');
      hv.style.transform = 'rotateY(' + (-16 + nx * 10).toFixed(2) + 'deg) rotateX(' + (8 - ny * 8).toFixed(2) + 'deg)';
    });
    heroEl.addEventListener('pointerleave', function () { hv.style.transform = ''; });
  }

  /* karty: světlo pod kurzorem */
  if (fine) $$('.ww-card').forEach(function (c) {
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect();
      c.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      c.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  /* měření: kliky na CTA, telefon, e-mail, odeslání formuláře (dataLayer pro GA4/GTM) */
  doc.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('tel:') === 0) track('phone_click', { where: a.className });
    else if (href.indexOf('mailto:') === 0) track('email_click', {});
    else if (/kontakt|poptavka/.test(href)) track('cta_click', { text: (a.textContent || '').trim().slice(0, 40) });
  });
  if (window.jQuery) window.jQuery(doc).on('submit_success', function () { track('generate_lead', { page: location.pathname }); });


  /* ukazatel scrollu */
  var prog = $('.wprog');
  if (prog) addEventListener('scroll', function () {
    var h = doc.documentElement.scrollHeight - innerHeight;
    prog.style.setProperty('--p', h > 0 ? (scrollY / h).toFixed(4) : 0);
  }, { passive: true });

  /* záře za kurzorem */
  var cur = $('.wcursor');
  if (cur && fine && !reduce && !inEditor) {
    var cx = 0, cy = 0, tx = 0, ty = 0, raf = 0;
    var loop = function () { cx += (tx - cx) * 0.12; cy += (ty - cy) * 0.12; cur.style.setProperty('--cx', cx.toFixed(1) + 'px'); cur.style.setProperty('--cy', cy.toFixed(1) + 'px'); raf = Math.abs(tx - cx) + Math.abs(ty - cy) > 0.5 ? requestAnimationFrame(loop) : 0; };
    addEventListener('pointermove', function (e) { tx = e.clientX; ty = e.clientY; var light = e.target.closest && e.target.closest('.ww-light, .ww-white, .ww-redbg'); cur.classList.toggle('is-on', !light); if (!raf) raf = requestAnimationFrame(loop); }, { passive: true });
    doc.addEventListener('pointerleave', function () { cur.classList.remove('is-on'); });
    addEventListener('scroll', function () { var el = doc.elementFromPoint(tx, ty); cur.classList.toggle('is-on', !!el && !(el.closest && el.closest('.ww-light, .ww-white, .ww-redbg'))); }, { passive: true });
  }

  /* hlavní nadpis: rozdělení na slova (jen na webu, ne v editoru) */
  if (!inEditor && !reduce) $$('.ww-h1 .elementor-heading-title').forEach(function (el) {
    var i = 0;
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = doc.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(doc.createTextNode(part)); return; }
            var wr = doc.createElement('span'); wr.className = 'ww-w';
            var inner = doc.createElement('span'); inner.textContent = part; inner.style.setProperty('--wd', (0.08 * i++).toFixed(2) + 's');
            wr.appendChild(inner); frag.appendChild(wr);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1) walk(n);
      });
    };
    walk(el);
    el.classList.add('ww-split');
    requestAnimationFrame(function () { requestAnimationFrame(function () { el.classList.add('is-split'); }); });
  });

  /* magnetická tlačítka */
  if (fine && !reduce) $$('.ww .elementor-button, .wbtn--red').forEach(function (b) {
    b.addEventListener('pointermove', function (e) {
      var r = b.getBoundingClientRect();
      b.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * 0.15).toFixed(1) + 'px,' + ((e.clientY - r.top - r.height / 2) * 0.25).toFixed(1) + 'px)';
    });
    b.addEventListener('pointerleave', function () { b.style.transform = ''; });
  });

  /* ===== HLAVNÍ STRÁNKA: scroll animace a interaktivní prvky ===== */
  if ($('.ww-home') && !inEditor) (function () {
    var vh = function () { return innerHeight; };
    var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
    /* průběh prvku viewportem: 0 když horní hrana na `start`*vh, 1 když na `end`*vh */
    var prog = function (el, start, end) { var r = el.getBoundingClientRect(); return clamp((vh() * start - r.top) / (vh() * (start - end)), 0, 1); };
    var tasks = [];

    /* 1) statement – slova se rozsvěcují */
    if (!reduce) $$('.ww-home .ww-statement .elementor-heading-title').forEach(function (el) {
      var words = [];
      var walk = function (node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (n) {
          if (n.nodeType === 3) {
            var frag = doc.createDocumentFragment();
            n.textContent.split(/(\s+)/).forEach(function (part) {
              if (!part) return;
              if (/^\s+$/.test(part)) { frag.appendChild(doc.createTextNode(part)); return; }
              var sp = doc.createElement('span'); sp.className = 'ww-sw'; sp.textContent = part; words.push(sp); frag.appendChild(sp);
            });
            n.parentNode.replaceChild(frag, n);
          } else if (n.nodeType === 1) walk(n);
        });
      };
      walk(el);
      tasks.push(function () { var p = prog(el, 0.9, 0.35), k = Math.round(p * words.length); words.forEach(function (w, i) { w.classList.toggle('is-lit', i < k); }); });
    });

    /* 2) proces – linka a aktivní krok */
    var steps = $('.ww-home .ww-steps');
    if (steps) {
      var items = $$('.ww-step', steps);
      tasks.push(function () {
        steps.style.setProperty('--prog', prog(steps, 0.6, 0.6 - steps.offsetHeight / vh()).toFixed(3));
        items.forEach(function (it) { it.classList.toggle('is-active', reduce || it.getBoundingClientRect().top < vh() * 0.62); });
      });
    }

    /* 3) hero – jemný parallax při scrollu */
    var hvw = $('.ww-home.ww-hero .hv'), hcopy = $('.ww-home.ww-hero .ww-hero-copy');
    if (!reduce && hvw) tasks.push(function () {
      var y = Math.min(scrollY, vh());
      hvw.style.translate = '0 ' + (y * 0.12).toFixed(1) + 'px';
      if (hcopy) { hcopy.style.translate = '0 ' + (y * 0.05).toFixed(1) + 'px'; hcopy.style.opacity = (1 - y / vh() * 0.6).toFixed(3); }
    });

    /* 4) CTA – rozbalení z karty na celou šířku */
    var cta = $('.ww-home.ww-redbg.ww-cta'), mega = cta && $('.ww-mega .elementor-heading-title', cta);
    if (!reduce && cta) tasks.push(function () {
      var p = prog(cta, 1, 0.35);
      cta.style.setProperty('--ci', ((1 - p) * 5).toFixed(2) + '%');
      cta.style.setProperty('--cr', ((1 - p) * 40).toFixed(1) + 'px');
      if (mega) mega.style.setProperty('--cs', (0.86 + p * 0.14).toFixed(3));
    });

    /* 5) pás s obcemi – rychlost a směr podle scrollu */
    var mq = $('.ww-home .mq__t'), anim = mq && mq.getAnimations ? mq.getAnimations()[0] : null, lastY = scrollY, vel = 0;
    if (!reduce && anim) tasks.push(function () {
      var d = scrollY - lastY; lastY = scrollY;
      vel += (clamp(d, -60, 60) / 6 - vel) * 0.3;
      anim.playbackRate = (d < 0 ? -1 : 1) * (1 + Math.abs(vel));
    });

    var ticking = false;
    var run = function () { ticking = false; tasks.forEach(function (f) { f(); }); };
    var req = function () { if (!ticking) { ticking = true; requestAnimationFrame(run); } };
    addEventListener('scroll', req, { passive: true }); addEventListener('resize', req); run();

    /* 6) postupné nabíhání karet */
    $$('.ww-home .ww-bento > .ww-rv, .ww-home .ww-refs > .ww-rv, .ww-home .ww-why > .ww-rv').forEach(function (el) {
      var i = Array.prototype.indexOf.call(el.parentNode.children, el);
      el.style.setProperty('--d', (i % 4 * 0.1).toFixed(2) + 's');
    });

    /* 7) 3D náklon karet pod kurzorem */
    if (fine && !reduce) $$('.ww-home .ww-bento > .ww-card, .ww-home .ww-refs > .ww-ref').forEach(function (c) {
      c.addEventListener('pointermove', function (e) {
        if (!c.classList.contains('is-in')) return;
        var r = c.getBoundingClientRect(), nx = (e.clientX - r.left) / r.width - 0.5, ny = (e.clientY - r.top) / r.height - 0.5;
        c.classList.add('is-tilt');
        c.style.transform = 'perspective(900px) rotateY(' + (nx * 7).toFixed(2) + 'deg) rotateX(' + (-ny * 7).toFixed(2) + 'deg) translateY(-4px)';
      });
      c.addEventListener('pointerleave', function () { c.style.transform = ''; setTimeout(function () { c.classList.remove('is-tilt'); }, 200); });
    });

    /* 8) počítadla */
    var nf = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); };
    if ('IntersectionObserver' in window) {
      var cio = new IntersectionObserver(function (en) {
        en.forEach(function (e) {
          if (!e.isIntersecting) return; cio.unobserve(e.target);
          var el = e.target, to = +el.getAttribute('data-count'), t0 = performance.now(), dur = 1600;
          if (reduce) return;
          var step = function (t) { var k = Math.min(1, (t - t0) / dur), v = Math.round(to * (1 - Math.pow(1 - k, 4))); el.textContent = nf(to >= 1000 ? Math.round(v / 100) * 100 : v); if (k < 1) requestAnimationFrame(step); };
          el.textContent = '0'; requestAnimationFrame(step);
        });
      }, { threshold: 0.6 });
      $$('.ww-home [data-count]').forEach(function (el) { cio.observe(el); });
    }

    /* 9) před / po */
    $$('.ww-home .wba').forEach(function (ba) {
      var rng = $('.wba__range', ba), touched = false;
      var set = function (v) { ba.style.setProperty('--pos', v + '%'); };
      rng.addEventListener('input', function () { touched = true; set(rng.value); });
      rng.addEventListener('pointerdown', function () { ba.classList.add('is-drag'); });
      addEventListener('pointerup', function () { ba.classList.remove('is-drag'); });
      rng.addEventListener('change', function () { track('before_after', { pos: rng.value }); });
      if (!reduce && 'IntersectionObserver' in window) {
        var bio = new IntersectionObserver(function (en) {
          if (!en[0].isIntersecting) return; bio.disconnect();
          var keys = [[0, 50], [900, 82], [1900, 22], [2900, 50]], t0 = performance.now();
          var ease = function (k) { return k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2; };
          var demo = function (t) {
            if (touched) return;
            var e = t - t0, i = 0; while (i < keys.length - 2 && e > keys[i + 1][0]) i++;
            var a = keys[i], b = keys[i + 1], k = clamp((e - a[0]) / (b[0] - a[0]), 0, 1), v = a[1] + (b[1] - a[1]) * ease(k);
            set(v.toFixed(1)); rng.value = v;
            if (e < keys[keys.length - 1][0]) requestAnimationFrame(demo);
          };
          setTimeout(function () { t0 = performance.now(); requestAnimationFrame(demo); }, 500);
        }, { threshold: 0.5 });
        bio.observe(ba);
      }
    });

    /* 10) kvíz */
    $$('.ww-home .wquiz').forEach(function (qz) {
      var qs = $$('.wquiz__q', qz), res = $('.wquiz__res', qz), bar = $('.wquiz__bar', qz), ans = {}, labels = {}, cur = 0;
      var show = function (i) {
        cur = i; qs.forEach(function (q, j) { q.classList.toggle('is-on', j === i); });
        res.classList.toggle('is-on', i >= qs.length);
        bar.style.setProperty('--qp', (Math.min(i, qs.length) / qs.length * 100) + '%');
      };
      var R = {
        eshop: ['E-shop, který prodává', 'Chcete prodávat online – potřebujete přehledný e-shop s jednoduchou objednávkou, platbami a dopravou.', ['Přehledné kategorie a filtry', 'Objednávka na pár kliků i z mobilu', 'Napojení plateb a dopravců'], '/tvorba-eshopu/'],
        redesign: ['Redesign webu', 'Web už máte, ale zastaral. Nový design, obsah a struktura z něj udělají obchodníka – bez ztráty pozic v Googlu.', ['Moderní vzhled a ovládání na mobilu', 'Texty, které vedou k poptávce', 'Přesměrování starých adres a zachování SEO'], '/redesign-webu/'],
        seo: ['SEO a obsah, který přivede zákazníky', 'Web máte, jen ho zákazníci nenajdou. Zaměříme se na obsah, strukturu a lokální SEO.', ['Analýza, co vaši zákazníci hledají', 'Stránky pro jednotlivé služby a města', 'Google Firemní profil a recenze'], '/seo-optimalizace-webu/'],
        rezervace: ['Web s online rezervací', 'Pro ubytování, gastro a služby je klíčové, aby si zákazník mohl rovnou rezervovat nebo objednat.', ['Fotky, ceny a dostupnost na jednom místě', 'Rezervace nebo poptávka termínu online', 'Jazykové verze pro turisty'], '/web-pro-penzion/'],
        komunita: ['Přehledný web pro obec, spolek nebo školu', 'Hlavní je, aby lidé rychle našli aktuality, kontakty a dokumenty – a abyste web snadno spravovali.', ['Aktuality a úřední deska', 'Kalendář akcí a kontakty', 'Jednoduchá správa pro více lidí'], '/weby-pro-obory/'],
        firemni: ['Firemní web na míru', 'Potřebujete web, který jasně řekne, co děláte, ukáže reference a přivede poptávky.', ['Jasné sdělení na první obrazovce', 'Služby, reference a důvěryhodnost', 'Poptávkový formulář a telefon vždy po ruce'], '/firemni-web/']
      };
      var pick = function () {
        if (ans.cil === 'prodej' || ans.obor === 'produkty') return 'eshop';
        if (ans.web === 'stary') return 'redesign';
        if (ans.web === 'seo') return 'seo';
        if (ans.obor === 'ubytovani' || ans.cil === 'rezervace') return 'rezervace';
        if (ans.obor === 'komunita') return 'komunita';
        return 'firemni';
      };
      var key;
      var result = function () {
        key = pick(); var r = R[key];
        $('[data-r="title"]', res).textContent = r[0];
        $('[data-r="text"]', res).textContent = r[1];
        var ul = $('[data-r="list"]', res); ul.innerHTML = '';
        r[2].concat(['Weby od 9 900 Kč, nabídka zdarma']).forEach(function (x) { var li = doc.createElement('li'); li.textContent = x; ul.appendChild(li); });
        $('[data-r="more"]', res).setAttribute('href', r[3]);
        track('quiz_complete', { result: key });
      };
      qs.forEach(function (q, i) {
        $$('button', q).forEach(function (b) {
          b.addEventListener('click', function () {
            $$('button', q).forEach(function (x) { x.classList.toggle('is-picked', x === b); });
            ans[q.getAttribute('data-q')] = b.getAttribute('data-v'); labels[i] = b.textContent;
            setTimeout(function () { if (i === qs.length - 1) result(); show(i + 1); }, 220);
          });
        });
      });
      $('.wquiz__again', res).addEventListener('click', function () { ans = {}; labels = {}; $$('button.is-picked', qz).forEach(function (b) { b.classList.remove('is-picked'); }); show(0); });
      $('[data-r="send"]', res).addEventListener('click', function () {
        var msg = $('#form-field-message');
        if (msg) {
          msg.value = 'Kvíz na webu: čím se živím – ' + labels[0] + '; web má hlavně – ' + labels[1] + '; současný web – ' + labels[2] + '. Doporučení: ' + R[key][0] + '.\n\n';
          setTimeout(function () { var nm = $('#form-field-name'); if (nm) nm.focus({ preventScroll: true }); }, 700);
        }
        track('quiz_to_form', { result: key });
      });
      show(0);
    });
  })();

  $$('[data-ww-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
