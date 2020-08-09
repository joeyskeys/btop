# license

from . import shading
from . import nodetree
from ..misc import registry


def register():
    registry.register()
    nodetree.register()


def unregister():
    registry.unregister()
    nodetree.unregister()
