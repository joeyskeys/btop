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

bl_info = {
    "name": "btop",
    "author": "Joey Chen",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "PBRT Renderer",
    "warning": "",
    "category": "Render"
}

if "bpy" in locals():
    import importlib

    importlib.reload(ui)

else:
    import bpy


def register():
    print('register pbrt')
    from . import render
    from . import ui
    from . import nodes

    render.register()
    ui.register()
    nodes.register()


def unregister():
    from . import render
    from . import ui
    from . import nodes

    render.unregister()
    ui.unregister()
    nodes.unregister()


if __name__ == '__main__':
    register()