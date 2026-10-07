import sys
exec(open('deploy_obory.py').read())
which=sys.stdin.read().split()
ids={}
if 'hub' in which or 'all' in which:
    ids['hub']=upsert('weby-pro-obory','Weby pro obory – co by měl mít web pro váš obor',
        'Co by měl mít web pro kadeřnictví, penzion, stavební firmu a dalších 70 oborů? Checklisty, struktura webu a SEO tipy od wwwwww.cz.','obory-hub.json','weby pro obory,web pro firmu,webové stránky pro živnostníky')
for o in b.OBORY:
    if 'all' not in which and o['slug'] not in which: continue
    slug=b.obor_url(o).strip('/')
    kw=o['name'].lower()
    ex=f"{o['name']}: co by měl mít, ukázková struktura stránek, funkce a SEO tipy. Weby od 9 900 Kč – wwwwww.cz, koncept agentury Yesmark."
    if len(ex)>160: ex=f"{o['name']}: co by měl mít, struktura stránek, funkce a SEO tipy. Weby od 9 900 Kč – wwwwww.cz."
    ids[o['slug']]=upsert(slug,f"{o['name']} – co by měl mít",ex[:160],f"obor-{o['slug']}.json",f"{kw},tvorba webu pro {o['short']}")
    print(ids[o['slug']], slug, flush=True)
import json; old={}
try: old=json.load(open('obory_pages.json'))
except Exception: pass
old.update({k:v for k,v in ids.items() if v}); json.dump(old,open('obory_pages.json','w'),indent=1)
try: api('DELETE','/elementor/v1/cache')
except Exception: pass
