# wwwwww.cz — tvorba webů Jeseník

Statický web (HTML + CSS + vanilla JS, bez knihoven) + PHP skript pro poptávkový formulář.

## Struktura
- `index.html` — hlavní stránka (služby, proces, konfigurátor zadání, reference, lokální SEO, FAQ, poptávka)
- `kontakt/index.html` — kontakt
- `404.html` — chybová stránka
- `send.php` — odeslání formuláře na `lukac@yesmark.eu` (antispam: honeypot + časová pojistka)
- `assets/` — CSS, JS, obrázky
- `.htaccess` — HTTPS, přesměrování starých WP URL, cache, komprese
- `robots.txt`, `sitemap.xml`

## Nasazení
Nahrát obsah repozitáře do kořene webu (hosting s PHP a Apache). Původní WordPress je potřeba
z kořene odstranit nebo přesunout, jinak bude mít přednost jeho `index.php`/`.htaccess`.

Pro doručitelnost e-mailů z formuláře musí adresa `web@wwwwww.cz` (konstanta `FROM` v `send.php`)
patřit doméně a mít správný SPF záznam.

## Měření
Kliky na CTA a odeslání formuláře se posílají do `window.dataLayer`
(`cta_click`, `configurator_send`, `generate_lead`) — stačí doplnit GTM / GA4.
Odkazy na yesmark.eu mají UTM `utm_source=wwwwww.cz&utm_medium=referral&utm_campaign=wwwwww_reference|wwwwww_brand`.
