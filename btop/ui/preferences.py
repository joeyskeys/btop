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


addon_name = os.path.basename(os.path.dirname(os.path.dirname(__file__)))


class PBRTPreferences(bpy.types.AddonPreferences):
    bl_idname = addon_name

    pbrt_location: bpy.props.StringProperty(name="pbrt_location",
                                            description="PBRT executable location",
                                            default=shutil.which('pbrt') or '',
                                            subtype='FILE_PATH')

    pbrt_cache_folder: bpy.props.StringProperty(name="pbrt_cache_folder",
                                                description="PBRT cache folder",
                                                default=os.path.join(os.path.expanduser("~"), 'pbrt_scene'),
                                                subtype='FILE_PATH')

    pbrt_use_v4: bpy.props.BoolProperty(name="pbrt_use_v4",
                                        description="Use version 4 pbrt binary",
                                        default=False)

    def draw(self, context):
        layout = self.layout

        layout.row().prop(self, 'pbrt_location', text="PBRT location")
        layout.row().prop(self, 'pbrt_cache_folder', text="Cache Folder")
        layout.row().prop(self, 'pbrt_use_v4', text="Use Version 4")


def get_pref():
    return bpy.context.preferences.addons[addon_name].preferences


def register():
    # Register UIs
    bpy.utils.register_class(PBRTPreferences)


def unregister():
    # Unregister UIs
    bpy.utils.unregister_class(PBRTPreferences)
