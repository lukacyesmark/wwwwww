import sys, json, pathlib
sys.path.insert(0,'/home/user/wwwwww/wordpress/elementor')
from wp import api
import importlib.util
spec=importlib.util.spec_from_file_location('b','/home/user/wwwwww/wordpress/elementor/build.py'); b=importlib.util.module_from_spec(spec)
sys.argv=['x','23','https://wwwwww.cz/wp-content/uploads/2026/10/roman-lukac-tvorba-webu-jesenik.jpg']; spec.loader.exec_module(b)
O=pathlib.Path('/home/user/wwwwww/wordpress/elementor/out')
og=api('GET','/wp/v2/media?search=tvorba-webovych-stranek-jesenik-og&_fields=id,source_url')[0]
only=set(sys.argv[1:]) if False else None
def page_id(slug):
    r=api('GET',f'/wp/v2/pages?slug={slug}&status=publish,draft&_fields=id')
    return r[0]['id'] if r else None
def upsert(slug,title,excerpt,datafile,kw):
    meta={"_elementor_data":(O/datafile).read_text(encoding='utf-8'),"_elementor_edit_mode":"builder","_elementor_template_type":"wp-page","_elementor_page_settings":{"hide_title":"yes"}}
    pid=page_id(slug)
    body={"title":title,"excerpt":excerpt,"meta":meta}
    if pid: r=api('POST',f'/wp/v2/pages/{pid}',body)
    else: r=api('POST','/wp/v2/pages',dict(body,slug=slug,status="publish",template="elementor_canvas",content="",comment_status="closed",ping_status="closed"))
    if '_error' in r: print('ERR',slug,r); return None
    api('POST','/rankmath/v1/updateMeta',{"objectType":"post","objectID":r['id'],"meta":{"rank_math_focus_keyword":kw,"rank_math_facebook_image":og['source_url'],"rank_math_facebook_image_id":og['id'],"rank_math_twitter_use_facebook":"on"}})
    return r['id']
targets=sys.argv_targets if hasattr(sys,'argv_targets') else None
