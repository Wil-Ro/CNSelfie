# CNSelfie
 CNC machine that draws your selfies!

## Requirements
To run this you will need to install opencv-python and an altered version of svg_to_gcode, to do this make sure you dont have any other open-cv versions installed then run:

``pip install opencv-python``
and
``pip install svg-to-gcode``

Once you've installed svg-to-gcode, replace its file (in site-packages) with the zip file in this repo

This should also install numpy if you dont already have that

You might also find knowing a bit about G-Code will be helpful too, I didnt know
much about how it actually worked until now, I found [this](https://howtomechatronics.com/tutorials/g-code-explained-list-of-most-important-g-code-commands/) guide very helpful

## Todo
- [x] Allow user to take photos
- [x] Generate edges from photo
- [x] Convert edges to vector (probably using potrace)
- [x] Convert vector to G-Code (give [this](https://pypi.org/project/svg-to-gcode/) a look)
- [x] QoL changes to edge detection
