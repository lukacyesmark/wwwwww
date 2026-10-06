# Nasazení na WordPress (wwwwww.cz)

1. **Hello Elementor → Nastavení**: vypnout `style.css`, `theme.css`, hlavičku a patičku šablony a titulek stránky.
2. **Pluginy → Přidat**: nainstalovat a aktivovat *Contact Form 7*.
3. **Kontakt → Přidat nový**: vložit šablonu a nastavení e-mailu z `contact-form-7.txt`, uložit a poznamenat si ID formuláře.
4. V souborech `uvod.html` a `kontakt.html` nahradit `CF7_ID` tímto ID.
5. **Stránky → Přidat**:
   - „Tvorba webových stránek Jeseník“: blok *Vlastní HTML* s obsahem `uvod.html`, šablona *Elementor Canvas*, do stručného výpisu (excerpt) meta popis.
   - „Kontakt“ (slug `kontakt`): totéž s obsahem `kontakt.html`.
6. **Nastavení → Čtení**: jako úvodní stránku nastavit „Tvorba webových stránek Jeseník“.
7. Smazat ukázky „Sample Page“ a „Hello world!“ a vyčistit cache v LiteSpeed Cache.
