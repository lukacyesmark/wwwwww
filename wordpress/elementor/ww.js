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

  $$('[data-ww-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
