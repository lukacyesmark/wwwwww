# Návrh nové hlavní stránky (redakční styl). Staví na pomocných funkcích z build.py.
# Výstup: out/home-v2.json a out/home-v2.html. Třídy začínají "v-", sekce mají třídu "wv2".
import json, sys, importlib.util, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
_spec = importlib.util.spec_from_file_location('b', HERE / 'build.py')
b = importlib.util.module_from_spec(_spec)
if len(sys.argv) < 3:
    sys.argv = ['x', '23', 'https://wwwwww.cz/wp-content/uploads/2026/10/roman-lukac-tvorba-webu-jesenik.jpg']
_spec.loader.exec_module(b)
con, w, h, t, btn, html, img, uid = b.con, b.w, b.h, b.t, b.btn, b.html, b.img, b.uid
TEL, TEL_H, MAIL, SHOT, CITIES = b.TEL, b.TEL_H, b.MAIL, b.SHOT, b.CITIES

def vsec(cls, *kids, eid=None, tag='section'):
    return con('wv2 v-sec ' + cls, *kids, tag=tag, eid=eid, inner=False)

def vwrap(cls, *kids):
    return con('v-wrap ' + cls, *kids)

def label(text, cls=''):
    return h(text, 'div', 'v-label ' + cls)

# velké logo wwwwww: první půlka světlá (na tmavé ploše), druhá červená
def bigmark(cls='v-bigmark'):
    return (f'<svg class="{cls}" viewBox="0 0 169 20" preserveAspectRatio="xMidYMid meet" aria-hidden="true">'
            '<defs><clipPath id="vbm"><rect x="-2" y="0" width="173" height="20"/></clipPath></defs>'
            '<g clip-path="url(#vbm)" fill="none" stroke-width="4.2" stroke-linejoin="miter" stroke-miterlimit="10">'
            '<path class="a" d="M0.25 -4.00 L6.38 24.00 L12.75 -4.00 L19.12 24.00 L25.25 -4.00 M28.95 -4.00 L35.08 24.00 L41.45 -4.00 L47.83 24.00 L53.95 -4.00 M57.65 -4.00 L63.77 24.00 L70.15 -4.00 L76.53 24.00 L82.65 -4.00"/>'
            '<path class="b" d="M86.35 -4.00 L92.47 24.00 L98.85 -4.00 L105.22 24.00 L111.35 -4.00 M115.05 -4.00 L121.17 24.00 L127.55 -4.00 L133.93 24.00 L140.05 -4.00 M143.75 -4.00 L149.88 24.00 L156.25 -4.00 L162.62 24.00 L168.75 -4.00"/>'
            '</g></svg>')

SLUZBY_MENU = [('Tvorba webových stránek', '/tvorba-webovych-stranek/'), ('Web na míru', '/tvorba-webu-na-miru/'),
               ('WordPress', '/tvorba-webu-wordpress/'), ('E-shopy', '/tvorba-eshopu/'), ('Redesign webu', '/redesign-webu/'),
               ('SEO optimalizace', '/seo-optimalizace-webu/'), ('Správa webu', '/sprava-webu/'), ('Firemní web', '/firemni-web/')]

def v_header():
    small = b.LOGO
    svc = ''.join(f'<a href="{u}">{n}</a>' for n, u in SLUZBY_MENU)
    code = ('<div class="v-head">'
            '<button class="v-tab v-tab--menu" type="button" aria-expanded="false" aria-controls="v-menu"><span class="v-burg"><i></i><i></i></span><span class="v-tab__t">Menu</span></button>'
            f'<div class="v-markw"><a class="v-mark" href="/" aria-label="wwwwww.cz – tvorba webových stránek">{small}</a>'
            f'<a class="v-by" href="{b.yes(x="header_logo_v2")}" target="_blank" rel="noopener"><small>koncept</small><img src="{b.YM["url"]}" alt="Yesmark" width="70" height="11"></a></div>'
            '<a class="v-tab v-tab--cta" href="#poptavka">Máte projekt?</a>'
            '</div>'
            '<div class="v-menu" id="v-menu" aria-hidden="true"><div class="v-menu__in">'
            '<nav class="v-menu__main" aria-label="Hlavní navigace">'
            '<a href="/tvorba-webovych-stranek/"><small>01</small>Služby</a><a href="/#reference"><small>02</small>Reference</a>'
            '<a href="/kolik-stoji-web/"><small>03</small>Ceník</a><a href="/weby-pro-obory/"><small>04</small>Obory</a><a href="/kontakt/"><small>05</small>Kontakt</a></nav>'
            f'<div class="v-menu__side"><p class="v-menu__k">Služby</p><div class="v-menu__svc">{svc}</div>'
            f'<p class="v-menu__k">Kontakt</p><p class="v-menu__contact"><a href="tel:{TEL}">{TEL_H}</a><a href="mailto:{MAIL}">{MAIL}</a></p>'
            '<p class="v-menu__note">wwwwww.cz je webový koncept agentury Yesmark z Jeseníku.</p></div>'
            '</div></div>')
    return con('v-headwrap', html(code), tag='div', inner=False)

def v_hero():
    shape = ('<svg class="v-shape" viewBox="0 0 1440 900" preserveAspectRatio="none" aria-hidden="true">'
             '<path d="M-40 300 L690 380 Q725 384 742 352 L930 -40 L1360 -40 L820 420 Q790 445 798 480 L900 960 L-40 960 Z"/></svg>')
    return vsec('v-hero',
        html(shape, 'v-hero__bg'),
        vwrap('v-hero__grid',
            con('v-hero__l', label('Tvorba webových stránek Jeseník · koncept Yesmark', 'v-hero__k'), h('Tvorba webových stránek v Jeseníku, které prodávají.', 'h1', 'v-h1')),
            con('v-hero__r',
                t('<p>Navrhneme a postavíme <strong>web nebo e-shop na míru</strong>, který zaujme, dobře se najde na Googlu a z návštěvníků dělá zákazníky. Z Jeseníku pro celé Česko.</p>', 'v-lead'),
                t(f'<p><a class="v-link" href="#poptavka">Nezávazná nabídka</a><a class="v-link" href="tel:{TEL}">{TEL_H}</a></p>', 'v-hero__links'))),
        html(bigmark(), 'v-hero__mark'), eid='uvod')

def v_statement():
    return vsec('v-statement',
        vwrap('', h('Navrženo tak, aby si vás zapamatovali. Stavíme weby, které zákazníci nejen projdou, ale ozvou se.', 'h2', 'v-giant v-clip')))

def v_yesmark():
    return vsec('v-yes v-dark',
        vwrap('v-yes__grid',
            con('v-yes__logo', label('Webový koncept agentury'), img(b.YM, 'Yesmark – marketingová agentura Jeseník', 'v-yes__img')),
            t('<p>Za wwwwww.cz stojí tým <strong>agentury Yesmark</strong> z Jeseníku. Stejné know-how jako u kampaní, grafiky a SEO pro naše klienty – jen s jasným zaměřením na weby. Když budete chtít, navážeme brandingem, kampaněmi i tiskem.</p>', 'v-serif v-serif--m'),
            t(f'<p><a class="v-btn v-btn--light" href="{b.yes(x="homepage_v2_strip")}" target="_blank" rel="noopener">Poznejte Yesmark ↗</a></p>', 'v-yes__cta')))

def v_marquee():
    towns = ['Jeseník', 'Lipová-lázně', 'Zlaté Hory', 'Javorník', 'Mikulovice', 'Vidnava', 'Žulová', 'Bělá pod Pradědem', 'Česká Ves', 'Velké Losiny', 'Hanušovice', 'Ramzová']
    code = '<div class="mq" aria-hidden="true"><div class="mq__t">' + ''.join(f'<span>{x}</span>' for x in towns * 2) + '</div></div>'
    return con('wv2 v-mq ww-home', html(code), tag='div', inner=False)

def v_why():
    pts = [('Design, který prodává', 'Každý prvek má důvod – přivést návštěvníka k telefonu nebo poptávce. Žádné hezké, ale prázdné stránky.'),
           ('Najde vás Google', 'Weby stavíme s ohledem na vyhledávače a místní hledání. Aby vás našli lidé z Jeseníku i turisté z celé republiky.'),
           ('Upravíte si ho sami', 'WordPress a Elementor: texty, fotky i nové stránky změníte sami. Ukážeme vám, jak na to.'),
           ('Člověk, ne tiket', 'Komunikujete přímo s tím, kdo web staví. Osobní schůzka v Jeseníku, nebo online hovor odkudkoli.')]
    cols = [con('v-why__i ww-rv', h(f'{i + 1:02d}', 'div', 'v-step__n'), h(a, 'h3', 'v-step__t'), t(f'<p>{c}</p>', 'v-small')) for i, (a, c) in enumerate(pts)]
    return vsec('v-why',
        vwrap('', label('Proč wwwwww'),
              h('Web není vizitka. Je to <em>obchodník</em>, který pro vás pracuje 24/7.', 'h2', 'v-statement2 ww-rv'),
              con('v-steps v-why__grid', *cols)))

def v_ba():
    return con('wv2 v-sec v-basec2 v-dark ww-home',
        vwrap('v-ba2',
            con('v-ba2__copy ww-rv', label('Redesign v praxi'), h('Před a po. Posuňte si to.', 'h2', 'v-h2'),
                t('<p>Starý web, který nikoho nepřesvědčí, vs. moderní web, který vede k poptávce. Chyťte jezdec a porovnejte – takhle vypadá rozdíl, který zákazník pozná za pár vteřin.</p>', 'v-serif v-serif--m'),
                t('<p><a class="v-more" href="/redesign-webu/"><span>Chci redesign webu</span><i>→</i></a></p>', 'v-more-w')),
            html(b.BEFORE_AFTER, 'ww-rv')), tag='section', eid='pred-a-po', inner=False)

def v_highlight():
    refs = [
        ('konradt', 'KONRADT', 'CNC obrábění a montáže', 'Pro společnost KONRADT jsme vytvořili nové webové stránky zaměřené na profesionální prezentaci služeb v oblasti CNC obrábění, montáže a zpracování kovů. Důraz jsme kladli na moderní technický vzhled, přehledné představení výrobních možností a srozumitelnou prezentaci služeb. Součástí byla i optimalizace struktury a obsahu pro lepší dohledatelnost CNC frézování, soustružení, montážních prací a dodávek odlitků.', 'https://www.konradt.cz/', 'Web · CNC obrábění', 'konradt.cz'),
        ('monika-velickova', 'Monika Veličková', 'Reality v Jeseníkách', 'Pro realitní makléřku Moniku Veličkovou jsme vytvořili nové webové stránky zaměřené na prezentaci nemovitostí a realitních služeb v Jeseníkách. Důraz jsme kladli na moderní a osobitý design, přehlednou prezentaci nabízených nemovitostí a především na budování osobní značky, která staví na znalosti regionu, individuálním přístupu a zkušenostech s realitami i investicemi.', 'https://monikavelickova.cz/', 'Web · Reality Jeseníky', 'monikavelickova.cz'),
        ('brincil', 'Břinčil', 'Technika a služby', 'Při realizaci webu pro firmu Břinčil jsme kladli důraz na moderní a přehledný design, snadnou orientaci návštěvníků a kvalitní prezentaci společnosti i její techniky. Nový web zároveň slouží jako podpůrná prezentace hlavní společnosti Břinčil &amp; Míka s.r.o., pro kterou jsme v minulosti rovněž realizovali kompletní online prezentaci.', 'https://brincil.cz/', 'Web · Technika a služby', 'brincil.cz')]
    slides = ''
    for i, (k, name, sub, text, url, t1, t2) in enumerate(refs):
        slides += (f'<article class="v-hl__slide{" is-on" if i == 0 else ""}" data-i="{i}">'
                   f'<img class="v-hl__img" src="{SHOT[k]["url"]}" alt="Reference: web {name}" loading="lazy">'
                   f'<div class="v-hl__body"><p class="v-hl__k">Vybraná realizace</p>'
                   f'<h3 class="v-hl__t">{name}: {sub}.</h3>'
                   f'<div class="v-hl__meta"><span>{t1}</span><span>{t2}</span><p>{text}</p></div>'
                   f'<a class="v-btn v-btn--light" href="{url}" target="_blank" rel="noopener">Zobrazit web ↗</a></div></article>')
    ctrl = ('<div class="v-hl__ctrl"><button type="button" class="v-sq" data-dir="-1" aria-label="Předchozí reference">←</button>'
            '<button type="button" class="v-sq" data-dir="1" aria-label="Další reference">→</button>'
            f'<span class="v-hl__count"><b>01</b> / 0{len(refs)}</span>'
            f'<a class="v-btn v-btn--light v-hl__all" href="{b.yes("reference/", "wwwwww_reference", "homepage_v2")}" target="_blank" rel="noopener">Všechny reference</a></div>')
    return vsec('v-hl', html(f'<div class="v-hl__stage">{slides}</div>{ctrl}'), eid='reference')

def v_obory():
    items = [('Instalatéry a řemeslníky', '/web-pro-instalater/'), ('Penziony a chaty', '/web-pro-penzion/'), ('Kadeřnictví a salony', '/web-pro-kadernictvi/'),
             ('Restaurace a kavárny', '/web-pro-restaurace/'), ('Stavební firmy', '/web-pro-stavebni-firma/'), ('Výrobní firmy', '/web-pro-strojirenska-firma/'),
             ('Obce a spolky', '/web-pro-obec/'), ('Realitní makléře', '/web-pro-realitni-makler/'), ('Svatby', '/svatebni-web/'), ('…a dalších 60 oborů', '/weby-pro-obory/')]
    return items

def v_list(items):
    links = ''.join(f'<a href="{u}"><span>{n}</span><i>→</i></a>' for n, u in items)
    return vsec('v-list v-dark',
        vwrap('v-list__grid',
            con('v-list__l', t('<p>Weby stavíme pro</p>', 'v-serif v-serif--l'),
                t('<p>Pro více než 70 oborů jsme sepsali, co by měl jejich web mít. Vyberte si ten svůj.</p>', 'v-small')),
            html(f'<nav class="v-biglist" aria-label="Weby podle oboru">{links}</nav>')))

SVC = [
    ('Weby', 'Tvorba webových stránek na míru', 'Od jednoduché firemní prezentace po rozsáhlý web. Moderní design, srozumitelný obsah a jasná cesta k poptávce – web, který vám dělá dobré jméno i obchod.', '/tvorba-webovych-stranek/', 'shot:konradt', ['UX &amp; UI design', 'Kódování na míru', 'WordPress + Elementor', 'October CMS', 'Responzivní design']),
    ('E-shopy', 'E-shopy, WooCommerce, PrestaShop', 'Přehledný obchod připravený na růst. Objednávky, platby i doprava bez starostí – a administrace, kterou zvládnete sami.', '/tvorba-eshopu/', 'shop', ['WooCommerce', 'PrestaShop']),
    ('Redesign', 'Nový web místo starého', 'Starý web, který nic nepřináší? Převlékneme ho do moderního kabátu a postavíme znovu – tentokrát na prodej a bez ztráty pozic v Googlu.', '/redesign-webu/', 'shot:monika-velickova', ['Nový design', 'Nový obsah']),
    ('SEO', 'SEO optimalizace a lokální SEO', 'Struktura, obsah a technické SEO od prvního dne, aby vás zákazníci našli dřív než konkurenci.', '/seo-optimalizace-webu/', 'serp', ['On-page SEO', 'Google Firemní profil']),
    ('Správa', 'Správa a propagace', 'Aktualizace, zabezpečení, úpravy obsahu i PPC kampaně. Zůstáváme s vámi i po spuštění.', '/sprava-webu/', 'photo', ['Údržba', 'PPC kampaně']),
    ('Grafika', 'Grafika a branding', 'Logo, vizuální styl a grafika pro web i tisk – všechno pod jednou střechou Yesmark.', 'yesmark', 'brand', ['Logo', 'Vizuální styl']),
]

def svc_visual(kind, name):
    if kind.startswith('shot:'):
        k = kind[5:]
        return f'<div class="v-vis v-vis--shot"><img src="{SHOT[k]["url"]}" alt="{name} – ukázka webu" loading="lazy"></div>'
    if kind == 'photo':
        return f'<div class="v-vis v-vis--photo"><img src="{b.PHOTO_URL}" alt="Roman Lukač – správa webu" loading="lazy"></div>'
    if kind == 'brand':
        return (f'<div class="v-vis v-vis--brand" aria-hidden="true"><div class="v-brand__logo">{b.LOGO}</div>'
                '<div class="v-brand__sw"><i style="background:#161616"></i><i style="background:#e3120b"></i><i style="background:#b3b3b3"></i><i style="background:#f2efea"></i></div>'
                '<p class="v-brand__type">Aa <span>Inter Tight</span></p></div>')
    if kind == 'shop':
        cards = ''.join(f'<div class="v-shop__p"><i></i><b>{n}</b><span>{p}</span></div>' for n, p in [('Lněná košile', '1 290 Kč'), ('Keramický hrnek', '390 Kč'), ('Svíčka Jeseníky', '249 Kč'), ('Dárkový set', '890 Kč')])
        return (f'<div class="v-vis v-vis--shop" aria-hidden="true"><div class="v-shop__bar"><b>obchod<em>.</em>cz</b><span>Košík <em>2</em></span></div>'
                f'<div class="v-shop__grid">{cards}</div></div>')
    if kind == 'serp':
        res = [('wwwwww.cz › tvorba-webovych-stranek', 'Tvorba webových stránek Jeseník | weby od 9 900 Kč', 'Navrhneme a postavíme web, který zaujme a dobře se najde na Googlu…', True),
               ('example.cz › weby', 'Webové stránky – šablony a stavebnice', 'Vytvořte si web sami za pár minut…', False),
               ('example2.cz', 'Tvorba webů – katalog firem', 'Seznam firem v oboru tvorba webu…', False)]
        rows = ''.join(f'<div class="v-serp__r{" is-me" if me else ""}"><small>{u}</small><b>{tt}</b><span>{d}</span></div>' for u, tt, d, me in res)
        return f'<div class="v-vis v-vis--serp" aria-hidden="true"><div class="v-serp__q">tvorba webových stránek jeseník</div>{rows}</div>'
    return ''

def v_services():
    panels = []
    for i, (word, sub, text, url, vis, tg) in enumerate(SVC):
        ext = url == 'yesmark'
        if ext: url = b.yes(x='homepage_v2_grafika')
        panels.append(con(f'v-svc v-svc--{i % 3}',
            vwrap('v-svc__in',
                h(word, 'h2', 'v-svc__word'),
                con('v-svc__row',
                    h(f'{i + 1:02d}', 'div', 'v-svc__num'),
                    con('v-svc__txt', h(sub, 'h3', 'v-serif v-serif--m'), t(f'<p>{text}</p>', 'v-body'),
                        t('<p>' + ''.join(f'<span>{x}</span>' for x in tg) + '</p>', 'v-chips'),
                        t(f'<p><a class="v-more" href="{url}"' + (' target="_blank" rel="noopener"><span>Yesmark.eu</span><i>↗</i>' if ext else '><span>Více o službě</span><i>→</i>') + '</a></p>', 'v-more-w')),
                    html(svc_visual(vis, sub), 'v-svc__vis')))))
    return con('wv2 v-svcs', *panels, tag='section', eid='sluzby', inner=False)

NUMS = [('9 900', 'Kč', 'Nový web už od', 'Tolik stojí základní web. Přesnou cenu podle rozsahu dostanete v nabídce zdarma.'),
        ('1', '', 'Člověk, ne tiket', 'Jeden člověk od prvního kafe po spuštění. Žádné předávání mezi odděleními.'),
        ('2–4', 'týdny', 'Do spuštění', 'Tak dlouho obvykle trvá jednodušší web. E-shop nebo web na míru 4–8 týdnů.')]

def v_numbers():
    items = ''.join(f'<div class="v-num__i" data-i="{i}"><p class="v-num__label">{l}</p><p class="v-num__big">{n}<sup>{u}</sup></p><p class="v-num__cap">{c}</p></div>'
                    for i, (n, u, l, c) in enumerate(NUMS))
    ghost = ''.join(f'<span>{n}</span>' for n, *_ in NUMS)
    code = (f'<div class="v-num" style="--n:{len(NUMS)}"><div class="v-num__stick">'
            f'<div class="v-num__ghost" aria-hidden="true">{ghost}</div>'
            f'<figure class="v-num__photo"><img src="{b.PHOTO_URL}" alt="Roman Lukač – webdesign a vývoj, Yesmark Jeseník" loading="lazy"></figure>'
            f'<div class="v-num__items">{items}</div></div></div>')
    return vsec('v-numsec', html(code))

def v_process():
    steps = [('Analýza a návrh', 'Poznáme váš byznys', 'Projdeme vaše cíle, zákazníky a konkurenci. Navrhneme strukturu webu a obsah, který prodává – šablonové řešení, nebo kódování na míru.'),
             ('Design a realizace', 'Navrhneme a postavíme', 'Design na míru, programování a obsah s důrazem na detail. Průběžně vidíte, jak web roste, a můžete říct svůj názor.'),
             ('Spuštění', 'Pustíme web do světa', 'Testy na mobilech i počítačích, SEO nastavení, analytika a Google Firemní profil. Pak teprve jde web ven.'),
             ('Správa a propagace', 'Rosteme spolu dál', 'Zabezpečení, aktualizace, úpravy obsahu, SEO a placená propagace. Zůstáváme s vámi i po spuštění.')]
    cols = [con('v-step ww-rv', h(f'{i + 1:02d} / {k}', 'div', 'v-step__n'), h(a, 'h3', 'v-step__t'), t(f'<p>{c}</p>', 'v-small')) for i, (k, a, c) in enumerate(steps)]
    return vsec('v-proc',
        vwrap('', con('v-row2 ww-rv', h('Od kafe ke spuštění.', 'h2', 'v-h2'),
                      t('<p>Jasný postup bez překvapení. Víte, co se děje, kdy to bude a kolik to stojí.</p>', 'v-serif v-serif--m')),
              con('v-steps', *cols)), eid='proces')

def v_local():
    towns = ''.join(f'<a href="/tvorba-webovych-stranek-{c["slug"]}/">{c["name"]}</a>' for c in CITIES)
    body = ('<p>Jsme <strong>webové studio z Jeseníku</strong> a koncept agentury Yesmark. Weby tvoříme pro firmy, řemeslníky, ubytování, gastro i realitní kanceláře z Jeseníku, Lipové-lázní, Zlatých Hor, Javorníku či Mikulovic – a stejně tak pro klienty z Olomouce, Ostravy, Prahy nebo Brna.</p>'
            '<p>Tvorba webových stránek Jeseník pro nás znamená víc než hezký design: web musí být dohledatelný na Googlu, srozumitelný na mobilu a vést návštěvníka k poptávce.</p>'
            '<h3>Weby pro ubytování a turistický ruch v Jeseníkách</h3><p>Penziony, apartmány a chaty potřebují web, který zaujme fotkami, jasně ukáže ceny a vede k rezervaci – v češtině, němčině i polštině.</p>'
            '<h3>Weby pro řemeslníky, služby a výrobní firmy z Jesenicka</h3><p>Instalatér z Jeseníku, truhlář ze Zlatých Hor nebo strojírna z Javorníku – každý potřebuje web, který se ukáže, když ho místní zákazník hledá na Googlu.</p>'
            f'<h3>Osobně v Jeseníku, online kdekoli v Česku</h3><p>Sídlíme v Jeseníku ({b.ADDR}). Místní klienty rádi potkáme u nás v kanceláři, s ostatními vše vyřešíme přes videohovor, telefon a sdílený návrh.</p>')
    return con('wv2 v-sec v-local ww-home',
        vwrap('v-local__grid',
            con('v-local__l ww-rv', label('Jeseník · celá ČR'), h('Tvorba webových stránek Jeseník – a kdekoli v Česku', 'h2', 'v-h2'),
                html(b.jesenik_map(), 'ww-rv v-map')),
            con('v-local__r ww-rv', t('<p>Sídlíme pod Pradědem. Weby ale stavíme pro klienty z celé republiky – osobně, nebo online.</p>', 'v-serif v-serif--m'),
                t(body, 'v-body v-prose'),
                label('Tvoříme weby také pro'), t(f'<p>{towns}</p>', 'v-towns'))), tag='section', eid='jesenicko', inner=False)

def v_quiz():
    return con('wv2 v-sec v-quizsec v-dark ww-home',
        vwrap('', con('v-row2 ww-rv', h('Jaký web potřebujete?', 'h2', 'v-h2'),
                      t('<p>Tři otázky, třicet vteřin. Dostanete doporučení na míru a odpovědi pak jedním klikem pošlete v poptávce.</p>', 'v-serif v-serif--m')),
              html(b.QUIZ, 'ww-rv')), tag='section', eid='kviz', inner=False)

def v_price(faq):
    return vsec('v-price',
        vwrap('v-price__grid',
            con('v-price__l ww-rv', label('Ceník'), h('<small>Tvorba webových stránek Jeseník</small>od 9 900 Kč', 'div', 'v-price__num'),
                t('<p>Tvorba webových stránek Jeseník u nás nemá šablonovitý ceník. Konečná částka se odvíjí od rozsahu, funkcí a grafického zpracování. Každý projekt naceňujeme individuálně a férově.</p>', 'v-body'),
                t('<p><a class="v-more" href="/kolik-stoji-web/"><span>Kolik stojí web</span><i>→</i></a></p>', 'v-more-w')),
            con('v-price__r ww-rv', h('Časté otázky – tvorba webových stránek Jeseník', 'h2', 'v-h3'),
                w('toggle', 'v-faq', faq_schema='yes', tabs=[{'_id': uid(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in faq]))), eid='cenik')

def v_contact():
    form = b.contact_section('home')['elements'][1]['elements'][2]
    form['settings']['_css_classes'] = 'v-form'
    return vsec('v-contact',
        vwrap('',
            h('Máte projekt?', 'h2', 'v-giant v-giant--l ww-rv'),
            con('v-contact__grid',
                con('v-contact__l ww-rv',
                    t('<p>Tvorba webových stránek Jeseník začíná jednou zprávou. Napište pár vět nebo rovnou zavolejte – ozvu se obvykle do jednoho pracovního dne.</p>', 'v-serif v-serif--m'),
                    t(f'<p class="v-contact__big"><a href="tel:{TEL}">{TEL_H}</a><a href="mailto:{MAIL}">{MAIL}</a></p>', 'v-contact__links'),
                    con('v-person', w('image', 'v-person__img', image={'id': b.PHOTO_ID, 'url': b.PHOTO_URL, 'alt': 'Roman Lukač – tvorba webových stránek Jeseník', 'source': 'library'}, image_size='medium'),
                        t('<p><strong>Roman Lukač</strong><br>Webdesign a vývoj · Yesmark Jeseník</p>', 'v-small'))),
                con('v-contact__r ww-rv', form,
                    t('<p>Údaje použijeme jen k vyřízení vaší poptávky a nikomu je neprodáváme.' + b.PRIV_LINK + '</p>', 'v-legal')))), eid='poptavka')

def v_footer():
    links = lambda items: ''.join(f'<a href="{u}">{n}</a>' for n, u in items)
    cities = ''.join(f'<a href="/tvorba-webovych-stranek-{c["slug"]}/">{c["name"]}</a>' for c in CITIES)
    code = ('<div class="v-foot">'
            '<div class="v-foot__cta"><p class="v-foot__k">Nový web?</p>'
            f'<a class="v-foot__big" href="tel:{TEL}">Začneme jedním telefonátem.</a></div>'
            '<div class="v-foot__cols">'
            f'<div><p class="v-foot__k">Služby</p>{links(SLUZBY_MENU)}</div>'
            f'<div><p class="v-foot__k">Odkazy</p>{links([("Weby pro obory", "/weby-pro-obory/"), ("Kolik stojí web", "/kolik-stoji-web/"), ("Kontakt", "/kontakt/")])}'
            f'<a href="{b.yes("reference/", "wwwwww_reference", "footer")}" target="_blank" rel="noopener">Reference ↗</a><a href="{b.yes(x="footer")}" target="_blank" rel="noopener">Yesmark.eu ↗</a></div>'
            f'<div><p class="v-foot__k">Kontakt</p><a href="tel:{TEL}">+420 {TEL_H}</a><a href="mailto:{MAIL}">{MAIL}</a><span>Yesmark, {b.ADDR}</span></div>'
            f'<div class="v-foot__cities"><p class="v-foot__k">Tvorba webových stránek v regionu</p><p>{cities}</p></div></div>'
            f'<div class="v-foot__yes"><span>wwwwww.cz je webový koncept agentury</span><a href="{b.yes(x="footer_v2")}" target="_blank" rel="noopener"><img src="{b.YM["url"]}" alt="Yesmark" width="140" height="21"></a></div>'
            f'<div class="v-foot__mark">{bigmark("v-bigmark v-bigmark--foot")}</div>'
            '<div class="v-foot__bottom"><p>© <span data-ww-year>2026</span> wwwwww.cz · koncept Yesmark · Provozovatel: Roman Lukač, IČO 14448157, Vápenná 124, 790 64 Vápenná · fyzická osoba zapsaná v živnostenském rejstříku</p>'
            f'<p>{b.PRIV_FOOT}<a href="#elementor-action%3Aaction%3DcookiezBanner%3AopenPreferences">Nastavení cookies</a></p></div></div>')
    return con('wv2 v-footer v-dark', html(code), tag='footer', inner=False)

def home_v2():
    faq = [
        ('Kolik stojí tvorba webových stránek v Jeseníku?', 'Tvorba webových stránek začíná na 9 900 Kč. Konečná cena záleží na rozsahu, funkcích a grafickém zpracování. Po krátké konzultaci dostanete nezávaznou cenovou nabídku zdarma.'),
        ('Jak dlouho trvá vytvoření webu?', 'Jednodušší prezentační web bývá hotový zhruba za 2–4 týdny, web na míru nebo e-shop podle rozsahu za 4–8 týdnů. Přesný harmonogram dostanete v nabídce.'),
        ('Budu si moci web upravovat sám?', 'Ano. Stavíme na WordPressu a Elementoru, pro zcela individuální projekty na October CMS. Texty, fotky i nové stránky si pohodlně upravíte sami a ukážeme vám, jak na to.'),
        ('Jaký je vztah wwwwww.cz a agentury Yesmark?', 'wwwwww.cz je webový koncept marketingové agentury Yesmark z Jeseníku. Za weby stojí stejný tým – a když budete chtít, navážeme grafikou, kampaněmi nebo reklamními předměty.'),
        ('Děláte weby i pro klienty mimo Jesenicko?', 'Ano. Sídlíme v Jeseníku, ale weby tvoříme pro klienty z celého Česka – konzultace, návrhy i předání zvládneme online. Místní firmy rádi potkáme osobně.'),
        ('Postaráte se i o SEO, doménu a hosting?', 'Ano. Každý web stavíme s ohledem na vyhledávače, pomůžeme s doménou i hostingem a po spuštění zajistíme správu, zabezpečení i propagaci.'),
    ]
    ld = {'@context': 'https://schema.org', '@graph': [b.BUSINESS, {'@type': 'WebSite', '@id': 'https://wwwwww.cz/#web', 'url': 'https://wwwwww.cz/', 'name': 'wwwwww.cz', 'inLanguage': 'cs-CZ', 'publisher': {'@id': 'https://wwwwww.cz/#business'}}]}
    sysc = b.system(ld, '<a class="wbtn wbtn--red" href="#poptavka">Poptat web</a>')
    return [b.header(), v_hero(), v_marquee(), v_statement(), v_yesmark(), v_highlight(), v_list(v_obory()), v_services(), v_why(), v_numbers(), v_process(),
            v_ba(), v_local(), v_quiz(), v_price(faq), v_contact(), b.footer(), sysc]

if __name__ == '__main__':
    d = home_v2()
    (b.OUT / 'home-v2.json').write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    (b.OUT / 'home-v2.html').write_text(b.to_html(d), encoding='utf-8')
    # nový design je hlavní stránka
    (b.OUT / 'home.json').write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    (b.OUT / 'home.html').write_text(b.to_html(d), encoding='utf-8')
    print('home-v2', len(json.dumps(d)) // 1024, 'kB')
