# Encoder Object

The Encoder object implements the encoding and compression functions for video data. It includes several methods such as `encode`, `send_frame`, `get_frame`, `close`, etc. The detailed description is as follows:

## encode

<font color='Blue'>[Description]</font>

Configures and enables the encode encoding module.

<font color='Blue'>[Function Declaration]</font>

```python
Encoder.encode(encode_type, [width, height], bits)
```

<font color='Blue'>[Parameter Description]</font>  

| Parameter      | Description               | Range                          |
| -------------- | --------------------------| ------------------------------|
| encode_type    | Video encoding type       | Range 2~3, corresponding to `H265`, `MJPEG` |
| width          | Image width for encoding module input | Not exceeding 4096 |
| height         | Image height for encoding module input | Not exceeding 4096 |
| bits           | Bit rate for the encoding module | Default: 8000kbps |

<font color='Blue'>[Usage]</font>

```python
#create encode object
encode = libsrcampy.Encoder()

#enable encode channel 0, solution: 1080p, format: H265
ret = encode.encode(2, [1920, 1080])
```

<font color='Blue'>[Return Value]</font>  

| Return Value | Definition            |                 
| ------------ | -----------------     |
| 0            | Success               |
| -1           | Failure               |

<font color='Blue'>[Notes]</font>

None<font color='Blue'>【功能描述】</font>

从编码后的图像缓冲区中获取解码后的图像数据

<font color='Blue'>【函数声明】</font> 

```python
Encoder.get_frame()
```

<font color='Blue'>【参数描述】</font>  

无

<font color='Blue'>【使用方法】</font> 

```python
#decode encoded image frame
decoded_frame = encode.get_frame()
```

<font color='Blue'>【返回值】</font>  

| 返回值  | 定义描述 |                 
| ------- | ------- |
| img      | 解码后的图像数据  |
| None    | 如果没有可用的解码后的图像数据  |

<font color='Blue'>【注意事项】</font> 

无

<font color='Blue'>【参考代码】</font>  

无<font color='Blue'>【Function Description】</font>

Get the encoded data

<font color='Blue'>【Function Declaration】</font>

```python
Encoder.get_frame()
```

<font color='Blue'>【Usage】</font>

None

<font color='Blue'>【Parameter Description】</font>

None

<font color='Blue'>【Return Value】</font>

| Return Value | Definition Description |                 
| ------ | ----- |
| 0      | Success  |
| -1    | Failure   |

<font color='Blue'>【Attention】</font> 

This interface needs to be used after calling `Encoder.encode()` to create an encoding channel

<font color='Blue'>【Reference Code】</font>  

```python
import sys, os, time

import numpy as np
import cv2
from hobot_vio import libsrcampy

def test_encode():
    #create encode object
    enc = libsrcampy.Encoder()
    ret = enc.encode(2, [1920, 1080])
    print("Encoder encode return:%d" % ret)

    #save encoded data to file
    fo = open("encode.h264", "wb+")
    a = 0
    fin = open("output.img", "rb")
    input_img = fin.read()
    fin.close()
``````python
while a < 100:
    #send image data to encoder
    ret = enc.send_frame(input_img)
    print("Encoder send_frame return:%d" % ret)
    #get encoded data
    img = enc.get_frame()
    if img is not None:
        fo.write(img)
        print("encode write image success count: % d" % a)
    else:
        print("encode write image failed count: % d" % a)
    a = a + 1

enc.close()
print("test_encode done!!!")

test_encode()
```

## close

<font color='Blue'>【Description】</font>

Close the enabled encoding channel.

<font color='Blue'>【Function Signature】</font>  

```python
Encoder.close()
```

<font color='Blue'>【Parameters】</font>  

None

<font color='Blue'>【Usage】</font> 

None

<font color='Blue'>【Return Values】</font>  

| Return Value | Description |
| ------------ | ----------- |
| 0            | Success     |
| -1           | Failure     |

<font color='Blue'>【Notes】</font> 

This interface needs to be used after calling `Encoder.encode()` to create the encoding channel.<font color='Blue'>【Reference Code】</font>  

None