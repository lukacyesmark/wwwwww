# wwwwww.cz — Elementor verze (aktuální)

Web běží na WordPressu (šablona Hello Elementor, Elementor Pro). Stránky jsou složené z nativních
widgetů, texty se upravují přímo v Elementoru. Vzhled řeší globální CSS a třídy `ww-…`.

- `ww.css`: globální styly. Nasazené v Elementor → Nastavení webu → Vlastní CSS.
- `ww.js`: interakce (menu, animace, měření kliků). Vložené zakódované v HTML widgetu „ww-sys“ na konci stránky.
- `build.py`: generuje `_elementor_data` pro úvod (ID 14) a kontakt (ID 15) do `out/`.

Úpravy textů dělejte v Elementoru. Pokud stránky přegenerujete z `build.py`, změny udělané v Elementoru se přepíšou.
Formulář je widget Elementor Pro a posílá poptávky na lukac@yesmark.eu.
