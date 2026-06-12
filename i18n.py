import json
import os

LOCALE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locales")

_locales = {}

def load_locale(lang_code):
    if lang_code in _locales:
        return _locales[lang_code]
    filepath = os.path.join(LOCALE_DIR, f"{lang_code}.json")
    if not os.path.exists(filepath):
        filepath = os.path.join(LOCALE_DIR, "en.json")
    with open(filepath, "r", encoding="utf-8") as f:
        _locales[lang_code] = json.load(f)
    return _locales[lang_code]

def tr(key, lang="en", **kwargs):
    locale = load_locale(lang)
    template = locale.get(key)
    if template is None:
        locale = load_locale("en")
        template = locale.get(key, key)
    if kwargs:
        return template.format(**kwargs)
    return template
