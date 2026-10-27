# Náhled podstránky v designu v4: vezme hotovou stránku z out/ (výchozí mesto-sumperk), nahradí globální šablony
# hlavičkou a patičkou v4 a nahraje ji na skrytou adresu /novy-design-3-podstranka/ (noindex).
# Spuštění: python3 deploy_preview4_sub.py [nazev-souboru-bez-pripony]
import json, sys, pathlib, importlib.util
HERE = pathlib.Path(__file__).resolve().parent
src = sys.argv[1] if len(sys.argv) > 1 else 'mesto-sumperk'
sys.argv = ['x']
sys.path.insert(0, '/tmp/claude-0/-home-user-wwwwww/994a82ae-2ecd-5423-8b81-22f8862c045f/scratchpad')
from wp import api
_sp = importlib.util.spec_from_file_location('hv4', HERE / 'home_v4.py'); hv4 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(hv4)
O = HERE / 'out'
d = json.loads((O / f'{src}.json').read_text(encoding='utf-8'))
body = [e for e in d if not any(c in e['settings'].get('css_classes', '') for c in ('ww-tpl', 'ww-sys'))]
d = [hv4.v4_header()] + body + [hv4.v4_footer(), hv4.v4_sys(False, extra_ld=False)]
slug = 'novy-design-3-podstranka'
meta = {'_elementor_data': json.dumps(d, ensure_ascii=False), '_elementor_edit_mode': 'builder',
        '_elementor_template_type': 'wp-page', '_elementor_page_settings': {'hide_title': 'yes'}}
body = {'title': 'Návrh designu 3 – podstránka', 'content': (O / f'{src}.html').read_text(encoding='utf-8'), 'meta': meta}
r = api('GET', f'/wp/v2/pages?slug={slug}&status=publish,draft,private&_fields=id')
res = api('POST', f'/wp/v2/pages/{r[0]["id"]}', body) if r else api('POST', '/wp/v2/pages', dict(body, slug=slug, status='publish', template='elementor_canvas', comment_status='closed', ping_status='closed'))
if '_error' in res: sys.exit(res)
api('POST', '/rankmath/v1/updateMeta', {'objectType': 'post', 'objectID': res['id'], 'meta': {'rank_math_robots': ['noindex', 'nofollow']}})
try: api('DELETE', '/elementor/v1/cache')
except Exception: pass
print(res['id'], res['link'])
