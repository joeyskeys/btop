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

import bpy

from .mesh import MeshIO
from .material import MaterialIO
from .light import LightIO


class SceneIO(object):
    """

    """

    def __init__(self):
        self.meshio = MeshIO()
        self.materialio = MaterialIO()
        self.lightio = LightIO()

    def write_to_file(self, writer):

        writer.write('WorldBegin\n\n')

        # Light should be written in the world block
        self.lightio.write_to_file(writer)

        for object in bpy.data.objects:

            if object.type == 'MESH' and object not in self.lightio.area_light_geometries:
                writer.write('AttributeBegin\n')
                self.materialio.write_to_file(writer, object)
                self.meshio.write_to_file(writer, object)
                writer.write('AttributeEnd\n\n')

        writer.write('WorldEnd\n')

    def read_from_file(self, parser):
        pass