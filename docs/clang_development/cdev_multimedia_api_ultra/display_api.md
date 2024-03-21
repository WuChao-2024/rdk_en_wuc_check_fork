---
sidebar_position: 4
---
# DISPLAY API

The `DISPLAY` API provides the following interfaces:

| Function | Description |
| ---- | ----- |
| sp_init_display_module | **Initialize the display module object** |
| sp_release_display_module | **Destroy the display module object** |
| sp_start_display | **Create a video display channel** |
| sp_stop_display | **Close the video display channel** |
| sp_display_set_image | **Pass an image to the video display channel** |
| sp_display_draw_rect | **Draw a rectangle on the display channel** |
| sp_display_draw_string | **Draw a string on the display channel** |
| sp_get_display_resolution | **Get the resolution of the display** |

## sp_init_display_module  

**【Function prototype】**  

`void *sp_init_display_module()`

**【Description】**  

Initialize the display module object. This module supports displaying video image data on a display connected to the `HDMI` interface, as well as providing the ability to draw rectangles and text on the display screen.

**【Parameters】**

None

**【Return type】** 

Returns a pointer to the `DISPLAY` object if successful, else returns NULL.

## sp_release_display_module  

**【Function prototype】**  

`void sp_release_display_module(void *obj)`

**【Description】**  

Destroy the `DISPLAY` object.

**【Parameters】**

- `obj`: Pointer to the initialized `DISPLAY` object.

**[Return Type]**

None

## sp_start_display  

**[Function Prototype]**

`int32_t sp_start_display(void *obj, int32_t width, int32_t height)`

**[Description]**

Creates a display channel. The maximum resolution supported by the RDK Ultra development board is `1920 x 1080`, with a maximum frame rate of `60fps`.

**[Parameters]**

- `obj`: Initialized `DISPLAY` object pointer
- `width`: Display output resolution - width
- `height`: Display output resolution - height

**[Return Type]**

Returns 0 on success, -1 on failure.

## sp_stop_display  

**[Function Prototype]**

`int32_t sp_stop_display(void *obj)`

**[Description]**

Closes the display channel.

**[Parameters]**

- `obj`: Initialized `DISPLAY` object pointer

**[Return Type]**

Returns 0 on success, -1 on failure.

## sp_display_set_image  

**[Function Prototype]**

`int32_t sp_display_set_image(void *obj, char *addr, int32_t size)`

**[Description]**

Send a frame image to the display module. The image format only supports `NV12` image.

**[Parameters]**

- `obj`: Initialized `DISPLAY` object pointer
- `addr`: Image data, the image format only supports `NV12`
- `size`: Image data size, calculated by the formula: width * height * 3 / 2

**[Return Type]**

Returns 0 on success, -1 on failure

## sp_display_draw_rect  

**[Function Prototype]**

`int32_t sp_display_draw_rect(void *obj, int32_t x0, int32_t y0, int32_t x1, int32_t y1, int32_t flush, int32_t color, int32_t line_width)`

**[Function Description]**

Draws a rectangle on the graphics layer of the display module.

**[Parameters]**

- `obj`: Initialized `DISPLAY` object pointer
- `x0`: x value of the first coordinate of the rectangle
- `y0`: y value of the first coordinate of the rectangle
- `x1`: x value of the second coordinate of the rectangle
- `y1`: y value of the second coordinate of the rectangle
- `flush`: Whether to clear the current buffer of the graphics layer
- `color`: Color of the rectangle (color format is ARGB8888)
- `line_width`: Line width of the rectangle

**[Return Type]**

Returns 0 on success, -1 on failure

## sp_display_draw_string  

**[Function Prototype]**

`int32_t sp_display_draw_string(void *obj, int32_t x, int32_t y, char *str, int32_t flush, int32_t color, int32_t line_width)`

**[Function Description]**

Draws a string on the graphics layer of the display module.

**[Parameters]**
- `obj`: Initialized `DISPLAY` object pointer
- `x`: The x value of the starting coordinate for drawing the string
- `y`: The y value of the starting coordinate for drawing the string
- `str`: The string to be drawn (encoded in GB2312)
- `flush`: Whether to clear the current graphics layer buffer
- `color`: The color of the rectangle (in ARGB8888 format)
- `line_width`: The line width of the text

**【Return Type】** 

Returns 0 if successful, -1 if failed



## sp_get_display_resolution  

**【Function prototype】**  

`void sp_get_display_resolution(int32_t *width, int32_t *height)`

**【Function Description】**  

Gets the resolution of the current connected display.

**【Parameters】**

- `width`: The width of the resolution to be obtained
- `height`: The height of the resolution to be obtained

**【Return Type】** 

None

:::note

Currently only supports the `1920x1080@60Fps` format.

:::