---
sidebar_position: 3
---

# Decoder Object

The Decoder object provides decoding functionality for video data, incorporating several methods such as `decode`, `send_frame`, `get_frame`, and `close`. Detailed explanations are given below:

## decode

<font color='Blue'>【Function Description】</font>

Activates the decode module to decode a video file.

<font color='Blue'>【Function Declaration】</font>  

```python
Decoder.decode(decode_type, [width, height], file)
```

<font color='Blue'>【Parameter Description】</font>  

| Parameter Name | Description           | Value Range                    |
| -------------- | --------------------- | ------------------- |
| file           | The name of the file to be decoded     |       N/A       |
| decode_type    | Video decoding type  | Range 2~3, corresponding to `H265` and `MJPEG`, respectively |
| width          | Image width input to the decoding module      | No more than 4096              |
| height         | Image height input to the decoding module     | No more than 4096              |

<font color='Blue'>【Usage Example】</font> 

```python
# Create a decode object
decode = libsrcampy.Decoder()

# Enable decode channel 0, resolution: 1080p, format: h265
ret = dec.decode(2, [1920, 1080], "encode.h265")
```

<font color='Blue'>【Return Value】</font>  

Returns a `list` containing 2 members.

| Return Value                | Definition Description      |
| ------------------------- | ----------- |
| list[0] | 0: Decoding successful, -1: Decoding failed      | 
| list[1] | Number of frames in the input bitstream file, valid when decoding is successful |

<font color='Blue'>【Notes】</font> 

None

<font color='Blue'>【Sample Code】</font>  

Not provided.

## get_img

<font color='Blue'>【Function Description】</font>

Retrieves the output result from the decoding module.

<font color='Blue'>【Function Declaration】</font>

```python
Decoder.get_img()
```

<font color='Blue'>【Parameter Description】</font>

No parameters.

<font color='Blue'>【Usage Example】</font>

```python
ret = dec.decode(2,[1920, 1080],"encode.h265")
print ("Decoder return:%d frame count: %d" %(ret[0], ret[1]))

img = dec.get_img()
```

<font color='Blue'>【Return Value】</font>

| Return Value | Definition Description |
| ------------ | ----- |
| -1           | Decoded data  |

<font color='Blue'>【Notes】</font>

This interface should be used after creating a decoding channel by calling `Decoder.decode()`.

<font color='Blue'>【Sample Code】</font>

```python
import sys, os, time
import numpy as np
import cv2
from hobot_vio import libsrcampy

def test_decode():
    # Create a decode object
    dec = libsrcampy.Decoder()

    # Enable the decoding function
    # Decode input: encode.h265, resolution: 1080p, format: h265
    ret = dec.decode(2, [1920, 1080], "encode.h265")
    print("Decoder return:%d frame count: %d" %(ret[0], ret[1]))
    
    # Get decoder output
    img = dec.get_img()
    if img is not None:
        # Save file
        with open("output.img", "wb") as fo:
            fo.write(img)
        print("Decode and save image file success")
    else:
        print("Decode and save image file failed")

    dec.close()
    print("test_decode done!!!")

test_decode()
```

## set_img

<font color='Blue'>【Function Description】</font>

Sends a single frame of encoded data into the decoding module for decoding.

<font color='Blue'>【Function Declaration】</font>  

```python
Decoder.set_img(img, chn=0, eos=0)
```

<font color='Blue'>【Parameter Description】</font>  

| Parameter Name | Definition Description | Value Range |
| -------------- | --------------------- | ---------- |
| img            | Encoded single frame to be decoded | N/A |
| chn            | Decoder channel number      | Range 0~31 |
| eos            | Whether the decode data has ended   | 0: Not ended, 1: Ended |

<font color='Blue'>【Usage Example】</font> 

None provided.

<font color='Blue'>【Return Value】</font>  

| Return Value | Description |
| ------------ | ---- |
| 0             | Success |
| -1           | Failure |

<font color='Blue'>【Notes】</font> 

This interface should be used after creating a decoding channel by calling `Decoder.decode()` with an empty `file` parameter.

<font color='Blue'>【Sample Code】</font>  

```python
import sys, os, time
import numpy as np
import cv2
from hobot_spdev import libsppydev as srcampy

def test_cam_bind_encode_decode_bind_display():
    # Start camera
    cam = srcampy.Camera()
    ret = cam.open_cam(-1, [[1920, 1080], [1280, 720]])
    print("Camera open_cam return:%d" % ret)

    # Enable encoder
    enc = srcampy.Encoder()
    ret = enc.encode(2, [1920, 1080])
    print("Encoder encode return:%d" % ret)

    # Enable decoder
    dec = srcampy.Decoder()
    ret = dec.decode(2, [1920, 1080], "")
    print ("Decoder return:%d frame count: %d" %(ret[0], ret[1]))

    ret = srcampy.bind(cam, enc)
    print("libsrcampy bind return:%d" % ret)

    a = 0
    while a < 100:
        # Get encoded image from encoder
        img = enc.get_frame()
        if img is not None:
            # Send encoded image to decoder
            dec.set_img(img)
            print("encode get image success count: %d" % a)
        else:
            print("encode get image failed count: %d" % a)
        a = a + 1

    ret = srcampy.unbind(cam, enc)
    dec.close()
    enc.close()
    cam.close()
    print("test_cam_bind_encode_decode_bind_display done!!!")

    test_cam_bind_encode_decode()
```

## close

<font color='Blue'>【Function Description】</font>

Closes the decoding module.

<font color='Blue'>【Function Declaration】</font>

```python
Decoder.close()
```

<font color='Blue'>【Parameter Description】</font>

No parameters.

<font color='Blue'>【Usage Example】</font> 

None provided.

<font color='Blue'>【Return Value】</font>

| Return Value | Description |
| ------------ | ---- |
| 0             | Success |
| -1           | Failure |

<font color='Blue'>【Notes】</font>

The `close` interface should be called when exiting the program to release resources.

<font color='Blue'>【Sample Code】</font>

None.