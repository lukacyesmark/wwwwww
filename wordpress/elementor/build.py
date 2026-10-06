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

TEL, TEL_H, MAIL = '+420731842606', '731 842 606', 'lukac@yesmark.eu'
ADDR = 'Boženy Němcové 922/2, 790 01 Jeseník'
UTM = 'utm_source=wwwwww.cz&utm_medium=referral&utm_campaign={c}&utm_content={x}'
def yes(path='', c='wwwwww_brand', x='web'):
    return f'https://yesmark.eu/{path}?' + UTM.format(c=c, x=x)

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

# ---------- sdílené části ----------
LOGO = ('<svg viewBox="-3 -2 132 25" aria-hidden="true">'
        '<path class="z" d="M0 2 L5 20 L10 9 L15 20 L20 2 L25 20 L30 9 L35 20 L40 2 L45 20 L50 9 L55 20 L60 2"/>'
        '<path class="z z2" d="M60 2 L65 20 L70 9 L75 20 L80 2 L85 20 L90 9 L95 20 L100 2 L105 20 L110 9 L115 20 L120 2"/></svg>')

def header():
    nav = ''.join(f'<a href="{u}">{n}</a>' for n, u in [('Služby', '/#sluzby'), ('Proces', '/#proces'), ('Reference', '/#reference'),
                                                         ('Jesenicko', '/#jesenicko'), ('Ceník', '/#cenik'), ('Kontakt', '/kontakt/')])
    code = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap">'
            '<header class="wh"><div class="wh__in">'
            f'<a class="wlogo" href="/" aria-label="wwwwww.cz – tvorba webových stránek Jeseník">{LOGO}</a>'
            f'<a class="wlogo__by" href="{yes(x="header_logo")}" target="_blank" rel="noopener">koncept<b>YES<i>MARK</i></b></a>'
            f'<nav class="wnav" aria-label="Hlavní navigace">{nav}</nav>'
            f'<a class="wbtn wbtn--ghost hide-m" href="tel:{TEL}">{TEL_H}</a>'
            '<a class="wbtn wbtn--red" href="/kontakt/#poptavka">Poptat web</a>'
            '<button class="wburger" type="button" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>'
            '</div></header>')
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
        t('<p>Odesláním souhlasíte se zpracováním údajů za účelem vyřízení poptávky. Nic dalšího s nimi neděláme.</p>', 'ww-legal'))
    return con('ww-contact', person, formcard)

def footer():
    return sec('ww-dark ww-footer', wrap('',
        con('ww-foot',
            con('', html(f'<a class="wlogo" href="/" aria-label="wwwwww.cz">{LOGO}</a>'),
                t('<p>Tvorba webových stránek a e-shopů pro firmy z Jeseníku a celého Jesenicka. <strong>wwwwww.cz je webový koncept agentury Yesmark.</strong></p>')),
            con('', h('Služby', 'div', 'ww-ft'),
                t('<p><a href="/#sluzby">Tvorba webových stránek</a><br><a href="/#sluzby">E-shopy</a><br><a href="/#sluzby">Redesign webu</a><br><a href="/#sluzby">SEO optimalizace</a><br><a href="/#sluzby">Správa webu</a></p>')),
            con('', h('Odkazy', 'div', 'ww-ft'),
                t(f'<p><a href="/kontakt/">Kontakt – tvorba webů Jeseník</a><br><a href="/#cenik">Ceník a FAQ</a><br>'
                  f'<a href="{yes("reference/", "wwwwww_reference", "footer")}" target="_blank" rel="noopener">Reference ↗</a><br>'
                  f'<a href="{yes(x="footer")}" target="_blank" rel="noopener">Yesmark.eu ↗</a></p>')),
            con('', h('Kontakt', 'div', 'ww-ft'),
                t(f'<p><a href="tel:{TEL}">+420 {TEL_H}</a><br><a href="mailto:{MAIL}">{MAIL}</a><br>Yesmark<br>{ADDR}</p>'))),
        con('ww-foot-bottom',
            t('<p>© <span data-ww-year>2026</span> wwwwww.cz · tvorba webových stránek Jeseník · koncept Yesmark</p>'),
            t('<p><a href="#">Nahoru ↑</a></p>'))), tag='footer')

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
                  + [{'@type': 'AdministrativeArea', 'name': 'Okres Jeseník'}, {'@type': 'AdministrativeArea', 'name': 'Jeseníky'}],
    'parentOrganization': {'@type': 'Organization', 'name': 'Yesmark', 'url': 'https://yesmark.eu/'},
    'employee': {'@type': 'Person', 'name': 'Roman Lukač', 'jobTitle': 'Webdesign a vývoj'},
    'knowsAbout': ['Tvorba webových stránek', 'Tvorba e-shopů', 'Webdesign', 'SEO optimalizace', 'WordPress', 'Elementor'],
}

# ---------- HLAVNÍ STRÁNKA ----------
def home():
    hero_visual = ('<div class="hv" aria-hidden="true"><div class="hv__stack">'
        '<div class="hv__win"><div class="hv__bar"><i></i><i></i><i></i><b>konradt.cz</b></div><div class="hv__body"><div class="hv__l hv__l--t"></div><div class="hv__l hv__l--m"></div><div class="hv__grid"><span></span><span></span><span></span></div></div></div>'
        '<div class="hv__win"><div class="hv__bar"><i></i><i></i><i></i><b>reality · Jeseníky</b></div><div class="hv__body"><div class="hv__img"></div><div class="hv__l hv__l--t"></div><div class="hv__l hv__l--s"></div></div></div>'
        '<div class="hv__win"><div class="hv__bar"><i></i><i></i><i></i><b>váš-novy-web.cz</b></div><div class="hv__body"><div class="hv__l hv__l--t"></div><div class="hv__l hv__l--m"></div><div class="hv__l hv__l--s"></div><div class="hv__btn"></div><div class="hv__grid"><span></span><span></span><span></span></div></div></div>'
        '<div class="hv__chip">Navrženo a postaveno v Jeseníku</div>'
        '<div class="hv__toast"><em>✓</em><div><strong>Nová poptávka z webu</strong><small>právě teď · Jeseník</small></div></div>'
        '</div></div>')
    towns = ['Jeseník', 'Lipová-lázně', 'Zlaté Hory', 'Javorník', 'Mikulovice', 'Vidnava', 'Žulová', 'Bělá pod Pradědem', 'Česká Ves', 'Velké Losiny', 'Hanušovice', 'Ramzová']
    marquee = '<div class="mq" aria-hidden="true"><div class="mq__t">' + ''.join(f'<span>{x}</span>' for x in towns * 2) + '</div></div>'

    hero = sec('ww-dark ww-hero', wrap('ww-hero-grid',
        con('ww-hero-copy',
            h('Webové studio z Jeseníku · koncept Yesmark', 'div', 'ww-eyebrow ww-rv'),
            h('Tvorba webových stránek v Jeseníku, které <span class="ww-red">prodávají.</span>', 'h1', 'ww-h1 ww-rv'),
            t('<p>Navrhneme a postavíme <strong>web nebo e-shop na míru</strong>, který zaujme, dobře se najde na Googlu a z návštěvníků dělá zákazníky. Osobně, tady na Jesenicku.</p>', 'ww-lead ww-mw ww-rv'),
            con('ww-row ww-rv',
                btn('Chci nezávaznou nabídku', '/kontakt/#poptavka'),
                btn(f'Zavolat {TEL_H}', f'tel:{TEL}', 'ww-btn--ghost ww-btn--plain')),
            t('<p><span>✓ Weby od 9 900 Kč</span><span>✓ Nabídka zdarma</span><span>✓ Osobní schůzka v Jeseníku</span></p>', 'ww-trust ww-rv')),
        html(hero_visual, 'ww-rv')), eid='uvod')

    yesmark = sec('ww-light', wrap('ww-yes ww-rv',
        h('YES<b>MARK</b>', 'div', 'ww-yesmark'),
        t('<p><strong>wwwwww.cz je webový koncept agentury Yesmark z Jeseníku.</strong> Stejný tým, stejné know-how jako u kampaní, grafiky a SEO pro naše klienty – jen s jasným zaměřením: tvorba webových stránek pro firmy a podnikatele z Jesenicka.</p>', 'ww-muted'),
        btn('Poznejte Yesmark', yes(x='homepage_strip'), 'ww-btn--dark ww-btn--ext', ext=True)))
    yesmark['settings']['css_classes'] += ' ww-yes-sec'

    def card(n, title, text, tg, main=False, d=''):
        c = con('ww-card ww-rv' + (' ww-card--main' if main else ''), h(n, 'div', 'ww-num'), h(title, 'h3', 'ww-h3'), t(f'<p>{text}</p>'), tags(*tg))
        return c
    services = sec('ww-dark', wrap('',
        head('Služby', 'Weby, které pracují za vás.', 'Postaráme se o vše od návrhu po spuštění – design, programování, obsah, SEO i analytiku. Vy řešíte byznys, web vám nosí poptávky.'),
        con('ww-bento',
            card('01 — hlavní služba', 'Tvorba webových stránek na míru', 'Od jednoduché firemní prezentace po rozsáhlý web. Moderní design, srozumitelný obsah a jasná cesta k poptávce – web, který vám dělá dobré jméno i obchod.',
                 ['UX &amp; UI design', 'Kódování na míru', 'WordPress + Elementor', 'October CMS', 'Responzivní design'], True),
            card('02', 'E-shopy', 'Přehledný obchod připravený na růst. Objednávky, platby i doprava bez starostí.', ['WooCommerce', 'PrestaShop']),
            card('03', 'Redesign webu', 'Starý web, který nic nepřináší? Převlékneme ho do moderního kabátu a postavíme znovu – tentokrát na prodej.', ['Nový design', 'Nový obsah']),
            card('04', 'SEO optimalizace', 'Struktura, obsah a technické SEO od prvního dne, aby vás zákazníci našli dřív než konkurenci.', ['On-page SEO', 'Google Firemní profil']),
            card('05', 'Správa a propagace', 'Aktualizace, zabezpečení, úpravy obsahu i PPC kampaně. Zůstáváme s vámi i po spuštění.', ['Údržba', 'PPC kampaně']),
            card('06', 'Grafika a branding', 'Logo, vizuální styl a grafika pro web i tisk – všechno pod jednou střechou Yesmark.', ['Logo', 'Vizuální styl']))), eid='sluzby')

    def why(n, title, text):
        return con('ww-rv', h(n, 'div', 'ww-ico'), h(title, 'h3', 'ww-h3'), t(f'<p>{text}</p>'))
    whysec = sec('ww-white', wrap('',
        h('Proč wwwwww', 'div', 'ww-eyebrow ww-rv'),
        h('Web není vizitka. Je to <em>obchodník</em>, který pro vás pracuje 24/7.', 'h2', 'ww-statement ww-rv'),
        con('ww-why',
            why('01', 'Design, který prodává', 'Každý prvek má důvod – přivést návštěvníka k telefonu nebo poptávce. Žádné hezké, ale prázdné stránky.'),
            why('02', 'Najde vás Google', 'Weby stavíme s ohledem na vyhledávače a místní hledání. Aby vás našli lidé z Jeseníku i turisté z celé republiky.'),
            why('03', 'Upravíte si ho sami', 'WordPress a Elementor: texty, fotky i nové stránky změníte sami. Ukážeme vám, jak na to.'),
            why('04', 'Člověk, ne tiket', 'Komunikujete přímo s tím, kdo web staví. Osobní schůzka v Jeseníku a rychlé odpovědi.'))))

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

    def ref(tag, name, text, label, url, ext=True):
        return con('ww-ref ww-rv',
            con('ww-ref-top', h(name, 'h3', 'ww-ref-name')),
            con('ww-ref-body', h(tag, 'div', 'ww-ref-tag'), t(text), btn(label, url, 'ww-btn--plain ww-btn--ext', ext=ext)))
    refs = sec('ww-light', wrap('',
        head('Reference', 'Weby, na které jsme hrdí.', 'Výběr realizací z Jeseníku a okolí. Celé portfolio webů, e-shopů a kampaní najdete na Yesmark.eu.'),
        con('ww-refs',
            ref('Web · CNC obrábění', 'Konradt',
                '<p>Pro společnost KONRADT jsme vytvořili nové webové stránky zaměřené na profesionální prezentaci služeb v oblasti CNC obrábění, montáže a zpracování kovů. Při realizaci jsme kladli důraz na moderní technický vzhled, přehledné představení výrobních možností společnosti a srozumitelnou prezentaci jednotlivých služeb.</p>'
                '<p>Součástí realizace byla také optimalizace struktury a obsahu webu s ohledem na vyhledávače a lepší dohledatelnost služeb v oblasti CNC frézování, CNC soustružení, montážních prací a dodávek odlitků.</p>',
                'konradt.cz', 'https://www.konradt.cz/'),
            ref('Web · Reality Jeseníky', 'Monika Veličková',
                '<p>Pro realitní makléřku Moniku Veličkovou jsme vytvořili nové webové stránky zaměřené na prezentaci nemovitostí a realitních služeb v Jeseníkách. Při realizaci jsme kladli důraz na moderní a osobitý design, přehlednou prezentaci nabízených nemovitostí a především na budování osobní značky, která staví na znalosti regionu, individuálním přístupu a zkušenostech s realitami i investicemi.</p>',
                'Reference na Yesmark', yes('reference/', 'wwwwww_reference', 'velickova')),
            ref('Web · Technika a služby', 'Břinčil',
                '<p>Při realizaci webu pro firmu Břinčil jsme kladli důraz na moderní a přehledný design, snadnou orientaci návštěvníků a kvalitní prezentaci společnosti i její techniky. Nový web zároveň slouží jako podpůrná prezentace hlavní společnosti Břinčil &amp; Míka s.r.o., pro kterou jsme v minulosti rovněž realizovali kompletní online prezentaci.</p>',
                'Reference na Yesmark', yes('reference/brincil-mika', 'wwwwww_reference', 'brincil'))),
        con('ww-row ww-refs-more ww-rv',
            t('<p>Další weby a e-shopy z Jesenicka najdete v portfoliu Yesmark.</p>', 'ww-muted'),
            btn('Všechny reference', yes('reference/', 'wwwwww_reference', 'homepage_all'), 'ww-btn--dark ww-btn--ext', ext=True))), eid='reference')

    rings = ''.join(f'<circle class="r" cx="270" cy="270" r="{r}"/>' for r in (46, 92, 184))
    pins = [('Lipová-lázně', 234, 273, -8, 17, 'end'), ('Česká Ves', 284, 242, 8, -4, 'start'), ('Mikulovice', 346, 199, 8, -3, 'start'),
            ('Zlaté Hory', 395, 234, 8, -3, 'start'), ('Javorník', 138, 105, -8, -7, 'end'), ('Vidnava', 258, 124, 8, -6, 'start'),
            ('Žulová', 200, 187, -8, -3, 'end'), ('Bělá pod Pradědem', 265, 337, 8, 15, 'start'), ('Velké Losiny', 162, 472, -8, 4, 'end')]
    rays = ''.join(f'<line class="ray" x1="270" y1="270" x2="{x}" y2="{y}"/>' for _, x, y, *_ in pins)
    pts = ''.join(f'<circle class="p" cx="{x}" cy="{y}" r="4"/><text class="l" x="{x+dx}" y="{y+dy}" text-anchor="{a}">{n}</text>' for n, x, y, dx, dy, a in pins)
    mapsvg = ('<div class="wmap"><svg viewBox="0 0 540 540" role="img" aria-label="Mapa Jesenicka – kde tvoříme webové stránky">'
              '<defs><linearGradient id="wsw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e3120b" stop-opacity="0"/><stop offset="1" stop-color="#e3120b" stop-opacity=".35"/></linearGradient></defs>'
              f'{rings}<circle class="r" cx="270" cy="270" r="262" stroke-dasharray="2 6"/>'
              '<path class="sw" d="M270 270 L532 270 A262 262 0 0 0 455 85 Z" fill="url(#wsw)"/>'
              f'{rays}{pts}<circle class="hqr" cx="270" cy="270" r="10"/><circle class="hq" cx="270" cy="270" r="9"/>'
              '<text class="lh" x="284" y="300">Jeseník</text></svg></div>')
    local = sec('ww-white', wrap('ww-local',
        con('ww-local-copy ww-rv',
            h('Jesenicko', 'div', 'ww-eyebrow'),
            h('Tvorba webových stránek pro Jeseník a celé Jesenicko', 'h2', 'ww-h2s'),
            t('<p>Jsme <strong>webové studio z Jeseníku</strong> a koncept agentury Yesmark. Weby tvoříme pro firmy, řemeslníky, ubytování, gastro i realitní kanceláře z Jeseníku, Lipové-lázní, Zlatých Hor, Javorníku, Mikulovic, Žulové, Bělé pod Pradědem a celých Jeseníků.</p>'
              '<h3>Weby pro ubytování a turistický ruch v Jeseníkách</h3>'
              '<p>Penziony, apartmány a chaty potřebují web, který zaujme fotkami, jasně ukáže ceny a vede k rezervaci – v češtině, němčině i polštině.</p>'
              '<h3>Weby pro řemeslníky, služby a výrobní firmy z Jesenicka</h3>'
              '<p>Instalatér z Jeseníku, truhlář ze Zlatých Hor nebo strojírna z Javorníku – každý potřebuje web, který se ukáže, když ho místní zákazník hledá na Googlu.</p>'
              '<h3>Osobně, ne přes call centrum</h3>'
              f'<p>Sídlíme v Jeseníku ({ADDR}). Rádi se potkáme u nás v kanceláři, nebo přijedeme za vámi kamkoli na Jesenicko.</p>'),
            t('<p>' + ''.join(f'<span>{x}</span>' for x in ['Jeseník', 'Lipová-lázně', 'Zlaté Hory', 'Javorník', 'Mikulovice', 'Vidnava', 'Žulová', 'Bělá pod Pradědem', 'Česká Ves', 'Velké Losiny', 'Hanušovice', 'Supíkovice']) + '</p>', 'ww-towns')),
        html(mapsvg, 'ww-rv')), eid='jesenicko')

    faq = [
        ('Kolik stojí tvorba webových stránek v Jeseníku?', 'Tvorba webových stránek začíná na 9 900 Kč. Konečná cena záleží na rozsahu, funkcích a grafickém zpracování. Po krátké konzultaci dostanete nezávaznou cenovou nabídku zdarma.'),
        ('Jak dlouho trvá vytvoření webu?', 'Jednodušší prezentační web bývá hotový zhruba za 2–4 týdny, web na míru nebo e-shop podle rozsahu za 4–8 týdnů. Přesný harmonogram dostanete v nabídce.'),
        ('Budu si moci web upravovat sám?', 'Ano. Stavíme na WordPressu a Elementoru, pro zcela individuální projekty na October CMS. Texty, fotky i nové stránky si pohodlně upravíte sami a ukážeme vám, jak na to.'),
        ('Jaký je vztah wwwwww.cz a agentury Yesmark?', 'wwwwww.cz je webový koncept marketingové agentury Yesmark z Jeseníku. Za weby stojí stejný tým – a když budete chtít, navážeme grafikou, kampaněmi nebo reklamními předměty.'),
        ('Děláte weby jen pro firmy z Jesenicka?', 'Sídlíme v Jeseníku a místní firmy jsou naše srdcovka – osobní schůzka je tu samozřejmost. Weby ale tvoříme pro klienty z celého Česka.'),
        ('Postaráte se i o SEO, doménu a hosting?', 'Ano. Každý web stavíme s ohledem na vyhledávače, pomůžeme s doménou i hostingem a po spuštění zajistíme správu, zabezpečení i propagaci.'),
    ]
    pricing = sec('ww-dark', wrap('ww-price',
        con('ww-price-card ww-rv',
            h('Ceník', 'div', 'ww-eyebrow'),
            h('<small>Tvorba webových stránek</small>od 9 900 Kč', 'div', 'ww-price-num'),
            t('<p>Konečná částka se odvíjí od rozsahu, funkcí a grafického zpracování. Každý projekt naceňujeme individuálně – férově a za skutečný přínos.</p>', 'ww-muted'),
            con('ww-row', btn('Chci cenovou nabídku', '/kontakt/#poptavka'))),
        con('ww-rv', h('Časté otázky', 'h2', 'ww-h2s'),
            w('toggle', 'ww-faq', faq_schema='yes', tabs=[{'_id': uid(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in faq]))), eid='cenik')

    contact = sec('ww-light', wrap('',
        head('Poptávka', 'Pojďme postavit váš nový web.', 'Napište pár vět nebo rovnou zavolejte. Ozvu se obvykle do jednoho pracovního dne s dalším postupem.'),
        contact_section('home')), eid='poptavka')

    cta = sec('ww-redbg ww-cta', wrap('ww-cta ww-rv',
        h('Nový web na Jesenicku?', 'div', 'ww-eyebrow'),
        h('Začneme jedním<br>telefonátem.', 'h2', 'ww-mega'),
        con('ww-row', btn(f'Zavolat {TEL_H}', f'tel:{TEL}', 'ww-btn--white ww-btn--plain'), btn('Napsat poptávku', '/kontakt/#poptavka', 'ww-btn--dark'))))

    ld = {'@context': 'https://schema.org', '@graph': [BUSINESS, {'@type': 'WebSite', '@id': 'https://wwwwww.cz/#web', 'url': 'https://wwwwww.cz/', 'name': 'wwwwww.cz', 'inLanguage': 'cs-CZ', 'publisher': {'@id': 'https://wwwwww.cz/#business'}}]}
    return [header(), hero, html_section(marquee), yesmark, services, whysec, process, refs, local, pricing, contact, cta, footer(),
            system(ld, '<a class="wbtn wbtn--red" href="#poptavka">Poptat web</a>')]

def html_section(code):
    return con('ww ww-marq', html(code), inner=False)

# ---------- KONTAKT ----------
def kontakt():
    hero = sec('ww-dark ww-phero', wrap('ww-stack',
        t('<p><a href="/">wwwwww.cz</a> / kontakt</p>', 'ww-crumbs'),
        h('Kontakt – tvorba webových stránek <span class="ww-red">Jeseník</span>', 'h1', 'ww-h1 ww-rv'),
        t('<p>Nový web, e-shop nebo redesign? Napište, zavolejte, nebo se zastavte v kanceláři Yesmark v Jeseníku. Nabídku připravím zdarma.</p>', 'ww-lead ww-mw ww-rv')))
    contact = sec('ww-light', wrap('', contact_section('kontakt')), eid='poptavka')
    contact['settings']['css_classes'] += ' ww-tight'

    def step(n, title, text):
        return con('ww-rv', h(n, 'div', 'ww-ico'), h(title, 'h3', 'ww-h3'), t(f'<p>{text}</p>'))
    nextsteps = sec('ww-white', wrap('',
        h('Co bude dál', 'div', 'ww-eyebrow ww-rv'),
        h('Žádné formuláře do prázdna. Ozve se vám <em>člověk</em>.', 'h2', 'ww-statement ww-rv'),
        con('ww-why',
            step('01', 'Ozvu se', 'Obvykle do jednoho pracovního dne – telefonem nebo e-mailem, jak vám to sedí.'),
            step('02', 'Konzultace', 'Krátký hovor nebo schůzka v Jeseníku. Projdeme cíle, konkurenci a rozsah.'),
            step('03', 'Nabídka', 'Jasná cena, rozsah a termín. Zdarma a nezávazně.'),
            step('04', 'Start', 'Pustíme se do návrhu. Průběžně vidíte, jak web roste.'))))
    nap = sec('ww-light', wrap('ww-nap',
        con('ww-napcard ww-rv',
            h('Kde nás najdete', 'div', 'ww-eyebrow'),
            h('Yesmark · wwwwww.cz', 'h2', 'ww-h2s'),
            t(f'<p><strong>{ADDR}</strong></p><p>Telefon: <a href="tel:{TEL}">+420 {TEL_H}</a><br>E-mail: <a href="mailto:{MAIL}">{MAIL}</a></p>'
              '<p>Tvoříme webové stránky pro Jeseník, Lipovou-lázně, Zlaté Hory, Javorník, Mikulovice, Žulovou, Bělou pod Pradědem a celé Jesenicko.</p>', 'ww-muted'),
            con('ww-row', btn('Prohlédnout reference', yes('reference/', 'wwwwww_reference', 'kontakt'), 'ww-btn--dark ww-btn--ext', ext=True))),
        w('google_maps', 'ww-mapw ww-rv', address='Boženy Němcové 922/2, Jeseník', zoom={'unit': 'px', 'size': 15, 'sizes': []},
          height={'unit': 'px', 'size': 460, 'sizes': []})))
    ld = {'@context': 'https://schema.org', '@graph': [
        BUSINESS,
        {'@type': 'ContactPage', 'url': 'https://wwwwww.cz/kontakt/', 'name': 'Kontakt – tvorba webových stránek Jeseník', 'about': {'@id': 'https://wwwwww.cz/#business'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Tvorba webových stránek Jeseník', 'item': 'https://wwwwww.cz/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Kontakt', 'item': 'https://wwwwww.cz/kontakt/'}]}]}
    return [header(), hero, contact, nextsteps, nap, footer(),
            system(ld, f'<a class="wbtn wbtn--red" href="mailto:{MAIL}">Napsat e-mail</a>')]

if __name__ == '__main__':
    for name, fn in [('home', home), ('kontakt', kontakt)]:
        data = fn()
        (OUT / f'{name}.json').write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        print(name, len(json.dumps(data)) // 1024, 'kB')
