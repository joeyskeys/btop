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

class Registry(object):
    def __init__(self):
        self.cls_to_register = []
        self.material_nodes = []
        self.texture_nodes = []

    def add_new_class(self, cls, node_type=None):
        self.cls_to_register.append(cls)

        # We need the class type bacause cls.__class__.__name__ is not the correct value
        if node_type == 'material':
            self.material_nodes.append((cls.class_type, cls.node_type))
            cls.category = 'Material'

        elif node_type == 'texture':
            self.texture_nodes.append((cls.class_type, cls.node_type))
            cls.category = 'Texture'

        else:
            cls.category = 'Default'

    def register(self):
        for c in self.cls_to_register:
            print('register', c)
            bpy.utils.register_class(c)

    def unregister(self):
        for c in self.cls_to_register:
            bpy.utils.unregister_class(c)


registry = Registry()


class PBRTNodeTypes(object):
    def __init__(self, node_type=None):
        self.node_type = node_type
        self.material_nodes = []
        self.texture_nodes = []

    def __call__(self, cls):
        registry.add_new_class(cls, self.node_type)
        return cls
