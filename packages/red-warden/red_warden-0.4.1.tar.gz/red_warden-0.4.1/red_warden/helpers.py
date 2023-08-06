import sys
import json
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
