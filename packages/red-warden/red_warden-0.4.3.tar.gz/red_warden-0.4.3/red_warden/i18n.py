import os
import json
from starlette.middleware.base import BaseHTTPMiddleware


class RWI18n:
    _locales = []
    _locale = None

    @property
    def locale(self):
        if not self._locales:
            raise Exception("No locales defined")

        return self._locale

    @locale.setter
    def locale(self, value):
        if value in self._locales:
            self._locale = value
        else:
            raise Exception("Missing locale %s" % value)

    @classmethod
    def load_from_json_file(cls, json_file, locale):
        with open(json_file, mode="r", encoding="utf8") as f:
            translations = json.load(f)
            cls._add_translations(translations, locale)

        if locale not in cls._locales:
            cls._locales.append(locale)

    @classmethod
    def load_from_kv_file(cls, kv_file, locale):
        with open(kv_file, mode="r", encoding="utf8") as f:
            for line in f:
                line = line.strip()
                if line:
                    key, message = line.split("=")
                    cls._add_translation(key.strip(), message.strip(), locale)

        if locale not in cls._locales:
            cls._locales.append(locale)

    @classmethod
    def load_from_kv_directory(cls, kv_directory):
        for file in os.listdir(kv_directory):
            if file.endswith(".txt"):
                cls.load_from_kv_file(
                    "%s/%s" % (kv_directory, file), file.replace(".txt", "")
                )

    def t(
        self,
        key,
        locale=None,
        missing_placeholder="___MISSING_TRANSLATION_%s___",
        **kwargs
    ):
        if not locale:
            locale = self._locale

        if (locale not in self._locales) or not self._has_translation(key, locale):
            return missing_placeholder % key

        return self._get_translation(key, locale, **kwargs)

    @classmethod
    def all(cls, key):
        translations = {}
        for locale in cls._locales:
            translations[locale] = cls._get_translation(key, locale)
        return translations

    @classmethod
    def _has_translation(cls, key, locale):
        raise NotImplementedError

    @classmethod
    def _get_translation(cls, key, locale, **kwargs):
        raise NotImplementedError

    @classmethod
    def _add_translation(cls, key, message, locale):
        raise NotImplementedError

    @classmethod
    def _add_translations(cls, translations, locale):
        raise NotImplementedError


class RWMemoryI18n(RWI18n):
    _translations = {}

    @classmethod
    def __check_locale(cls, locale):
        if locale not in cls._translations.keys():
            cls._translations[locale] = {}

    @classmethod
    def _has_translation(cls, key, locale):
        cls.__check_locale(locale)
        return key in cls._translations[locale]

    @classmethod
    def _get_translation(cls, key, locale, **kwargs):
        cls.__check_locale(locale)
        translated = cls._translations[locale].get(key, key)
        return translated.format(**kwargs) if kwargs else translated

    @classmethod
    def _add_translation(cls, key, message, locale):
        cls.__check_locale(locale)
        cls._translations[locale][key] = message

    @classmethod
    def _add_translations(cls, locale, translations):
        cls.__check_locale(locale)
        cls._translations[locale].update(translations)


class RWI18nMiddleware(BaseHTTPMiddleware):
    _adapter_class = None

    def __init__(self, app, adapter_class):
        self._adapter_class = adapter_class
        super().__init__(app)

    async def dispatch(self, request, call_next):
        i18n = self._adapter_class()
        request.state.i18n = i18n

        try:
            locale = (
                str(request.url).replace(str(request.base_url), "").split("/", 1)[0]
            )
            i18n.locale = locale
        except:
            pass

        return await call_next(request)
