import sys, json, pathlib
sys.path.insert(0,'/home/user/wwwwww/wordpress/elementor')
from wp import api
from sluzby import S
O=pathlib.Path('/home/user/wwwwww/wordpress/elementor/out')
og=api('GET','/wp/v2/media?search=tvorba-webovych-stranek-jesenik-og&_fields=id,source_url')[0]
ids={}
for x in S:
    r=api('GET',f'/wp/v2/pages?slug={x["slug"]}&status=publish,draft,private&_fields=id,status')
    meta={"_elementor_data":(O/f'sluzba-{x["slug"]}.json').read_text(encoding='utf-8'),"_elementor_edit_mode":"builder","_elementor_template_type":"wp-page","_elementor_page_settings":{"hide_title":"yes"}}
    body={"title":x['h1'],"excerpt":x['desc'],"content":(O/f'sluzba-{x["slug"]}.html').read_text(encoding='utf-8'),"meta":meta}
    if r: res=api('POST',f'/wp/v2/pages/{r[0]["id"]}',dict(body,status='publish'))
    else: res=api('POST','/wp/v2/pages',dict(body,slug=x['slug'],status="publish",template="elementor_canvas",comment_status="closed",ping_status="closed"))
    if '_error' in res: print('ERR',x['slug'],res); continue
    i=res['id']; ids[x['slug']]=i
    m=api('POST','/rankmath/v1/updateMeta',{"objectType":"post","objectID":i,"meta":{"rank_math_focus_keyword":x['kw']+','+x['extra'],"rank_math_title":x['title'],"rank_math_description":x['desc'],
        "rank_math_facebook_image":og['source_url'],"rank_math_facebook_image_id":og['id'],"rank_math_twitter_use_facebook":"on"}})
    print(i,x['slug'],res['link'],flush=True)
json.dump(ids,open('sluzby_pages.json','w'),indent=1)
try: api('DELETE','/elementor/v1/cache')
except Exception: pass
