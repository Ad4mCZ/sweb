# Sweb - Webový prohlížeč pro seniory

[![en](https://img.shields.io/badge/lang-en-green?style=for-the-badge)](https://github.com/Ad4mCZ/sweb/blob/main/README.md)

**Sweb** je modulární a přístupný webový prohlížeč navržený speciálně pro seniory. Aplikace byla vyvinuta jako součást diplomové práce na Fakultě elektrotechniky a komunikačních technologií Vysokého učení technického v Brně (FEKT VUT) s využitím Pythonu, PyQt6 a QtWebEngine. Prohlížeč se zaměřuje na odstranění běžných frustrací, kterým starší dospělí čelí při procházení moderního webu, a to poskytnutím jednoduchého a bezpečného prostředí bez rušivých elementů.

## 🌟 Hlavní funkce
* **Zjednodušené rozhraní:** Velká, jasně označená tlačítka a intuitivní navigační lišta přizpůsobená pro sníženou motorickou přesnost.
* **Kioskový režim (Kiosk Mode):** Spuštění v režimu celé obrazovky bez rámečku zabraňuje nechtěnému minimalizování, změně velikosti nebo ukončení aplikace.
* **Integrovaný AdBlock:** Automatický síťový filtr, který blokuje reklamy a sledovací skripty, čímž zajišťuje čistý zážitek ze čtení a předchází pádům vykreslovacího jádra na náročných stránkách.
* **Modulární architektura:** Rozšiřitelný systém doplňků (`module_manager`) pro snadnou integraci funkcí na pozadí (jako AdBlock) a rozšíření uživatelského rozhraní (jako připravovaná Lupa).
* **Multiplatformní stabilita:** Upravená konfigurace jádra Chromium pro zajištění plynulého chodu napříč prostředími, od Linuxu po macOS.

## ⚙️ Konfigurační soubory
Prohlížeč je plně přizpůsobitelný pomocí JSON souborů, což udržuje uživatelská data a preference oddělené od zdrojového kódu. Tyto soubory jsou bezpečně uloženy v konfigurační složce aplikace specifické pro daný operační systém (Linux: `~/.config/vut/sweb` a `~/.local/share/vut/sweb`; macOS: `~/Library/Application Support/vut/sweb` a `~/Library/Preferences/vut/sweb`):

* `config.json` - Spravuje obecná nastavení prohlížeče, stavy uživatelského rozhraní a konfigurace motivů.
* `bookmarks.json` - Ukládá předdefinované oblíbené webové stránky (např. Seznam, ČT24, Počasí) zobrazené přímo na hlavní obrazovce.
* `adblock.json` - Obsahuje snadno udržovatelný a rozšiřitelný seznam blokovaných reklamních a sledovacích domén.

## 🎨 Vizuální režimy
Sweb nabízí různé vizuální motivy, aby vyhověl různým zrakovým potřebám. Níže uvedené animace demonstrují výchozí zobrazení rozhraní, stejně jako zřetelnou vizuální odezvu poskytovanou při **najetí myší (hover)** a **kliknutí (click)**.

### Výchozí barevné schéma
*(Standardní, klidný vizuální motiv navržený pro každodenní použití.)*  
![Výchozí barevné schéma](images/default_gif.gif)

### Vysoký kontrast
*(Speciální režim maximalizující viditelnost textu a prvků pro uživatele se zrakovým postižením.)*  
![Vysoký kontrast](images/highcontrast_gif.gif)
