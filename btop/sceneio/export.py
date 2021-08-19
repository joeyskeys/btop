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

import bpy, copy

from .camera import CameraIO
from .film import FilmIO
from .sampler import SamplerIO
from .integrator import IntegratorIO
from .scene import SceneIO


class PBRTExporter(object):
    """
    Export blender scene into a pbrt scene file
    """

    def __init__(self):
        self.cameraio = CameraIO()
        self.samplerio = SamplerIO()
        self.integratorio = IntegratorIO()
        self.filmio = FilmIO()
        self.sceneio = SceneIO()

    def export(self, output_path):
        file_handler = open(output_path, 'w')

        self.cameraio.write_to_file(file_handler)

        self.samplerio.write_to_file(file_handler)
        self.integratorio.write_to_file(file_handler)
        self.filmio.write_to_file(file_handler)

        self.sceneio.write_to_file(file_handler)

        file_handler.close()