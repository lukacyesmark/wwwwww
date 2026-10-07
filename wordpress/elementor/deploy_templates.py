# Vytvoří / aktualizuje globální šablony hlavičky a patičky v Elementoru a uloží jejich ID do tpl.json.
# Spuštění: python3 deploy_templates.py  (potřebuje wp.py s přístupem k REST API)
import json, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, '/tmp/claude-0/-home-user-wwwwww/994a82ae-2ecd-5423-8b81-22f8862c045f/scratchpad')
from wp import api
TPLS = {'header': ('ww-globalni-hlavicka', 'wwwwww – globální hlavička', 'tpl-header.json'),
        'footer': ('ww-globalni-paticka', 'wwwwww – globální patička + skripty', 'tpl-footer.json')}
subprocess.run([sys.executable, str(HERE / 'build.py'), '23', 'https://wwwwww.cz/wp-content/uploads/2026/10/roman-lukac-tvorba-webu-jesenik.jpg'], check=True, stdout=subprocess.DEVNULL)
ids = {}
for key, (slug, title, f) in TPLS.items():
    meta = {'_elementor_data': (HERE / 'out' / f).read_text(encoding='utf-8'), '_elementor_edit_mode': 'builder', '_elementor_template_type': 'container'}
    r = api('GET', f'/wp/v2/elementor_library?slug={slug}&status=publish,draft&_fields=id')
    body = {'title': title, 'status': 'publish', 'meta': meta}
    res = api('POST', f'/wp/v2/elementor_library/{r[0]["id"]}', body) if r else api('POST', '/wp/v2/elementor_library', dict(body, slug=slug))
    if '_error' in res: sys.exit(f'ERR {key} {res}')
    ids[key] = res['id']; print(key, res['id'])
(HERE / 'tpl.json').write_text(json.dumps(ids, indent=1))
try: api('DELETE', '/elementor/v1/cache')
except Exception: pass
