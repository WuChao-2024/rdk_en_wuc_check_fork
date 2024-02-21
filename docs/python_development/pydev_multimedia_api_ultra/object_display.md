---
sidebar_position: 4
---
# Display Object

The Display object implements video display functionality and can output image data to a monitor through the HDMI interface. This object includes methods such as `display`, `send_frame`, `set_rect`, `set_word`, `close`, etc. Detailed explanations are as follows:

## display
<font color='Blue'>[Description]</font>

Initialize the display module and configure the display parameters.

<font color='Blue'>[Function Signature]</font>

```python
Display.display([width, height])
```

<font color='Blue'>[Parameter Description]</font>

| Parameter Name | Definition | Value Range |
| ------------ | ----------------------- | ----------------- |
| width        | Width of the input image | Up to 1920 |
| height       | Height of the input image | Up to 1080 |

<font color='Blue'>[Usage]</font>

```python
#create display object
disp = srcampy.Display()

#enable display function, solution: 1080p, interface: HDMI
ret = disp.display([1920, 1080])
```

<font color='Blue'>[Return Value]</font>

| Return Value | Description |
| ------ | ---- |
| 0      | Success |
| -1    | Failure |

<font color='Blue'>[Notes]</font>

Currently, only supports the `1920x1080` resolution.

<font color='Blue'>[Reference Code]</font>

None## send_frame

<font color='Blue'>【Description】</font>

Input display data to the display module, and the format needs to be `NV12`

<font color='Blue'>【Function Declaration】</font>

```python
Display.send_frame(img)
```

<font color='Blue'>【Parameter Description】</font>

| Parameter | Definition | Value Range |
| --- | --- | --- |
| img | Image data to be displayed | NV12 format |

<font color='Blue'>【Usage】</font>

None

<font color='Blue'>【Return Value】</font>

| Return Value | Description |
| --- | --- |
| 0 | Success |
| -1 | Failure |

<font color='Blue'>【Note】</font>

This interface needs to be used after enabling the display function with the `display` interface. The input data needs to be in the `NV12` format.

<font color='Blue'>【Reference Code】</font>

```python
import sys, os, time

import numpy as np
import cv2
from hobot_spdev import libsppydev as srcampy

def test_display():
    #create display object
    disp = srcampy.Display()

    #enable display function
    ret = disp.display([1920, 1080])
    print ("Display display 0 return:%d" % ret)
```fo = open("output.img", "rb")
img = fo.read()
fo.close()

#send image data to display
ret = disp.send_frame(img)
print ("Display send_frame return:%d" % ret)

time.sleep(3)

disp.close()
print("test_display done!!!")

test_display()
```

## set_rect

<font color='Blue'>【Function Description】</font>

Draw a rectangular box on the graphic layer of the display module.

<font color='Blue'>【Function Declaration】</font>

```python
Display.set_rect(x0, y0, x1, y1, flush, color, line_width)
```

<font color='Blue'>【Parameter Description】</font>

| Parameter Name | Definition |  Range |
| ---------- | ----------------------- | --------- |
| x0 | x-coordinate of the upper left corner of the rectangular box | Within video frame size |
| y0 | y-coordinate of the upper left corner of the rectangular box | Within video frame size |
| x1 | x-coordinate of the lower right corner of the rectangular box | Within video frame size |
| y1 | y-coordinate of the lower right corner of the rectangular box | Within video frame size |
| flush | Whether to clear the buffer of the graphic layer | 0: No, 1: Yes |
| color | Color setting of the rectangular box | ARGB8888 format |
| line_width | Width of the edges of the rectangular box | Range: 1~16, default value: 4 |

<font color='Blue'>【Usage】</font>

```python
#enable graph layer 2
ret = disp.display(2)
print ("Display display 2 return:%d" % ret)

#set osd rectangle
ret = disp.set_rect(100, 100, 1920, 200,  flush = 1,  color = 0xffff00ff)```<font color='Blue'>[Return Value]</font>

| Return Value | Description |
| ------------ | ----------- |
| 0            | Success     |
| -1           | Failure     |

<font color='Blue'>[Note]</font>

This interface needs to be used after enabling the display function using the `display` interface.

<font color='Blue'>[Reference Code]</font>

None

## set_word

<font color='Blue'>[Function Description]</font>

Draws characters on the graphic layer of the display module.

<font color='Blue'>[Function Declaration]</font>

```python
Display.set_word(x, y, str, flush, color, line_width)
```

<font color='Blue'>[Parameter Description]</font>

| Parameter Name | Description           | Value Range        |
| -------------- | --------------------- | ----------------- |
| x              | Starting coordinate value of the character to be drawn (x) | Not exceeding the size of the video screen    |
| y              | Starting coordinate value of the character to be drawn (y) | Not exceeding the size of the video screen    |
| str            | Character data to be drawn | GB2312 encoding |
| flush          | Whether to clear the graphics layer buffer | 0: No, 1: Yes |
| color          | Character color setting | ARGB8888 format |
| line_width     | Width of the character line | Range 1~16, default: 1 |

<font color='Blue'>[Usage]</font>

```python
# enable graph layer 2
ret = disp.display(2)
print ("Display display 2 return:%d" % ret)

# set osd string
string = "horizon"
ret = disp.set_word(300, 300, string.encode('gb2312'), 0, 0xff00ffff)
```print ("Display set_word return:%d" % ret)

<font color='Blue'>[Return Value]</font>  

| Return Value | Description |
| ------------ | ----------- |
| 0            | Success     |
| -1           | Failure     |

<font color='Blue'>[Note]</font> 

This interface needs to be used after enabling the display function with the `display` interface.

<font color='Blue'>[Reference Code]</font>  

None

## close

<font color='Blue'>[Function Description]</font>

Close the display module.

<font color='Blue'>[Function Declaration]</font>  

```python
Display.close()
```

<font color='Blue'>[Parameter Description]</font>  

None

<font color='Blue'>[Usage]</font> 

None

<font color='Blue'>[Return Value]</font>  

| Return Value | Description |
| ------------ | ----------- |
| 0            | Success     |
| -1           | Failure     |

<font color='Blue'>[Note]</font> 

This interface needs to be used after enabling the display function with the `display` interface.

<font color='Blue'>[Reference Code]</font>## bind interface

<font color='Blue'>[Function Description]</font>

This interface can bind the output and input data streams of the `Camera`, `Encoder`, `Decoder`, and `Display` modules, and the data can flow automatically between the bound modules without user operations. For example, after binding the `Camera` and `Display` modules, the camera data will be automatically output to the display screen through the display module without the need to call additional interfaces.

<font color='Blue'>[Function Declaration]</font>
```python
    srcampy.bind(src, dst)
```

<font color='Blue'>[Parameter Description]</font>

| Parameter Name | Description   | Value Range |
| -------------- | ------------- | ----------- |
| src            | Source module | `Camera`, `Encoder`, `Decoder` modules |
| dst            | Target module | `Camera`, `Encoder`, `Decoder`, `Display` modules |

<font color='Blue'>[Usage]</font>
```python
#create camera object
cam = srcampy.Camera()
ret = cam.open_cam(-1,[1920, 1080], [1280, 720])
print("Camera open_cam return:%d" % ret)

#encode start
enc = srcampy.Encoder()
ret = enc.encode(2, [1920, 1080])
print("Encoder encode return:%d" % ret)

#bind, input: cam, output: enc
ret = srcampy.bind(cam, enc)
print("srcampy bind return:%d" % ret)
```

 <font color='Blue'>[Return Value]</font>

| Return Value | Description |
| ------------ | ----------- |
| 0            | Success     |
| -1           | Failure     |

<font color='Blue'>[Notes]</font>

None## unbind interface

<font color='Blue'>【Description】</font>

Unbind two bound modules.

<font color='Blue'>【Function Declaration】</font>
```python
srcampy.unbind(src, dst)
```

<font color='Blue'>【Parameter Description】</font>

| Parameter Name | Description       | Value Range                    |
| -------------- | ----------------- | ------------------------------ |
| src            | Source data module | `Camera`, `Encoder`, `Decoder` |
| dst            | Target data module | `Camera`, `Encoder`, `Decoder`, `Display` |

<font color='Blue'>【Usage】</font>

```python
#create camera object
cam = srcampy.Camera()
ret = cam.open_cam(-1,[1920, 1080], [1280, 720])
print("Camera open_cam return:%d" % ret)

#encode start
enc = srcampy.Encoder()
ret = enc.encode(2, [1920, 1080])
print("Encoder encode return:%d" % ret)

#bind, input: cam, output: enc
ret = srcampy.bind(cam, enc)
print("srcampy bind return:%d" % ret)
#unbind, input: cam, output: enc
ret = srcampy.unbind(cam, enc)
print("srcampy unbind return:%d" % ret)
```

 <font color='Blue'>【Return Value】</font>

| Return Value | Description |
| ------------ | ----------- |
| 0            | Success     |
| -1           | Fail        |<font color='Blue'>【Notes】</font>

None

<font color='Blue'>【Reference Code】</font>

None