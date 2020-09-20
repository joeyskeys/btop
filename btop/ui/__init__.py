# This source file is part of btop
#
# This software is released under the GPL-3.0 license.
#
# Copyright (c) 2020 Joey Chen. All rights reserved.
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from . import camera
from . import film
from . import world
from . import sampler
from . import integrator
from . import material
from . import preferences


def register():
    camera.register()
    film.register()
    world.register()
    sampler.register()
    integrator.register()
    material.register()
    preferences.register()


def unregister():
    camera.unregister()
    film.unregister()
    world.unregister()
    sampler.unregister()
    integrator.unregister()
    material.unregister()
    preferences.unregister()
