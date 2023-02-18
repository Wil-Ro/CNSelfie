# CNSelfie
 CNC machine that draws your selfies!

## Requirements
To run this you will need to install opencv-python, svg-to-gcode and pypotrace, to do this make sure you dont have any other open-cv versions installed then run:

``pip install opencv-python``
and
``pip install svg-to-gcode``

Then, follow the steps found [here](https://pypi.org/project/pypotrace/) to install pypotrace on your given system

This should also install numpy if you dont already have that

You might also find knowing a bit about G-Code will be helpful too, I didnt know
much about how it actually worked until now, I found [this](https://howtomechatronics.com/tutorials/g-code-explained-list-of-most-important-g-code-commands/) guide very helpful

## Todo
- [x] Allow user to take photos
- [x] Generate edges from photo
- [ ] Convert edges to vector (probably using potrace)
- [ ] Convert vector to G-Code (give [this](https://pypi.org/project/svg-to-gcode/) a look)
- [ ] QoL changes to edge detection
