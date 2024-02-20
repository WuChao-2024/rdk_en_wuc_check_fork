# 4.6 RDK Ultra Multimedia Interface Instructions

The development board's Ubuntu system comes pre-installed with the Python version of the `hobot_spdev` image multimedia module, which can create several objects such as `Camera`, `Encode`, `Decode`, `Display`, etc., to complete functions such as camera image capture, image processing, video encoding, video decoding, and display output.

The basic usage of the module is as follows:

```python
from hobot_spdev import libsppydev as srcampy

#create camera object
camera = srcampy.Camera()

#create encode object
encode = srcampy.Encode()

#create decode object
decode = srcampy.Decode()

#create display object
display = srcampy.Display()
```