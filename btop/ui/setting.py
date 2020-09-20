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

import os
import shutil

import bpy


def find_pbrt_binary():
    pass


def find_home_directory():
    pass


class PBRTSettingProperties(bpy.types.PropertyGroup):
    pbrt_location: bpy.props.StringProperty(name="pbrt_location",
                                            description="PBRT executable location",
                                            default=shutil.which('pbrt') or '',
                                            subtype='FILE_PATH')

    pbrt_cache_folder: bpy.props.StringProperty(name="pbrt_cache_folder",
                                                description="PBRT cache folder",
                                                default=os.path.join(os.path.expanduser("~"), 'pbrt_scene'),
                                                subtype='FILE_PATH')


class PBRT_PT_setting(bpy.types.Panel):
    bl_label = "Setting"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    COMPAT_ENGINES = {'PBRT_RENDER'}
    bl_context = 'render'

    @classmethod
    def poll(cls, context):
        renderer = context.scene.render
        return renderer.engine == 'PBRT_RENDER'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        setting_props = context.scene.pbrt_setting_props
        layout.row().prop(setting_props, "pbrt_location", text="PBRT Location")
        layout.row().prop(setting_props, "pbrt_cache_folder", text="Cache Folder")


def register():
    # Register property group
    bpy.utils.register_class(PBRTSettingProperties)
    bpy.types.Scene.pbrt_setting_props = bpy.props.PointerProperty(type=PBRTSettingProperties)

    # Register UIs
    bpy.utils.register_class(PBRT_PT_setting)


def unregister():
    # Unregister property group
    del bpy.types.Scene.pbrt_setting_props
    bpy.utils.unregister_class(PBRTSettingProperties)

    # Unregister UIs
    bpy.utils.unregister_class(PBRT_PT_setting)