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

from ..nodes import shading


class MaterialIO(object):
    """

    """

    def __init__(self):
        pass

    def write_to_file(self, writer, meshobj, indent=0):

        def write_with_indent(idnt, content):
            writer.write('\t' * idnt + content)

        def find_node(nodes, name):
            for n in nodes:
                if n.bl_idname == name:
                    return n
            return None

        # Get output node from active material
        material = meshobj.active_material
        output_node = find_node(material.node_tree.nodes, 'ShaderNodeOutputMaterial')

        if output_node is None:
            raise Exception('Cannot find output node for material : %s' %material.name)

        # Get PBRT shader node from output surface socket
        shader = output_node.inputs['Surface'].links[0].from_node
        # Export from the shader node
        if hasattr(shader, 'export'):
            shader.export(indent, writer)

        else:
            # No shader fits; attribute a silly material instead
            print( '[btop.material.py] None pbrt material assigned : %s' %shader.name )

            #repl_shader = shading.PBRTShaderNodeMatte()
            #repl_shader.socket_dict['Kd'] = ('NodeSocketColor', (1.0, 0.412, 0.706, 1.0))
            #repl_shader.export(indent, writer)

            raise Exception('None pbrt material assigned : %s' %shader.name)
