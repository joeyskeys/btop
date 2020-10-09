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


class PBRTLightProperties(bpy.types.PropertyGroup):
    pass


class PBRT_PT_light(bpy.types.Panel):
    bl_label = "Light"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    COMPAT_ENGINES = {'PBRT_RENDER'}
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        renderer = context.scene.render
        return renderer.engine == 'PBRT_RENDER' and context.active_object.type == 'LIGHT'

    def draw(self, context):
        layout = self.layout
        light = context.active_object.data

        layout.use_property_split = True

        layout.prop(light, "type", expand=True)
        layout.prop(light, "color")
        layout.prop(light, "")
        col = layout.column()
