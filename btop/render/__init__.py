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

import bpy

from ..sceneio import PBRTExporter
from ..ui.preferences import get_pref


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

        # Get executable from preference
        pref = get_pref()
        pbrt_executable = pref.pbrt_location
        cache_folder = pref.pbrt_cache_folder
        use_v4 = pref.pbrt_use_v4

        # 2021-05-20: Bizarro bug that James couldn't work out:
        # - When rendering stills (F12; Render->Render Image), the current animation 
        # frame works fine and the expected output is produced.
        # - When rendering animations (CTRL-F12; Render->Render Animation), only the
        # viewport frame set at the beginning of the sequence is rendered, 
        # e.g., if frame 7 is set before CTRL-F12, only frame 7 will ever be rendered.
        # - The fix is weird - we pull the current frame (which interates correctly 
        # when rendering an animation) and then re-set the scene frame.
        # - Clearly a hack. I spent ~2 hours digging around in Blender source code to
        # try and find out why, but failed. So, we live with the hack.
        #
        # Get animation frame from scene
        animframe = bpy.context.scene.frame_current
        # Set the current frame to be
        bpy.context.scene.frame_set(animframe)

        # Setup output file name
        # todo : decide output file type with an user option
        filename = os.path.basename(bpy.data.filepath) or 'tmp.blend'
        # Insert framenumber from animation
        filename = filename.replace( '.blend', '_{:04d}.blend'.format(animframe) )
        cache_filepath = os.path.join(cache_folder, filename.replace('.blend', '.pbrt'))
        converted_cache_filepath = os.path.join(cache_folder, filename.replace('.blend', '_converted.pbrt'))
        outfile = os.path.join(cache_folder, filename.replace('.blend', '.exr'))

        # Get film resolution from camera attributes
        render = bpy.context.scene.render
        x_resolution = render.resolution_x
        y_resolution = render.resolution_y

        # Export pbrt cache file
        exporter.export(cache_filepath)

        try:
            cmd_comps = [pbrt_executable, '--outfile', outfile]
            if use_v4:
                convert_cmd_comps = [pbrt_executable, '--upgrade', cache_filepath, '>', converted_cache_filepath]
                print('Convert command : ', ' '.join(convert_cmd_comps))
                os.system(' '.join(convert_cmd_comps))
                cmd_comps.append(converted_cache_filepath)
            else:
                cmd_comps.append(cache_filepath)

            print('Render command : ', ' '.join(cmd_comps))
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