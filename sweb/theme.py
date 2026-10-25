# Barevna temata a styly (QSS) pro celou aplikaci na jednom miste.


# Barvy navigacnich menu. Klic odpovida hodnote "color_theme" v config.json.
#  - bg:        pozadi toolbaru i tlacitek
#  - text:      barva popisku tlacitek
#  - border:    ramecek tlacitek
#  - hover_*:   vzhled pri najeti mysi
#  - pressed_*: vzhled pri stisknuti
THEMES: dict[str, dict[str, str]] = {
    "default": {
        "bg": "#f5f5f5",
        "text": "#000000",
        "border": "#b0b0b0",
        "hover_bg": "#fff9c4",
        "hover_text": "#000000",
        "hover_border": "#fbc02d",
        "pressed_bg": "#81d4fa",
        "pressed_text": "#000000",
        "pressed_border": "#0288d1",
    },
    # vysoky kontrast: zluta na cerne, pro slabozrake
    "high_contrast": {
        "bg": "#000000",
        "text": "#ffff00",
        "border": "#ffff00",
        "hover_bg": "#ffff00",
        "hover_text": "#000000",
        "hover_border": "#ffffff",
        "pressed_bg": "#ffffff",
        "pressed_text": "#000000",
        "pressed_border": "#000000",
    },
}

DEFAULT_THEME = "default"

# Barvy dialogu (vyhledavani, kriticka chyba). Zamerne nezavisi na tematu:
# chybovy dialog se muze zobrazit jeste pred nactenim nastaveni
# (napr. kdyz je poskozeny config.json), takze tema v tu chvili nezname.
DIALOG_COLORS: dict[str, str] = {
    "bg": "#f5f5f5",
    "text": "#000000",
    "input_bg": "#ffffff",
    "border": "#aaaaaa",
    "button_bg": "#e0e0e0",
    "accent_bg": "#ff2a2a",
    "accent_text": "#ffffff",
    "accent_border": "#cc0000",
}

DIALOG_TEXT_SIZE = 24
DIALOG_BUTTON_SIZE = 20


def get_theme(name: str) -> dict[str, str]:
    """Vrati barvy tematu podle nazvu, pri neznamem nazvu vychozi tema."""
    return THEMES.get(name, THEMES[DEFAULT_THEME])


def nav_stylesheet(theme: dict[str, str], font_size: int) -> str:
    """Stylesheet pro oba navigacni toolbary a jejich tlacitka.

    :param theme: slovnik barev z get_theme()
    :param font_size: velikost pisma popisku v px (nastaveni "ui_font_size")
    """
    return f"""
        QToolBar {{
            spacing: 0px;
            padding: 0px;
            background-color: {theme["bg"]};
        }}
        QToolButton {{
            padding: 10px;
            background-color: {theme["bg"]};
            border: 2px solid {theme["border"]};
            border-radius: 0px;
            color: {theme["text"]};

            font-size: {font_size}px;
            font-weight: bold;
            font-family: Arial, sans-serif;
        }}
        QToolButton:hover {{
            background-color: {theme["hover_bg"]};
            border: 2px solid {theme["hover_border"]};
        }}
        QToolButton:pressed {{
            background-color: {theme["pressed_bg"]};
            border: 2px solid {theme["pressed_border"]};
        }}
    """


def _accent_button_rule(selector: str) -> str:
    """Spolecne pravidlo pro cervene tlacitko hlavni akce."""
    c = DIALOG_COLORS
    return f"""
        {selector} {{
            background-color: {c["accent_bg"]};
            color: {c["accent_text"]};
            border: 2px solid {c["accent_border"]};
        }}
    """


def search_dialog_stylesheet() -> str:
    """Stylesheet pro celoobrazovkovou vyhledavaci stranku (SearchWidget):
    obri pismo, siroke textove pole pres obrazovku a velka tlacitka.
    """
    c = DIALOG_COLORS
    return f"""
        QWidget#searchScreen {{
            background-color: {c["bg"]};
        }}
        QLabel {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
            color: {c["text"]};
        }}
        QLineEdit {{
            font-size: 32px;
            padding: 20px;
            border: 3px solid {c["border"]};
            background-color: {c["input_bg"]};
            color: {c["text"]};
        }}
        QPushButton {{
            font-size: 26px;
            font-weight: bold;
            padding: 20px;
            background-color: {c["button_bg"]};
            border: 2px solid {c["border"]};
            color: {c["text"]};
        }}
    """ + _accent_button_rule("QPushButton#searchBtn")


def error_dialog_stylesheet() -> str:
    """Stylesheet pro celoobrazovkovou kritickou chybu (utils.show_critical_error)."""
    c = DIALOG_COLORS
    return f"""
        QDialog#errorScreen {{
            background-color: {c["bg"]};
        }}
        QLabel#errorTitle {{
            font-size: 36px;
            font-weight: bold;
            color: {c["accent_border"]};
        }}
        QLabel#errorMessage {{
            font-size: 28px;
            color: {c["text"]};
        }}
        QLabel#errorDetail {{
            font-size: 20px;
            padding: 20px;
            background-color: {c["input_bg"]};
            border: 2px solid {c["border"]};
            color: {c["text"]};
            font-family: monospace;
        }}
        QPushButton {{
            font-size: 24px;
            font-weight: bold;
            padding: 20px 50px;
            background-color: {c["button_bg"]};
            border: 2px solid {c["border"]};
            color: {c["text"]};
        }}
    """ + _accent_button_rule("QPushButton#exitBtn")
