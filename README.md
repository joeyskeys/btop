# btop

btop is a blender(2.8 and above) addon for PBRT.
Currently still in an early stage.

### How to use

  - Clone the repository
  - Make an zip archive of the btop folder inside the repository(Linux users can use the create_archive.sh).
  - Install the addon inside blender

After installing the addon, setup pbrt executable and cache folder in the addon preference.
![preference picture](https://github.com/joeyskeys/btop/blob/master/resources/preference.png)

Please note that this addon doesn't provide pbrt executable by itself, it just converts the blender scene into pbrt cache file and then invoke the pbrt command to render the image.

By default this addon uses pbrt-v3 but an option to use v4 is also provided in the preferences. Currently it will convert the v3 scene file to the v4 version with the upgrade option provided by the v4 executable but still some bugs there.

### Features

  - Most attributes are supported in the editor
  
  - Complete shader graph support
  
  - Auto render output display

![render output](https://github.com/joeyskeys/btop/blob/master/resources/output.png)


### Area light support

Area light currently can only use triangle mesh in the scene as its geometry(Procedual shape support will come soon).

![area light](https://github.com/joeyskeys/btop/blob/master/resources/area_light.png)


### Bugs & feedback
Please note this addon is still in development and there might be some bugs. Open an issue if you find one or you can send your PR directly.

Notes from JamesTompkin:
- Textures - only tri and quad meshes are currently supported; ngons are not supported. So, triangulate before rendering.
- Textures - the process to generate UVs is currently memory and scene-declaration inefficient; see notes in code.
- Textures - the code to triangulate a mesh also duplicates work within its data structures, but it works for now.
