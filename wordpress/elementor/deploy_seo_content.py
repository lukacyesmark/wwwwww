import sys, json, pathlib, importlib.util
from wp import api
sys.path.insert(0,'/home/user/wwwwww/wordpress/elementor')
spec=importlib.util.spec_from_file_location('b','/home/user/wwwwww/wordpress/elementor/build.py'); b=importlib.util.module_from_spec(spec)
sys.argv=['x','23','https://wwwwww.cz/wp-content/uploads/2026/10/roman-lukac-tvorba-webu-jesenik.jpg']; spec.loader.exec_module(b)
O=pathlib.Path('/home/user/wwwwww/wordpress/elementor/out')
def pid(slug):
    r=api('GET',f'/wp/v2/pages?slug={slug}&status=publish&_fields=id')
    return r[0]['id'] if r else None
jobs=[]  # (slug, htmlfile, jsonfile or None, rm title)

for o in b.OBORY: jobs.append((b.obor_url(o).strip('/'),f'obor-{o["slug"]}',True,b.obor_title(o)))
jobs.append(('weby-pro-obory','obory-hub',True,f'Weby pro {len(b.OBORY)} oborů – co by měl mít váš web | wwwwww.cz'))
for c in b.CITIES: jobs.append((f'tvorba-webovych-stranek-{c["slug"]}',f'mesto-{c["slug"]}',True,f'Tvorba webových stránek {c["name"]} | weby od 9 900 Kč'))
jobs.append(('zasady-ochrany-osobnich-udaju','zasady',True,None))
jobs=[j for j in jobs if j[1]]
ids={'home':14,'kontakt':15}
for name,title in [('home','Tvorba webových stránek Jeseník | weby od 9 900 Kč'),('kontakt',None)]:
    jobs.append((None,name,True,title))
which=sys.stdin.read().split()
for slug,f,data,title in jobs:
    if which and 'all' not in which and f not in which: continue
    i=ids.get(f) or pid(slug)
    if not i: print('MISSING',slug); continue
    body={'content':(O/f'{f}.html').read_text(encoding='utf-8')}
    if data: body['meta']={'_elementor_data':(O/f'{f}.json').read_text(encoding='utf-8')}
    r=api('POST',f'/wp/v2/pages/{i}',body)
    if '_error' in r: print('ERR',f,r); continue
    if title:
        m=api('POST','/rankmath/v1/updateMeta',{'objectType':'post','objectID':i,'meta':{'rank_math_title':title}})
    print(i,f,len(r['content']['raw'] if 'raw' in r['content'] else r['content']['rendered']),title or '',flush=True)
try: api('DELETE','/elementor/v1/cache')
except Exception: pass
