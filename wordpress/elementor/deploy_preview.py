# Nahraje návrh nové hlavní stránky na skrytou adresu /novy-design/ (noindex).
import sys, pathlib
sys.path.insert(0, '/tmp/claude-0/-home-user-wwwwww/994a82ae-2ecd-5423-8b81-22f8862c045f/scratchpad')
from wp import api
O = pathlib.Path(__file__).resolve().parent / 'out'
slug = 'novy-design'
meta = {'_elementor_data': (O / 'home-v2.json').read_text(encoding='utf-8'), '_elementor_edit_mode': 'builder',
        '_elementor_template_type': 'wp-page', '_elementor_page_settings': {'hide_title': 'yes'}}
body = {'title': 'Návrh nového designu', 'content': (O / 'home-v2.html').read_text(encoding='utf-8'), 'meta': meta}
r = api('GET', f'/wp/v2/pages?slug={slug}&status=publish,draft,private&_fields=id')
res = api('POST', f'/wp/v2/pages/{r[0]["id"]}', body) if r else api('POST', '/wp/v2/pages', dict(body, slug=slug, status='publish', template='elementor_canvas', comment_status='closed', ping_status='closed'))
if '_error' in res: sys.exit(res)
api('POST', '/rankmath/v1/updateMeta', {'objectType': 'post', 'objectID': res['id'], 'meta': {'rank_math_robots': ['noindex', 'nofollow']}})
try: api('DELETE', '/elementor/v1/cache')
except Exception: pass
print(res['id'], res['link'])
