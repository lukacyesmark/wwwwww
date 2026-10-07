import sys, json, pathlib
sys.path.insert(0,'/home/user/wwwwww/wordpress/elementor')
from wp import api
from cities import CITIES
O=pathlib.Path('/home/user/wwwwww/wordpress/elementor/out')
ids={}
for c in CITIES:
    slug='tvorba-webovych-stranek-'+c['slug']
    found=api('GET',f'/wp/v2/pages?slug={slug}&status=publish&_fields=id')
    if not found: print('CHYBÍ', slug); continue   # nikdy nezakládat nové
    pid=found[0]['id']
    meta={"_elementor_data":(O/f"mesto-{c['slug']}.json").read_text(encoding='utf-8')}
    r=api('POST',f"/wp/v2/pages/{pid}",{"meta":meta})
    if '_error' in r: print(c['slug'],r); continue
    ids[c['slug']]=pid; print('upd', pid, slug, flush=True)
json.dump(ids,open('city_pages.json','w'),indent=1)
try: api('DELETE','/elementor/v1/cache')
except Exception: pass
