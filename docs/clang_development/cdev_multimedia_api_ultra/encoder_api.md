---
sidebar_position: 2
---
# ENCODER API

The ENCODER API provides the following interfaces:

| Function | Description |
| ---- | ----- |
| sp_init_encoder_module | **Initialize the encoding module object** |
| sp_release_encoder_module | **Destroy the encoding module object** |
| sp_start_encode | **Create an image encoding channel** |
| sp_stop_encode | **Close the image encoding channel** |
| sp_encoder_set_frame | **Pass image frames to the encoding channel** |
| sp_encoder_get_stream | **Get the encoded stream from the encoding channel** |

:::note

RDK Ultra does **not** support H264 encoding or decoding.

:::

## sp_init_encoder_module

**【Function prototype】**

`void *sp_init_encoder_module()`

**【Description】**

Initialize the encoding module object. This function needs to be called to obtain the handle for using the encoding module.

**【Parameters】**

None

**【Return type】**

If successful, it returns a pointer to an ENCODER object. Otherwise, it returns NULL.

## sp_release_encoder_module

**【Function prototype】**

`void sp_release_encoder_module(void *obj)`

**【Description】**

Destroy the encoding module object.

**【Parameters】**

- `obj`: Pointer to the object obtained when calling the initialization interface.

**【Return Type】**

None

## sp_start_encode  

**【Function Prototype】**  

`int32_t sp_start_encode(void *obj, int32_t type, int32_t width, int32_t height, int32_t bits)`

**【Function Description】**

Create an image encoding channel, supporting up to `32` encodings. Supported encoding types include `H264`, `H265`, and `MJPEG`.

**【Parameters】**

- `obj`: Pointer to the initialized `ENCODER` object.
- `type`: Image encoding type. Supported types include `SP_ENCODER_H264`, `SP_ENCODER_H265`, and `SP_ENCODER_MJPEG`.
- `width`: Width of the image data sent to the encoding channel.
- `height`: Height of the image data sent to the encoding channel.
- `bits`: Encoding bitrate. Common values include 512, 1024, 2048, 4096, 8192, 16384 (unit: Mbps). Other values are also acceptable. The higher the bitrate, the clearer the encoded image, but the larger the compressed data.

**【Return Type】**

Returns 0 on success, -1 on failure.

## sp_stop_encode  

**【Function Prototype】**  

`int32_t sp_stop_encode(void *obj)`

**【Function Description】**

Close the open encoding channel.

**【Parameters】**

- `obj`: Pointer to the initialized `ENCODER` object.

**【Return Type】**

Returns 0 on success, -1 on failure.

## sp_encoder_set_frame

**【Function Prototype】**

`int32_t sp_encoder_set_frame(void *obj, char *frame_buffer, int32_t size)`

**【Function Description】**

This function is used to pass the image frame data that needs to be encoded to the encoding channel. The format must be `NV12`.

**【Parameters】**

- `obj`: Pointer to the initialized `ENCODER` object.
- `frame_buffer`: Image frame data to be encoded. It must be in `NV12` format and have the same resolution as the image frame resolution when calling the `sp_start_encode` interface.
- `size`: Size of the image frame data. The formula to calculate the size of an `NV12` format image is width * height * 3 / 2.

**【Return Type】**

Returns 0 for success, -1 for failure.

## sp_encoder_get_stream  

**【Function Prototype】**

`int32_t sp_encoder_get_stream(void *obj, char *stream_buffer)`

**【Function Description】**

This function is used to retrieve the encoded bitstream data from the encoding channel.

**【Parameters】**

- `obj`: Pointer to the initialized `ENCODER` object.
- `stream_buffer`: After a successful retrieval, the bitstream data will be stored in this buffer. The size of this buffer needs to be adjusted according to the encoding resolution and bitrate.

**【Return Type】**

Returns the size of the bitstream data for success, -1 for failure.