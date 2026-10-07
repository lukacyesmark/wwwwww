"""Sestaví Elementor data (_elementor_data) pro stránky wwwwww.cz.

Výstup: wordpress/elementor/out/{home,kontakt}.json
Texty jsou v nativních widgetech (nadpis, text, tlačítko, formulář…), takže se dají upravovat v Elementoru.
Vzhled řeší globální CSS (ww.css) přes třídy „ww-…“.

Použití: python3 build.py <ID fotky v knihovně> <URL fotky>
"""
import base64, json, pathlib, random, sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'out'
OUT.mkdir(exist_ok=True)
PHOTO_ID = int(sys.argv[1]) if len(sys.argv) > 1 else 0
PHOTO_URL = sys.argv[2] if len(sys.argv) > 2 else ''
MEDIA = json.loads((HERE / 'media.json').read_text(encoding='utf-8'))
YM = MEDIA['yesmark-logo.png']
SHOT = {k: MEDIA[f'reference-{k}-web.jpg'] for k in ('konradt', 'monika-velickova', 'brincil')}
def img(m, alt, cls='', size='full'):
    return w('image', cls, image={'id': m['id'], 'url': m['url'], 'alt': alt, 'source': 'library'}, image_size=size)

TEL, TEL_H, MAIL = '+420731842606', '731 842 606', 'lukac@yesmark.eu'
ADDR = 'Boženy Němcové 922/2, 790 01 Jeseník'
UTM = 'utm_source=wwwwww.cz&utm_medium=referral&utm_campaign={c}&utm_content={x}'
def yes(path='', c='wwwwww_brand', x='web'):
    return f'https://yesmark.eu/{path}?' + UTM.format(c=c, x=x)

from cities import CITIES

def city_links(cls='ww-towns ww-citylinks', current=None):
    items = ''.join(f'<a href="/tvorba-webovych-stranek-{c["slug"]}/">{c["name"]}</a>' for c in CITIES if c['slug'] != current)
    return t(f'<p>{items}</p>', cls)

PRIVACY_PUBLISHED = True
PRIV_URL = '/zasady-ochrany-osobnich-udaju/'
PRIV_LINK = f' <a href="{PRIV_URL}">Zásady ochrany osobních údajů</a>' if PRIVACY_PUBLISHED else ''
PRIV_FOOT = f'<a href="{PRIV_URL}">Ochrana osobních údajů</a> · ' if PRIVACY_PUBLISHED else ''

_seen = set()
def uid():
    while True:
        i = '%07x' % random.randrange(16 ** 7)
        if i not in _seen:
            _seen.add(i); return i

# ---------- Elementor stavební bloky ----------
def con(cls, *kids, tag='div', eid=None, inner=True):
    s = {'content_width': 'full', 'flex_direction': 'column', 'css_classes': 'ww-c ' + cls, 'html_tag': tag}
    if eid: s['_element_id'] = eid
    return {'id': uid(), 'elType': 'container', 'isInner': inner, 'settings': s, 'elements': [k for k in kids if k]}

def sec(cls, *kids, tag='section', eid=None):
    return con('ww ww-sec ' + cls, *kids, tag=tag, eid=eid, inner=False)

def wrap(cls, *kids):
    return con('ww-wrap ' + cls, *kids)

def w(kind, cls='', **s):
    if cls: s['_css_classes'] = cls
    return {'id': uid(), 'elType': 'widget', 'widgetType': kind, 'settings': s, 'elements': []}

def h(text, size='h2', cls=''):
    return w('heading', cls, title=text, header_size=size)

def t(html, cls=''):
    return w('text-editor', cls, editor=html)

def btn(text, url, cls='', ext=False):
    return w('button', cls, text=text, link={'url': url, 'is_external': 'on' if ext else '', 'nofollow': ''})

def html(code, cls=''):
    return w('html', cls, html=code)

def head(kicker, title, lead):
    return con('ww-head ww-rv', con('', h(kicker, 'div', 'ww-eyebrow'), h(title, 'h2', 'ww-h2')), t(f'<p>{lead}</p>', 'ww-muted ww-lead'))

def tags(*items):
    return t('<p>' + ''.join(f'<span>{i}</span>' for i in items) + '</p>', 'ww-tags')

# ---------- čistý HTML výstup pro post_content (Rank Math analýza, fallback) ----------
import re as _re
def to_html(elements):
    out = []
    def walk(e):
        cls = e.get('settings', {}).get('css_classes', '') + ' ' + e.get('settings', {}).get('_css_classes', '')
        if any(k in cls.split() for k in ('ww-headwrap', 'ww-sys', 'ww-footer', 'ww-crumbs', 'ww-toc')): return
        if e['elType'] == 'container':
            for k in e['elements']: walk(k)
            return
        s, k = e['settings'], e['widgetType']
        if k == 'heading':
            tag = s.get('header_size', 'h2')
            txt = _re.sub(r'<(?!/?(small|span|strong|em|br)\b)[^>]+>', '', s['title'])
            if s.get('link', {}).get('url'): txt = f'<a href="{s["link"]["url"]}">{txt}</a>'
            out.append(f'<{tag}>{txt}</{tag}>' if tag in ('h1', 'h2', 'h3', 'h4') else f'<p><strong>{txt}</strong></p>')
        elif k == 'text-editor':
            if 'ww-towns' in cls: out.append('<ul>' + ''.join(f'<li>{a}</li>' for a in _re.findall(r'<a [^>]*>.*?</a>', s['editor'])) + '</ul>')
            else: out.append(s['editor'])
        elif k == 'button':
            u = s['link']['url']
            if not u.startswith('#') and not u.startswith('tel:'): out.append(f'<p><a href="{u}">{s["text"]}</a></p>')
        elif k == 'image': out.append(f'<p><img src="{s["image"]["url"]}" alt="{s["image"]["alt"]}"></p>')
        elif k == 'html': out.extend(f'<p>{m}</p>' for m in _re.findall(r'<img [^>]*>', s['html']))
        elif k == 'toggle':
            for tb in s['tabs']: out.append(f'<h3>{tb["tab_title"]}</h3>{tb["tab_content"]}')
    for e in elements: walk(e)
    return '\n'.join(x for x in out if x.strip())

def toc(items):
    return t('<p><b>Na této stránce:</b>' + ''.join(f'<a href="#{a}">{b}</a>' for a, b in items) + '</p>', 'ww-toc')

# ---------- sdílené části ----------
LOGO = '<svg viewBox="0 0 169.0 20" aria-hidden="true"><defs><linearGradient id="wwg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8e1b20"/><stop offset="1" stop-color="#e31e24"/></linearGradient><clipPath id="wwc"><rect x="-2" y="0" width="173.0" height="20"/></clipPath></defs><g clip-path="url(#wwc)" fill="none" stroke-width="2.5" stroke-linejoin="miter" stroke-miterlimit="10"><path d="M0.25 -4.00 L6.38 24.00 L12.75 -4.00 L19.12 24.00 L25.25 -4.00 M28.95 -4.00 L35.08 24.00 L41.45 -4.00 L47.83 24.00 L53.95 -4.00 M57.65 -4.00 L63.77 24.00 L70.15 -4.00 L76.53 24.00 L82.65 -4.00" stroke="#b3b3b3"/><path d="M86.35 -4.00 L92.47 24.00 L98.85 -4.00 L105.22 24.00 L111.35 -4.00 M115.05 -4.00 L121.17 24.00 L127.55 -4.00 L133.93 24.00 L140.05 -4.00 M143.75 -4.00 L149.88 24.00 L156.25 -4.00 L162.62 24.00 L168.75 -4.00" stroke="url(#wwg)"/></g></svg>'

def header():
    nav = ''.join(f'<a href="{u}">{n}</a>' for n, u in [('Služby', '/#sluzby'), ('Proces', '/#proces'), ('Reference', '/#reference'),
                                                         ('Jesenicko', '/#jesenicko'), ('Ceník', '/#cenik'), ('Kontakt', '/kontakt/')])
    code = ('<header class="wh"><div class="wh__in">'
            f'<a class="wlogo" href="/" aria-label="wwwwww.cz – tvorba webových stránek Jeseník">{LOGO}</a>'
            f'<a class="wlogo__by" href="{yes(x="header_logo")}" target="_blank" rel="noopener"><small>koncept</small><img src="{YM["url"]}" alt="Yesmark" width="92" height="14"></a>'
            f'<nav class="wnav" aria-label="Hlavní navigace">{nav}</nav>'
            f'<a class="wbtn wbtn--ghost hide-m" href="tel:{TEL}">{TEL_H}</a>'
            '<a class="wbtn wbtn--red" href="/kontakt/#poptavka">Poptat web</a>'
            '<button class="wburger" type="button" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>'
            '</div><div class="wprog" aria-hidden="true"></div></header><div class="wcursor" aria-hidden="true"></div>')
    return con('ww ww-headwrap', html(code), tag='div', inner=False)

def contact_section(page):
    person = con('ww-person ww-rv',
        w('image', 'ww-photo', image={'id': PHOTO_ID, 'url': PHOTO_URL, 'alt': 'Roman Lukač – tvorba webových stránek Jeseník', 'source': 'library'}, image_size='medium'),
        h('Přijímám nové projekty', 'div', 'ww-status'),
        h('Roman Lukač', 'h3', 'ww-h3'),
        t('<p>Webdesign a vývoj · Yesmark Jeseník. Web s vámi proberu osobně – od prvního kafe až po spuštění.</p>'),
        btn(TEL_H, f'tel:{TEL}', 'ww-bigbtn ww-btn--plain'),
        btn(MAIL, f'mailto:{MAIL}', 'ww-bigbtn2 ww-btn--plain'))
    form = w('form', 'ww-form',
        form_name='Poptávka wwwwww.cz', show_labels='', mark_required='',
        form_fields=[
            {'_id': 'name', 'custom_id': 'name', 'field_type': 'text', 'field_label': 'Jméno', 'placeholder': 'Jméno *', 'required': 'true', 'width': '50'},
            {'_id': 'phone', 'custom_id': 'phone', 'field_type': 'text', 'field_label': 'Telefon', 'placeholder': 'Telefon', 'width': '50'},
            {'_id': 'email', 'custom_id': 'email', 'field_type': 'email', 'field_label': 'E-mail', 'placeholder': 'E-mail *', 'required': 'true', 'width': '100'},
            {'_id': 'intro', 'custom_id': 'intro', 'field_type': 'html', 'field_label': '', 'field_html': '<span class="ww-flabel">Mám zájem o</span>', 'width': '100'},
            {'_id': 'interest', 'custom_id': 'interest', 'field_type': 'checkbox', 'field_label': 'Mám zájem o', 'field_options': 'Nový web\nRedesign\nE-shop\nSEO\nSpráva webu', 'inline_list': 'elementor-subgroup-inline', 'width': '100'},
            {'_id': 'message', 'custom_id': 'message', 'field_type': 'textarea', 'field_label': 'Zpráva', 'placeholder': 'Co potřebujete? Stačí pár vět. *', 'required': 'true', 'rows': 5, 'width': '100'},
            {'_id': 'hp', 'custom_id': 'hp', 'field_type': 'honeypot', 'field_label': '', 'width': '100'},
        ],
        button_text='Odeslat nezávaznou poptávku', button_width='100', button_size='md',
        submit_actions=['email'],
        email_to=MAIL, email_subject='Poptávka z wwwwww.cz — [field id="name"]',
        email_content='[all-fields]', email_from='web@wwwwww.cz', email_from_name='wwwwww.cz',
        email_reply_to='[field id="email"]', email_content_type='plain',
        form_metadata=['date', 'time', 'page_url', 'remote_ip'],
        success_message='Díky, poptávka dorazila. Ozvu se obvykle do jednoho pracovního dne. Spěcháte? Volejte 731 842 606.',
        error_message='Odeslání se nepovedlo. Napište prosím na lukac@yesmark.eu nebo volejte 731 842 606.',
        required_field_message='Toto pole je povinné.', invalid_message='Zkontrolujte prosím zadané údaje.',
        form_id='poptavka-' + page)
    formcard = con('ww-formcard ww-rv',
        h('Nezávazná poptávka', 'h3', 'ww-h3'),
        t('<p>Nabídka je zdarma a k ničemu vás nezavazuje.</p>', 'ww-muted'),
        form,
        t('<p>Údaje použijeme jen k vyřízení vaší poptávky a nikomu je neprodáváme.' + PRIV_LINK + '</p>', 'ww-legal'))
    return con('ww-contact', person, formcard)

def footer():
    return sec('ww-dark ww-footer', wrap('',
        con('ww-foot',
            con('', html(f'<a class="wlogo" href="/" aria-label="wwwwww.cz">{LOGO}</a>'),
                t('<p>Tvorba webových stránek a e-shopů. Sídlíme v Jeseníku, weby tvoříme pro klienty z celé ČR. <strong>wwwwww.cz je webový koncept agentury Yesmark.</strong></p>'),
                img(YM, 'Yesmark', 'ww-footlogo')),
            con('', h('Služby', 'div', 'ww-ft'),
                t('<p><a href="/tvorba-webovych-stranek/">Tvorba webových stránek</a><br><a href="/tvorba-webu-wordpress/">Weby na WordPressu</a><br><a href="/tvorba-eshopu/">E-shopy</a><br><a href="/redesign-webu/">Redesign webu</a><br><a href="/seo-optimalizace-webu/">SEO optimalizace</a><br><a href="/sprava-webu/">Správa webu</a><br><a href="/kolik-stoji-web/">Kolik stojí web</a></p>')),
            con('', h('Odkazy', 'div', 'ww-ft'),
                t(f'<p><a href="/kontakt/">Kontakt – tvorba webů Jeseník</a><br><a href="/weby-pro-obory/">Weby pro obory</a><br><a href="/#cenik">Ceník a FAQ</a><br>'
                  f'<a href="{yes("reference/", "wwwwww_reference", "footer")}" target="_blank" rel="noopener">Reference ↗</a><br>'
                  f'<a href="{yes(x="footer")}" target="_blank" rel="noopener">Yesmark.eu ↗</a></p>')),
            con('', h('Kontakt', 'div', 'ww-ft'),
                t(f'<p><a href="tel:{TEL}">+420 {TEL_H}</a><br><a href="mailto:{MAIL}">{MAIL}</a><br>Yesmark<br>{ADDR}</p>'))),
        con('ww-footcities', h('Tvorba webových stránek v regionu', 'div', 'ww-ft'), city_links('ww-footlinks')),
        con('ww-foot-bottom',
            t('<p>© <span data-ww-year>2026</span> wwwwww.cz · tvorba webových stránek Jeseník · koncept Yesmark<br>Provozovatel: Roman Lukač, IČO 14448157, Vápenná 124, 790 64 Vápenná · fyzická osoba zapsaná v živnostenském rejstříku</p>'),
            t('<p>' + PRIV_FOOT + '<a href="#elementor-action%3Aaction%3DcookiezBanner%3AopenPreferences">Nastavení cookies</a> · <a href="#">Nahoru ↑</a></p>'))), tag='footer')

def system(ld, mbar_right):
    js = (HERE / 'ww.js').read_text(encoding='utf-8')
    b64 = base64.b64encode(js.encode('utf-8')).decode()
    loader = ('<script>(function(){var b=atob("' + b64 + '");'
              'new Function(new TextDecoder().decode(Uint8Array.from(b,function(c){return c.charCodeAt(0)})))()})()</script>')
    mbar = (f'<div class="wmbar"><a class="wbtn wbtn--ghost" href="tel:{TEL}">Zavolat</a>{mbar_right}</div>')
    ldj = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'
    return con('ww ww-sys', html(mbar + ldj + loader), inner=False)

BUSINESS = {
    '@type': 'ProfessionalService', '@id': 'https://wwwwww.cz/#business',
    'name': 'wwwwww.cz – tvorba webových stránek Jeseník', 'alternateName': 'wwwwww',
    'url': 'https://wwwwww.cz/', 'telephone': TEL, 'email': MAIL, 'priceRange': 'od 9 900 Kč',
    'description': 'Tvorba webových stránek a e-shopů na míru pro firmy z Jeseníku a Jesenicka. Webový koncept agentury Yesmark.',
    'image': PHOTO_URL or 'https://wwwwww.cz/',
    'address': {'@type': 'PostalAddress', 'streetAddress': 'Boženy Němcové 922/2', 'addressLocality': 'Jeseník',
                'postalCode': '790 01', 'addressRegion': 'Olomoucký kraj', 'addressCountry': 'CZ'},
    'geo': {'@type': 'GeoCoordinates', 'latitude': 50.2294, 'longitude': 17.2047},
    'areaServed': [{'@type': 'City', 'name': n} for n in ['Jeseník', 'Lipová-lázně', 'Zlaté Hory', 'Javorník', 'Mikulovice', 'Vidnava',
                                                          'Žulová', 'Bělá pod Pradědem', 'Česká Ves', 'Velké Losiny']]
                  + [{'@type': 'AdministrativeArea', 'name': 'Okres Jeseník'}, {'@type': 'AdministrativeArea', 'name': 'Jeseníky'}, {'@type': 'Country', 'name': 'Česká republika'}],
    'parentOrganization': {'@type': 'Organization', 'name': 'Yesmark', 'url': 'https://yesmark.eu/'},
    'employee': {'@type': 'Person', 'name': 'Roman Lukač', 'jobTitle': 'Webdesign a vývoj'},
    'knowsAbout': ['Tvorba webových stránek', 'Tvorba e-shopů', 'Webdesign', 'SEO optimalizace', 'WordPress', 'Elementor'],
}

def services_section(title='Weby, které pracují za vás.', eid='sluzby'):
    links = {'Tvorba webových stránek na míru': '/tvorba-webu-na-miru/', 'E-shopy': '/tvorba-eshopu/', 'Redesign webu': '/redesign-webu/',
             'SEO optimalizace': '/seo-optimalizace-webu/', 'Správa a propagace': '/sprava-webu/'}
    def card(n, title, text, tg, main=False, d=''):
        hd = h(title, 'h3', 'ww-h3')
        if title in links: hd['settings']['link'] = {'url': links[title], 'is_external': '', 'nofollow': ''}
        c = con('ww-card ww-rv' + (' ww-card--main' if main else ''), h(n, 'div', 'ww-num'), hd, t(f'<p>{text}</p>'), tags(*tg))
        return c
    return sec('ww-dark', wrap('',
        head('Služby', title, 'Postaráme se o vše od návrhu po spuštění – design, programování, obsah, SEO i analytiku. Vy řešíte byznys, web vám nosí poptávky.'),
        con('ww-bento',
            card('01 — hlavní služba', 'Tvorba webových stránek na míru', 'Od jednoduché firemní prezentace po rozsáhlý web. Moderní design, srozumitelný obsah a jasná cesta k poptávce – web, který vám dělá dobré jméno i obchod.',
                 ['UX &amp; UI design', 'Kódování na míru', 'WordPress + Elementor', 'October CMS', 'Responzivní design'], True),
            card('02', 'E-shopy', 'Přehledný obchod připravený na růst. Objednávky, platby i doprava bez starostí.', ['WooCommerce', 'PrestaShop']),
            card('03', 'Redesign webu', 'Starý web, který nic nepřináší? Převlékneme ho do moderního kabátu a postavíme znovu – tentokrát na prodej.', ['Nový design', 'Nový obsah']),
            card('04', 'SEO optimalizace', 'Struktura, obsah a technické SEO od prvního dne, aby vás zákazníci našli dřív než konkurenci.', ['On-page SEO', 'Google Firemní profil']),
            card('05', 'Správa a propagace', 'Aktualizace, zabezpečení, úpravy obsahu i PPC kampaně. Zůstáváme s vámi i po spuštění.', ['Údržba', 'PPC kampaně']),
            card('06', 'Grafika a branding', 'Logo, vizuální styl a grafika pro web i tisk – všechno pod jednou střechou Yesmark.', ['Logo', 'Vizuální styl']))), eid=eid)


def refs_section():
    def ref(tag, name, text, label, url, key):
        return con('ww-ref ww-rv',
            con('ww-ref-top', img(SHOT[key], f'Reference: web {name}', 'ww-ref-shot', 'large'), html('<span class="ww-ref-hint">Projeďte web ↓</span>', 'ww-ref-hintw')),
            con('ww-ref-body', h(tag, 'div', 'ww-ref-tag'), h(name, 'h3', 'ww-h3'), t(text), btn(label, url, 'ww-btn--plain ww-btn--ext', ext=True)))
    return sec('ww-light', wrap('',
        head('Reference', 'Weby, na které jsme hrdí.', 'Výběr realizací. Celé portfolio webů, e-shopů a kampaní najdete na Yesmark.eu.'),
        con('ww-refs',
            ref('Web · CNC obrábění', 'Konradt',
                '<p>Pro společnost KONRADT jsme vytvořili nové webové stránky zaměřené na profesionální prezentaci služeb v oblasti CNC obrábění, montáže a zpracování kovů. Při realizaci jsme kladli důraz na moderní technický vzhled, přehledné představení výrobních možností společnosti a srozumitelnou prezentaci jednotlivých služeb.</p>'
                '<p>Součástí realizace byla také optimalizace struktury a obsahu webu s ohledem na vyhledávače a lepší dohledatelnost služeb v oblasti CNC frézování, CNC soustružení, montážních prací a dodávek odlitků.</p>',
                'konradt.cz', 'https://www.konradt.cz/', 'konradt'),
            ref('Web · Reality Jeseníky', 'Monika Veličková',
                '<p>Pro realitní makléřku Moniku Veličkovou jsme vytvořili nové webové stránky zaměřené na prezentaci nemovitostí a realitních služeb v Jeseníkách. Při realizaci jsme kladli důraz na moderní a osobitý design, přehlednou prezentaci nabízených nemovitostí a především na budování osobní značky, která staví na znalosti regionu, individuálním přístupu a zkušenostech s realitami i investicemi.</p>',
                'monikavelickova.cz', 'https://monikavelickova.cz/', 'monika-velickova'),
            ref('Web · Technika a služby', 'Břinčil',
                '<p>Při realizaci webu pro firmu Břinčil jsme kladli důraz na moderní a přehledný design, snadnou orientaci návštěvníků a kvalitní prezentaci společnosti i její techniky. Nový web zároveň slouží jako podpůrná prezentace hlavní společnosti Břinčil &amp; Míka s.r.o., pro kterou jsme v minulosti rovněž realizovali kompletní online prezentaci.</p>',
                'brincil.cz', 'https://brincil.cz/', 'brincil')),
        con('ww-row ww-refs-more ww-rv',
            t('<p>Další weby, e-shopy a kampaně najdete v portfoliu Yesmark.</p>', 'ww-muted'),
            btn('Všechny reference', yes('reference/', 'wwwwww_reference', 'homepage_all'), 'ww-btn--dark ww-btn--ext', ext=True))), eid='reference')


def hero_visual(kw):
    def win(label, key, name):
        return (f'<div class="hv__win"><div class="hv__bar"><i></i><i></i><i></i><b>{label}</b></div>'
                f'<div class="hv__shot"><img src="{SHOT[key]["url"]}" alt="{kw} – ukázka webu {name}" decoding="async"></div></div>')
    return ('<div class="hv"><div class="hv__stack">'
        + win('brincil.cz', 'brincil', 'Břinčil') + win('monikavelickova.cz', 'monika-velickova', 'Monika Veličková') + win('konradt.cz', 'konradt', 'KONRADT') +
        '<div class="hv__chip" aria-hidden="true">Navrženo a postaveno v Jeseníku</div>'
        '<div class="hv__toast" aria-hidden="true"><em>✓</em><div><strong>Nová poptávka z webu</strong><small>právě teď</small></div></div>'
        '</div></div>')


# ---------- interaktivní bloky hlavní stránky ----------
STATS = ('<div class="wstats">'
    '<div class="wstat"><b data-count="72">72</b><span>oborů s checklistem, co má web mít</span></div>'
    '<div class="wstat"><b data-count="24">24</b><span>měst s vlastní stránkou a lokálním SEO</span></div>'
    '<div class="wstat"><b data-count="9900">9 900</b><span>Kč – za tolik začíná nový web</span></div>'
    '<div class="wstat"><b data-count="1">1</b><span>člověk, se kterým řešíte vše od kafe po spuštění</span></div>'
    '</div>')

BEFORE_AFTER = ('<div class="wba" style="--pos:50%">'
    '<div class="wba__pane wba__new" aria-hidden="true">'
      '<div class="wba__nav"><b>novak<i>.</i>cz</b><span>Služby</span><span>Reference</span><span>Ceník</span><em>Poptat opravu</em></div>'
      '<div class="wba__hero"><small>Instalatér · Jeseník a okolí</small><strong>Voda teče, kde má. Do 24 hodin u vás.</strong>'
      '<p>Opravy, rekonstrukce koupelen a topení. Férová cena předem.</p><div class="wba__btns"><em>Poptat opravu</em><span>Zavolat</span></div>'
      '<div class="wba__chips"><span>★ 4,9 Google</span><span>✓ 15 let praxe</span><span>✓ Cena předem</span></div></div>'
      '<div class="wba__toast"><em>✓</em><div><b>Nová poptávka</b><small>před 2 minutami</small></div></div>'
    '</div>'
    '<div class="wba__pane wba__old" aria-hidden="true">'
      '<div class="wba__oldhead">Vítejte na stránkách firmy NOVÁK</div>'
      '<div class="wba__oldnav"><u>Úvod</u> | <u>O nás</u> | <u>Služby</u> | <u>Fotogalerie</u> | <u>Kniha návštěv</u></div>'
      '<div class="wba__oldbody"><p><b>Firma Novák</b> provádí instalatérské práce již od roku 1998. Naše firma nabízí širokou škálu služeb v oblasti vody, topení a plynu. Pro více informací nás kontaktujte telefonicky nebo e-mailem.</p>'
      '<p class="wba__blink">!!! STRÁNKY JSOU V REKONSTRUKCI !!!</p>'
      '<p>Počet návštěv: <span class="wba__cnt">0 0 1 2 3 4</span></p><p class="wba__ie">Optimalizováno pro Internet Explorer 6.0 a rozlišení 800×600</p></div>'
    '</div>'
    '<div class="wba__line" aria-hidden="true"><span>‹ ›</span></div>'
    '<em class="wba__tag wba__tag--old">Před</em><em class="wba__tag wba__tag--new">Po</em>'
    '<input class="wba__range" type="range" min="0" max="100" value="50" aria-label="Porovnání starého a nového webu">'
    '</div>')

def _q(n, key, title, opts):
    return (f'<div class="wquiz__q" data-q="{key}"><p class="wquiz__n">Otázka {n} / 3</p><h3>{title}</h3><div class="wquiz__opts">'
            + ''.join(f'<button type="button" data-v="{v}">{l}</button>' for v, l in opts) + '</div></div>')
QUIZ = ('<div class="wquiz"><div class="wquiz__bar"><i></i></div>'
    + _q(1, 'obor', 'Čím se živíte?', [('sluzby', 'Služby a řemesla'), ('ubytovani', 'Ubytování a gastro'), ('produkty', 'Prodávám produkty'), ('komunita', 'Obec, spolek, škola'), ('jine', 'Něco jiného')])
    + _q(2, 'cil', 'Co má web hlavně dělat?', [('poptavky', 'Přivádět poptávky'), ('rezervace', 'Rezervace a objednávky'), ('prodej', 'Prodávat online'), ('info', 'Informovat a budovat důvěru')])
    + _q(3, 'web', 'Máte už web?', [('ne', 'Zatím ne'), ('stary', 'Ano, ale je zastaralý'), ('seo', 'Ano, ale nenosí zákazníky')])
    + '<div class="wquiz__res"><p class="wquiz__n">Naše doporučení</p><h3 data-r="title"></h3><p data-r="text"></p><ul data-r="list"></ul>'
      '<div class="wquiz__cta"><a class="wbtn wbtn--red" data-r="send" href="#poptavka">Poslat poptávku s odpověďmi</a><a class="wbtn wbtn--ghost" data-r="more" href="/">Více o řešení</a></div>'
      '<button type="button" class="wquiz__again">↺ Začít znovu</button></div>'
    '</div>')

# ---------- HLAVNÍ STRÁNKA ----------
def home():
    towns = ['Jeseník', 'Lipová-lázně', 'Zlaté Hory', 'Javorník', 'Mikulovice', 'Vidnava', 'Žulová', 'Bělá pod Pradědem', 'Česká Ves', 'Velké Losiny', 'Hanušovice', 'Ramzová']
    marquee = '<div class="mq" aria-hidden="true"><div class="mq__t">' + ''.join(f'<span>{x}</span>' for x in towns * 2) + '</div></div>'

    hero = sec('ww-dark ww-hero', wrap('ww-hero-grid',
        con('ww-hero-copy',
            h('Tvorba webových stránek Jeseník · koncept Yesmark', 'div', 'ww-eyebrow ww-rv'),
            h('Tvorba webových stránek v Jeseníku, které <span class="ww-red">prodávají.</span>', 'h1', 'ww-h1 ww-rv'),
            t('<p>Navrhneme a postavíme <strong>web nebo e-shop na míru</strong>, který zaujme, dobře se najde na Googlu a z návštěvníků dělá zákazníky. Z Jeseníku pro celé Česko.</p>', 'ww-lead ww-mw ww-rv'),
            con('ww-row ww-rv',
                btn('Chci nezávaznou nabídku', '/kontakt/#poptavka'),
                btn(f'Zavolat {TEL_H}', f'tel:{TEL}', 'ww-btn--ghost ww-btn--plain')),
            t('<p><span>✓ Weby od 9 900 Kč</span><span>✓ Nabídka zdarma</span><span>✓ Osobně i online po celé ČR</span></p>', 'ww-trust ww-rv')),
        html(hero_visual('Tvorba webových stránek Jeseník'), 'ww-rv')), eid='uvod')

    yesmark = sec('ww-light', wrap('ww-yes ww-rv',
        img(YM, 'Yesmark – marketingová agentura Jeseník', 'ww-yeslogo'),
        t('<p><strong>wwwwww.cz je webový koncept agentury Yesmark z Jeseníku.</strong> Stejný tým, stejné know-how jako u kampaní, grafiky a SEO pro naše klienty – jen s jasným zaměřením: tvorba webových stránek pro firmy a podnikatele z Jeseníku i celé republiky.</p>', 'ww-muted'),
        btn('Poznejte Yesmark', yes(x='homepage_strip'), 'ww-btn--dark ww-btn--ext', ext=True)))
    yesmark['settings']['css_classes'] += ' ww-yes-sec'

    def why(n, title, text):
        return con('ww-rv', h(n, 'div', 'ww-ico'), h(title, 'h3', 'ww-h3'), t(f'<p>{text}</p>'))
    whysec = sec('ww-white', wrap('',
        h('Proč wwwwww', 'div', 'ww-eyebrow ww-rv'),
        h('Web není vizitka. Je to <em>obchodník</em>, který pro vás pracuje 24/7.', 'h2', 'ww-statement ww-rv'),
        con('ww-why',
            why('01', 'Design, který prodává', 'Každý prvek má důvod – přivést návštěvníka k telefonu nebo poptávce. Žádné hezké, ale prázdné stránky.'),
            why('02', 'Najde vás Google', 'Weby stavíme s ohledem na vyhledávače a místní hledání. Aby vás našli lidé z Jeseníku i turisté z celé republiky.'),
            why('03', 'Upravíte si ho sami', 'WordPress a Elementor: texty, fotky i nové stránky změníte sami. Ukážeme vám, jak na to.'),
            why('04', 'Člověk, ne tiket', 'Komunikujete přímo s tím, kdo web staví. Osobní schůzka v Jeseníku, nebo online hovor odkudkoli.')),
        html(STATS, 'ww-rv')))

    def step(n, title, text):
        return con('ww-step', h(n, 'div', 'ww-num'), h(title, 'h3', 'ww-h3'), t(f'<p>{text}</p>'))
    process = sec('ww-dark', wrap('ww-proc',
        con('ww-sticky ww-rv',
            h('Proces', 'div', 'ww-eyebrow'),
            h('Od kafe ke spuštění.', 'h2', 'ww-h2'),
            t('<p>Jasný postup bez překvapení. Víte, co se děje, kdy to bude a kolik to stojí.</p>', 'ww-muted ww-lead'),
            con('ww-row', btn('Domluvit konzultaci', '/kontakt/#poptavka'))),
        con('ww-steps',
            step('01 / Analýza a návrh', 'Poznáme váš byznys', 'Projdeme vaše cíle, zákazníky a konkurenci. Navrhneme strukturu webu a obsah, který prodává – šablonové řešení, nebo kódování na míru.'),
            step('02 / Design a realizace', 'Navrhneme a postavíme', 'Design na míru, programování a obsah s důrazem na detail. Průběžně vidíte, jak web roste, a můžete říct svůj názor.'),
            step('03 / Spuštění', 'Pustíme web do světa', 'Testy na mobilech i počítačích, SEO nastavení, analytika a Google Firemní profil. Pak teprve jde web ven.'),
            step('04 / Správa a propagace', 'Rosteme spolu dál', 'Zabezpečení, aktualizace, úpravy obsahu, SEO a placená propagace. Zůstáváme s vámi i po spuštění.'))), eid='proces')

    rings = ''.join(f'<circle class="r" cx="270" cy="270" r="{r}"/>' for r in (46, 92, 184))
    pins = [('Lipová-lázně', 234, 273, -8, 17, 'end'), ('Česká Ves', 284, 242, 8, -4, 'start'), ('Mikulovice', 346, 199, 8, -3, 'start'),
            ('Zlaté Hory', 395, 234, 8, -3, 'start'), ('Javorník', 138, 105, -8, -7, 'end'), ('Vidnava', 258, 124, 8, -6, 'start'),
            ('Žulová', 200, 187, -8, -3, 'end'), ('Bělá pod Pradědem', 265, 337, 8, 15, 'start'), ('Velké Losiny', 162, 472, -8, 4, 'end')]
    rays = ''.join(f'<line class="ray" style="--i:{i}" x1="270" y1="270" x2="{x}" y2="{y}"/>' for i, (_, x, y, *_) in enumerate(pins))
    pts = ''.join(f'<g class="pin" style="--i:{i}"><circle class="p" cx="{x}" cy="{y}" r="4"/><text class="l" x="{x+dx}" y="{y+dy}" text-anchor="{a}">{n}</text></g>' for i, (n, x, y, dx, dy, a) in enumerate(pins))
    mapsvg = ('<div class="wmap"><svg viewBox="0 0 540 540" role="img" aria-label="Mapa Jesenicka – kde tvoříme webové stránky">'
              '<defs><linearGradient id="wsw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e3120b" stop-opacity="0"/><stop offset="1" stop-color="#e3120b" stop-opacity=".35"/></linearGradient></defs>'
              f'{rings}<circle class="r" cx="270" cy="270" r="262" stroke-dasharray="2 6"/>'
              '<path class="sw" d="M270 270 L532 270 A262 262 0 0 0 455 85 Z" fill="url(#wsw)"/>'
              f'{rays}{pts}<circle class="hqr" cx="270" cy="270" r="10"/><circle class="hq" cx="270" cy="270" r="9"/>'
              '<text class="lh" x="284" y="300">Jeseník</text></svg></div>')
    local = sec('ww-white', wrap('ww-local',
        con('ww-local-copy ww-rv',
            h('Jeseník · celá ČR', 'div', 'ww-eyebrow'),
            h('Tvorba webových stránek Jeseník – a kdekoli v Česku', 'h2', 'ww-h2s'),
            t('<p>Jsme <strong>webové studio z Jeseníku</strong> a koncept agentury Yesmark. Weby tvoříme pro firmy, řemeslníky, ubytování, gastro i realitní kanceláře z Jeseníku, Lipové-lázní, Zlatých Hor, Javorníku či Mikulovic – a stejně tak pro klienty z Olomouce, Ostravy, Prahy nebo Brna. Vzdálenost nehraje roli.</p>'
              '<p>Tvorba webových stránek Jeseník pro nás znamená víc než hezký design: web musí být dohledatelný na Googlu, srozumitelný na mobilu a vést návštěvníka k poptávce.</p>'
              '<h3>Weby pro ubytování a turistický ruch v Jeseníkách</h3>'
              '<p>Penziony, apartmány a chaty potřebují web, který zaujme fotkami, jasně ukáže ceny a vede k rezervaci – v češtině, němčině i polštině.</p>'
              '<h3>Weby pro řemeslníky, služby a výrobní firmy z Jesenicka</h3>'
              '<p>Instalatér z Jeseníku, truhlář ze Zlatých Hor nebo strojírna z Javorníku – každý potřebuje web, který se ukáže, když ho místní zákazník hledá na Googlu.</p>'
              '<h3>Osobně v Jeseníku, online kdekoli v Česku</h3>'
              f'<p>Sídlíme v Jeseníku ({ADDR}). Místní klienty rádi potkáme u nás v kanceláři, s ostatními vše vyřešíme přes videohovor, telefon a sdílený návrh – stejně rychle a osobně.</p>'),
            t('<p>' + ''.join(f'<span>{x}</span>' for x in ['Jeseník', 'Lipová-lázně', 'Zlaté Hory', 'Javorník', 'Mikulovice', 'Vidnava', 'Žulová', 'Bělá pod Pradědem', 'Česká Ves', 'Velké Losiny', 'Hanušovice', 'celá ČR']) + '</p>', 'ww-towns'),
            h('Tvoříme weby také pro', 'div', 'ww-eyebrow'), city_links(),
            con('ww-row', btn('Weby pro obory', '/weby-pro-obory/', 'ww-btn--dark'))),
        html(mapsvg, 'ww-rv')), eid='jesenicko')

    faq = [
        ('Kolik stojí tvorba webových stránek v Jeseníku?', 'Tvorba webových stránek začíná na 9 900 Kč. Konečná cena záleží na rozsahu, funkcích a grafickém zpracování. Po krátké konzultaci dostanete nezávaznou cenovou nabídku zdarma.'),
        ('Jak dlouho trvá vytvoření webu?', 'Jednodušší prezentační web bývá hotový zhruba za 2–4 týdny, web na míru nebo e-shop podle rozsahu za 4–8 týdnů. Přesný harmonogram dostanete v nabídce.'),
        ('Budu si moci web upravovat sám?', 'Ano. Stavíme na WordPressu a Elementoru, pro zcela individuální projekty na October CMS. Texty, fotky i nové stránky si pohodlně upravíte sami a ukážeme vám, jak na to.'),
        ('Jaký je vztah wwwwww.cz a agentury Yesmark?', 'wwwwww.cz je webový koncept marketingové agentury Yesmark z Jeseníku. Za weby stojí stejný tým – a když budete chtít, navážeme grafikou, kampaněmi nebo reklamními předměty.'),
        ('Děláte weby i pro klienty mimo Jesenicko?', 'Ano. Sídlíme v Jeseníku, ale weby tvoříme pro klienty z celého Česka – konzultace, návrhy i předání zvládneme online. Místní firmy rádi potkáme osobně.'),
        ('Postaráte se i o SEO, doménu a hosting?', 'Ano. Každý web stavíme s ohledem na vyhledávače, pomůžeme s doménou i hostingem a po spuštění zajistíme správu, zabezpečení i propagaci.'),
    ]
    pricing = sec('ww-dark', wrap('ww-price',
        con('ww-price-card ww-rv',
            h('Ceník', 'div', 'ww-eyebrow'),
            h('<small>Tvorba webových stránek Jeseník</small>od 9 900 Kč', 'div', 'ww-price-num'),
            t('<p>Tvorba webových stránek Jeseník u nás nemá šablonovitý ceník. Konečná částka se odvíjí od rozsahu, funkcí a grafického zpracování. Každý projekt naceňujeme individuálně – férově a za skutečný přínos.</p>', 'ww-muted'),
            con('ww-row', btn('Chci cenovou nabídku', '/kontakt/#poptavka'))),
        con('ww-rv', h('Časté otázky – tvorba webových stránek Jeseník', 'h2', 'ww-h2s'),
            w('toggle', 'ww-faq', faq_schema='yes', tabs=[{'_id': uid(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in faq]))), eid='cenik')

    contact = sec('ww-light', wrap('',
        head('Poptávka', 'Pojďme postavit váš nový web.', 'Tvorba webových stránek Jeseník začíná jednou zprávou. Napište pár vět nebo rovnou zavolejte – ozvu se obvykle do jednoho pracovního dne.'),
        contact_section('home')), eid='poptavka')

    cta = sec('ww-redbg ww-cta', wrap('ww-cta ww-rv',
        h('Nový web?', 'div', 'ww-eyebrow'),
        h('Začneme jedním<br>telefonátem.', 'h2', 'ww-mega'),
        con('ww-row', btn(f'Zavolat {TEL_H}', f'tel:{TEL}', 'ww-btn--white ww-btn--plain'), btn('Napsat poptávku', '/kontakt/#poptavka', 'ww-btn--dark'))))

    ld = {'@context': 'https://schema.org', '@graph': [BUSINESS, {'@type': 'WebSite', '@id': 'https://wwwwww.cz/#web', 'url': 'https://wwwwww.cz/', 'name': 'wwwwww.cz', 'inLanguage': 'cs-CZ', 'publisher': {'@id': 'https://wwwwww.cz/#business'}}]}
    ba = sec('ww-dark ww-basec', wrap('ww-ba-grid',
        con('ww-rv ww-ba-copy',
            h('Redesign v praxi', 'div', 'ww-eyebrow'),
            h('Před a po. Posuňte si to.', 'h2', 'ww-h2'),
            t('<p>Starý web, který nikoho nepřesvědčí, vs. moderní web, který vede k poptávce. Chyťte jezdec a porovnejte – takhle vypadá rozdíl, který zákazník pozná za pár vteřin.</p>', 'ww-muted ww-lead'),
            con('ww-row', btn('Chci redesign webu', '/redesign-webu/', 'ww-btn--ghost ww-btn--plain'))),
        html(BEFORE_AFTER, 'ww-rv')), eid='pred-a-po')
    quiz = sec('ww-dark ww-quizsec', wrap('',
        head('Kvíz · 30 vteřin', 'Jaký web potřebujete?', 'Tři rychlé otázky a dostanete doporučení na míru – i s tím, co by váš web neměl postrádat. Odpovědi pak jedním klikem pošlete v poptávce.'),
        html(QUIZ, 'ww-rv')), eid='kviz')
    page = [header(), hero, html_section(marquee), yesmark, services_section(), whysec, process, refs_section(), ba, local, quiz, pricing, contact, cta, footer(),
            system(ld, '<a class="wbtn wbtn--red" href="#poptavka">Poptat web</a>')]
    for el in page: el['settings']['css_classes'] += ' ww-home'
    return page

def html_section(code):
    return con('ww ww-marq', html(code), inner=False)

# ---------- KONTAKT ----------
def kontakt():
    hero = sec('ww-dark ww-phero', wrap('ww-stack',
        t('<p><a href="/">wwwwww.cz</a> / kontakt</p>', 'ww-crumbs'),
        h('Kontakt – tvorba webových stránek <span class="ww-red">Jeseník</span>', 'h1', 'ww-h1 ww-rv'),
        t('<p>Nový web, e-shop nebo redesign? Napište, zavolejte, nebo se zastavte v kanceláři Yesmark v Jeseníku. Pracujeme pro klienty z celé ČR, nabídku připravím zdarma.</p>', 'ww-lead ww-mw ww-rv')))
    contact = sec('ww-light', wrap('', contact_section('kontakt')), eid='poptavka')
    contact['settings']['css_classes'] += ' ww-tight'

    def step(n, title, text):
        return con('ww-rv', h(n, 'div', 'ww-ico'), h(title, 'h3', 'ww-h3'), t(f'<p>{text}</p>'))
    nextsteps = sec('ww-white', wrap('',
        h('Co bude dál', 'div', 'ww-eyebrow ww-rv'),
        h('Žádné formuláře do prázdna. Ozve se vám <em>člověk</em>.', 'h2', 'ww-statement ww-rv'),
        con('ww-why',
            step('01', 'Ozvu se', 'Obvykle do jednoho pracovního dne – telefonem nebo e-mailem, jak vám to sedí.'),
            step('02', 'Konzultace', 'Telefon, videohovor nebo schůzka v Jeseníku. Projdeme cíle, konkurenci a rozsah.'),
            step('03', 'Nabídka', 'Jasná cena, rozsah a termín. Zdarma a nezávazně.'),
            step('04', 'Start', 'Pustíme se do návrhu. Průběžně vidíte, jak web roste.'))))
    nap = sec('ww-light', wrap('ww-nap',
        con('ww-napcard ww-rv',
            h('Kde nás najdete', 'div', 'ww-eyebrow'),
            h('Kontakt a adresa', 'h2', 'ww-h2s'),
            t(f'<p><strong>{ADDR}</strong></p><p>Telefon: <a href="tel:{TEL}">+420 {TEL_H}</a><br>E-mail: <a href="mailto:{MAIL}">{MAIL}</a></p>'
              '<p>Tvoříme webové stránky pro firmy z Jeseníku a okolí i pro klienty z celé České republiky.</p>', 'ww-muted'),
            con('ww-row', btn('Prohlédnout reference', yes('reference/', 'wwwwww_reference', 'kontakt'), 'ww-btn--dark ww-btn--ext', ext=True))),
        con('ww-napmap ww-rv',
            html('<div class="wmapbox"><span class="wmapbox__pin"></span><strong>Boženy Němcové 922/2</strong><span>790 01 Jeseník</span></div>'),
            btn('Navigovat v Google Mapách', 'https://www.google.com/maps/search/?api=1&query=Bo%C5%BEeny+N%C4%9Bmcov%C3%A9+922%2F2+Jesen%C3%ADk', 'ww-btn--dark ww-btn--ext', ext=True))))
    ld = {'@context': 'https://schema.org', '@graph': [
        BUSINESS,
        {'@type': 'ContactPage', 'url': 'https://wwwwww.cz/kontakt/', 'name': 'Kontakt – tvorba webových stránek Jeseník', 'about': {'@id': 'https://wwwwww.cz/#business'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Tvorba webových stránek Jeseník', 'item': 'https://wwwwww.cz/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Kontakt', 'item': 'https://wwwwww.cz/kontakt/'}]}]}
    return [header(), hero, contact, nextsteps, nap, footer(),
            system(ld, f'<a class="wbtn wbtn--red" href="mailto:{MAIL}">Napsat e-mail</a>')]


# ---------- MĚSTSKÉ LANDING PAGES ----------
def city_page(c):
    n, loc, gen = c['name'], c['loc'], c['gen']
    hero = sec('ww-dark ww-phero ww-cityhero', wrap('ww-hero-grid', con('ww-hero-copy',
        t(f'<p><a href="/">wwwwww.cz</a> / tvorba webů {n}</p>', 'ww-crumbs'),
        h(f'Tvorba webových stránek <span class="ww-red">{n}</span>', 'h1', 'ww-h1 ww-rv'),
        t(f'<p>{c["intro"]}</p>', 'ww-lead ww-mw ww-rv'),
        con('ww-row ww-rv', btn('Chci nezávaznou nabídku', '#poptavka'), btn(f'Zavolat {TEL_H}', f'tel:{TEL}', 'ww-btn--ghost ww-btn--plain')),
        t('<p><span>✓ Weby od 9 900 Kč</span><span>✓ Nabídka zdarma</span><span>✓ Koncept agentury Yesmark</span></p>', 'ww-trust ww-rv')),
        html(hero_visual(f'Tvorba webových stránek {n}'), 'ww-rv')), eid='uvod')
    steps = ''.join(f'<li><b>{a}</b> {b}</li>' for a, b in [
        ('Úvodní hovor', '– telefonem, online nebo osobně.'), ('Návrh a nabídka', '– jasná cena a termín zdarma.'),
        ('Realizace', '– průběžně vidíte, jak web roste.'), ('Spuštění a SEO', '– aby vás našli lidé ' + gen + '.')])
    local = sec('ww-white', wrap('ww-local',
        con('ww-local-copy ww-rv',
            h(f'Weby pro firmy {gen}', 'div', 'ww-eyebrow'),
            h(f'Web, který vám přivede zákazníky {loc}', 'h2', 'ww-h2s'),
            t(''.join(f'<p>{x}</p>' for x in c['text']) +
              f'<p>Tvorba webových stránek {n} u nás začíná krátkým hovorem o vašem podnikání a končí webem, který přivádí poptávky – ne jen vizitkou na internetu.</p>'
              f'<h3>Lokální SEO pro {n}</h3><p>Každý web stavíme tak, aby se ukázal lidem, kteří hledají vaše služby {loc} a okolí – správná struktura, obsah, rychlá orientace na mobilu a propojení s Google Firemním profilem.</p>')),
        con('ww-citycard ww-rv',
            h(f'Pro koho tvoříme {loc}', 'h3', 'ww-h3'),
            tags(*c['who']),
            h('Jak spolupráce probíhá', 'div', 'ww-eyebrow'),
            t(f'<ol class="ww-steps-list">{steps}</ol>'),
            btn('Domluvit konzultaci', '#poptavka'))))
    faq = [
        (f'Kolik stojí tvorba webových stránek {loc}?', f'Tvorba webových stránek {n} začíná na 9 900 Kč. Konečná cena záleží na rozsahu, funkcích a grafickém zpracování. Po krátké konzultaci dostanete nezávaznou nabídku zdarma.'),
        ('Musím za vámi jezdit do Jeseníku?', 'Nemusíte. Konzultace, návrhy i předání webu zvládneme online – telefonem, videohovorem a e-mailem. Když je to potřeba, rádi se potkáme i osobně.'),
        (f'Pomůžete, aby nás našli zákazníci {gen}?', f'Ano. Web postavíme s ohledem na lokální SEO pro {n} – obsah zaměřený na vaše služby a lokalitu, Google Firemní profil a technické SEO od prvního dne.'),
        c['faq'],
        ('Budu si moci web upravovat sám?', 'Ano. Stavíme na WordPressu a Elementoru – texty, fotky i nové stránky si upravíte sami a ukážeme vám, jak na to.'),
    ]
    pricing = sec('ww-dark', wrap('ww-price',
        con('ww-price-card ww-rv',
            h(f'Ceník · {n}', 'div', 'ww-eyebrow'),
            h(f'<small>Tvorba webových stránek {n}</small>od 9 900 Kč', 'div', 'ww-price-num'),
            t('<p>Konečná částka se odvíjí od rozsahu, funkcí a grafického zpracování. Každý projekt naceňujeme individuálně a férově.</p>', 'ww-muted'),
            con('ww-row', btn('Chci cenovou nabídku', '#poptavka'))),
        con('ww-rv', h(f'Časté otázky – tvorba webových stránek {n}', 'h2', 'ww-h2s'),
            w('toggle', 'ww-faq', faq_schema='yes', tabs=[{'_id': uid(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in faq]))), eid='cenik')
    contact = sec('ww-light', wrap('',
        head('Poptávka', f'Nový web pro vaši firmu {gen}?', f'Tvorba webových stránek {n} začíná jednou zprávou. Napište pár vět nebo rovnou zavolejte – ozvu se obvykle do jednoho pracovního dne.'),
        contact_section('mesto-' + c['slug'])), eid='poptavka')
    others = sec('ww-white ww-others', wrap('ww-stack ww-rv',
        h('Tvoříme weby také pro', 'div', 'ww-eyebrow'),
        t('<p><a href="/">Jeseník</a>' + ''.join(f'<a href="/tvorba-webovych-stranek-{o["slug"]}/">{o["name"]}</a>' for o in CITIES if o['slug'] != c['slug']) + '</p>', 'ww-towns ww-citylinks'),
        h(f'Weby podle oboru – {n}', 'div', 'ww-eyebrow'),
        obor_links(),
        btn('Všechny obory', HUB_URL, 'ww-btn--dark')))
    url = f'https://wwwwww.cz/tvorba-webovych-stranek-{c["slug"]}/'
    ld = {'@context': 'https://schema.org', '@graph': [
        BUSINESS,
        {'@type': 'Service', '@id': url + '#service', 'name': f'Tvorba webových stránek {n}', 'serviceType': 'Tvorba webových stránek',
         'url': url, 'provider': {'@id': 'https://wwwwww.cz/#business'},
         'areaServed': {'@type': 'City', 'name': n, 'containedInPlace': {'@type': 'AdministrativeArea', 'name': c['kraj']}},
         'offers': {'@type': 'Offer', 'priceCurrency': 'CZK', 'price': '9900', 'description': 'Tvorba webových stránek od 9 900 Kč'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Tvorba webových stránek Jeseník', 'item': 'https://wwwwww.cz/'},
            {'@type': 'ListItem', 'position': 2, 'name': f'Tvorba webů {n}', 'item': url}]}]}
    return [header(), hero, local, services_section(f'Tvorba webových stránek {n}: co umíme.'), refs_section(), pricing, contact, others, footer(),
            system(ld, '<a class="wbtn wbtn--red" href="#poptavka">Poptat web</a>')]


# ---------- ZÁSADY OCHRANY OSOBNÍCH ÚDAJŮ ----------
OP = {'firma': 'Roman Lukač', 'ico': '14448157', 'sidlo': 'Vápenná 124, 790 64 Vápenná', 'rejstrik': 'fyzická osoba podnikající podle živnostenského zákona, zapsaná v živnostenském rejstříku'}

def privacy_page():
    body = f"""
<h2>1. Kdo zpracovává vaše údaje</h2>
<p>Správcem osobních údajů je <strong>{OP['firma']}</strong>, IČO {OP['ico']}, se sídlem {OP['sidlo']}, {OP['rejstrik']} (dále jen „správce“). Kontaktní adresa (kancelář Yesmark): {ADDR}. Web wwwwww.cz je webový koncept agentury Yesmark.</p>
<p>Kontakt pro otázky k osobním údajům: <a href="mailto:{MAIL}">{MAIL}</a>, tel. <a href="tel:{TEL}">+420 {TEL_H}</a>.</p>
<h2>2. Jaké údaje zpracováváme a proč</h2>
<h3>Poptávkový formulář a e-mail</h3>
<p>Když nám pošlete poptávku, zpracováváme jméno, e-mail, telefon (nepovinný), zvolené služby, text zprávy a technické údaje o odeslání (datum, čas, stránka, IP adresa). Údaje používáme jen k vyřízení vaší poptávky a k jednání o případné spolupráci.</p>
<p>Právním základem je jednání o smlouvě na vaši žádost (čl. 6 odst. 1 písm. b) GDPR) a oprávněný zájem správce odpovědět na dotaz (čl. 6 odst. 1 písm. f) GDPR). Údaje uchováváme po dobu jednání a nejdéle 2 roky od posledního kontaktu, pokud nevznikne smluvní vztah. Pokud spolupráce vznikne, uchováváme je po dobu trvání smlouvy a lhůt stanovených zákonem.</p>
<h3>Analytické cookies</h3>
<p>S vaším souhlasem používáme Google Analytics (Google Ireland Limited) k měření návštěvnosti webu. Bez souhlasu se analytické cookies neukládají (Google Consent Mode). Souhlas můžete kdykoli změnit v nastavení cookies v patičce webu. Právním základem je souhlas (čl. 6 odst. 1 písm. a) GDPR).</p>
<h3>Nezbytné cookies</h3>
<p>Web používá technicky nezbytné cookies, například pro uložení vaší volby v cookie liště. Ty nevyžadují souhlas.</p>
<h2>3. Komu údaje předáváme</h2>
<p>Údaje nepředáváme třetím osobám za účelem marketingu. Zpracovateli jsou poskytovatel webhostingu, poskytovatel e-mailových služeb a Google (Analytics, pouze se souhlasem). Při využití služeb Google může docházet k předání do USA na základě rozhodnutí o odpovídající ochraně (EU-U.S. Data Privacy Framework).</p>
<h2>4. Vaše práva</h2>
<p>Máte právo na přístup ke svým údajům, jejich opravu, výmaz, omezení zpracování, přenositelnost a právo vznést námitku proti zpracování založenému na oprávněném zájmu. Udělený souhlas můžete kdykoli odvolat. Svá práva uplatníte na e-mailu <a href="mailto:{MAIL}">{MAIL}</a>.</p>
<p>Máte také právo podat stížnost u Úřadu pro ochranu osobních údajů (<a href="https://uoou.gov.cz" target="_blank" rel="noopener">uoou.gov.cz</a>).</p>
<h2>5. Účinnost</h2>
<p>Tyto zásady jsou účinné od <span data-ww-date>6. 10. 2026</span>.</p>
"""
    hero = sec('ww-dark ww-phero', wrap('ww-stack',
        t('<p><a href="/">wwwwww.cz</a> / ochrana osobních údajů</p>', 'ww-crumbs'),
        h('Zásady ochrany osobních údajů', 'h1', 'ww-h1'),
        t('<p>Jak na wwwwww.cz nakládáme s vašimi osobními údaji a cookies.</p>', 'ww-lead ww-mw')))
    content = sec('ww-white', wrap('ww-legal-wrap', t(body, 'ww-legaltext')))
    ld = {'@context': 'https://schema.org', '@graph': [BUSINESS]}
    return [header(), hero, content, footer(), system(ld, '<a class="wbtn wbtn--red" href="/kontakt/#poptavka">Poptat web</a>')]


# ---------- OBOROVÉ LANDING PAGES ----------
from obory_a import A as _OA
from obory_b import B as _OB
from obory_c import C as _OC
OBORY = _OA + _OB + _OC
GROUPS = []
for _o in OBORY:
    if _o['group'] not in GROUPS: GROUPS.append(_o['group'])
def obor_url(o):
    return '/' + (('web-pro-' + o['slug']) if o['name'].startswith('Web pro') else o['slug']) + '/'
HUB_URL = '/weby-pro-obory/'

def obor_links(cls='ww-towns ww-citylinks', exclude=None, group=None):
    items = ''.join(f'<a href="{obor_url(o)}">{o["short"][:1].upper() + o["short"][1:]}</a>' for o in OBORY
                    if o['slug'] != exclude and (group is None or o['group'] == group))
    return t(f'<p>{items}</p>', cls)

GOALS = {'svatebni-web': 'ušetřil vám starosti s hosty', 'obec': 'dobře sloužil občanům', 'spolek': 'přiváděl nové členy a podporovatele',
         'sportovni-klub': 'přiváděl nové členy', 'hasici': 'pomáhal s náborem a prezentací sboru', 'materska-skola': 'dobře sloužil rodičům',
         'skola': 'dobře sloužil rodičům i uchazečům', 'svj': 'ušetřil práci výboru', 'farnost': 'sloužil farníkům i návštěvníkům',
         'umelec-muzikant': 'přiváděl pořadatele a fanoušky', 'chovatelska-stanice': 'přiváděl ty správné zájemce'}

def obor_title(o):
    for f in ('{n}: 8 věcí, které musí mít | wwwwww.cz', '{n}: 8 věcí, které musí mít', '{n}: 8 věcí, co musí mít', '{n}: 8 tipů'):
        x = f.format(n=o['name'])
        if len(x) <= 60: return x
    return o['name']

def obor_page(o):
    n, short = o['name'], o['short']
    goal = GOALS.get(o['slug'], 'přiváděl zákazníky')
    kw = n.lower()
    hero = sec('ww-dark ww-phero ww-cityhero', wrap('ww-hero-grid', con('ww-hero-copy',
        t(f'<p><a href="/">wwwwww.cz</a> / <a href="{HUB_URL}">weby pro obory</a> / {short}</p>', 'ww-crumbs'),
        h(o['group'], 'div', 'ww-eyebrow ww-rv'),
        h(f'{n}<span class="ww-red">.</span>', 'h1', 'ww-h1 ww-rv'),
        t(f'<p>Co by měl mít {kw}, aby {goal}? Praktický přehled od webového studia z Jeseníku – checklist, struktura stránek, funkce i SEO tipy.</p>', 'ww-lead ww-mw ww-rv'),
        con('ww-row ww-rv', btn('Chci nezávaznou nabídku', '#poptavka'), btn(f'Zavolat {TEL_H}', f'tel:{TEL}', 'ww-btn--ghost ww-btn--plain')),
        t('<p><span>✓ Weby od 9 900 Kč</span><span>✓ Nabídka zdarma</span><span>✓ Koncept agentury Yesmark</span></p>', 'ww-trust ww-rv')),
        html(hero_visual(n), 'ww-rv')), eid='uvod')
    nav = sec('ww-white ww-tocsec', wrap('', toc([('problem', 'Typický problém'), ('checklist', 'Co musí mít'), ('struktura', 'Struktura webu'),
                                              ('reference', 'Reference'), ('cenik', 'Cena a FAQ'), ('poptavka', 'Poptávka')])))
    problem = sec('ww-white', wrap('',
        h('Typický problém', 'div', 'ww-eyebrow ww-rv'),
        h(f'Proč {kw} často nefunguje', 'h2', 'ww-h2s ww-rv'),
        t(f'<p>{o["problem"]}</p>', 'ww-bigtext ww-rv')), eid='problem')
    cards = [con('ww-card ww-mustcard ww-rv', h(f'{i+1:02d}', 'div', 'ww-num'), t(f'<p>{m}</p>', 'ww-musttext')) for i, m in enumerate(o['must'])]
    must = sec('ww-dark', wrap('',
        head('Checklist', f'Co musí mít {kw}', 'Těchto osm věcí rozhoduje, jestli web návštěvníka přesvědčí, nebo pošle ke konkurenci.'),
        con('ww-grid4', *cards)), eid='checklist')
    sitemap = ''.join(f'<li><span>{i+1:02d}</span>{pg}</li>' for i, pg in enumerate(o['pages']))
    feats = ''.join(f'<li>{f}</li>' for f in o['features'])
    seo = ''.join(f'<li>{x}</li>' for x in o['seo'])
    struct = sec('ww-light', wrap('ww-local',
        con('ww-local-copy ww-rv',
            h('Ukázková struktura', 'div', 'ww-eyebrow'),
            h(f'Jak by mohl vypadat {kw}', 'h2', 'ww-h2s'),
            t(f'<p>Typický {kw} má {len(o["pages"])}–{len(o["pages"]) + 8} stránek. Tady je osvědčený základ, který podle potřeby rozšíříme:</p><ol class="ww-sitemap">{sitemap}</ol>')),
        con('ww-citycard ww-rv',
            h('Funkce a napojení', 'h3', 'ww-h3'),
            t(f'<ul class="ww-checklist">{feats}</ul>'),
            h('SEO tipy pro obor', 'div', 'ww-eyebrow'),
            t(f'<ul class="ww-checklist">{seo}</ul>'),
            btn('Probrat můj web', '#poptavka'))), eid='struktura')
    faq = list(o['faq']) + [
        (f'Jak dlouho trvá vytvoření webu – {short}?', 'Jednodušší web bývá hotový za 2–4 týdny, rozsáhlejší s rezervacemi nebo e-shopem za 4–8 týdnů. Přesný harmonogram dostanete v nabídce.'),
        ('Budu si web upravovat sám?', 'Ano. Stavíme na WordPressu a Elementoru – texty, ceník, fotky i nové stránky změníte sami a ukážeme vám, jak na to.'),
        ('Tvoříte weby jen v Jeseníku?', 'Sídlíme v Jeseníku, ale weby tvoříme pro klienty z celé České republiky. Spolupráce běží online, místní rádi potkáme osobně.')]
    pricing = sec('ww-dark', wrap('ww-price',
        con('ww-price-card ww-rv',
            h('Cena', 'div', 'ww-eyebrow'),
            h(f'<small>{n}</small>od 9 900 Kč', 'div', 'ww-price-num'),
            t('<p>Konečná cena záleží na počtu stránek, funkcích (rezervace, e-shop, jazyky) a grafice. Nabídku vám připravíme zdarma.</p>', 'ww-muted'),
            con('ww-row', btn('Chci cenovou nabídku', '#poptavka'))),
        con('ww-rv', h(f'Časté otázky – {kw}', 'h2', 'ww-h2s'),
            w('toggle', 'ww-faq', faq_schema='yes', tabs=[{'_id': uid(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in faq]))), eid='cenik')
    contact = sec('ww-light', wrap('',
        head('Poptávka', f'Chcete {kw}?', 'Napište pár vět o svém podnikání nebo rovnou zavolejte. Ozvu se obvykle do jednoho pracovního dne.'),
        contact_section('obor-' + o['slug'])), eid='poptavka')
    links = sec('ww-white ww-others', wrap('ww-stack ww-rv',
        h(f'{n} tvoříme v těchto městech', 'div', 'ww-eyebrow'),
        t('<p><a href="/">Jeseník</a>' + ''.join(f'<a href="/tvorba-webovych-stranek-{c["slug"]}/">{c["name"]}</a>' for c in CITIES) + '</p>', 'ww-towns ww-citylinks'),
        h(f'Další obory – {o["group"].lower()}', 'div', 'ww-eyebrow'),
        obor_links(exclude=o['slug'], group=o['group']),
        btn('Všechny obory', HUB_URL, 'ww-btn--dark')))
    url = 'https://wwwwww.cz' + obor_url(o)
    ld = {'@context': 'https://schema.org', '@graph': [BUSINESS,
        {'@type': 'Service', '@id': url + '#service', 'name': n, 'serviceType': 'Tvorba webových stránek', 'url': url,
         'audience': {'@type': 'BusinessAudience', 'name': short}, 'provider': {'@id': 'https://wwwwww.cz/#business'},
         'areaServed': {'@type': 'Country', 'name': 'Česká republika'},
         'offers': {'@type': 'Offer', 'priceCurrency': 'CZK', 'price': '9900', 'description': 'Tvorba webu od 9 900 Kč'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Tvorba webových stránek Jeseník', 'item': 'https://wwwwww.cz/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Weby pro obory', 'item': 'https://wwwwww.cz' + HUB_URL},
            {'@type': 'ListItem', 'position': 3, 'name': n, 'item': url}]}]}
    return [header(), hero, nav, problem, must, struct, refs_section(), pricing, contact, links, footer(),
            system(ld, '<a class="wbtn wbtn--red" href="#poptavka">Poptat web</a>')]

def hub_page():
    hero = sec('ww-dark ww-phero', wrap('ww-stack',
        t('<p><a href="/">wwwwww.cz</a> / weby pro obory</p>', 'ww-crumbs'),
        h('Weby pro obory<span class="ww-red">.</span>', 'h1', 'ww-h1 ww-rv'),
        t(f'<p>Co by měl mít web pro kadeřnictví, penzion nebo stavební firmu? Pro {len(OBORY)} oborů jsme sepsali checklist, ukázkovou strukturu, funkce i SEO tipy. Najděte ten svůj.</p>', 'ww-lead ww-mw ww-rv')))
    groups = []
    for g in GROUPS:
        cards = [con('ww-card ww-hubcard ww-rv', h(o['name'], 'h3', 'ww-h3'), t(f'<p>{o["problem"].split(".")[0]}.</p>'), btn('Co má web mít', obor_url(o), 'ww-btn--plain ww-btn--ghost'))
                 for o in OBORY if o['group'] == g]
        groups.append(con('ww-hubgroup', h(g, 'h2', 'ww-h2s ww-rv'), con('ww-grid3', *cards)))
    body = sec('ww-dark', wrap('ww-stack ww-hubwrap', *groups))
    contact = sec('ww-light', wrap('', head('Poptávka', 'Váš obor tu není?', 'Nevadí – weby tvoříme pro jakékoli podnikání. Napište nám, co děláte.'), contact_section('obory')), eid='poptavka')
    ld = {'@context': 'https://schema.org', '@graph': [BUSINESS, {'@type': 'CollectionPage', 'name': 'Weby pro obory', 'url': 'https://wwwwww.cz' + HUB_URL}]}
    return [header(), hero, body, contact, footer(), system(ld, '<a class="wbtn wbtn--red" href="#poptavka">Poptat web</a>')]

# ---------- STRÁNKY SLUŽEB ----------
from sluzby import S as SLUZBY
def sluzby_links(exclude=None):
    return t('<p>' + ''.join(f'<a href="/{x["slug"]}/">{x["nav"]}</a>' for x in SLUZBY if x['slug'] != exclude) + '</p>', 'ww-towns ww-citylinks')

def service_page(x):
    n, kw = x['h1'], x['kw']
    hero = sec('ww-dark ww-phero ww-cityhero', wrap('ww-hero-grid', con('ww-hero-copy',
        t(f'<p><a href="/">wwwwww.cz</a> / {x["nav"].lower()}</p>', 'ww-crumbs'),
        h(x['eyebrow'], 'div', 'ww-eyebrow ww-rv'),
        h(f'{n}<span class="ww-red">.</span>', 'h1', 'ww-h1 ww-rv'),
        t(f'<p>{x["lead"]}</p>', 'ww-lead ww-mw ww-rv'),
        con('ww-row ww-rv', btn('Chci nezávaznou nabídku', '#poptavka'), btn(f'Zavolat {TEL_H}', f'tel:{TEL}', 'ww-btn--ghost ww-btn--plain')),
        t('<p><span>✓ Weby od 9 900 Kč</span><span>✓ Nabídka zdarma</span><span>✓ Koncept agentury Yesmark</span></p>', 'ww-trust ww-rv')),
        html(hero_visual(n), 'ww-rv')), eid='uvod')
    nav = sec('ww-white ww-tocsec', wrap('', toc([('o-sluzbe', x['intro_h2']), ('prehled', x['grid_head'][0]), ('detail', 'Podrobnosti'),
                                              ('reference', 'Reference'), ('cenik', 'Cena a FAQ'), ('poptavka', 'Poptávka')])))
    intro = sec('ww-white', wrap('ww-local',
        con('ww-local-copy ww-rv', h(x['eyebrow'], 'div', 'ww-eyebrow'), h(x['intro_h2'], 'h2', 'ww-h2s'),
            t(''.join(f'<p>{p}</p>' for p in x['intro']))),
        con('ww-citycard ww-rv', h(x['card_h3'], 'h3', 'ww-h3'),
            t('<ul class="ww-checklist">' + ''.join(f'<li>{i}</li>' for i in x['card']) + '</ul>'),
            btn('Probrat můj web', '#poptavka'))), eid='o-sluzbe')
    k, ttl, lead = x['grid_head']
    cards = [con('ww-card ww-mustcard ww-rv', h(f'{i+1:02d}', 'div', 'ww-num'), h(a, 'h3', 'ww-h3'), t(f'<p>{b}</p>', 'ww-musttext')) for i, (a, b) in enumerate(x['grid'])]
    grid = sec('ww-dark', wrap('', head(k, ttl, lead), con('ww-grid4', *cards)), eid='prehled')
    deep = sec('ww-light', wrap('ww-legal-wrap ww-rv', h(x['deep_h2'], 'h2', 'ww-h2s'), t(x['deep'], 'ww-legaltext')), eid='detail')
    pricing = sec('ww-dark', wrap('ww-price',
        con('ww-price-card ww-rv',
            h('Cena', 'div', 'ww-eyebrow'),
            h(f'<small>{n}</small>od 9 900 Kč', 'div', 'ww-price-num') if x['slug'] not in ('tvorba-eshopu', 'sprava-webu', 'seo-optimalizace-webu') else h(f'<small>{n}</small>na míru', 'div', 'ww-price-num'),
            t('<p>Konečná cena záleží na rozsahu, funkcích a grafice. Nabídku vám připravíme zdarma a nezávazně.</p>', 'ww-muted'),
            con('ww-row', btn('Chci cenovou nabídku', '#poptavka'))),
        con('ww-rv', h(f'Časté otázky – {kw}', 'h2', 'ww-h2s'),
            w('toggle', 'ww-faq', faq_schema='yes', tabs=[{'_id': uid(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in x['faq']]))), eid='cenik')
    contact = sec('ww-light', wrap('',
        head('Poptávka', 'Pojďme to probrat.', 'Napište pár vět o svém podnikání nebo rovnou zavolejte. Ozvu se obvykle do jednoho pracovního dne.'),
        contact_section('sluzba-' + x['slug'])), eid='poptavka')
    links = sec('ww-white ww-others', wrap('ww-stack ww-rv',
        h('Další služby', 'div', 'ww-eyebrow'), sluzby_links(x['slug']),
        h('Tvoříme weby v těchto městech', 'div', 'ww-eyebrow'),
        t('<p><a href="/">Jeseník</a>' + ''.join(f'<a href="/tvorba-webovych-stranek-{c["slug"]}/">{c["name"]}</a>' for c in CITIES) + '</p>', 'ww-towns ww-citylinks'),
        btn('Weby pro obory', HUB_URL, 'ww-btn--dark')))
    url = f'https://wwwwww.cz/{x["slug"]}/'
    ld = {'@context': 'https://schema.org', '@graph': [BUSINESS,
        {'@type': 'Service', '@id': url + '#service', 'name': n, 'serviceType': n, 'url': url, 'description': x['desc'],
         'provider': {'@id': 'https://wwwwww.cz/#business'}, 'areaServed': {'@type': 'Country', 'name': 'Česká republika'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Tvorba webových stránek Jeseník', 'item': 'https://wwwwww.cz/'},
            {'@type': 'ListItem', 'position': 2, 'name': n, 'item': url}]}]}
    return [header(), hero, nav, intro, grid, deep, refs_section(), pricing, contact, links, footer(),
            system(ld, '<a class="wbtn wbtn--red" href="#poptavka">Poptat web</a>')]

if __name__ == '__main__':
    for name, fn in [('home', home), ('kontakt', kontakt)]:
        data = fn()
        (OUT / f'{name}.html').write_text(to_html(data), encoding='utf-8')
        (OUT / f'{name}.json').write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        print(name, len(json.dumps(data)) // 1024, 'kB')
    for c in CITIES:
        d = city_page(c)
        (OUT / f'mesto-{c["slug"]}.json').write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
        (OUT / f'mesto-{c["slug"]}.html').write_text(to_html(d), encoding='utf-8')
    print('města:', len(CITIES))
    for o in OBORY:
        d = obor_page(o)
        (OUT / f'obor-{o["slug"]}.json').write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
        (OUT / f'obor-{o["slug"]}.html').write_text(to_html(d), encoding='utf-8')
    d = hub_page()
    (OUT / 'obory-hub.json').write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    (OUT / 'obory-hub.html').write_text(to_html(d), encoding='utf-8')
    print('obory:', len(OBORY))
    for x in SLUZBY:
        d = service_page(x)
        (OUT / f'sluzba-{x["slug"]}.json').write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
        (OUT / f'sluzba-{x["slug"]}.html').write_text(to_html(d), encoding='utf-8')
    print('služby:', len(SLUZBY))
    d = privacy_page()
    (OUT / 'zasady.json').write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    (OUT / 'zasady.html').write_text(to_html(d), encoding='utf-8')
