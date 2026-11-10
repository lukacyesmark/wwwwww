# Indexace stránek oborů. Ponechá v indexu jen vybrané obory, ostatním nastaví noindex (follow zůstává).
# Spuštění: python3 obory_robots.py noindex   – stáhne nevybrané obory z indexu
#           python3 obory_robots.py index     – vrátí všechny obory do indexu
import sys, json, pathlib, importlib.util
HERE = pathlib.Path(__file__).resolve().parent
mode = sys.argv[1] if len(sys.argv) > 1 else ''
if mode not in ('noindex', 'index'): sys.exit('použití: python3 obory_robots.py noindex|index')
sys.argv = ['x', '23', 'u']
sys.path.insert(0, '/tmp/claude-0/-home-user-wwwwww/994a82ae-2ecd-5423-8b81-22f8862c045f/scratchpad')
from wp import api
_sp = importlib.util.spec_from_file_location('b', HERE / 'build.py'); b = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(b)

# obory s největším potenciálem (hledanost v ČR, místní trh, reference) – zůstávají v indexu
KEEP = {'web-pro-restaurace', 'web-pro-penzion', 'web-pro-svj', 'web-pro-skola', 'web-pro-realitni-makler'}

done = []
for o in b.OBORY:
    slug = b.obor_url(o).strip('/')
    robots = ['index', 'follow'] if (mode == 'index' or slug in KEEP) else ['noindex', 'follow']
    r = api('GET', f'/wp/v2/pages?slug={slug}&status=publish&_fields=id')
    if not r: print('CHYBÍ', slug); continue
    res = api('POST', '/rankmath/v1/updateMeta', {'objectType': 'post', 'objectID': r[0]['id'], 'meta': {'rank_math_robots': robots}})
    if isinstance(res, dict) and '_error' in res: print('ERR', slug, res); continue
    done.append((slug, robots[0]))
    print(robots[0], slug, flush=True)
print('hotovo', len(done), 'index:', sum(1 for _, x in done if x == 'index'), 'noindex:', sum(1 for _, x in done if x == 'noindex'))
try: api('DELETE', '/elementor/v1/cache')
except Exception: pass
