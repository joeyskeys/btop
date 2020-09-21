# btop

btop is a blender(2.8 and above) addon for PBRT.
Currently still in an early stage.

### How to use

  - Clone the repository
  - Make an zip archive of the btop folder inside the repository(Linux users and use the create_archive.sh).
  - Install the addon inside blender

After installing the addon, setup pbrt executable and cache folder in the addon preference.
![preference picture](https://github.com/joeyskeys/btop/blob/master/resources/preference.png)

Please note that this addon doesn't provide pbrt executable by itself, it just converts the blender scene into pbrt cache file and then invoke the pbrt command to render the image.

### Features

  - Renderer options
  
  ![renderer options](https://github.com/joeyskeys/btop/blob/master/resources/renderer_option.png)
  
  - Film options
  
  ![film options](https://github.com/joeyskeys/btop/blob/master/resources/film_option.png)
  
  - World options
  
  ![world options](https://github.com/joeyskeys/btop/blob/master/resources/world_option.png)

  - Materials

  ![materials](https://github.com/joeyskeys/btop/blob/master/resources/material.png)

  - Render output
  
  ![output](https://github.com/joeyskeys/btop/blob/master/resources/output.png)

### Bugs & feedback
Please note this addon is still in development and there might be some bugs. Open an issue if you find one or you can send your PR directly.