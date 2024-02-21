---
sidebar_position: 3
---
# DECODER API

The `DECODER` API provides the following interfaces:

| Function | Description |
| ---- | ----- |
| sp_init_decoder_module | **Initialize the decoder module object** |
| sp_release_decoder_module | **Destroy the decoder module object** |
| sp_start_decode | **Create an image decoding channel** |
| sp_stop_decode | **Close the image decoding channel** |
| sp_decoder_get_image | **Get the decoded image frame from the decoding channel** |
| sp_decoder_set_image | **Pass the bitstream data to the decoding channel for decoding** |

:::note

RDK Ultra does **not** support `H264` encoding and decoding.

:::

## sp_init_decoder_module

**[Function Prototype]**

`void *sp_init_decoder_module()`

**[Description]**

Initialize the decoder module object. The operation handle needs to be obtained when using the decoder module. It supports video bitstreams in H264, H265, and Mjpeg formats.

**[Parameters]**

None.

**[Return Type]**

Returns the `DECODER` object on success and NULL on failure.

## sp_release_decoder_module

**[Function Prototype]**

`void sp_release_decoder_module(void *obj)`

**[Description]**

Destroy the decoder module object.**【Parameters】**

 - `obj`: Object pointer obtained when calling the initialization interface.

**【Return Type】** 

Void

## sp_start_decode  

**【Function Prototype】**  

`int sp_start_decode(void *decoder_object, const char *stream_file, int32_t type, int32_t width, int32_t height)`

**【Function Description】**  

Create a decoding channel and set the type and resolution of the decoding stream.

**【Parameters】**

- `obj`: Initialized `DECODER` object pointer.
- `stream_file`: If `stream_file` is set to a stream file name, it represents decoding of this stream file. For example, setting the stream file of H.265 as "stream.h265". If `stream_file` is an empty string, it indicates that the decoding data stream needs to be passed in through the `sp_decoder_set_image` function.
- `type`: The data type to be decoded, which supports `SP_ENCODER_H265` and `SP_ENCODER_MJPEG`.
- `width`: The width of the decoded image frame resolution.
- `height`: The height of the decoded image frame resolution.

**【Return Type】** 

Returns 0 on success and -1 on failure.

## sp_stop_decode  

**【Function Prototype】**  

`int32_t sp_stop_decode(void *obj)`

**【Function Description】**  

Close the decoding channel.

**【Parameters】**

- `obj`: Initialized `DECODER` object pointer.

**【Return Type】** 

Returns 0 on success and -1 on failure.

## sp_decoder_get_image**【Function Prototype】**

`int32_t sp_decoder_get_image(void *obj, char *image_buffer)`

**【Description】**

Get the decoded frame data from the decoding channel. The format of the returned image data is `NV12` YUV image.

**【Parameters】**

- `obj`: Pointer to the initialized `DECODER` object.
- `image_buffer`: Buffer for the returned image frame data. The size of this buffer is related to the resolution of the image, which is width * height * 3 / 2.

**【Return Type】**

Return 0 on success, -1 on failure.

## sp_decoder_set_image

**【Function Prototype】**

`int32_t sp_decoder_set_image(void *obj, char *image_buffer, int32_t size, int32_t eos)`

**【Description】**

Send the bitstream data to the open decoding channel. 
If decoding H264 or H265 bitstream, you need to send 3-5 frames of data first to allow the decoder to complete the frame buffer before retrieving decoded frame data.
If decoding H264 bitstream, the first frame of input data must be the description information of sps and pps. Otherwise, the decoder will return an error and exit.

**【Parameters】**

- `obj`: Pointer to the initialized `DECODER` object.
- `image_buffer`: Pointer to the bitstream data.
- `size`: Size of the bitstream data.
- `eos`: Whether this is the last frame of data.

**【Return Type】**

Return 0 on success, -1 on failure.