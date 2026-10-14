# Návrh hlavní stránky ve stylu Collins (světlý, patkové písmo, barevné „médium“).
# Výstup: out/home-v3.json/.html. Třídy c3-*, sekce mají třídu wv3. Obsah přebírá z home_v2 / build.
import json, sys, importlib.util, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
_sp = importlib.util.spec_from_file_location('hv2', HERE / 'home_v2.py')
hv2 = importlib.util.module_from_spec(_sp)
if len(sys.argv) < 3:
    sys.argv = ['x', '23', 'https://wwwwww.cz/wp-content/uploads/2026/10/roman-lukac-tvorba-webu-jesenik.jpg']
_sp.loader.exec_module(hv2)
b = hv2.b
con, w, h, t, btn, html, uid = b.con, b.w, b.h, b.t, b.btn, b.html, b.uid
TEL, TEL_H, MAIL, SHOT, CITIES = b.TEL, b.TEL_H, b.MAIL, b.SHOT, b.CITIES

def sec(cls, *kids, eid=None, tag='section'):
    return con('wv3 c3-sec ' + cls, *kids, tag=tag, eid=eid, inner=False)

def wrap(cls, *kids):
    return con('c3-wrap ' + cls, *kids)

def lab(text):
    return h(text, 'div', 'c3-lab')

def pill(text, url, cls='', ext=False):
    tgt = ' target="_blank" rel="noopener"' if ext else ''
    return f'<a class="c3-pill {cls}" href="{url}"{tgt}>{text}</a>'

SVC = [('Tvorba webových stránek', 'Web, který přivádí poptávky.', '/tvorba-webovych-stranek/', 'konradt'),
       ('Web na míru', 'Struktura a design pro váš obor.', '/tvorba-webu-na-miru/', 'monika-velickova'),
       ('Weby na WordPressu', 'Upravíte si ho sami.', '/tvorba-webu-wordpress/', 'brincil'),
       ('Firemní web', 'Důvěra na první pohled.', '/firemni-web/', 'konradt'),
       ('Tvorba e-shopu', 'Prodávejte, i když spíte.', '/tvorba-eshopu/', 'brincil'),
       ('Redesign webu', 'Nový web místo starého.', '/redesign-webu/', 'monika-velickova'),
       ('SEO optimalizace', 'Aby vás našel Google.', '/seo-optimalizace-webu/', 'konradt'),
       ('Správa webu', 'Postaráme se. Vy podnikáte.', '/sprava-webu/', 'brincil')]

REFS = [('konradt', 'KONRADT', 'CNC obrábění a montáže', 'Technický web, který srozumitelně představí výrobu a služby.', 'https://www.konradt.cz/'),
        ('monika-velickova', 'Monika Veličková', 'Reality v Jeseníkách', 'Osobní značka makléřky postavená na znalosti regionu.', 'https://monikavelickova.cz/'),
        ('brincil', 'Břinčil', 'Technika a služby', 'Přehledná prezentace firmy a její techniky.', 'https://brincil.cz/')]

def c3_header():
    svc = ''.join(f'<a href="{u}">{n}</a>' for n, _, u, _ in SVC)
    code = ('<header class="c3-head"><a class="c3-logo" href="/" aria-label="wwwwww.cz – tvorba webových stránek">' + b.LOGO + '</a>'
            f'<a class="c3-by" href="{b.yes(x="header_v3")}" target="_blank" rel="noopener">koncept <img src="{b.YM["url"]}" alt="Yesmark" width="64" height="10"></a>'
            '<div class="c3-head__r">' + pill('Poptat web', '#poptavka', 'c3-pill--dark c3-hide-s') +
            '<button class="c3-burger" type="button" aria-expanded="false" aria-controls="c3-menu" aria-label="Menu"><i></i><i></i></button></div></header>'
            '<div class="c3-menu" id="c3-menu" aria-hidden="true"><div class="c3-menu__in">'
            '<nav class="c3-menu__main" aria-label="Hlavní navigace"><a href="/tvorba-webovych-stranek/">Služby</a><a href="/#reference">Reference</a>'
            '<a href="/weby-pro-obory/">Obory</a><a href="/kolik-stoji-web/">Ceník</a><a href="/kontakt/">Kontakt</a></nav>'
            f'<div class="c3-menu__svc">{svc}</div>'
            f'<p class="c3-menu__c"><a href="tel:{TEL}">{TEL_H}</a> · <a href="mailto:{MAIL}">{MAIL}</a></p></div></div>')
    return con('c3-headwrap', html(code), tag='div', inner=False)

def c3_hero():
    cols = ''.join(f'<div class="c3-col" style="--d:{i * -9}s"><img src="{SHOT[k]["url"]}" alt="Reference: web {n}" loading="eager"><img src="{SHOT[k]["url"]}" alt="" aria-hidden="true"></div>'
                   for i, (k, n, *_) in enumerate(REFS))
    media = (f'<div class="c3-media"><div class="c3-media__in"><div class="c3-cols">{cols}</div>'
             '<p class="c3-media__cap"><span>Weby, které jsme postavili</span><span>Konradt · Monika Veličková · Břinčil</span></p></div></div>')
    return sec('c3-hero',
        wrap('c3-hero__c',
            h('Tvorba webových stránek v Jeseníku, které prodávají.', 'h1', 'c3-h1'),
            t('<p><span>Koncept agentury Yesmark</span><span>Weby od 9 900 Kč</span><span>Jeseník · celá ČR</span></p>', 'c3-meta')),
        html(media, 'c3-media-w'), eid='uvod')

def c3_services():
    rows = ''.join(f'<a class="c3-row" href="{u}" data-img="{SHOT[k]["url"]}"><span class="c3-row__n">{n}</span><span class="c3-row__t">{tl}</span><i>→</i></a>'
                   for n, tl, u, k in SVC)
    return sec('c3-svc',
        wrap('',
            lab('Služby'),
            h('Osm způsobů, jak vám web začne vydělávat.', 'h2', 'c3-h2 c3-rv'),
            html(pill('Všechny služby', '/tvorba-webovych-stranek/', 'c3-pill--dark'), 'c3-rv'),
            html(f'<nav class="c3-rows" aria-label="Služby">{rows}</nav><div class="c3-float" aria-hidden="true"><img alt=""></div>', 'c3-rv')), eid='sluzby')

def c3_refs():
    cards = ''.join(f'<a class="c3-card" href="{u}" target="_blank" rel="noopener"><div class="c3-card__img"><img src="{SHOT[k]["url"]}" alt="Reference: web {n}" loading="lazy"></div>'
                    f'<p class="c3-card__n">{n}</p><p class="c3-card__t">{sub} – {d}</p></a>' for k, n, sub, d, u in REFS)
    cards += ('<a class="c3-card c3-card--you" href="#poptavka"><div class="c3-card__img"><span>Váš web?</span></div>'
              '<p class="c3-card__n">Další na řadě</p><p class="c3-card__t">Napište nám, co děláte. Nabídku připravíme zdarma.</p></a>')
    return sec('c3-refs c3-dark',
        wrap('',
            lab('Reference'),
            h('Weby, které pro klienty pracují každý den.', 'h2', 'c3-h2 c3-rv'),
            html(pill('Všechny reference', b.yes('reference/', 'wwwwww_reference', 'homepage_v3'), 'c3-pill--light', ext=True), 'c3-rv')),
        html(f'<div class="c3-track" tabindex="0" aria-label="Reference – posuňte do strany">{cards}</div>', 'c3-track-w'), eid='reference')

def c3_obory():
    links = ''.join(f'<a href="{u}"><span>{n}</span><i>→</i></a>' for n, u in hv2.v_obory())
    return sec('c3-obory',
        wrap('c3-two',
            con('c3-two__l', lab('Weby pro obory'), h('Co by měl mít web právě pro vás?', 'h2', 'c3-h2 c3-rv'),
                t('<p>Pro více než 70 oborů jsme sepsali checklist, ukázkovou strukturu a SEO tipy. Najděte ten svůj.</p>', 'c3-p c3-rv')),
            html(f'<nav class="c3-list" aria-label="Weby podle oboru">{links}</nav>', 'c3-rv')))

SLIDES = [('Proč wwwwww', 'Web není vizitka. Je to obchodník.', 'Každý prvek má důvod – přivést návštěvníka k telefonu nebo poptávce.', '/tvorba-webovych-stranek/', 'Jak web stavíme', 'red'),
          ('Najde vás Google', 'Aby vás našli dřív než konkurenci.', 'Weby stavíme s ohledem na vyhledávače a místní hledání – od prvního dne.', '/seo-optimalizace-webu/', 'SEO optimalizace', 'sand'),
          ('Upravíte si ho sami', 'Bez programátora, bez čekání.', 'WordPress a Elementor: texty, fotky i nové stránky změníte sami. Ukážeme vám, jak na to.', '/tvorba-webu-wordpress/', 'Weby na WordPressu', 'ink'),
          ('Člověk, ne tiket', 'Jeden člověk od kafe po spuštění.', 'Komunikujete přímo s tím, kdo web staví. Osobně v Jeseníku, nebo online odkudkoli.', '/kontakt/', 'Kontakt', 'green')]

def c3_slides():
    s = ''.join(f'<div class="c3-slide c3-slide--{c}{" is-on" if i == 0 else ""}"><p class="c3-slide__k">{k}</p><p class="c3-slide__t">{tt}</p>'
                f'<p class="c3-slide__p">{p}</p>{pill("Více", u, "c3-pill--light")}<span class="c3-slide__cap">{cap} ↗</span></div>'
                for i, (k, tt, p, u, cap, c) in enumerate(SLIDES))
    bars = ''.join('<i><b></b></i>' for _ in SLIDES)
    return sec('c3-slides', html(f'<div class="c3-show">{s}<div class="c3-bars">{bars}</div></div>'), eid='proc')

def c3_process():
    steps = [('Poznáme váš byznys', 'Projdeme cíle, zákazníky a konkurenci. Navrhneme strukturu webu a obsah, který prodává.'),
             ('Navrhneme a postavíme', 'Design na míru, programování a obsah s důrazem na detail. Průběžně vidíte, jak web roste.'),
             ('Pustíme web do světa', 'Testy na mobilech, SEO nastavení, analytika a Google Firemní profil.'),
             ('Rosteme spolu dál', 'Zabezpečení, aktualizace, úpravy obsahu, SEO a kampaně. Zůstáváme s vámi.')]
    cols = [con('c3-step c3-rv', h(f'0{i + 1}', 'div', 'c3-step__n'), h(a, 'h3', 'c3-h3'), t(f'<p>{c}</p>', 'c3-p')) for i, (a, c) in enumerate(steps)]
    return sec('c3-proc', wrap('', lab('Postup'), h('Od kafe ke spuštění.', 'h2', 'c3-h2 c3-rv'), con('c3-steps', *cols)), eid='proces')

def c3_quiz():
    return con('wv3 c3-sec c3-quiz ww-home',
        wrap('c3-two', con('c3-two__l', lab('Kvíz · 30 vteřin'), h('Jaký web potřebujete?', 'h2', 'c3-h2'),
                           t('<p>Tři otázky a dostanete doporučení na míru. Odpovědi pak jedním klikem pošlete v poptávce.</p>', 'c3-p')),
             html(b.QUIZ)), tag='section', eid='kviz', inner=False)

def c3_ba():
    return con('wv3 c3-sec c3-ba ww-home',
        wrap('c3-two',
            con('c3-two__l', lab('Redesign v praxi'), h('Před a po. Posuňte si to.', 'h2', 'c3-h2'),
                t('<p>Starý web, který nikoho nepřesvědčí, vs. moderní web, který vede k poptávce.</p>', 'c3-p'),
                html(pill('Redesign webu', '/redesign-webu/', 'c3-pill--dark'))),
            html(b.BEFORE_AFTER)), tag='section', eid='pred-a-po', inner=False)

def c3_local():
    loc = hv2.v_local()
    body = loc['elements'][0]['elements'][1]['elements'][1]['settings']['editor']   # text o Jeseníku z návrhu v2
    towns = ''.join(f'<a href="/tvorba-webovych-stranek-{c["slug"]}/">{c["name"]}</a>' for c in CITIES)
    return con('wv3 c3-sec c3-local ww-home',
        wrap('c3-two',
            con('c3-two__l', lab('Jeseník · celá ČR'), h('Tvorba webových stránek Jeseník – a kdekoli v Česku', 'h2', 'c3-h2'),
                html(b.jesenik_map(), 'c3-map')),
            con('c3-two__r', t(body, 'c3-prose'), lab('Tvoříme weby také pro'), t(f'<p>{towns}</p>', 'c3-towns'))), tag='section', eid='jesenicko', inner=False)

def c3_price(faq):
    return sec('c3-price',
        wrap('c3-two',
            con('c3-two__l', lab('Ceník'), h('<small>Tvorba webových stránek Jeseník</small>od 9 900 Kč', 'div', 'c3-price'),
                t('<p>Tvorba webových stránek Jeseník u nás nemá šablonovitý ceník. Konečná částka se odvíjí od rozsahu, funkcí a grafického zpracování. Každý projekt naceňujeme individuálně a férově.</p>', 'c3-p'),
                html(pill('Kolik stojí web', '/kolik-stoji-web/', 'c3-pill--dark'))),
            con('c3-two__r', h('Časté otázky – tvorba webových stránek Jeseník', 'h2', 'c3-h3'),
                w('toggle', 'c3-faq', faq_schema='yes', tabs=[{'_id': uid(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in faq]))), eid='cenik')

def c3_contact():
    form = b.contact_section('home')['elements'][1]['elements'][2]
    form['settings']['_css_classes'] = 'c3-form'
    return sec('c3-contact',
        wrap('c3-two',
            con('c3-two__l', lab('Poptávka'), h('Pojďme postavit váš nový web.', 'h2', 'c3-h2'),
                t('<p>Tvorba webových stránek Jeseník začíná jednou zprávou. Napište pár vět nebo rovnou zavolejte – ozvu se obvykle do jednoho pracovního dne.</p>', 'c3-p'),
                t(f'<p class="c3-big"><a href="tel:{TEL}">{TEL_H}</a><a href="mailto:{MAIL}">{MAIL}</a></p>', ''),
                con('c3-person', w('image', 'c3-person__img', image={'id': b.PHOTO_ID, 'url': b.PHOTO_URL, 'alt': 'Roman Lukač – tvorba webových stránek Jeseník', 'source': 'library'}, image_size='medium'),
                    t('<p><strong>Roman Lukač</strong><br>Webdesign a vývoj · Yesmark Jeseník</p>', 'c3-p'))),
            con('c3-two__r', form, t('<p>Údaje použijeme jen k vyřízení vaší poptávky a nikomu je neprodáváme.' + b.PRIV_LINK + '</p>', 'c3-legal'))), eid='poptavka')

def c3_footer():
    cities = ''.join(f'<a href="/tvorba-webovych-stranek-{c["slug"]}/">{c["name"]}</a>' for c in CITIES)
    svc = ''.join(f'<a href="{u}">{n}</a>' for n, _, u, _ in SVC)
    code = ('<div class="c3-foot">'
            '<nav class="c3-foot__big"><a href="/tvorba-webovych-stranek/">Služby</a><a href="/#reference">Reference</a><a href="/weby-pro-obory/">Obory</a><a href="/kontakt/">Kontakt</a></nav>'
            '<p class="c3-foot__pills">' + pill('Poptat web', '/kontakt/#poptavka', 'c3-pill--light') + f'<a href="tel:{TEL}">{TEL_H}</a><a href="mailto:{MAIL}">{MAIL}</a></p>'
            f'<div class="c3-foot__cols"><div><p class="c3-foot__k">Služby</p>{svc}</div>'
            f'<div><p class="c3-foot__k">Tvorba webových stránek v regionu</p><p class="c3-foot__cities">{cities}</p></div>'
            f'<div><p class="c3-foot__k">Yesmark</p><a href="{b.yes(x="footer_v3")}" target="_blank" rel="noopener"><img src="{b.YM["url"]}" alt="Yesmark" width="120" height="18"></a>'
            f'<span>wwwwww.cz je webový koncept agentury Yesmark. {b.ADDR}</span></div></div>'
            '<div class="c3-foot__bottom"><p>© <span data-ww-year>2026</span> wwwwww.cz · Provozovatel: Roman Lukač, IČO 14448157, Vápenná 124, 790 64 Vápenná · fyzická osoba zapsaná v živnostenském rejstříku</p>'
            f'<p>{b.PRIV_FOOT}<a href="#elementor-action%3Aaction%3DcookiezBanner%3AopenPreferences">Nastavení cookies</a></p></div></div>')
    return con('wv3 c3-footer c3-dark', html(code), tag='footer', inner=False)

def home_v3(live=False):
    """live=True: hlavička a patička jako globální šablony (hlavní stránka), jinak vše přímo ve stránce (náhled)."""
    faq = _faq()
    ld = {'@context': 'https://schema.org', '@graph': [b.BUSINESS, {'@type': 'WebSite', '@id': 'https://wwwwww.cz/#web', 'url': 'https://wwwwww.cz/', 'name': 'wwwwww.cz', 'inLanguage': 'cs-CZ', 'publisher': {'@id': 'https://wwwwww.cz/#business'}}]}
    mbar = (f'<div class="wmbar"><a class="wbtn wbtn--ghost" href="tel:{TEL}">Zavolat</a><a class="wbtn wbtn--red" href="#poptavka">Poptat web</a></div>'
            '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>')
    sysc = con('ww ww-sys wv3-sys', html(mbar + ('' if live else b.js_loader())), inner=False)
    if live:
        return [b.header(), c3_hero(), c3_services(), c3_refs(), c3_obory(), c3_slides(), c3_process(), c3_quiz(), c3_ba(),
                c3_local(), c3_price(faq), c3_contact(), b.footer(), sysc]
    return [c3_header(), c3_hero(), c3_services(), c3_refs(), c3_obory(), c3_slides(), c3_process(), c3_quiz(), c3_ba(),
            c3_local(), c3_price(faq), c3_contact(), c3_footer(), sysc]

def _faq():
    return [
        ('Kolik stojí tvorba webových stránek v Jeseníku?', 'Tvorba webových stránek začíná na 9 900 Kč. Konečná cena záleží na rozsahu, funkcích a grafickém zpracování. Po krátké konzultaci dostanete nezávaznou cenovou nabídku zdarma.'),
        ('Jak dlouho trvá vytvoření webu?', 'Jednodušší prezentační web bývá hotový zhruba za 2–4 týdny, web na míru nebo e-shop podle rozsahu za 4–8 týdnů. Přesný harmonogram dostanete v nabídce.'),
        ('Budu si moci web upravovat sám?', 'Ano. Stavíme na WordPressu a Elementoru, pro zcela individuální projekty na October CMS. Texty, fotky i nové stránky si pohodlně upravíte sami a ukážeme vám, jak na to.'),
        ('Jaký je vztah wwwwww.cz a agentury Yesmark?', 'wwwwww.cz je webový koncept marketingové agentury Yesmark z Jeseníku. Za weby stojí stejný tým – a když budete chtít, navážeme grafikou, kampaněmi nebo reklamními předměty.'),
        ('Děláte weby i pro klienty mimo Jesenicko?', 'Ano. Sídlíme v Jeseníku, ale weby tvoříme pro klienty z celého Česka – konzultace, návrhy i předání zvládneme online. Místní firmy rádi potkáme osobně.'),
        ('Postaráte se i o SEO, doménu a hosting?', 'Ano. Každý web stavíme s ohledem na vyhledávače, pomůžeme s doménou i hostingem a po spuštění zajistíme správu, zabezpečení i propagaci.'),
    ]

if __name__ == '__main__':
    d = home_v3()
    (b.OUT / 'home-v3.json').write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    (b.OUT / 'home-v3.html').write_text(b.to_html(d), encoding='utf-8')
    # hlavní stránka (globální hlavička a patička)
    d = home_v3(live=True)
    (b.OUT / 'home.json').write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    (b.OUT / 'home.html').write_text(b.to_html(d), encoding='utf-8')
    print('home-v3', len(json.dumps(d)) // 1024, 'kB')
