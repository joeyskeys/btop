# license

from . import camera
from . import film
from . import sampler
from . import integrator


def register():
    camera.register()
    film.register()
    sampler.register()
    integrator.register()


def unregister():
    camera.unregister()
    film.unregister()
    sampler.unregister()
    integrator.unregister()
