from django.core.exceptions import ImproperlyConfigured
from importlib import import_module

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text
from django.utils.functional import Promise

import json


def import_class(path):
    path_bits = path.split('.')

    if len(path_bits) < 2:
        message = "'{0}' is not a complete Python path.".format(path)
        raise ImproperlyConfigured(message)

    class_name = path_bits.pop()
    module_path = '.'.join(path_bits)
    module_itself = import_module(module_path)

    if not hasattr(module_itself, class_name):
        message = "The Python module '{0}' has no '{1}' class.".format(
            module_path,
            class_name
        )
        raise ImportError(message)

    return getattr(module_itself, class_name)


def is_module_image_installed():
    try:
        from PIL import Image
        from PIL import ImageFile
    except ImportError:
        try:
            import Image
            import ImageFile
        except ImportError:
            return False
    return True


class LazyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


def json_dumps(data):
    return json.dumps(data, cls=LazyEncoder)
