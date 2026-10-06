"""Sestaví obsah WP stránek (blok Vlastní HTML) ze statické verze webu.
Použití: python3 wordpress/build.py <CF7_ID>
"""
import base64, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CF7_ID = sys.argv[1] if len(sys.argv) > 1 else 'CF7_ID'

css = (ROOT / 'assets/css/style.css').read_text(encoding='utf-8')
css += ("\n/* WP: pojistky proti stylům šablony a pluginů */\n"
        "body{margin:0}.ww-root a:hover{color:inherit}"
        ".ww-root .btn--accent,.ww-root .btn--accent:hover{color:var(--accent-ink)}"
        ".ww-root .btn--dark,.ww-root .btn--dark:hover{color:var(--paper)}"
        ".ww-root .nav a:hover{color:var(--text)}"
        ".ww-root .footer a:hover,.ww-root .refs-more__list a:hover{color:var(--accent)}"
        ".ww-root button:hover,.ww-root button:focus{background:transparent}\n")
js = (ROOT / 'assets/js/main.js').read_text(encoding='utf-8')
js = js.replace('      `jQuery, pluginy <span class="v">0</span> <span class="ok">✓</span>`,\n',
                '      `mobile first &nbsp;&nbsp;<span class="v">ano</span> <span class="ok">✓</span>`,\n')
webp = 'data:image/webp;base64,' + base64.b64encode((ROOT / 'assets/img/roman-lukac.webp').read_bytes()).decode()

for src, out in [('index.html', 'uvod.html'), ('kontakt/index.html', 'kontakt.html')]:
    h = (ROOT / src).read_text(encoding='utf-8')
    ld = re.search(r'<script type="application/ld\+json">.*?</script>', h, re.S).group(0)
    body = h[h.index('<a class="skip"'):h.index('<script src="/assets/js/main.js"')]
    body = body.replace('<picture><source srcset="/assets/img/roman-lukac.webp" type="image/webp"><img src="/assets/img/roman-lukac.jpg"',
                        f'<picture><img src="{webp}"')
    body = body.replace('action="/send.php" method="post" data-form', f'method="post" data-form data-cf7="{CF7_ID}"')
    body = body.replace('<div class="stat"><div class="stat__v">0</div><div class="stat__l">sledovacích cookies a pluginů navíc</div></div>',
                        '<div class="stat"><div class="stat__v">24/7</div><div class="stat__l">web, který sbírá poptávky i v noci</div></div>')
    body = '<div class="ww-root">\n' + body + '</div>\n'
    # JS v base64: filtry WordPressu (wptexturize & spol.) by jinak mohly přepsat např. && na &#038;&#038;
    js_b64 = base64.b64encode(js.encode('utf-8')).decode()
    loader = ('<script>(function(){var b=atob("' + js_b64 + '");'
              'new Function(new TextDecoder().decode(Uint8Array.from(b,function(c){return c.charCodeAt(0)})))()})()</script>')
    content = ("<!-- wp:html -->\n<script>document.documentElement.classList.add('js')</script>\n"
               f"<style>\n{css}</style>\n{ld}\n{body}{loader}\n<!-- /wp:html -->\n")
    (ROOT / 'wordpress' / out).write_text(content, encoding='utf-8')
    print(out, len(content) // 1024, 'kB')
