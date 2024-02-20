# VIO (Video Input) API

The `VIO` module provides functions for operating `MIPI` cameras and image processing.

The `VIO` API provides the following interfaces:

| Function | Description |
| ---- | ----- |
| sp_init_vio_module | **Initialize the VIO object** |
| sp_release_vio_module | **Destroy the VIO object** |
| sp_open_camera | **Open the camera** |
| sp_open_vps | **Open VPS** |
| sp_vio_close | **Close the camera** |
| sp_vio_get_frame | **Get video frame** |
| sp_vio_set_frame | **Send video frame to VPS module** |

## sp_init_vio_module  

**[Function Prototype]**  

`void *sp_init_vio_module()`

**[Description]**  

Initialize the VIO object and create an operating handle. This must be executed before calling other interfaces.

**[Parameters]**

None

**[Return Type]**  

If successful, returns a pointer to the VIO object. If unsuccessful, returns `NULL`.

## sp_release_vio_module  

**[Function Prototype]**  

`void sp_release_vio_module(void *obj)`

**[Description]**  

Destroy the VIO object.

**[Parameters]**- `obj`: Pointer to the `VIO` object obtained when calling the initialization interface.

**[Return Type]**

N/A

## sp_open_camera

**[Function Prototype]**

`int32_t sp_open_camera(void *obj, int32_t chn_num, int32_t *width, int32_t *height)`

**[Function Description]**

Initialize the MIPI camera connected to RDK X3.
Set the output resolution, supporting up to 5 groups of resolutions, where only 1 group can be enlarged and 4 groups can be reduced. The maximum zoom is 1.5 times the original image, and the minimum reduction is 1/8 of the original image.

**[Parameters]**

- `obj`: Pointer to the initialized `VIO` object
- `chn_num`: Set the number of different resolution images to output, with a maximum of 5 and a minimum of 1.
- `width`: Address of the array for configuring the output width
- `height`: Address of the array for configuring the output height

**[Return Type]**

Returns 0 on success, -1 on failure


## sp_open_vps

**[Function Prototype]**

`int32_t sp_open_vps(void *obj, int32_t chn_num, int32_t src_width, int32_t src_height, int32_t *dst_width, int32_t *dst_height, int32_t *crop_x, int32_t *crop_y, int32_t *crop_width, int32_t *crop_height, int32_t *rotate)`

**[Function Description]**

Open an image processing module, supporting zoom, enlargement, rotation, and cropping tasks on the input image.

**[Parameters]**

- `obj`: Pointer to the initialized `VIO` object
- `chn_num`: Set the number of output images, which is a maximum of 5 and is related to the size of the target height array
- `src_width`: Original frame width
- `src_height`: Original frame height
- `dst_width`: Address of the array for configuring the target output width
- `dst_height`: Address of the array for configuring the target output height
- `crop_x`: Collection of the top-left x coordinates of the cropping area. Pass `NULL` if the cropping function is not used.
- `crop_y`: Collection of the top-left y coordinates of the cropping area. Pass `NULL` if the cropping function is not used.- `crop_width`: The width of the cropping area. Pass `NULL` if cropping is not used.
- `crop_height`: The height of the cropping area. Pass `NULL` if cropping is not used.
- `rotate`: The rotation angle. Currently supports `ROTATION_90` (90°), `ROTATION_180` (180°), and `ROTATION_270` (270°). Pass `NULL` if rotation is not used.

**[Return Type]**

Returns 0 on success, -1 on failure.

## sp_vio_close

**[Function Prototype]**

`int32_t sp_vio_close(void *obj)`

**[Description]**

Closes the camera or VPS module based on the input `obj`.

**[Parameters]**

- `obj`: Initialized 'VIO' object pointer.

**[Return Type]**

Returns 0 on success, -1 on failure.

## sp_vio_get_frame

**[Function Prototype]**

`int32_t sp_vio_get_frame(void *obj, char *frame_buffer, int32_t width, int32_t height, const int32_t timeout)`

**[Description]**

Gets the image frame data of the specified resolution (resolution needs to be passed when opening the module, otherwise it will fail). Returns the image data in `NV12` format.

**[Parameters]**

- `obj`: Initialized 'VIO' object pointer.
- `frame_buffer`: Pointer to the pre-allocated buffer used to save the retrieved image. Currently, the retrieved image is in `NV12` format, so the pre-allocated buffer size can be calculated using the formula `height * width * 3 / 2`, or using the provided macro definition `FRAME_BUFFER_SIZE(w, h)`.
- `width`: Width of the image buffer to save the image, must be the same as the configured output width in `sp_open_camera` or `sp_open_vps`.
- `height`: Height of the image buffer to save the image, must be the same as the configured output height in `sp_open_camera` or `sp_open_vps`.
- `timeout`: Timeout for retrieving the image, in milliseconds. Generally set to `2000`.

**[Return Type]**

Returns 0 on success, -1 on failure.

## sp_vio_get_raw**[Function Prototype]**

`int32_t sp_vio_get_raw(void *obj, char *frame_buffer, int32_t width, int32_t height, const int32_t timeout)`

**[Function Description]**

Get raw image data from the camera.

**[Parameters]**

- `obj`: Pointer to initialized `VIO` object.
- `frame_buffer`: Pointer to pre-allocated buffer for storing the fetched raw image. The size of the allocated memory can be calculated using the formula `(height * width * image_depth) / 8`.
- `width`: Pass `NULL` when getting raw image.
- `height`: Pass `NULL` when getting raw image.
- `timeout`: Timeout for getting the image, in milliseconds. Usually set to `2000`.

**[Return Type]**

Returns 0 on success, -1 on failure.

## sp_vio_get_yuv  

**[Function Prototype]**

`int32_t sp_vio_get_yuv(void *obj, char *frame_buffer, int32_t width, int32_t height, const int32_t timeout)`

**[Function Description]**

Get YUV data from the camera's ISP module.

**[Parameters]**

- `obj`: Pointer to initialized `VIO` object.
- `frame_buffer`: Pointer to pre-allocated buffer for storing the fetched image. The images obtained are in `NV12` format, so the size of the allocated memory can be calculated using the formula `height * width * 3 / 2`, or by using the provided macro `FRAME_BUFFER_SIZE(w, h)`.
- `width`: Pass `NULL` when getting ISP's YUV data.
- `height`: Pass `NULL` when getting ISP's YUV data.
- `timeout`: Timeout for getting the image, in milliseconds. Usually set to `2000`.

**[Return Type]**

Returns 0 on success, -1 on failure.

## sp_vio_set_frame  

**[Function Prototype]**

`int32_t sp_vio_set_frame(void *obj, void *frame_buffer, int32_t size)`

**[Function Description]**

When using the `vps` module, the source data needs to be passed into this interface through a call. The data in `frame_buffer` must be image data in the `NV12` format, and the resolution must be consistent with the original frame resolution when calling the `sp_open_vps` interface.

**[Parameters]**

- `obj`: Initialized `VIO` object pointer.
- `image_buffer`: The image frame data to be processed, which must be image data in the `NV12` format, and the resolution must be consistent with the original frame resolution when calling the `sp_open_vps` interface.
- `size`: Frame size.

**[Return Type]**

Return 0 for success, -1 for failure.