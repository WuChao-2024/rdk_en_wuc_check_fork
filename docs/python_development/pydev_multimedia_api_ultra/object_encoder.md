---
sidebar_position: 2
---

# Encoder Object

The Encoder object implements video data compression encoding functionality, comprising several methods including `encode`, `send_frame`, `get_frame`, and `close`. Detailed explanations are provided below:

## encode

<font color='Blue'>【Function Description】</font>

Configures and enables the encode coding module.

<font color='Blue'>【Function Declaration】</font>

```python
Encoder.encode(encode_type , [width, height], bits)
```

<font color='Blue'>【Parameter Description】</font>  

| Parameter Name | Description           | Value Range                    |
| -------------- | --------------------- | ------------------- |
| encode_type    | Video Encoding Type   | Range 2~3, corresponding to `H265` and `MJPEG` respectively |
| width          | Image Width for Input to Encoding Module | Not exceeding 4096              |
| height         | Image Height for Input to Encoding Module | Not exceeding 4096              |
| bits           | Bitrate of Encoding Module | Default 8000kbps         |

<font color='Blue'>【Usage】</font>

```python
# Create an encode object
encode = libsrcampy.Encoder()

# Enable encode channel 0, resolution: 1080p, format: H265
ret = encode.encode(2, [1920, 1080])
```

<font color='Blue'>【Return Value】</font>  

| Return Value | Definition Description |                 
| ------------ | ----- |
| 0            | Success  |
| -1           | Failure   |

<font color='Blue'>【Notes】</font>

None

<font color='Blue'>【Sample Code】</font>

None

## send_frame

<font color='Blue'>【Function Description】</font>

Inputs image files into the enabled encoding channel for encoding according to a predetermined format.

<font color='Blue'>【Function Declaration】</font> 

```python
Encoder.send_frame(img)
```

<font color='Blue'>【Parameter Description】</font>  

| Parameter Name | Description               | Value Range                     |
| -------------- | ------------------------- | --------------------- |
| img            | Image Data to be Encoded, in NV12 format | None |

<font color='Blue'>【Usage】</font> 

```python
fin = open("output.img", "rb")
input_img = fin.read()
fin.close()

# Input image data into the encoder
ret = encode.send_frame(input_img)
```

<font color='Blue'>【Return Value】</font>  

| Return Value | Definition Description |                 
| ------------ | ----- |
| 0            | Success  |
| -1           | Failure   |

<font color='Blue'>【Notes】</font> 

None

<font color='Blue'>【Sample Code】</font>  

None

## get_frame

<font color='Blue'>【Function Description】</font>

Retrieves encoded data.

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
| ------------ | ----- |
| 0            | Success  |
| -1           | Failure   |

<font color='Blue'>【Notes】</font> 

This interface should be used after calling `Encoder.encode()` to create an encoding channel.

<font color='Blue'>【Sample Code】</font>  

```python
import sys, os, time
import numpy as np
import cv2
from hobot_vio import libsrcampy

def test_encode():
    # Create an encode object
    enc = libsrcampy.Encoder()
    ret = enc.encode(2, [1920, 1080])
    print("Encoder encode return:%d" % ret)

    # Save encoded data to file
    fo = open("encode.h264", "wb+")
    a = 0
    fin = open("output.img", "rb")
    input_img = fin.read()
    fin.close()
    while a < 100:
        # Send image data to the encoder
        ret = enc.send_frame(input_img)
        print("Encoder send_frame return:%d" % ret)
        # Get encoded data
        img = enc.get_frame()
        if img is not None:
            fo.write(img)
            print("Encoded write image success count: %d" % a)
        else:
            print("Encoded write image failed count: %d" % a)
        a = a + 1

    enc.close()
    print("test_encode done!!!")

test_encode()
```

## close

<font color='Blue'>【Function Description】</font>

Closes the enabled encoding channel.

<font color='Blue'>【Function Declaration】</font>  

```python
Encoder.close()
```

<font color='Blue'>【Parameter Description】</font>  

None

<font color='Blue'>【Usage】</font> 

None

<font color='Blue'>【Return Value】</font>  

| Return Value | Definition Description |
| ------------ | ----- |
| 0            | Success  |
| -1           | Failure   |

<font color='Blue'>【Notes】</font> 

This interface should be used after calling `Encoder.encode()` to create an encoding channel.

<font color='Blue'>【Sample Code】</font>  

None
