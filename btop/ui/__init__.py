# license

from . import camera
from . import film
from . import world
from . import sampler
from . import integrator
from . import material
from . import setting


def register():
    camera.register()
    film.register()
    world.register()
    sampler.register()
    integrator.register()
    material.register()
    setting.register()


def unregister():
    camera.unregister()
    film.unregister()
    world.unregister()
    sampler.unregister()
    integrator.unregister()
    material.unregister()
    setting.unregister()
