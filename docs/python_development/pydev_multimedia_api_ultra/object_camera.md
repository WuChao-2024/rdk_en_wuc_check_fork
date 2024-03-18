---
sidebar_position: 1
---

# Camera Object

The Camera object is used to perform image acquisition and processing functions for MIPI Cameras. It includes several methods such as `open_cam`, `open_vps`, `get_frame`, `send_frame`, and `close`. The detailed description is as follows:

## open_cam

<font color='Blue'>[Description]</font>

Open the specified channel of the MIPI camera and set the camera output frame rate and resolution format.

<font color='Blue'>[Function Declaration]</font>

```python
Camera.open_cam(video_index, [width, height])
```

<font color='Blue'>[Parameter Description]</font>

| Parameter Name | Definition Description | Value Range |
| -------------- | --------------------- | ----------- |
| video_index    | The host index corresponding to the camera. -1 means automatic detection. The index can be found in the /etc/board_config.json configuration file. | Values: -1, 0, 1, 2, 3 |
| fps            | The frame rate of the camera output image | Depending on the camera model, default value is 30 |
| width          | The final width of the camera output image | Depending on the camera model, default value is 1920 (2560 for GC4663) |
| height         | The final height of the camera output image | Depending on the camera model, default value is 1080 (1440 for GC4663) |

<font color='Blue'>[Usage]</font>

```python
#create camera object
camera = libsrcampy.Camera()

#open MIPI Camera, fps: 30, solution: 1080p
ret = camera.open_cam(-1,  [1920, 1080])
```

<font color='Blue'>[Return Value]</font>

| Return Value | Description |
| ------------ | ----------- |
| 0            | Success     |
| -1           | Failure     |

<font color='Blue'>[Notes]</font>

The resolution output part supports two-dimensional `list` type input, which enables multiple groups of different resolution outputs for the camera. The `list` supports up to 4 groups of reduction and 1 group of enlargement, with a zoom range between `1/8` and `1.5` times the original resolution of the camera. To use it, follow the example below:

```python
ret = cam.open_cam(0, -1, 30, [[1920, 1080], [1280, 720]])
```

<font color='Blue'>【Reference Code】</font>  

None

## open_vps

<font color='Blue'>【Function Description】</font>

Enable the video process function of the specified camera channel, supporting image scaling, rotation, cropping, and other functions for the input image.

<font color='Blue'>【Function Declaration】</font>  

```python
Camera.open_vps([src_width, src_height], [dst_width, dst_height], crop_rect, rotate)
```

<font color='Blue'>【Parameter Description】</font>  


| Parameter Name      | Definition                  | Value Range    |
| ----------- | ------------------------ | --------  |
| src_width  | Width of the input image                 | Determine by the camera output width |
| src_height | Height of the input image                 | Determine by the camera output height |
| dst_width  | Width of the output image | 1/8 to 1.5 times the input width |
| dst_height | Height of the output image | 1/8 to 1.5 times the input height |
| crop_rect  | Width and height of the cropped area, input format[x, y] | Not exceed the input image size |
| rotate     | Rotation angle, supports rotation in two channels | Range is 0 to 3, representing "no rotation", "90 degrees", "180 degrees", "270 degrees" respectively |


<font color='Blue'>【Usage】</font> 

```python
#create camera object
camera = libsrcampy.Camera()

#enable vps function
ret = camera.open_vps([1920, 1080],[ 512, 512])
```

<font color='Blue'>【Return Value】</font>  

| Return Value | Definition |                 
| ------ | ----- |
| 0      | Success  |
| -1    | Failure |

<font color='Blue'>【Important Note】</font>- The image cropping function crops the image according to the configured size with the upper-left corner of the image as the origin.
- The image cropping is performed before scaling and rotation operations, and the multi-channel configuration is passed through the input parameter `list`.

<font color='Blue'>【Reference Code】</font>

None

## get_frame

<font color='Blue'>【Function Description】</font>

Get the image output of the camera object. It needs to be called after `open_cam` and `open_vps`.

<font color='Blue'>【Function Declaration】</font>

```python
Camera.get_frame(module, [width, height])
```

<font color='Blue'>【Parameter Description】</font>

| Parameter Name | Definition                       | Value Range                      |
| -------------- | --------------------------- | --------------------------------- |
| module         | The module of the image to be obtained | Default is 2                      |
| width          | The width of the image to be obtained  | The output width set by `open_cam` and `open_vps` |
| height         | The height of the image to be obtained | The output height set by `open_cam` and `open_vps` |


<font color='Blue'>【Usage】</font>

```python
cam = libsrcampy.Camera()

#create camera object
camera = libsrcampy.Camera()

#enable vps function
ret = camera.open_vps([1920, 1080],[ 512, 512])

#get one image from camera
img = cam.get_frame(2,[512,512])
```

<font color='Blue'>【Return Value】</font>

| Return Value | Definition |
| ------ | ----- |
| 0      | Success |
| -1    | Failure |

<font color='Blue'>[Caution]</font> 

This method needs to be called after `open_cam` and `open_vps`

<font color='Blue'>[Reference Code]</font>  

```python
import sys, os, time

from hobot_spdev import libsppydev as srcampy

def test_camera():
    cam = srcampy.Camera()

    #open MIPI camera, fps: 30, solution: 1080p
    ret = cam.open_cam(-1, [1920, 1080])
    print("Camera open_cam return:%d" % ret)

    # wait for 1s
    time.sleep(1)

    #get one image from camera   
    img = cam.get_frame(2,1920, 1080)
    if img is not None:
        #save file
        fo = open("output.img", "wb")
        fo.write(img)
        fo.close()
        print("camera save img file success")
    else:
        print("camera save img file failed")
    
    #close MIPI camera
    cam.close()
    print("test_camera done!!!")

test_camera()
```

## send_frame

<font color='Blue'>[Function Description]</font>

Input an image to the `vps` module and trigger image processing.

<font color='Blue'>[Function Declaration]</font>

```python
Camera.send_frame(img)
```

<font color='Blue'>【Parameter Description】</font>  

| Parameter Name | Definition | Value Range |
| -------------- | ---------- | ----------- |
| img            | The image data to be processed | Consistent with the input size of VPS |

<font color='Blue'>【Usage】</font> 

```python
camera = libsrcampy.Camera()

#enable vps function, input: 1080p, output: 512x512
ret = camera.open_vps( [1920, 1080], [512, 512])
print("Camera vps return:%d" % ret)

fin = open("output.img", "rb")
img = fin.read()
fin.close()

#send image to vps module
ret = vps.send_frame(img)
```

<font color='Blue'>【Return Value】</font>  

| Return Value | Definition |                 
| ------------ | ---------- |
| 0            | Success    |
| -1           | Failed     |

<font color='Blue'>【Note】</font> 

This interface needs to be called after `open_vps`.

<font color='Blue'>【Reference Code】</font>  

```python
import sys, os, time

import numpy as np
import cv2
from hobot_spdev import libsppydev as srcampy

def test_camera_vps():
    vps = srcampy.Camera()
    #enable vps function, input: 1080p, output: 512x512
    ret = vps.open_vps( [1920, 1080], [512, 512])
    print("Camera vps return:%d" % ret)

    fin = open("output.img", "rb")
    img = fin.read()
    fin.close()

    #send image data to vps
    ret = vps.send_frame(img)
    print ("Process send_frame return:%d" % ret)

    fo = open("output_vps.img", "wb+")

    #get image data from vps
    img = vps.get_frame()
    if img is not None:
        fo.write(img)
        print("encode write image success")
    else:
        print("encode write image failed")
    fo.close()

    #close vps function
    vps.close()
    print("test_camera_vps done!!!")

    test_camera_vps():
```
## close

<font color='Blue'>【Function Description】</font>

Enable the MIPI camera to close.

<font color='Blue'>【Function Declaration】</font>  

```python
Camera.close()
```

<font color='Blue'>【Parameter Description】</font>  

None

<font color='Blue'>【Usage Method】</font> 

```python
cam = libsrcampy.Camera()

# Open MIPI camera with fps set to 30 and resolution set to 1080p
ret = cam.open_cam(-1, [1920, 1080])
print("Camera open_cam return:%d" % ret)

# Close the MIPI camera
cam.close()
```

<font color='Blue'>【Return Value】</font>  

None

<font color='Blue'>【Precautions】</font> 

None

<font color='Blue'>【Sample Code】</font>  

None