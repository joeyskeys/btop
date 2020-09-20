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
import subprocess

import bpy

from ..sceneio import PBRTExporter


class PBRTRenderEngine(bpy.types.RenderEngine):
    bl_idname = 'PBRT_RENDER'
    bl_label = 'pbrt'
    bl_use_preview = True
    bl_use_shading_nodes_custom = False
    bl_use_postprocess = True

    # Constructor
    def __init__(self):
        self.renderer = None

    def __del__(self):
        pass

    def render(self, depsgraph):
        exporter = PBRTExporter()

        setting_props = bpy.context.scene.pbrt_setting_props
        filename = os.path.basename(bpy.data.filepath) or 'tmp.blend'
        pbrt_executable = setting_props.pbrt_location
        cache_filepath = os.path.join(setting_props.pbrt_cache_folder, filename.replace('.blend', '.pbrt'))
        outfile = os.path.join(setting_props.pbrt_cache_folder, filename.replace('.blend', '.exr'))

        film_props = bpy.context.scene.pbrt_film_props
        x_resolution = film_props.x_resolution
        y_resolution = film_props.y_resolution

        #exporter.export("/home/joey/Desktop/scene.pbrt")
        exporter.export(cache_filepath)

        try:
            #subprocess.call([pbrt_executable, '--outfile', outfile, cache_filepath])
            cmd_comps = [pbrt_executable, '--outfile', outfile, cache_filepath]
            print('command is : ', ' '.join(cmd_comps))
            os.system(' '.join(cmd_comps))

            # Load rendered picture and display it in the viewport
            result = self.begin_result(0, 0, x_resolution, y_resolution)
            layer = result.layers[0]
            layer.load_from_file(outfile)
            self.end_result(result)

        except Exception as e:
            print('execute pbrt command failed:\n', e)

    def view_update(self, context, depsgraph):
        pass

    def view_draw(self, context, depsgraph):
        pass


def register():
    bpy.utils.register_class(PBRTRenderEngine)


def unregister():
    bpy.utils.unregister_class(PBRTRenderEngine)