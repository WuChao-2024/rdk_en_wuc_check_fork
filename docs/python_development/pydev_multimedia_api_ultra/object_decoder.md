# Decoder Object

The Decoder object implements the decoding function for video data and includes several methods such as `decode`, `send_frame`, `get_frame`, `close`, etc. The detailed description is as follows:

## decode

<font color='Blue'>[Description]</font>

Enables the decode module and decodes the video file.

<font color='Blue'>[Function Declaration]</font>  

```python
Decoder.decode(decode_type, [width, height], file)
```

<font color='Blue'>[Parameter Description]</font>  

| Parameter    | Description           | Value Range                    |
| --------- | --------------- | ------------------- |
| file      | The name of the file to be decoded     |       N/A       |
| decode_type | The type of video decoding  | Range 2~3, corresponding to `H265` and `MJPEG` respectively |
| width     | The width of the input image for the decode module      | Not exceeding 4096              |
| height    | The height of the input image for the decode module      | Not exceeding 4096              |

<font color='Blue'>[Usage]</font> 

```python
#create decode object
decode = libsrcampy.Decoder()

#enable decode channel 0, solution: 1080p, format: h265
ret = dec.decode(2,[ 1920, 1080],"encode.h265")
```

 <font color='Blue'>[Return Value]</font>  

The return value is a `list` data with two elements.

| Return Value                | Definition      |
| ---------------- | ----------- |
| list[0] | 0: Decoding successful, -1: Decoding failed      | 
| list[1] | The number of frames in the input bitstream file, valid when decoding is successful     |

<font color='Blue'>[Note]</font><font color='Blue'>【参考代码】</font>  

None

## get_img

<font color='Blue'>【功能描述】</font>

Get the output results of the decoding module.

<font color='Blue'>【函数声明】</font>
```python
Decoder.get_img()
```

<font color='Blue'>【参数描述】</font>

None

<font color='Blue'>【使用方法】</font>

```python
ret = dec.decode(2,[ 1920, 1080],"encode.h265")
print ("Decoder return:%d frame count: %d" %(ret[0], ret[1]))

img = dec.get_img()
```

<font color='Blue'>【返回值】</font>

| 返回值 | 定义描述 |
| ------ | ----- |
| -1      | Decoded data |

<font color='Blue'>【注意事项】</font>

This interface needs to be used after calling `Decoder.decode()` to create a decoding channel.

<font color='Blue'>【参考代码】</font>

```python
import sys, os, time

import numpy as np
import cv2
from hobot_vio import libsrcampy

def test_decode():    #create decode object
    dec = libsrcampy.Decoder()

    #enable decode function
    #decode input: encode.h265, solution: 1080p, format: h265
    ret = dec.decode(2,[ 1920, 1080],"encode.h265")
    print ("Decoder return:%d frame count: %d" %(ret[0], ret[1]))
    
    #get decoder output
    img = dec.get_img()
    if img is not None:
        #save file
        fo = open("output.img", "wb")
        fo.write(img)
        fo.close()
        print("decode save img file success")
    else:
        print("decode save img file failed")

    dec.close()
    print("test_decode done!!!")| Return | Description |
| ------ | ----------- |
| 0      | Success     |
| -1     | Failure     |

<font color='Blue'>【Notes】</font> 

This interface needs to be used after calling `Decoder.decode()` to create a decoding channel, and the parameter `file` should be left empty when creating the decoding channel.

<font color='Blue'>【Reference code】</font>  

```python
import sys, os, time

import numpy as np
import cv2
from hobot_spdev import libsppydev as srcampy

def test_cam_bind_encode_decode_bind_display():
    #camera start
    cam = srcampy.Camera()
    ret = cam.open_cam(-1, [[1920, 1080], [1280, 720]])
    print("Camera open_cam return:%d" % ret)

    #enable encoder
    enc = srcampy.Encoder()
    ret = enc.encode(2, [1920, 1080])
    print("Encoder encode return:%d" % ret)

    #enable decoder
    dec = srcampy.Decoder()
    ret = dec.decode(2,[ 1920, 1080],"")
    print ("Decoder return:%d frame count: %d" %(ret[0], ret[1]))

    ret = srcampy.bind(cam, enc)
    print("libsrcampy bind return:%d" % ret)

    a = 0
    while a < 100:
        #get encode image from encoder
        img = enc.get_frame()
        if img is not None:
            #send encode image to decoder
            dec.set_frame(img)
            print("encode get image success count: %d" % a)
        else:
            print("encode get image failed count: %d" % a)
        a = a + 1

```ret = srcampy.unbind(cam, enc)
dec.close()
enc.close()
cam.close()
print("test_cam_bind_encode_decode_bind_display done!!!")

test_cam_bind_encode_decode()
```

## close

<font color='Blue'>【Function Description】</font>

Close the decoder module.

<font color='Blue'>【Function Declaration】</font>
```python
Decoder.close()
```

<font color='Blue'>【Parameter Description】</font>

None

<font color='Blue'>【Usage】</font> 

None

<font color='Blue'>【Return Value】</font>

| Return Value | Definition |
| ------ | ---- |
| 0      | Success |
| -1    | Failure |

<font color='Blue'>【Notes】</font>

When exiting the program, you need to call the `close` interface to release resources.

<font color='Blue'>【Sample Code】</font>

None