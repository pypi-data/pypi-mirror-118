import sys
import json
import aiofiles
import datetime
import uuid
import socket
import random
import traceback
from red_warden.config import RWConfig
from pydantic import ValidationError
from importlib import import_module


def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(("10.255.255.255", 1))
        the_ip = s.getsockname()[0]
    except:
        the_ip = "127.0.0.1"
    finally:
        s.close()
    return the_ip


def get_random_element(elements, separator=","):
    if isinstance(elements, str):
        elements = elements.split(separator)

    return random.choice(elements)


class RWCustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return obj.hex.upper()
        elif isinstance(obj, datetime.datetime):
            return datetime.datetime.strftime(obj, "%Y%m%d%H%M%S")
        elif isinstance(obj, datetime.date):
            return datetime.date.strftime(obj, "%Y%m%d")
        elif isinstance(obj, datetime.time):
            return datetime.time.strftime(obj, "%H%M%S")
        elif isinstance(obj, bytes):
            return obj.hex().upper()

        return super().default(obj)


def exception_as_dict(ex):
    if isinstance(ex, ValidationError):
        msg = ex.errors()
    else:
        msg = str(ex)

    if msg:
        error = {"message": msg}
    else:
        error = {}

    if RWConfig["RW_DEBUG"]:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        error.update(
            {"type": exception_type.__name__, "trace": traceback.format_stack()}
        )
    return error


# taken from Graphene
def import_string(dotted_path, dotted_attributes=None):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. When a dotted attribute path is also provided, the
    dotted attribute path would be applied to the attribute/class retrieved from
    the first step, and return the corresponding value designated by the
    attribute path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError:
        raise ImportError("%s doesn't look like a module path" % dotted_path)

    module = import_module(module_path)

    try:
        result = getattr(module, class_name)
    except AttributeError:
        raise ImportError(
            'Module "%s" does not define a "%s" attribute/class'
            % (module_path, class_name)
        )

    if not dotted_attributes:
        return result
    else:
        attributes = dotted_attributes.split(".")
        traveled_attributes = []
        try:
            for attribute in attributes:
                traveled_attributes.append(attribute)
                result = getattr(result, attribute)
            return result
        except AttributeError:
            raise ImportError(
                'Module "%s" does not define a "%s" attribute inside attribute/class "%s"'
                % (module_path, ".".join(traveled_attributes), class_name)
            )


class ViteHelper:
    """
    This helper prepares the tags to be added when developing along Vite.
    """

    manifest = None

    @classmethod
    def _js_tag(cls, entry):
        url = (
            cls._asset_url(entry)
            if RWConfig["RW_ENV"] == "production"
            else "http://localhost:3000/%s" % entry
        )

        return (
            '<script type="module" crossorigin src="%s"></script>' % url if url else ""
        )

    @classmethod
    def _css_tag(cls, entry):
        tags = ""
        if RWConfig["RW_ENV"] == "production":
            for url in cls._css_urls(entry):
                tags += '<link rel="stylesheet" href="%s">' % url
        return tags

    @classmethod
    def _asset_url(cls, entry):
        item = cls.manifest.get(entry, None)
        return item.get("file", "") if item else ""

    @classmethod
    def _css_urls(cls, entry):
        urls = []
        item = cls.manifest.get(entry, None)

        if item:
            for css_file in item.get("css", []):
                urls.append("/dist/%s" % css_file)

        return urls

    @classmethod
    def _js_preload_imports(cls, entry):
        results = ""
        if RWConfig["RW_ENV"] == "production":
            for url in cls._imports_urls(entry):
                results += '<link rel="modulepreload" href="%s">' % url
        return results

    @classmethod
    def _imports_urls(cls, entry):
        urls = []
        manifest_entry = cls.manifest.get(entry, None)
        if manifest_entry:
            for _import in manifest_entry.get("imports", []):
                urls.append("/dist/%s" % _import)
        return urls

    @classmethod
    def get_js_and_css(cls, manifest_file, entry):
        with open(manifest_file, mode="r") as f:
            contents = f.read()
        cls.manifest = json.loads(contents)

        return {
            "js": cls._js_tag(entry),
            "preload": cls._js_preload_imports(entry),
            "cls": cls._css_tag(entry),
        }
