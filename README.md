# Sweb - Senior-Friendly Web Browser

[![cs](https://img.shields.io/badge/lang-cs-green?style=for-the-badge)](https://github.com/Ad4mCZ/sweb/blob/main/README.cs.md)

**Sweb** is a modular and accessible web browser designed specifically for seniors. Developed as part of a diploma thesis at the Faculty of Electrical Engineering and Communication, Brno University of Technology, the application is built with Python, PyQt6, and QtWebEngine. The browser focuses on eliminating common frustrations older adults face when navigating the modern web by providing a distraction-free, simplified, and safe environment.

## 🌟 Key Features
* **Simplified Interface:** Large, clearly labeled buttons and an intuitive navigation bar tailored for reduced motor precision.
* **Kiosk Mode:** Fullscreen, frameless window execution prevents accidental application minimization, resizing, or exits.
* **Built-in AdBlock:** An automatic network-level interceptor that blocks ads and tracking scripts, ensuring a clean reading experience and preventing core render crashes on heavy sites.
* **Modular Architecture:** An extensible plugin system (`module_manager`) for easily integrating background features (like AdBlock) and UI extensions (like Magnifier (TBA)).
* **Cross-Platform Stability:** Hardened Chromium engine configurations to ensure smooth performance across environments, from Linux to macOS.

## ⚙️ Configuration Files
The browser is fully customizable via JSON files, keeping user data and preferences separated from the source code. These files are securely stored in the OS-specific application configuration directory (Linux: `~/.config/vut/sweb` and `~/.local/share/vut/sweb`; macOS: `~/Library/Application Support/vut/sweb` and `~/Library/Preferences/vut/sweb`):

* `config.json` - Manages general browser settings, UI states, and theme configurations.
* `bookmarks.json` - Stores pre-defined favorite websites (e.g., Seznam, ČT24, Počasí) displayed directly on the main screen.
* `adblock.json` - Contains a maintainable, easily extensible list of blocked advertising and tracking domains.

### `config.json` Options

| Key | Default | Description |
|-----|---------|-------------|
| `ui_font_size` | `24` | Font size (in `px`) of button labels in the navigation bar. |
| `web_zoom_factor` | `1.5` | Default zoom level for web pages (`1.0` = 100%, `1.5` = 150%). |
| `color_theme` | `"default"` | Visual theme of the navigation bar: `"default"` or `"high_contrast"`. |
| `home_url` | `"https://www.seznam.cz"` | Initial page loaded on startup and when navigating home. |
| `search_url` | `"https://search.seznam.cz/?q={}"` | Search engine URL template (`{}` is replaced with the URL-encoded query). |
| `search_button_position` | `"after"` | Position of the Search button in Menu 2 relative to bookmarks: `"before"` or `"after"`. |

Example `config.json`:
```json
{
    "ui_font_size": 24,
    "web_zoom_factor": 1.5,
    "color_theme": "default",
    "home_url": "https://www.seznam.cz",
    "search_url": "https://search.seznam.cz/?q={}",
    "search_button_position": "after"
}
```

Example `bookmarks.json`:
```json
{
    "first_menu": [
        {
            "name": "Seznam",
            "url": "https://www.seznam.cz"
        },
        {
            "name": "ČT24",
            "url": "https://ct24.ceskatelevize.cz"
        },
        {
            "name": "Počasí",
            "url": "https://www.in-pocasi.cz"
        }
    ],
    "second_menu": [
        {
            "name": "Deník",
            "url": "https://www.denik.cz"
        },
        {
            "name": "Novinky",
            "url": "https://www.novinky.cz"
        },
        {
            "name": "Lékárna",
            "url": "https://www.lekarna.cz"
        }
    ]
}
```

Example `adblock.json`:
```json
{
    "blocked_domains": [
        "doubleclick.net",
        "googlesyndication.com",
        "google-analytics.com",
        "googletagmanager.com",
        "clarity.ms",
        "facebook.com/tr",
        "imrworldwide.com",
        "chartbeat.net",
        "imedia.cz",
        "criteo.com",
        "adform.net"
    ]
}
```

## 🎨 Visual Modes
Sweb provides different visual themes to accommodate varying visual needs. The animations below demonstrate the default interface view, as well as the distinct visual feedback provided during **hover** and **click** interactions.

### Default Color Scheme
*(The standard, calm visual theme designed for everyday use.)*  
![Default Color Scheme](images/default.png)

### High Contrast
*(A specialized mode maximizing text and element visibility for users with visual impairments.)*  
![High Contrast](images/hc.png)

## 📄 License & Attribution
This project is licensed under the **GNU General Public License v3.0 (GPL-3.0-or-later)** — see the [LICENSE](LICENSE) file for details.

* **PyQt6 & PyQt6-WebEngine:** Licensed under the GNU GPL v3 by Riverbank Computing Limited.
* **Qt 6 & Qt WebEngine:** Licensed under the GNU LGPL v3 / GPL v3 by The Qt Company.
* **Chromium:** Licensed under the 3-Clause BSD License and respective open-source licenses of its submodules.
* **Icons:** Navigation icons in `sweb/icons/` created by [Roundicons - Flaticon](https://www.flaticon.com).


