# Redesign v4 – světlý, výrazný, čitelný. Jedno písmo (Inter Tight), černá + červená, motiv „wwwwww = hřebeny Jeseníků“.
# Výstup: out/home-v4.json/.html (náhled se vším ve stránce) a out/home.json/.html (hlavní stránka s globálními šablonami).
# Třídy v4-*, sekce mají třídu wv4. Obsah (služby, reference, FAQ, místní text) přebírá z home_v3 / home_v2 / build.
import json, os, sys, importlib.util, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
if len(sys.argv) < 3:
    sys.argv = ['x', '23', 'https://wwwwww.cz/wp-content/uploads/2026/10/roman-lukac-tvorba-webu-jesenik.jpg']
_sp = importlib.util.spec_from_file_location('hv3', HERE / 'home_v3.py')
hv3 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(hv3)
b, hv2 = hv3.b, hv3.hv2
con, w, h, t, html, uid = b.con, b.w, b.h, b.t, b.html, b.uid
TEL, TEL_H, MAIL, SHOT, CITIES = b.TEL, b.TEL_H, b.MAIL, b.SHOT, b.CITIES

def sec(cls, *kids, eid=None, tag='section'):
    return con('wv4 v4-sec ' + cls, *kids, tag=tag, eid=eid, inner=False)

def wrap(cls, *kids):
    return con('v4-wrap ' + cls, *kids)

def kick(text, cls=''):
    return h(text, 'div', ('v4-kick ' + cls).strip())

def a_btn(text, url, cls='v4-btn--red', ext=False):
    tgt = ' target="_blank" rel="noopener"' if ext else ''
    return f'<a class="v4-btn {cls}" href="{url}"{tgt}>{text}</a>'

def zig(n, sw=2, step=12, hgt=8, cls='v4-zig'):
    """Klikatá čára – motiv hřebenů hor / písmen W."""
    d = 'M0 %d ' % hgt + ' '.join(f'L{(i + 1) * step} {0 if i % 2 == 0 else hgt}' for i in range(n * 2))
    return f'<svg class="{cls}" viewBox="-1 -1 {n * 2 * step + 2} {hgt + 2}" preserveAspectRatio="none" aria-hidden="true"><path d="{d}" fill="none" stroke="currentColor" stroke-width="{sw}" vector-effect="non-scaling-stroke" stroke-linejoin="miter"/></svg>'

PHOTO = {'id': b.PHOTO_ID, 'url': b.PHOTO_URL, 'alt': 'Roman Lukač – tvorba webových stránek Jeseník', 'source': 'library'}

# ---------- hlavička / patička ----------
NAV = [('Služby', '/tvorba-webovych-stranek/'), ('Reference', '/#reference'), ('Ceník', '/kolik-stoji-web/'), ('Obory', '/weby-pro-obory/'), ('Kontakt', '/kontakt/')]

def v4_header():
    nav = ''.join(f'<a href="{u}">{n}</a>' for n, u in NAV)
    svc = ''.join(f'<a href="{u}">{n}</a>' for n, _, u, _ in hv3.SVC)
    code = ('<header class="v4-head"><div class="v4-head__in">'
            '<a class="v4-logo" href="/" aria-label="wwwwww.cz – tvorba webových stránek">' + b.LOGO + '</a>'
            f'<a class="v4-by" href="{b.yes(x="header_v4")}" target="_blank" rel="noopener">koncept <img src="{b.YM["url"]}" alt="Yesmark" width="64" height="10"></a>'
            f'<nav class="v4-nav" aria-label="Hlavní navigace">{nav}</nav>'
            f'<div class="v4-head__r"><a class="v4-tel" href="tel:{TEL}">{TEL_H}</a>' + a_btn('Nezávazná poptávka', '#poptavka', 'v4-btn--red v4-btn--sm v4-hide-s') +
            '<button class="v4-burger" type="button" aria-expanded="false" aria-controls="v4-menu" aria-label="Menu"><i></i><i></i></button></div></div></header>'
            '<div class="v4-menu" id="v4-menu" aria-hidden="true"><div class="v4-menu__in">'
            f'<nav class="v4-menu__main" aria-label="Menu">{nav}</nav>'
            f'<div class="v4-menu__svc"><p>Služby</p>{svc}</div>'
            f'<div class="v4-menu__c"><a href="tel:{TEL}">{TEL_H}</a><a href="mailto:{MAIL}">{MAIL}</a>' + a_btn('Nezávazná poptávka', '#poptavka') + '</div>'
            '</div></div>')
    return con('v4-headwrap ww-headwrap wv4-on', html(code), tag='div', inner=False)

def v4_footer():
    svc = ''.join(f'<a href="{u}">{n}</a>' for n, _, u, _ in hv3.SVC)
    cities = ''.join(f'<a href="/tvorba-webovych-stranek-{c["slug"]}/">{c["name"]}</a>' for c in CITIES)
    big = b.LOGO.replace('<svg ', '<svg class="v4-foot__mark" ').replace('stroke-width="2.5"', 'stroke-width="2.2"')
    code = ('<div class="v4-foot">'
            '<div class="v4-foot__cta"><p class="v4-foot__t">Máte projekt?<br><span>Pojďme to probrat.</span></p>'
            '<div class="v4-foot__btns">' + a_btn('Nezávazná poptávka', '/kontakt/#poptavka') + a_btn(TEL_H, f'tel:{TEL}', 'v4-btn--ghostw') + '</div></div>'
            '<div class="v4-foot__cols">'
            f'<div><p class="v4-foot__k">Služby</p>{svc}</div>'
            '<div><p class="v4-foot__k">Web</p><a href="/kolik-stoji-web/">Ceník</a><a href="/weby-pro-obory/">Weby pro obory</a><a href="/#reference">Reference</a><a href="/kontakt/">Kontakt</a>'
            f'<a href="{b.yes("reference/", "wwwwww_reference", "footer_v4")}" target="_blank" rel="noopener">Další reference ↗</a></div>'
            f'<div class="v4-foot__cities"><p class="v4-foot__k">Tvorba webových stránek v regionu</p><p>{cities}</p></div>'
            f'<div><p class="v4-foot__k">Kontakt</p><a href="tel:{TEL}">+420 {TEL_H}</a><a href="mailto:{MAIL}">{MAIL}</a><span>{b.ADDR}</span>'
            f'<a class="v4-foot__ym" href="{b.yes(x="footer_v4")}" target="_blank" rel="noopener"><small>webový koncept agentury</small><img src="{b.YM["url"]}" alt="Yesmark" width="110" height="17"></a></div>'
            '</div>'
            f'<div class="v4-foot__bigw" aria-hidden="true">{big}</div>'
            '<div class="v4-foot__bottom"><p>© <span data-ww-year>2026</span> wwwwww.cz · Provozovatel: Roman Lukač, IČO 14448157, Vápenná 124, 790 64 Vápenná · fyzická osoba zapsaná v živnostenském rejstříku</p>'
            f'<p>{b.PRIV_FOOT}<a href="#elementor-action%3Aaction%3DcookiezBanner%3AopenPreferences">Nastavení cookies</a></p></div></div>')
    return con('wv4 v4-footer ww-footer wv4-on', html(code), tag='footer', inner=False)

# ---------- úvod ----------
LANDSCAPE = ('<svg class="v4-b-land" viewBox="0 0 200 120" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
             '<rect width="200" height="120" fill="#f3d9c9"/><circle cx="150" cy="38" r="14" fill="#e3120b" opacity=".85"/>'
             '<path d="M0 120 L0 78 L22 52 L40 70 L62 40 L84 66 L104 44 L126 72 L150 50 L174 74 L200 56 L200 120Z" fill="#8e1b20" opacity=".55"/>'
             '<path d="M0 120 L0 92 L28 70 L52 90 L80 64 L108 92 L136 70 L164 94 L200 74 L200 120Z" fill="#2b1a17"/></svg>')

def build_visual():
    return ('<div class="v4-build" data-s="0" aria-hidden="true">'
            '<div class="v4-build__win"><div class="v4-build__bar"><i></i><i></i><i></i><span>truhlarstvi-jesenik.cz</span></div>'
            '<div class="v4-build__page">'
              '<div class="v4-b-nav"><b>Truhlářství <em>Hořák</em></b><span>Nábytek</span><span>Kuchyně</span><span>Reference</span><u>Poptat</u></div>'
              '<div class="v4-b-hero"><div class="v4-b-copy"><small>Truhlářství · Jeseník</small>'
                '<strong><span>Nábytek na míru</span> <span>z Jeseníků.</span></strong>'
                '<p>Kuchyně, vestavěné skříně a schody. Zaměření a cena zdarma.</p>'
                '<div class="v4-b-btns"><u>Nezávazná poptávka</u><span>Naše práce</span></div>'
                '</div>'
              f'<div class="v4-b-img">{LANDSCAPE}</div></div>'
              '<div class="v4-b-cards"><div><b>Kuchyně</b><span>na míru</span></div><div><b>Skříně</b><span>vestavěné</span></div><div><b>★ 4,9</b><span>hodnocení</span></div></div>'
            '</div></div>'
            '<div class="v4-build__toast"><em>✓</em><div><b>Nová poptávka z webu</b><small>Kuchyně na míru · právě teď</small></div></div>'
            '<div class="v4-build__cursor"></div>'
            '<ol class="v4-build__steps"><li>Návrh</li><li>Design</li><li>Obsah</li><li>Spuštění</li></ol>'
            '</div>')

def v4_hero():
    return sec('v4-hero',
        wrap('v4-hero__grid',
            con('v4-hero__copy',
                kick('Jeseník · weby pro celou ČR', 'v4-kick--dot'),
                h('Tvorba webových stránek v Jeseníku, které <em>prodávají</em>.', 'h1', 'v4-h1'),
                t('<p>Navrhnu a postavím vám moderní web na míru – srozumitelný na mobilu, rychlý a připravený pro Google. Jednodušší web bývá hotový za 2–4 týdny.</p>', 'v4-lead'),
                html(a_btn('Chci nezávaznou nabídku <i>→</i>', '#poptavka', 'v4-btn--red v4-btn--lg') + a_btn(f'Zavolat {TEL_H}', f'tel:{TEL}', 'v4-btn--line v4-btn--lg'), 'v4-btns'),
                html(f'<div class="v4-trust"><div class="v4-trust__me"><img src="{b.PHOTO_URL}" alt="" width="48" height="48"><p><b>Roman Lukač</b><span>ozvu se do 1 pracovního dne</span></p></div>'
                     '<div class="v4-trust__f"><b>od 9 900 Kč</b><span>cena nového webu</span></div>'
                     '<div class="v4-trust__f"><b>1 člověk</b><span>od návrhu po spuštění</span></div></div>', 'v4-trust-w')),
            html(build_visual(), 'v4-build-w')), eid='uvod')

# ---------- reference ----------
def v4_refs():
    cards = ''.join(
        f'<a class="v4-ref v4-rv" href="{u}" target="_blank" rel="noopener"><div class="v4-ref__win"><div class="v4-ref__bar"><i></i><i></i><i></i><span>{u.split("//")[1].strip("/").replace("www.", "")}</span></div>'
        f'<div class="v4-ref__view"><img src="{SHOT[k]["url"]}" alt="Reference: web {n} – {sub}" loading="lazy"></div></div>'
        f'<p class="v4-ref__tag">{sub}</p><h3 class="v4-ref__n">{n}</h3><p class="v4-ref__d">{d}</p><span class="v4-ref__go">Navštívit web ↗</span></a>'
        for k, n, sub, d, u in hv3.REFS)
    cards += ('<a class="v4-ref v4-ref--you v4-rv" href="#poptavka"><div class="v4-ref__win"><div class="v4-ref__bar"><i></i><i></i><i></i><span>vas-web.cz</span></div><div class="v4-ref__view v4-ref__you">'
              + zig(3, 2, 12, 8, 'v4-zig v4-ref__z') + '<strong>Váš web<br>může být další.</strong><span>Nabídku připravím zdarma.</span></div></div>'
              '<p class="v4-ref__tag">Volné termíny</p><h3 class="v4-ref__n">Další na řadě</h3><p class="v4-ref__d">Napište mi, co děláte – ozvu se s návrhem a cenou.</p><span class="v4-ref__go">Nezávazná poptávka →</span></a>')
    return sec('v4-refs v4-soft',
        wrap('',
            con('v4-headrow',
                con('v4-headrow__l', kick('Reference'), h('Weby, které už vydělávají svým majitelům.', 'h2', 'v4-h2 v4-rv')),
                html(a_btn('Všechny reference ↗', b.yes('reference/', 'wwwwww_reference', 'homepage_v4'), 'v4-btn--line', ext=True), 'v4-headrow__r')),
            html(f'<div class="v4-refgrid" tabindex="0" aria-label="Reference">{cards}</div>', 'v4-seo')), eid='reference')

# ---------- služby ----------
SVC_DESC = {
    '/tvorba-webovych-stranek/': 'Nový web od návrhu po spuštění – postavený tak, aby z návštěvníků dělal zákazníky.',
    '/tvorba-webu-na-miru/': 'Struktura, texty a design přesně pro váš obor. Žádná šablona, kterou má půl města.',
    '/tvorba-webu-wordpress/': 'WordPress a Elementor: texty, fotky i nové stránky si upravíte sami, bez programátora.',
    '/firemni-web/': 'Profesionální prezentace firmy, která budí důvěru na první pohled – i na mobilu.',
    '/tvorba-eshopu/': 'Katalog, košík, platby a dopravci. E-shop, ve kterém se dobře nakupuje.',
    '/redesign-webu/': 'Zastaralý web převedu do moderní podoby a zachovám to, co už funguje ve vyhledávání.',
    '/seo-optimalizace-webu/': 'Struktura, obsah a technické SEO, aby vás zákazníci našli dřív než konkurenci.',
    '/sprava-webu/': 'Aktualizace, zálohy, zabezpečení a drobné úpravy. Vy podnikáte, o web se starám já.',
}

def v4_services():
    cards = ''.join(f'<a class="v4-svc v4-rv" href="{u}"><span class="v4-svc__n">{i + 1:02d}</span><h3>{n}</h3><p>{SVC_DESC[u]}</p><i>→</i></a>'
                    for i, (n, _, u, _) in enumerate(hv3.SVC))
    return sec('v4-svcs',
        wrap('',
            con('v4-headrow',
                con('v4-headrow__l', kick('Služby'), h('Co pro vás můžu udělat', 'h2', 'v4-h2 v4-rv')),
                t('<p>Od jednostránkového webu pro živnostníka po e-shop. Každý web stavím s důrazem na mobil, rychlost a Google.</p>', 'v4-p v4-headrow__r')),
            html(f'<nav class="v4-svcgrid" aria-label="Služby">{cards}</nav>', 'v4-seo')), eid='sluzby')

# ---------- před a po ----------
def v4_ba():
    return con('wv4 v4-sec v4-ba v4-soft ww-home',
        wrap('v4-two v4-two--ba',
            con('v4-two__l', kick('Redesign v praxi'), h('Před a po. Posuňte si to.', 'h2', 'v4-h2'),
                t('<p>Vlevo web, který nikoho nepřesvědčí. Vpravo web, který za tři vteřiny řekne, co nabízíte, a dovede člověka k poptávce.</p>', 'v4-p'),
                html(a_btn('Redesign webu →', '/redesign-webu/', 'v4-btn--line'))),
            html(b.BEFORE_AFTER, 'v4-ba__w')), tag='section', eid='pred-a-po', inner=False)

# ---------- kdo za tím stojí ----------
def v4_about():
    pts = [('Jednáte přímo se mnou', 'Žádné přehazování mezi obchodníkem, grafikem a programátorem.'),
           ('Web si upravíte sami', 'Stavím na WordPressu a Elementoru. Po spuštění vás zaškolím.'),
           ('Na Google myslím od začátku', 'Struktura, rychlost a základní SEO jsou v ceně každého webu.')]
    lis = ''.join(f'<li><em>✓</em><div><b>{a}</b><span>{c}</span></div></li>' for a, c in pts)
    ridge = zig(6, 2.4, 14, 12, 'v4-zig v4-why__z')
    return sec('v4-about',
        wrap('v4-two v4-two--about',
            con('v4-about__photo',
                w('image', 'v4-photo', image=PHOTO, image_size='full'),
                html(f'<div class="v4-why">{ridge}<p><b>Proč šest W?</b> Jako hřebeny Jeseníků, pod kterými weby vznikají – a jako www, přes které vás najdou zákazníci.</p></div>')),
            con('v4-two__r',
                kick('Kdo za webem stojí'),
                h('Ahoj, jsem Roman. Váš web udělám osobně.', 'h2', 'v4-h2'),
                t('<p>Weby navrhuji a stavím v Jeseníku pod křídly marketingové agentury Yesmark. Spojuji osobní přístup malého studia se zázemím agentury, která vám umí navázat grafikou, kampaněmi i tiskem.</p>', 'v4-p v4-p--lg'),
                html(f'<ul class="v4-points">{lis}</ul>', 'v4-seo'),
                html(a_btn('Napište mi →', '#poptavka', 'v4-btn--ink') + a_btn('Co dělá Yesmark ↗', b.yes(x='about_v4'), 'v4-btn--line', ext=True), 'v4-btns'))), eid='o-mne')

# ---------- postup ----------
def v4_process():
    steps = [('Poznám váš byznys', 'Krátký hovor nebo kafe. Projdeme cíle, zákazníky a konkurenci. Nabídku dostanete zdarma.'),
             ('Navrhnu a postavím', 'Struktura, design na míru a obsah. Průběžně vidíte, jak web roste, a můžete do toho mluvit.'),
             ('Spustíme web', 'Testy na mobilech, SEO nastavení, analytika a Google Firemní profil. Pak vás zaškolím.'),
             ('Starám se dál', 'Aktualizace, zálohy a úpravy obsahu. Když budete chtít, rosteme dál se SEO a kampaněmi.')]
    cols = ''.join(f'<li class="v4-step v4-rv" style="--i:{i}"><span class="v4-step__n">{i + 1}</span><h3>{a}</h3><p>{c}</p></li>' for i, (a, c) in enumerate(steps))
    return sec('v4-proc v4-soft',
        wrap('',
            con('v4-headrow',
                con('v4-headrow__l', kick('Postup'), h('Od prvního kafe ke spuštění', 'h2', 'v4-h2 v4-rv')),
                t('<p>Jasný postup, jasná cena a žádná překvapení. Vždycky víte, co se právě děje.</p>', 'v4-p v4-headrow__r')),
            html(f'<div class="v4-steps-w">{zig(8, 2, 16, 10, "v4-zig v4-steps__z")}<ol class="v4-steps">{cols}</ol></div>', 'v4-seo')), eid='proces')

# ---------- ceník ----------
INCL = ['Návrh struktury a designu', 'Web pro mobil, tablet i počítač', 'Kontaktní formulář a mapa', 'Základní SEO nastavení',
        'Napojení na Google Analytics', 'Cookies lišta a GDPR', 'Zaškolení do administrace', 'Nabídka a konzultace zdarma']

def v4_price():
    lis = ''.join(f'<li>{x}</li>' for x in INCL)
    return sec('v4-price v4-red',
        wrap('v4-two v4-two--price',
            con('v4-two__l',
                kick('Ceník', 'v4-kick--w'),
                h('<small>Tvorba webových stránek Jeseník</small>od 9 900 Kč', 'div', 'v4-price__num'),
                t('<p>Žádný šablonovitý ceník. Konečná cena se odvíjí od rozsahu, funkcí a grafiky – a vždycky ji znáte předem, s jasným rozpisem, co v ní je a co ne.</p>', 'v4-p v4-p--w'),
                html(a_btn('Chci cenovou nabídku →', '#poptavka', 'v4-btn--white v4-btn--lg') + a_btn('Kolik stojí web', '/kolik-stoji-web/', 'v4-btn--ghostw v4-btn--lg'), 'v4-btns')),
            html(f'<div class="v4-incl"><p class="v4-incl__k">V ceně je vždy</p><ul>{lis}</ul></div>', 'v4-seo')), eid='cenik')

# ---------- kvíz ----------
def v4_quiz():
    return con('wv4 v4-sec v4-quiz ww-home',
        wrap('v4-two',
            con('v4-two__l', kick('Kvíz · 30 vteřin'), h('Nevíte, jaký web potřebujete?', 'h2', 'v4-h2'),
                t('<p>Odpovězte na tři otázky a dostanete doporučení na míru. Odpovědi pak jedním klikem pošlete v poptávce.</p>', 'v4-p')),
            html(b.QUIZ, 'v4-quiz__w')), tag='section', eid='kviz', inner=False)

# ---------- FAQ ----------
def v4_faq(faq):
    return sec('v4-faqs v4-soft',
        wrap('v4-two v4-two--faq',
            con('v4-two__l', kick('Časté otázky'), h('Časté otázky – tvorba webových stránek Jeseník', 'h2', 'v4-h2 v4-h2--sm'),
                t(f'<p>Nenašli jste odpověď? Zavolejte na <a href="tel:{TEL}">{TEL_H}</a> nebo napište na <a href="mailto:{MAIL}">{MAIL}</a>.</p>', 'v4-p')),
            w('toggle', 'v4-faq', faq_schema='yes', tabs=[{'_id': uid(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in faq])), eid='faq')

# ---------- obory + Jeseník ----------
def v4_local():
    links = ''.join(f'<a href="{u}"><span>{n}</span><i>→</i></a>' for n, u in hv2.v_obory())
    loc = hv2.v_local()
    body = loc['elements'][0]['elements'][1]['elements'][1]['settings']['editor']
    towns = ''.join(f'<a href="/tvorba-webovych-stranek-{c["slug"]}/">{c["name"]}</a>' for c in CITIES)
    return con('wv4 v4-sec v4-local',
        wrap('v4-two v4-two--local',
            con('v4-two__l', kick('Weby pro obory'), h('Co by měl mít web právě pro váš obor?', 'h2', 'v4-h2 v4-h2--sm'),
                t('<p>Pro více než 70 oborů jsem sepsal checklist, ukázkovou strukturu a SEO tipy.</p>', 'v4-p'),
                html(f'<nav class="v4-list" aria-label="Weby podle oboru">{links}</nav>')),
            con('v4-two__r', kick('Jeseník · celá ČR'), h('Tvorba webových stránek Jeseník – a kdekoli v Česku', 'h2', 'v4-h2 v4-h2--sm'),
                t(body, 'v4-prose'), kick('Tvořím weby také pro'), t(f'<p>{towns}</p>', 'v4-towns ww-towns'))), tag='section', eid='jesenicko', inner=False)

# ---------- kontakt ----------
def v4_contact():
    form = b.contact_section('home')['elements'][1]['elements'][2]
    form['settings']['_css_classes'] = 'v4-form'
    return sec('v4-contact v4-soft',
        wrap('v4-two v4-two--contact',
            con('v4-two__l', kick('Poptávka'), h('Pojďme postavit váš nový web.', 'h2', 'v4-h2'),
                t('<p>Stačí pár vět o tom, co děláte a co od webu čekáte. Ozvu se obvykle do jednoho pracovního dne s návrhem dalšího postupu a cenou.</p>', 'v4-p v4-p--lg'),
                html(f'<div class="v4-cbig"><a href="tel:{TEL}"><small>Telefon</small>{TEL_H}</a><a href="mailto:{MAIL}"><small>E-mail</small>{MAIL}</a></div>'
                     f'<div class="v4-trust__me v4-trust__me--c"><img src="{b.PHOTO_URL}" alt="" width="56" height="56" loading="lazy"><p><b>Roman Lukač</b><span>Webdesign a vývoj · Yesmark Jeseník</span></p></div>')),
            con('v4-formcard', h('Nezávazná poptávka', 'h3', 'v4-h3'), form,
                t('<p>Údaje použiji jen k vyřízení vaší poptávky a nikomu je neprodám.' + b.PRIV_LINK + '</p>', 'v4-legal'))), eid='poptavka')

def v4_sys(live, extra_ld=True):
    ld = {'@context': 'https://schema.org', '@graph': [b.BUSINESS, {'@type': 'WebSite', '@id': 'https://wwwwww.cz/#web', 'url': 'https://wwwwww.cz/', 'name': 'wwwwww.cz', 'inLanguage': 'cs-CZ', 'publisher': {'@id': 'https://wwwwww.cz/#business'}}]}
    mbar = f'<div class="wmbar"><a class="wbtn wbtn--ghost" href="tel:{TEL}">Zavolat</a><a class="wbtn wbtn--red" href="#poptavka">Poptat web</a></div>'
    if extra_ld: mbar += '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'
    return con('ww ww-sys wv4-sys', html(mbar + ('' if live else b.js_loader())), inner=False)

def home_v4(live=False):
    """live=True: hlavička a patička jako globální šablony, jinak vše přímo ve stránce (náhled)."""
    body = [v4_hero(), v4_refs(), v4_services(), v4_ba(), v4_about(), v4_process(), v4_price(), v4_quiz(), v4_faq(hv3._faq()), v4_local(), v4_contact()]
    if live:
        return [b.header()] + body + [b.footer(), v4_sys(True)]
    return [v4_header()] + body + [v4_footer(), v4_sys(False)]

# ---------- text pro post_content: včetně textu z HTML widgetů označených v4-seo ----------
import re as _re
def _seo_html(code):
    code = _re.sub(r'<(svg|script|style|button)\b.*?</\1>', '', code, flags=_re.S)
    code = _re.sub(r'<(?!/?(h2|h3|h4|p|a|ul|ol|li|strong|b|em|br)\b)[^>]+>', ' ', code)
    code = _re.sub(r'<(h2|h3|h4|p|ul|ol|li|strong|b|em)\b[^>]*>', r'<\1>', code)
    return _re.sub(r'\s+', ' ', code).strip()

def to_html(elements):
    out = [b.to_html(elements)]
    def walk(e):
        s = e.get('settings', {})
        if e['elType'] == 'container':
            for k in e['elements']: walk(k)
        elif e.get('widgetType') == 'html' and 'v4-seo' in s.get('_css_classes', ''):
            out.append(_seo_html(s['html']))
    for e in elements: walk(e)
    return '\n'.join(out)

if __name__ == '__main__':
    d = home_v4()
    (b.OUT / 'home-v4.json').write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    (b.OUT / 'home-v4.html').write_text(to_html(d), encoding='utf-8')
    d = home_v4(live=True)
    if os.environ.get('WW_LIVE') == '1':   # hlavní stránku přepisujeme až po schválení
        (b.OUT / 'home.json').write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
        (b.OUT / 'home.html').write_text(to_html(d), encoding='utf-8')
    print('home-v4', len(json.dumps(d)) // 1024, 'kB', len(_re.sub('<[^>]+>', ' ', to_html(d)).split()), 'slov')
