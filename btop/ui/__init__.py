# license

from . import camera
from . import film


def register():
    camera.register()
    film.register()


def unregister():
    camera.unregister()
    film.unregister()

