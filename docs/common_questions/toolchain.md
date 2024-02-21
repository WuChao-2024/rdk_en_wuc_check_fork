---
sidebar_position: 4
---
# 10.4 Algorithm toolchain class

### Model quantization errors and solutions {#model_convert_errors_and_solutions}

#### hb_mapper checker (01_check.sh) model verification error

<font color='Blue'>[Problem]</font> 


```bash
  ERROR The shape of model input:input is [xxx] which has dimensions of 0. Please specify input-shape parameter. 
```

<font color='Green'>[Solution]</font> 


- The reason for this error may be that the model input has a dynamic shape. To solve this error, you can use the parameter ``--input-shape input_name input_shape`` to specify the shape information of the input node.

<font color='Blue'>[Problem]</font> 


```bash
  ERROR HorizonRT not support these cpu operators: {op_type}
```

<font color='Green'>[Solution]</font> 


- The reason for this error may be that the CPU operator used is not supported by Horizon. To solve this error, you can replace the operator according to the content in our provided operator support list; if the unsupported CPU operator is a core operator of the model, please contact Horizon for development evaluation.

<font color='Blue'>[Problem]</font> 


```bash
  Unsupported op {op_type} 
```

<font color='Green'>[Solution]</font> 


- The reason for this error may be that the BPU operator used is not supported by Horizon. To solve this error, if the overall performance of the model meets the requirements, you can ignore this log; if the overall performance of the model does not meet your expectations, you can replace the operator according to the content in our provided operator support list.<font color='Green'>【Answer】</font> 

- The reason for this error may be that the specified nodes '{op_type}' are not supported by official ONNX and are defined by yourself. Please check whether these ops are official ONNX ops or defined by yourself.

#### ERROR in hb_mapper makertbin (03_build.sh) model conversion

<font color='Blue'>【Issue】</font> 

  ```bash
  Layer {op_name}  
      xxx expect data shape range:[[xxx][xxx]], but the data shape is [xxx]
  Layer {op_name}
      Tensor xxx expects be n dimensions, but m provided
  ```

<font color='Green'>【Answer】</font> 

- The reason for this error may be that the {op_name} operator exceeds the support limit and falls back to CPU calculation. If the performance loss caused by CPU operators is acceptable to you, you don't need to pay attention to this information. If the performance does not meet your requirements, you can modify the op to a range supported by BPU according to the operator support list we provide.

<font color='Blue'>【Issue】</font> 

  ```bash
  INFO： Layer {op_name} will be executed on CPU
  ```

<font color='Green'>【Answer】</font> 

- The reason for this error may be that the {op_name} operator falls back to CPU calculation because the shape (CxHxW) exceeds 8192. If only a few operators are fallbacks to CPU calculation and the overall performance of the model meets the requirements, you don't need to pay attention to this information. If the performance does not meet the requirements, it is recommended to replace it with other BPU operators without shape restrictions according to the operator support list.

<font color='Blue'>【Issue】</font> 

  ```bash
  ERROR There is an error in pass: {op_name}. Error message:xxx
  ```

<font color='Green'>【Answer】</font> 

- The reason for this error may be that the optimization of the {op_name} operator fails. For this error, please collect the model and the .log file and provide them to the Horizon technical staff for analysis and processing.- 发生此错误的原因可能是在模型量化/编译过程中发生了core dump。针对此错误，建议您检查是否使用了正确的编译工具，并尝试使用其他编译器进行编译，或者检查输入数据是否合法。同时，可以尝试减少量化/编译的模型的大小，以避免core dump错误。- The reason for this error could be the failure of model quantization/compilation. For this error, please collect the model and .log files and provide them to Horizon technical staff for analysis and handling.

<font color='Blue'>[Question]</font> 


  ```bash
  ERROR model conversion faild: Inferred shape and existing shape differ in dimension x: (n) vs (m)
  ```

<font color='Green'>[Answer]</font> 


- The reason for this error could be the illegal input shape of the ONNX model or an error in the optimization pass of the tool. For this error, please ensure the validity of the ONNX model. If the ONNX model can infer normally, please provide the model to Horizon technical staff for analysis and handling.

<font color='Blue'>[Question]</font> 


  ```bash
  WARNING got unexpected input/output/sumin threshold on conv {op_name}! value: xxx
  ```

<font color='Green'>[Answer]</font> 


- The reason for this error could be an error in data preprocessing or the weight value of the node is too small/large. For this error, 1. please check if there is an error in data preprocessing; 2. we recommend you to use BN operator to optimize data distribution.

<font color='Blue'>[Question]</font> 


  ```bash
  ERROR hbdk-cc compile hbir model failed with returncode -n
  ```

<font color='Green'>[Answer]</font> 


- The reason for this error could be the failure of model compilation. For this error, please collect the model and .log files and provide them to Horizon technical staff for analysis and handling.

<font color='Blue'>[Question]</font> 


  ```bash
  ERROR {op_type}  only support 4 dim input
  ```

<font color='Green'>[Answer]</font> 


- The reason for this error could be that the toolchain does not currently support non-four-dimensional input for this op. For this error, we recommend you to adjust the input dimension of the op to four dimensions.```bash
  ERROR {op_type} does not support quantization/dequantization yet
  ```

<font color='Green'>【解答】</font> 


- 发生此错误的原因可能是某个算子暂时还不支持量化/去量化操作。针对此错误，我们建议您尝试使用其他算子替代或者等待更新版本进行支持。ERROR xxd_create_tensor failed
  ```
<font color='Green'>【解答】</font> 


- 发生此错误的原因可能是创建张量时发生了错误。请检查代码中创建张量的部分，确认是否有错误。<font color='Green'>【Answer】</font>

- The reason for this error may be that the toolchain version does not match. Please use the corresponding toolchain version in the SDK provided by us.

<font color='Green'>【Answer】</font>

- The reason for this error may be that the Docker is loaded incorrectly. We recommend using the nvidia Docker loading command when loading Docker.

<font color='Green'>【Answer】</font>

- The reason for this error may be that the onnx version does not match. Please export the onnx opset10 version again and use the opencv method for preprocessing.

<font color='Green'>【Answer】</font>

- The reason for this error may be a problem with onnxruntime itself. It cannot batch calibration and can only calibrate one image at a time because the reshape and batch dimensions in the model do not match, but it does not affect the result.

<font color='Green'>【Answer】</font>

- No quantifiable nodes were found, and the model is not supported.<font color='Green'>【Answer】</font> 


- The reason for this error may be that the model structure does not include the output nodes.


### Algorithm model on-board error and solution

<font color='Blue'>【Issue】</font> 


  ```bash
  (common.h:79): HR:ERROR: op_name:xxx invalid attr key xxx
  ```

<font color='Green'>【Answer】</font> 


- The reason for this error may be that libDNN does not support a certain attribute of this operator at the moment. For this error, you can replace it with the content in the operator support list we provided or contact Horizon for development evaluation.

<font color='Blue'>【Issue】</font> 


  ```bash
  (hb_dnn_ndarray.cpp:xxx): data type of ndarray do not match specified type. NDArray dtype_: n, given：m
  ```

<font color='Green'>【Answer】</font> 


- The reason for this error may be that libDNN does not support this input type at the moment (we will gradually move the operator constraints to the model conversion stage to remind). For this error, you can replace it with the content in the operator support list we provided or contact Horizon for development evaluation.

<font color='Blue'>【Issue】</font> 


  ```bash
  (validate_util.cpp:xxx)：tensor aligned shape size is xxx, but tensor hbSysMem memSize is xxx, tensor hbSysMem memSize should >= tensor aligned shape size!
  ```

<font color='Green'>【Answer】</font> 


- The reason for this error may be insufficient memory for the input data. For this error, please use hbDNNTensorProperties.alignedByteSize to allocate memory space.

<font color='Blue'>【Issue】</font> 


  ```bash
  (bpu_model_info.cpp:xxx): HR:ERROR: hbm model input feature names must be equal to graph node input names
```<font color='Green'>【Answer】</font> 


- Regarding this error, please update the latest version of the toolchain SDK development package.

### Model Quantization and On-board Usage Tips

#### Transformer Usage Instructions

This section will explain the concepts and parameters of each transformer, and provide usage examples for your reference, making it easier for you to perform transformer operations.

Before reading the document content, please pay attention to the following:

- The image data is "three-dimensional data", but the transformers provided by Horizon are obtained and processed in a "four-dimensional data" format. The transformer only performs this operation on the "first" image in the input data.

##### AddTransformer

**Description**:

Performs an operation of adding a value to every pixel in the input image. This transformer will convert the data format to float32 in the output.

**Parameters**:

- value: The value to be added to each pixel. Note that the value can be negative, such as -128.

**Usage example**:

``` bash
  # Perform subtracting 128 operation on the image data
  AddTransformer(-128)

  # Perform adding 127 operation on the image data
  AddTransformer(127)
```

##### MeanTransformer

**Description**:

Performs subtraction of mean_value on every pixel in the input image.

**Parameters**:

- means: The value to be subtracted from each pixel. Note that the value can be negative, such as -128.

- data_format: The input layout type, with a value range of ["CHW", "HWC"]. Default is "CHW".Translate the parts in Chinese to English while keeping the original format and content:

**Example usage**:

``` bash
  # Subtract 128.0 from each pixel. The input type is CHW.
  MeanTransformer(np.array([128.0, 128.0, 128.0])) 

  # Subtract different values from each pixel: 103.94, 116.78, 123.68. The input type is HWC.
  MeanTransformer(np.array([103.94, 116.78, 123.68]), data_format="HWC") 
```

##### ScaleTransformer

**Description**:

Scales all pixel values in the input image by multiplying data_scale.

**Parameters**:

- scale_value: The scale factor to be multiplied, such as 0.0078125 or 1/128.

**Example usage**:

```bash
  # Adjusts the pixel values in the range of -128 to 127 to the range of -1 to 1.
  ScaleTransformer(0.0078125) 
  # or
  ScaleTransformer(1/128)
```

##### NormalizeTransformer

**Description**:

Normalizes the input image. This transformer converts the data format to float32 during output.

**Parameters**:

- std: The value that needs to be divided by the first image.

**Example usage**:

``` bash
  # Adjusts the pixel values in the range of [-128, 127] to the range of -1 to 1.
  NormalizeTransformer(128) 
```

##### TransposeTransformer

**Description**:Transformation used for center cropping an image.

**Parameters**:

- size: The size of the output image after center cropping. 

**Usage example**:

``` bash
  # Center crop the image to size (224, 224)
  CenterCropTransformer((224, 224))
```

##### ResizeTransformer

**说明**：

Transformation used for resizing an image.

**Parameters**:

- size: The desired size of the output image after resizing, specified as (width, height).

**Usage example**:

``` bash
  # Resize the image to size (512, 512)
  ResizeTransformer((512, 512))
```

请注意，以上内容中的中文部分已经被我翻译成了英文，保留了原有的格式和内容。如需进一步的翻译服务，可以随时告诉我。# Operations to crop a square image of a specific size from the center of the image. The transformer will convert the data format to float32 in the output. When the value of data_type is uint8, the output will be uint8.

**Parameters**:
- crop_size: The edge length of the square to be cropped from the center.

- data_type: The type of the output result, with the value range ["float", "uint8"].

**Usage Examples**:
``` bash
# Crop from the center with a size of 224*224, and the default output type is float32
CenterCropTransformer(crop_size=224)

# Crop from the center with a size of 224*224, and the output type is uint8
CenterCropTransformer(crop_size=224, data_type="uint8")
```

##### PILCenterCropTransformer

**Description**:
This operation uses PIL to crop a square image from the center of the image. The transformer will convert the data format to float32 in the output.

**Parameters**:
- size: The edge length of the square to be cropped from the center.

**Usage Examples**:
``` bash
# Crop from the center with a size of 224*224, using PIL
PILCenterCropTransformer(size=224)
```

##### LongSideCropTransformer

**Description**:
Used for cropping the long side of an image. The transformer will convert the data format to float32 in the output.

When the width is greater than the height, it will crop a square image with the height as the basis, such as a width of 100 and a height of 70, resulting in a size of 70*70 after cropping.

When the height is greater than the width, it will crop a rectangle with the width unchanged and the height as half the difference plus the width, such as a width of 70 and a height of 100, resulting in a size of `70* (100-70) /2 +70`, which is a rectangle of size 70*85.

**Parameters**: None.

**Usage Examples**:
``` bashLongSideCropTransformer()

##### PadResizeTransformer

**Description**:

Performs image enlargement using padding. This transformer converts data format to float32 during output.

**Parameters**:

- target_size: The target size, specified as a tuple, e.g., (240, 240).

- pad_value: The value to pad the array with. Default value is 127.

- pad_position: The position to pad. Valid values are ["boundary", "bottom_right"]. Default value is "boundary".

**Example**:

``` bash
  # Crop an image of size 512*512, pad to the bottom right corner, pad value is 0
  PadResizeTransformer((512, 512), pad_position='bottom_right', pad_value=0)

  # Crop an image of size 608*608, pad to the border, pad value is 127
  PadResizeTransformer(target_size=(608, 608))
```

##### ResizeTransformer

**Description**:

Resize operation for adjusting image size.

**Parameters**:

- target_size: The target size, specified as a tuple, e.g., (240, 240).

- mode: Image processing mode. Valid values are ("skimage", "opencv"). Default value is "skimage".

- method: Interpolation method. This parameter is only effective when mode is "skimage". Valid values are 0-5. Default value is 1, where:

  - 0 represents Nearest-neighbor;
  
  - 1 represents Bi-linear (default);
  
  - 2 represents Bi-quadratic;
  
  - 3 represents Bi-cubic;
  
  - 4 represents Bi-quartic;- 5 represents Bi-quintic.

- data_type: The output type, with possible values (uint8, float), defaulting to float. When set to uint8, the output type is uint8, otherwise it is float32.

- interpolation: The interpolation method, this parameter is only effective when mode is set to "opencv". Default is empty, with possible values (interpolation methods in opencv). Currently, only two interpolation methods are supported: empty or "INTER_CUBIC" in opencv. When interpolation is empty, "INTER_LINEAR" method is used by default.

  Here are the interpolation methods supported in opencv, along with their explanations (unsupported methods will be gradually supported in future iterations):

  - INTER_NEAREST: Nearest neighbor interpolation.

  - INTER_LINEAR: Bilinear interpolation, used by default when interpolation is empty.

  - INTER_CUBIC: Bicubic interpolation within a 4x4 pixel neighborhood.

  - INTER_AREA: Resampling using pixel area relation. It may be the preferred method for image decimation, as it gives more moire'-free results. But when the image is zoomed, it is similar to the "INTER_NEAREST" method.

  - INTER_LANCZOS4: Lanczos interpolation over 8x8 neighborhood.

  - INTER_LINEAR_EXACT: Bit exact bilinear interpolation.

  - INTER_NEAREST_EXACT: Bit exact nearest neighbor interpolation. This will produce the same result as the nearest neighbor method in PIL, scikit-image or Matlab.

  - INTER_MAX: Mask for interpolation codes.

  - WARP_FILL_OUTLIERS: Flag, fills all the destination image pixels. If some of them correspond to outliers in the source image, they are set to zero.

  - WARP_INVERSE_MAP: Flag, inverse transformation.

**Usage example**:

``` bash
  # Resize input image to 224*224, process the image using opencv, use bilinear interpolation, output as float32
  ResizeTransformer(target_size=(224, 224), mode='opencv', method=1)

  # Resize input image to 256*256, process the image using skimage, use bilinear interpolation, output as float32
  ResizeTransformer(target_size=(256, 256))

  # Resize input image to 256*256, process the image using skimage, use bilinear interpolation, output as uint8
  ResizeTransformer(target_size=(256, 256), data_type="uint8")
```

##### PILResizeTransformer

**Explanation**:

Uses the PIL library to resize images.

**Parameters**:- size: The target size, represented as a tuple, e.g. (240,240).

- interpolation: Specifies the interpolation method, with options: (Image.NEAREST, Image.BILINEAR, Image.BICUBIC, Image.LANCZOS). The default value is Image.BILINEAR.

  - Image.NEAREST: Nearest neighbor sampling;
  
  - Image.BILINEAR: Bilinear interpolation;
  
  - Image.BICUBIC: Bicubic interpolation;
  
  - Image.LANCZOS: High-quality downsampling filter.

**Example usage**:

``` bash
  # Resize the input image to 256*256 using bilinear interpolation
  PILResizeTransformer(size=256)

  # Resize the input image to 256*256 using high-quality downsampling filter
  PILResizeTransformer(size=256, interpolation=Image.LANCZOS)
```

##### ShortLongResizeTransformer

**Explanation**:

Resizes the input image with respect to the original aspect ratio. The size of the new image depends on the specified parameters. The operation is performed as follows:

1. Divide the short_size by the minimum of the width and height of the original image to obtain a scaling factor.

2. If the scaling factor multiplied by the maximum of the width and height of the original image is larger than the long_size, the scaling factor is adjusted to the long_size divided by the maximum of the width and height of the original image.

3. Use the resize function in OpenCV to resize the image based on the calculated scaling factor.

**Parameters**:

- short_size: The desired length of the shorter side after cropping.

- long_size: The desired length of the longer side after cropping.

- include_im: The default value is True. When set to True, the function will return the processed image as well as the original image.

**Example usage**:

``` bash
  # Crop the image with a short side length of 20 and long side length of 100, and return the processed image along with the original image
  ShortLongResizeTransformer(short_size=20, long_size=100)
```##### PadTransformer

**Description**:

Resizes the image by dividing the target size value by the maximum value of the input image's width or height, and then multiplying this coefficient by the original width and height. After resizing the image, the new size is calculated by dividing it by the size divisor and then rounding up to the nearest integer. The final width and height are obtained by multiplying the result by the size divisor.

**Parameters**:

- size_divisor: Size divisor, default value is 128.

- target_size: Target size, default value is 512.

**Usage Example**:

``` bash
# Pad with size 1024*1024
PadTransformer(size_divisor=1024, target_size=1024)
```

##### ShortSideResizeTransformer

**Description**:

Crops the image to the desired size based on the length of the short side, using the ratio of the current long and short sides.

**Parameters**:

- short_size: Length of the desired short side.

- data_type: Output result type, valid values are "float" and "uint8". Default value is "float32". When set to "uint8", the output type will be uint8.

- interpolation: Specifies the interpolation method used in OpenCV, valid values are opencv interpolation methods. Default value is empty.
  
  Currently, interpolation only supports two interpolation methods: empty (default) or INTER_CUBIC from OpenCV.

  The following are the interpolation methods supported by OpenCV:

  - INTER_NEAREST: Nearest-neighbor interpolation.

  - INTER_LINEAR: Bilinear interpolation. This is the default method when interpolation is empty.

  - INTER_CUBIC: Bicubic interpolation using a 4x4 pixel neighborhood.

  - INTER_AREA: Resampling using pixel area relation. It may be the preferred method for image decimation, as it gives moire-free results. But when the image is zoomed, it is similar to the INTER_NEAREST method.

  - INTER_LANCZOS4: Lanczos interpolation over 8x8 neighborhood.

  - INTER_LINEAR_EXACT: Bit-accurate bilinear interpolation.- INTER_NEAREST_EXACT, exact nearest neighbor interpolation. This will produce the same result as the nearest neighbor method in PIL, scikit-image, or Matlab.

- INTER_MAX, mask for interpolation code.

- WARP_FILL_OUTLIERS, flag, fill all target image pixels. If some of them correspond to outliers in the source image, set them to zero.

- WARP_INVERSE_MAP, flag, inverse transformation.

**Example usage**:

``` bash
  # Resize the short side to 256, interpolation method is bilinear interpolation
  ShortSideResizeTransformer(short_size=256)

  # Resize the short side to 256, interpolation method is Lanczos interpolation within an 8x8 pixel neighborhood
  ShortSideResizeTransformer(short_size=256, interpolation=Image.LANCZOS4) 
```

##### PaddedCenterCropTransformer

**Description**:

Performs cropping on the center of the image using padding.

.. attention::

  Only applicable to EfficientNet-lite related instance models.

  Calculation method:

  1. Calculate the coefficient, int((float( image_size ) / ( image_size + crop_pad )).

  2. Calculate the size of the center, coefficient * np.minimum( original image height, original image width )).

  3. Crop the image based on the calculated size.

**Parameters**:

- image_size: size of the image, default value is 224.

- crop_pad: padding size for the center crop, default value is 32.

**Example usage**:

``` bash
  # Crop size is 240*240, padding value is 32
  PaddedCenterCropTransformer(image_size=240, crop_pad=32)

  # Crop size is 224*224, padding value is 32
  PaddedCenterCropTransformer()
```##### BGR2RGBTransformer

**Description**:

Transforms the input format from BGR to RGB.

**Parameters**:

- data_format: Data format, with possible values of (CHW, HWC), default is CHW.

**Usage example**:

``` bash
  # when the layout is NCHW, transform BGR to RGB
  BGR2RGBTransformer() 

  # when the layout is NHWC, transform BGR to RGB
  BGR2RGBTransformer(data_format="HWC")
```

##### RGB2BGRTransformer

**Description**:

Transforms the input format from RGB to BGR.

**Parameters**:

- data_format: Data format, with possible values of (CHW, HWC), default is CHW.

**Usage example**:

``` bash
  # when the layout is NCHW, transform RGB to BGR
  RGB2BGRTransformer() 

  # when the layout is NHWC, transform RGB to BGR
  RGB2BGRTransformer(data_format="HWC")
```

##### RGB2GRAYTransformer

**Description**:

Transforms the input format from RGB to GRAY.

**Parameters**:
- data_format: The type of input layout, with possible values of "CHW" and "HWC", defaulting to "CHW".

**Example**:

```bash
  # When the layout is NCHW, convert RGB to GRAY
  RGB2GRAYTransformer(data_format='CHW')

  # When the layout is NHWC, convert RGB to GRAY
  RGB2GRAYTransformer(data_format='HWC')
```

##### BGR2GRAYTransformer

**Description**:

Converts input format from BGR to GRAY.

**Parameters**:

- data_format: The type of input layout, with possible values of ["CHW","HWC"], defaulting to "CHW".

**Example**:

```bash
  # When the layout is NCHW, convert BGR to GRAY
  BGR2GRAYTransformer(data_format='CHW')

  # When the layout is NHWC, convert BGR to GRAY
  BGR2GRAYTransformer(data_format='HWC')
```

##### RGB2GRAY_128Transformer

**Description**:

Converts input format from RGB to GRAY_128. GRAY_128 has a value range of (-128, 127).

**Parameters**:

- data_format: The type of input layout, with possible values of ["CHW","HWC"]. This parameter is required.

**Example**:

```bash
  # When the layout is NCHW, convert RGB to GRAY_128
  RGB2GRAY_128Transformer(data_format='CHW')

  # When the layout is NHWC, convert RGB to GRAY_128
  RGB2GRAY_128Transformer(data_format='HWC')
```##### RGB2YUV444Transformer

**Description**:

Converts input format from RGB to YUV444.

**Parameters**:

- data_format: the layout type of the input, with possible values of ["CHW", "HWC"]. The default value is "CHW", and this is a required field.

**Example**:

``` bash
  # Convert BGR to YUV444 with layout as NCHW
  BGR2YUV444Transformer(data_format='CHW')

  # Convert BGR to YUV444 with layout as NHWC
  BGR2YUV444Transformer(data_format='HWC')
```

##### BGR2YUV444Transformer

**Description**:

Converts input format from BGR to YUV444.

**Parameters**:

- data_format: the layout type of the input, with possible values of ["CHW", "HWC"]. The default value is "CHW", and this is a required field.

**Example**:

``` bash
  # Convert BGR to YUV444 with layout as NCHW
  BGR2YUV444Transformer(data_format='CHW')

  # Convert BGR to YUV444 with layout as NHWC
  BGR2YUV444Transformer(data_format='HWC')
```

##### BGR2YUV444_128Transformer

**Description**:

Converts input format from BGR to YUV444_128. YUV444_128 has a range of (-128, 127).

**Parameters**:- data_format: The format of the input layout, with the options being ["CHW", "HWC"]. The default value is "CHW", and it is a required field.

**Example usage**:

``` bash
  # When the layout is NCHW, convert BGR to YUV444_128
  BGR2YUV444_128Transformer(data_format='CHW') 

  # When the layout is NHWC, convert BGR to YUV444_128
  BGR2YUV444_128Transformer(data_format='HWC')
```

##### RGB2YUV444_128Transformer

**Description**:

Converts the input format from RGB to YUV444_128. The range of YUV444_128 values is (-128, 127).

**Parameters**:

- data_format: The format of the input layout, with the options being ["CHW", "HWC"]. The default value is "CHW", and it is a required field.

**Example usage**:

``` bash
  # When the layout is NCHW, convert RGB to YUV444_128
  RGB2YUV444_128Transformer(data_format='CHW') 

  # When the layout is NHWC, convert RGB to YUV444_128
  RGB2YUV444_128Transformer(data_format='HWC')
```

##### BGR2YUVBT601VIDEOTransformer

**Description**:

Converts the input format from BGR to YUV_BT601_Video_Range.

YUV_BT601_Video_Range is a format used by some cameras, where the value range is 16~235. This transformer is used to adapt to this format of data.

**Parameters**:

- data_format: The format of the input layout, with the options being ["CHW", "HWC"]. The default value is "CHW", and it is a required field.

**Example usage**:

``` bash
  # When the layout is NCHW, convert BGR to YUV_BT601_Video_Range
  BGR2YUVBT601VIDEOTransformer(data_format='CHW')When the layout is NHWC, convert BGR to YUV_BT601_Video_Range
BGR2YUVBT601VIDEOTransformer(data_format='HWC')

##### RGB2YUVBT601VIDEOTransformer

**Description**:

Converts the input format from RGB to YUV_BT601_Video_Range.

YUV_BT601_Video_Range: Some camera input data is in YUV BT601 (Video Range) format, with a value range of 16~235. This transformer is used to adapt to this format.

**Parameters**:

- data_format: The input layout type, with possible values ["CHW", "HWC"]. Default value is "CHW". This parameter is mandatory.

**Examples**:

```bash
  # When the layout is NCHW, convert RGB to YUV_BT601_Video_Range
  RGB2YUVBT601VIDEOTransformer(data_format='CHW')

  # When the layout is NHWC, convert RGB to YUV_BT601_Video_Range
  RGB2YUVBT601VIDEOTransformer(data_format='HWC')
```

##### YUVTransformer

**Description**:

Converts the input format to YUV444.

**Parameters**:

- color_sequence: The color sequence. This parameter is mandatory.

**Examples**:

```bash
  # Convert BGR images to YUV444
  YUVTransformer(color_sequence="BGR")

  # Convert RGB images to YUV444
  YUVTransformer(color_sequence="RGB")
```

##### ReduceChannelTransformer

**Description**:
Reduce the C channel to a single channel operation. This transformer is mainly for the C channel, such as shape changes from 1*3*224*224 to 1*1*224*224. When using, the layout must be aligned with the data_format value to avoid deleting the wrong channel.

**Parameters**:

- data_format: The layout type of the input, with a value range of ["CHW", "HWC"], and a default value of "CHW".

**Usage example**:

``` bash  
  # Remove the C channel with layout NCHW
  ReduceChannelTransformer()
  # or
  ReduceChannelTransformer(data_format="CHW") 

  # Remove the C channel with layout NHWC
  ReduceChannelTransformer(data_format="HWC")
```

##### BGR2NV12Transformer

**Description**:

Convert the input format from BGR to NV12.

**Parameters**:

- data_format: The layout type of the input, with a value range of ["CHW", "HWC"], and a default value of "CHW".

- cvt_mode: The cvt mode, with a value range of (rgb_calc, opencv), and a default value of rgb_calc.

  - rgb_calc: Use the mergeUV method to process the images.

  - opencv: Use the opencv method to process the images.

**Usage example**:

``` bash
  # Convert from BGR to NV12 with layout NCHW, using the rgb_calc mode to process the images
  BGR2NV12Transformer()
  # or
  BGR2NV12Transformer(data_format="CHW") 

  # Convert from BGR to NV12 with layout NHWC, using the opencv mode to process the images
  BGR2NV12Transformer(data_format="HWC", cvt_mode="opencv")
```

##### RGB2NV12Transformer

**Description**：##### RGB2NV12Transformer

**Description**:

Convert the input format from RGB to NV12.

**Parameters**:

- data_format: The layout type of the input, options are ["CHW", "HWC"], default value is "CHW".

- cvt_mode: The conversion mode, options are (rgb_calc, opencv), default value is rgb_calc.

  - rgb_calc: Process the image using the mergeUV method.

  - opencv: Process the image using the OpenCV method.

**Usage example**:

``` bash
  # Convert RGB to NV12 with layout NCHW and process the image using rgb_calc mode
  RGB2NV12Transformer()
  # or
  RGB2NV12Transformer(data_format="CHW") 

  # Convert RGB to NV12 with layout NHWC and process the image using opencv mode
  RGB2NV12Transformer(data_format="HWC", cvt_mode="opencv")
```

##### NV12ToYUV444Transformer

**Description**:

Convert the input format from NV12 to YUV444.

**Parameters**:

- target_size: The target size, with a tuple value such as (240,240).
- yuv444_output_layout: The output layout of yuv444, options are (HWC, CHW), default value is "HWC".

**Usage example**:

``` bash
  # Convert NV12 to YUV444 with layout NCHW and size 768*768
  NV12ToYUV444Transformer(target_size=(768, 768))

  # Convert NV12 to YUV444 with layout NHWC and size 224*224
  NV12ToYUV444Transformer((224, 224), yuv444_output_layout="HWC") 
```

##### WarpAffineTransformer

**Description**:

Used to perform image affine transformations.**Parameters**:

- input_shape: The shape value of input.

- scale: The coefficient to multiply.

**Example of Usage**:

``` bash
  # The size is 512*512, and the length of the longest side is 1.0
  WarpAffineTransformer((512, 512), 1.0)
```

##### F32ToS8Transformer

**Description**: 

Used to convert the input format from float32 to int8.

**Parameters**: None.

**Example of Usage**:

``` bash
  # Convert the input format from float32 to int8 
  F32ToS8Transformer()
```

##### F32ToU8Transformer

**Description**: 

Used to convert the input format from float32 to uint8.

**Parameters**: None.

**Example of Usage**:

``` bash
  # Convert the input format from float32 to uint8 
  F32ToU8Transformer()
```

#### Instructions for Using YOLOv5x Model

1. YOLOv5x model:

  - You can download the corresponding pt file from URL:[yolov5-2.0](https://github.com/ultralytics/yolov5/releases/tag/v2.0).When cloning the code, please make sure you are using the ``v2.0`` tag, otherwise it will cause conversion failure.

-   md5sum codes:

|           **md5sum**             | **File**   |
| -------------------------------- | -----------|
| 2e296b5e31bf1e1b6b8ea4bf36153ea5 | yolov5l.pt |
| 16150e35f707a2f07e7528b89c032308 | yolov5m.pt |
| 42c681cf466c549ff5ecfe86bcc491a0 | yolov5s.pt |
| 069a6baa2a741dec8a2d44a9083b6d6e | yolov5x.pt |

-   To better adapt the post-processing code, we made the following modifications to the GitHub code before exporting the ONNX model
    (code can be found at: https://github.com/ultralytics/yolov5/blob/v2.0/models/yolo.py):

```python

    def forward(self, x):
        # x = x.copy()  # for profiling
        z = []  # inference output
        self.training |= self.export
        for i in range(self.nl):
            x[i] = self.m[i](x[i])  # conv
            bs, _, ny, nx = x[i].shape  # x(bs,255,20,20) to x(bs,3,20,20,85)
            #  x[i] = x[i].view(bs, self.na, self.no, ny, nx).permute(0, 1, 3, 4, 2).contiguous()
            x[i] = x[i].permute(0, 2, 3, 1).contiguous()
```

-   **Note:** 
      Removed the reshape from 4D to 5D at the end of each output branch (i.e., not splitting 255 channels into 3x85), and then outputted the layout from NHWC to NCHW.

    The left image shows the visualization of a certain output node of the model before modification, and the right image shows the visualization of the corresponding output node after modification.

    ![yolov5](./image/multimedia/yolov5.png)

-   After downloading, use the script https://github.com/ultralytics/yolov5/blob/v2.0/models/export.py to convert the pt file to the ONNX file.

-   **Points to note**

    When using the export.py script, please note:

    1. Since the ONNX opset versions supported by the Horizon AI toolchain are ``10`` and ``11``, please modify the ``opset_version`` parameter of ``torch.onnx.export`` according to the version you want to use.
    2. Change the default input name parameter of ``torch.onnx.export`` from ``'images'`` to ``'data'`` to match the example script of the YOLOv5x model conversion package.
    3. Change the default input size of 640x640 in the ``parser.add_argument`` section to 672x672 as shown in the example script of the YOLOv5x model conversion package.

#### Model accuracy optimization checklist{#checklist}

Please follow steps 1-5 in the following image to perform model accuracy verification and retain the code and results of each step:

Please verify the inference results of the floating-point ONNX model.

Enter the model conversion environment to test the inference results of the floating-point ONNX model (specifically the ONNX model exported from the DL framework) for a single image. The results of this step should be consistent with the inference results of the trained model (except for the nv12 format, which may introduce slight differences).

You can refer to the following example code steps to confirm whether the steps, data preprocessing, and post-processing code for the inference of the floating-point ONNX model are correct!

```python  
  from horizon_tc_ui import HB_ONNXRuntime
  import numpy as np
  import cv2

  def preprocess(input_name):
      # BGR->RGB, Resize, CenterCrop...
      # HWC->CHW
      # normalization
      return data

  def main(): 
      # Load the model file
      sess = HB_ONNXRuntime(model_file=MODEL_PATH)
      # Get the input & output node names
      input_names = [input.name for input in sess.get_inputs()]
      output_names = [output.name for output in sess.get_outputs()]
      # Prepare model input data
      feed_dict = dict()
      for input_name in input_names:
          feed_dict[input_name] = preprocess(input_name)
          
      # Original floating-point ONNX, data dtype=float32     
      outputs = sess.run_feature(output_names, feed_dict, input_offset=0)     
      
      # Post-processing
      postprocess(outputs)
          
  if __name__ == '__main__':
      main()
```

Verify the correctness of the yaml configuration file and the pre-processing and post-processing code.

Test the inference results of the "original_float.onnx" model for a single image, which should be consistent with the results of the inference of the floating-point ONNX model (except for the nv12 format, which may introduce slight differences).

Open the "original_float.onnx" model using the open-source tool Netron, and view the detailed properties of the "HzPreprocess" operator in the pre-processing node to obtain the parameters "data_format" and "input_type" needed for our "data preprocessing".Due to the presence of the HzPreprocess node, the pre-processing operations of the converted model may be different from the original model. This operator determines whether to add the HzPreprocess node to the model during the model conversion process based on the configuration parameters (input_type_rt, input_type_train, norm_type, mean_value, scale_value) in the yaml configuration file. For details on the generation of the pre-processing node, please refer to the "norm_type configuration parameter description" in the PTQ principle and step-by-step explanation chapter. In addition, the pre-processing node will appear in all artifacts generated during the conversion process.

Ideally, the HzPreprocess node should complete the full conversion from input_type_rt to input_type_train, but in reality, the entire type conversion process needs to be done using the Horizon AI chip hardware. However, the ONNX model does not include the hardware conversion part. Therefore, the real input type of ONNX will use an intermediate type, which is the result type of the hardware processing for input_type_rt. Therefore, for models with image input data types: RGB/BGR/NV12/YUV444/GRAY, and data dtype=uint8, the preprocessing code needs to perform "-128" operation, while the featuremap data type does not need to perform "-128" operation because it uses float32. The data layout (NCHW/NHWC) of the original_float.onnx will remain consistent with the input layout of the original floating-point model.

Please refer to the following example code steps to confirm whether the inference steps, data preprocessing, and post-processing code of the original_float.onnx model are correct!

**It is recommended to refer to the data preprocessing part using the Horizon model conversion "horizon_model_convert_sample" example package's caffe, onnx, and other example models' preprocessing steps method**

```python

  from horizon_tc_ui import HB_ONNXRuntime
  import numpy as np
  import cv2

  def preprocess(input_name):
      # BGR->RGB, Resize, CenterCrop...
      # HWC->CHW (determine whether layout conversion is needed based on the specific shape of the input node of the onnx model)
      # normalization (if the norm operation has been put into the model through the yaml file, no need to repeat it in the preprocessing code)
      #-128 (for models with image input, -128 needs to be performed after preprocessing when using the hb_session.run interface. For other interfaces, it can be controlled by input_offset)
      return data

  def main(): 
      # load the model file
      sess = HB_ONNXRuntime(model_file=MODEL_PATH)
      # get input & output node names
      input_names = [input.name for input in sess.get_inputs()]
      output_names = [output.name for output in sess.get_outputs()]
      # prepare model input data
      feed_dict = dict()
      for input_name in input_names:
          feed_dict[input_name] = preprocess(input_name)
      # for models with image input (RGB/BGR/NV12/YUV444/GRAY), data dtype=uint8
      outputs = sess.run(output_names, feed_dict, input_offset=128)
      # for featuremap models, data dtype=float32. If the model input is not a featuremap, please comment out the following line of code!
      outputs = sess.run_feature(output_names, feed_dict, input_offset=0)
      # post-processing
      postprocess(outputs)
          
  if __name__ == '__main__':
      main()

```

##### 3. Verify that no precision error is introduced in the graph optimization stage of the model

Test the single result of the optimize_float.onnx model, which should be exactly the same as the inference result of the original_float.onnx model.

Use the open source tool Netron to open the optimize_float.onnx model and view the detailed properties of the pre-processing node "HzPreprocess" operator to obtain the parameters needed for our data preprocessing: "data_format" and "input_type".

Please refer to the following example code steps to confirm whether the inference steps, data preprocessing, and post-processing code of the optimize_float.onnx model are correct!**Data preprocessing can refer to the preprocessing steps in the "horizon_model_convert_sample" example package, including the preprocessing steps for models in formats like Caffe and ONNX.**

```python

  from horizon_tc_ui import HB_ONNXRuntime
  import numpy as np
  import cv2

  def preprocess(input_name):
      # BGR->RGB, Resize, CenterCrop...
      # HWC->CHW (determine if layout conversion is needed based on the specific shape of the input node in the ONNX model)
      # normalization (if the norm operation has been included in the model through the yaml file, there is no need to repeat it in the preprocessing)
      #-128 (for image input models, -128 needs to be subtracted after the preprocessing only when using the hb_session.run interface, for other interfaces, input_offset can control this)
      return data

  def main(): 
      # Load the model file
      sess = HB_ONNXRuntime(model_file=MODEL_PATH)
      # Get the input and output node names
      input_names = [input.name for input in sess.get_inputs()]
      output_names = [output.name for output in sess.get_outputs()]
      # Prepare the model input data
      feed_dict = dict()
      for input_name in input_names:
          feed_dict[input_name] = preprocess(input_name)
      # For image input models (RGB/BGR/NV12/YUV444/GRAY), the data type should be uint8     
      outputs = sess.run(output_names, feed_dict, input_offset=128)         
      # For feature map models, the data type should be float32. If the input of the model is not a feature map, please comment out the line of code below!
      outputs = sess.run_feature(output_names, feed_dict, input_offset=0)     
      # Postprocessing
      postprocess(outputs)
          
  if __name__ == '__main__':
      main()

```

##### 4. Validate the quantization accuracy meets the expected requirements  

Test the accuracy of the quantized.onnx model.

Open the "quantized.onnx" model using the open-source tool Netron, and check the detailed properties of the preprocessing node "HzPreprocess" operator to obtain the parameters needed for our data preprocessing: "data_format" and "input_type";

Refer to the following example code steps to perform inference with the quantized.onnx model and confirm whether the inference steps, data preprocessing, and postprocessing code for the quantized.onnx model are correct!

**Data preprocessing can refer to the preprocess steps in the "horizon_model_convert_sample" example package, including the preprocessing steps for models in formats like Caffe and ONNX.**

```python

```from horizon_tc_ui import HB_ONNXRuntime
import numpy as np
import cv2

def preprocess(input_name):
    # BGR->RGB, Resize, CenterCrop...
    # HWC->CHW (determine whether layout conversion is needed based on the specific shape of input nodes)
    # normalization (if the norm operation has been included in the model through the yaml file, no need to repeat it in preprocessing)
    #-128 (for image input models, it is only necessary to perform -128 after preprocessing when using the hb_session.run interface, other interfaces can be controlled by input_offset)
    return data

def main():
    # load model file
    sess = HB_ONNXRuntime(model_file=MODEL_PATH)
    # get input and output node names
    input_names = [input.name for input in sess.get_inputs()]
    output_names = [output.name for output in sess.get_outputs()]
    # prepare model input data
    feed_dict = dict()
    for input_name in input_names:
        feed_dict[input_name] = preprocess(input_name)
    # models with image input (RGB/BGR/NV12/YUV444/GRAY), data type = uint8
    outputs = sess.run(output_names, feed_dict, input_offset=128)
    # feature map models, data type = float32, if the input of the model is not a feature map, please comment out the following line of code!
    outputs = sess.run_feature(output_names, feed_dict, input_offset=0)
    # post-processing
    postprocess(outputs)

if __name__ == '__main__':
    main()

```

##### 5. Ensure that the model compilation process is error-free and the inference code on the board is correct

Use the `hb_model_verifier` tool to verify the consistency between quantized.onnx and .bin. The model output should at least have alignment to 2-3 decimal places.

For how to use the hb_model_verifier tool, please refer to the section "hb_model_verifier tool" in the "PTQ Principle and Step-by-Step Explanation" chapter.

If the model consistency verification is passed, please carefully check the pre-processing and post-processing code on the board!

If the consistency verification of the quantized.onnx and .bin models fails, please contact Horizon technical support.

#### Model Quantization YAML Configuration File Template

##### RDK X3 Caffe Model Quantization YAML File Template {#rdk_x3_caffe_yaml_template}

Please create a file named `caffe_config.yaml` and copy the following content. Then, only fill in the parameters marked as **"required"** to perform model conversion. For more information on parameter usage, please refer to the chapter "Explanation of YAML Configuration File".

```python# Copyright (c) 2020 Horizon Robotics.All Rights Reserved.

# Parameters related to model conversion
model_parameters:

  # Required parameter
  # Caffe floating point network model file, for example: caffe_model: './horizon_x3_caffe.caffemodel'
  caffe_model: ''  

  # Required parameter
  # Caffe network description file, for example: prototxt: './horizon_x3_caffe.prototxt'
  prototxt: ''

  march: "bernoulli2"
  layer_out_dump: False
  working_dir: 'model_output'
  output_model_file_prefix: 'horizon_x3'

# Parameters related to model input
input_parameters:

  input_name: ""
  input_shape: ''
  input_type_rt: 'nv12'
  input_layout_rt: ''

  # Required parameter
  # Data type used for training in the original floating point model framework, optional values: rgb/bgr/gray/featuremap/yuv444, for example: input_type_train: 'bgr'
  input_type_train: ''

  # Required parameter
  # Data layout used for training in the original floating point model framework, optional values: NHWC/NCHW, for example: input_layout_train: 'NHWC'
  input_layout_train: ''

  #input_batch: 1
  
  # Required parameter   
  # Data preprocessing method used in the original floating point model framework, options: no_preprocess/data_mean/data_scale/data_mean_and_scale
  # no_preprocess: no operation is performed, mean_value and scale_value are not required to be configured
  # data_mean: subtract channel mean_value, mean_value needs to be configured and scale_value needs to be commented out
  # data_scale: multiply image pixels by data_scale coefficient, scale_value needs to be configured and mean_value needs to be commented out
  # data_mean_and_scale: subtract channel mean_value and then multiply by scale coefficient, mean_value and scale_value needs to be configured
  norm_type: ''

  # Required parameter
  # Mean value subtracted from the image, if it is channel mean value, values must be separated by spaces
  # For example: mean_value: 128.0 or mean_value: 111.0 109.0 118.0# Required Parameters
 # Image preprocessing scaling factor. If it is a channel scaling factor, values must be separated by spaces. Calculation formula: scale = 1/std
 # For example: scale_value: 0.0078125 or scale_value: 0.0078125 0.001215 0.003680
 scale_value: 

# Model quantization related parameters
calibration_parameters:

 # Required Parameters
 # Directory to store reference images for model quantization. Supported image formats are Jpeg, Bmp, etc. Generally, 100 images are selected from the test set to cover typical scenarios, avoiding obscure scenarios such as overexposure, saturation, blur, pure black, pure white, etc.
 # Please configure it based on the folder path in the 02_preprocess.sh script, such as: cal_data_dir: './calibration_data_yuv_f32'
 cal_data_dir: ''

 cal_data_type: 'float32'
 calibration_type: 'default'
 # max_percentile: 0.99996

# Compiler related parameters
compiler_parameters:

 compile_mode: 'latency'
 debug: False
 # core_num: 2
 optimize_level: 'O3'

```

##### RDK X3 ONNX Model Quantization YAML File Template{#rdk_x3_onnx_yaml_template}

Please create a new file named onnx_config.yaml, then copy the following content directly. You only need to fill in the parameters marked as **"Required Parameters"** to perform model conversion. If you need to learn more about the usage of other parameters, please refer to the [yaml configuration file details](../toolchain_development/intermediate/ptq_process#yaml_config) section.

```python

# Copyright (c) 2020 Horizon Robotics.All Rights Reserved.

# Model conversion parameters
model_parameters:

 # Required Parameters
 # Onnx floating-point network data model file, for example: onnx_model: './horizon_x3_onnx.onnx'
 onnx_model: ''

 bernoulli2
 layer_out_dump: False
 working_dir: 'model_output'
 output_model_file_prefix: 'horizon_x3'

# Model input parameters
input_parameters:input_name: ""
  input_shape: ''
  input_type_rt: 'nv12'
  input_layout_rt: ''

  # Required parameter
  # The data type used in the original floating-point model training framework, optional values are rgb/bgr/gray/featuremap/yuv444, for example: input_type_train: 'bgr'
  input_type_train: ''

  # Required parameter
  # The data layout used in the original floating-point model training framework, optional values are NHWC/NCHW, for example: input_layout_train: 'NHWC'
  input_layout_train: ''

  #input_batch: 1
  
  # Required parameter  
  # The data preprocessing method used in the original floating-point model training framework, can be configured as: no_preprocess/data_mean/data_scale/data_mean_and_scale
  # no_preprocess: No operation is performed, mean_value or scale_value do not need to be configured
  # data_mean: Subtract the channel mean value mean_value, mean_value needs to be configured and scale_value needs to be commented out
  # data_scale: Multiply the image pixels by the data_scale factor, scale_value needs to be configured and mean_value needs to be commented out
  # data_mean_and_scale: Subtract the channel mean value and then multiply by the scale factor, mean_value and scale_value below need to be configured
  norm_type: ''

  # Required parameter
  # The mean value subtracted from the image, if it is the channel mean value, the values must be separated by spaces
  # For example: mean_value: 128.0 or mean_value: 111.0 109.0 118.0 
  mean_value: 

  # Required parameter
  # The scaling factor for image preprocessing, if it is the channel scaling factor, the values must be separated by spaces, calculation formula: scale = 1/std
  # For example: scale_value: 0.0078125 or scale_value: 0.0078125 0.001215 0.003680
  scale_value: 

# Model quantization related parameters
calibration_parameters:

  # Required parameter
  # The directory for storing reference images for model quantization, the supported image formats are Jpeg, Bmp, etc., 
  # The images usually come from selecting 100 images from the test set and covering typical scenarios, avoiding remote scenarios such as overexposure, saturation, blur, pure black, pure white, etc.
  # Please configure according to the folder path in the 02_preprocess.sh script, for example: cal_data_dir: './calibration_data_yuv_f32'
  cal_data_dir: ''

  cal_data_type: 'float32'
  calibration_type: 'default'
  # max_percentile: 0.99996

# Compiler related parameters
compiler_parameters:

  compile_mode: 'latency'
  debug: False# core_num: 2
  optimize_level: 'O3'

```

##### RDK Ultra Caffe Model Quantization YAML File Template{#rdk_ultra_caffe_yaml_template}

Please create a new file named `caffe_config.yaml` and directly copy the following content. Then, you only need to fill in the parameters marked as **``Required Parameters``** to perform model conversion. If you need to learn more about the usage of parameters, please refer to the chapter [YAML Configuration File Explanation](../toolchain_development/intermediate/ptq_process#yaml_config).

```python

# Copyright (c) 2020 Horizon Robotics.All Rights Reserved.

# Model conversion related parameters
model_parameters:

  # Required Parameters
  # Caffe floating-point network model file, e.g., caffe_model: './horizon_ultra_caffe.caffemodel'
  caffe_model: ''  

  # Required Parameters
  # Caffe network description file, e.g., prototxt: './horizon_ultra_caffe.prototxt'
  prototxt: ''

  march: "bayes"
  layer_out_dump: False
  working_dir: 'model_output'
  output_model_file_prefix: 'horizon_ultra'

# Model input related parameters
input_parameters:

  input_name: ""
  input_shape: ''
  input_type_rt: 'nv12'
  input_layout_rt: ''

  # Required Parameters
  # Data type used in the original floating-point model training framework, the optional values are rgb/bgr/gray/featuremap/yuv444, e.g., input_type_train: 'bgr'
  input_type_train: ''

  # Required Parameters
  # Data layout used in the original floating-point model training framework, the optional values are NHWC/NCHW, e.g., input_layout_train: 'NHWC'
  input_layout_train: ''

  #input_batch: 1
  
  # Required Parameters  
  # Data preprocessing method used in the original floating-point model training framework, can be configured as: no_preprocess/data_mean/data_scale/data_mean_and_scale
  # no_preprocess does not perform any operations, and mean_value or scale_value do not need to be configured
```# data_mean Subtract the channel mean value mean_value, the corresponding mean_value needs to be configured and commented out scale_value
  # data_scale Multiply the image pixels by the data_scale factor, the corresponding scale_value needs to be configured and commented out mean_value
  # data_mean_and_scale Subtract the channel mean value and multiply by the scale factor, indicating that the mean_value and scale_value below need to be configured
  norm_type: ''

  # Required parameters
  # Mean value subtracted from the image, if it is a channel mean value, the values must be separated by spaces
  # For example: mean_value: 128.0 or mean_value: 111.0 109.0 118.0
  mean_value:

  # Required parameters
  # Image preprocessing scaling factor, if it is a channel scaling factor, the values must be separated by spaces, formula: scale = 1/std
  # For example: scale_value: 0.0078125 or scale_value: 0.0078125 0.001215 0.003680
  scale_value: 

# Model quantization related parameters
calibration_parameters:

  # Required parameters
  # The directory where the reference images for model quantization are stored. The image formats support Jpeg, Bmp, etc. The images are generally selected from the test set, covering typical scenarios, and should not be remote scenes, such as overexposure, saturation, blur, pure black, pure white and other images
  # Please configure according to the folder path in the 02_preprocess.sh script, for example: cal_data_dir: './calibration_data_yuv_f32'
  cal_data_dir: ''

  cal_data_type: 'float32'
  calibration_type: 'default'
  # max_percentile: 0.99996

# Compiler related parameters
compiler_parameters:

  compile_mode: 'latency'
  debug: False
  # core_num: 2
  optimize_level: 'O3'

```

##### RDK Ultra ONNX model quantization yaml file template {#rdk_ultra_onnx_yaml_template}

Please create a new onnx_config.yaml file and simply copy the following content. Then you only need to fill in the parameters marked as **``Required parameters``** to perform the model conversion. If you want to learn more about the use of other parameters, please refer to [yaml configuration file interpretation](../toolchain_development/intermediate/ptq_process#yaml_config) chapter.

```python

# Copyright (c) 2020 Horizon Robotics.All Rights Reserved.

# Parameters related to model conversion
model_parameters:

  # Required parameters
  # Onnx floating point network data model file, for example: onnx_model: './horizon_ultra_onnx.onnx'onnx_model: ''

march: "bayes"
layer_out_dump: False
working_dir: 'model_output'
output_model_file_prefix: 'horizon_ultra'

# Model input parameters
input_parameters:

  input_name: ""
  input_shape: ''
  input_type_rt: 'nv12'
  input_layout_rt: ''

  # Required parameter
  # Data type used for training in the original floating point model framework, possible values are rgb/bgr/gray/featuremap/yuv444, for example: input_type_train: 'bgr'
  input_type_train: ''

  # Required parameter
  # Data layout used for training in the original floating point model framework, possible values are NHWC/NCHW, for example: input_layout_train: 'NHWC'
  input_layout_train: ''

  #input_batch: 1
  
  # Required parameter  
  # Data preprocessing method used in the original floating point model framework, can be configured as: no_preprocess/data_mean/data_scale/data_mean_and_scale
  # no_preprocess: no operation is performed, mean_value or scale_value do not need to be configured
  # data_mean: subtract channel mean_value, mean_value needs to be configured and scale_value needs to be commented out
  # data_scale: multiply image pixels by data_scale coefficient, scale_value needs to be configured and mean_value needs to be commented out
  # data_mean_and_scale: subtract channel mean_value and multiply by scale coefficient, mean_value and scale_value both need to be configured
  norm_type: ''

  # Required parameter
  # Mean value subtracted from the image, if it is channel mean, values must be separated by spaces
  # For example: mean_value: 128.0 or mean_value: 111.0 109.0 118.0 
  mean_value: 

  # Required parameter
  # Scale factor for image preprocessing, if it is channel scale factor, values must be separated by spaces, calculation formula: scale = 1/std
  # For example: scale_value: 0.0078125 or scale_value: 0.0078125 0.001215 0.003680
  scale_value: 

# Model quantization parameters
calibration_parameters:

  # Required parameter
  # Directory where reference images for model quantization are stored, image formats supported are Jpeg, Bmp, etc. The images are usually selected from the test set, covering typical scenes, not remote scenes such as overexposure, saturation, blurriness, pure black, pure white, etc.
  # Please configure it according to the folder path in the 02_preprocess.sh script, for example: cal_data_dir: './calibration_data_yuv_f32'
  cal_data_dir: ''cal_data_type: 'float32'
  calibration_type: 'default'
  # max_percentile: 0.99996

# Compiler related parameters
compiler_parameters:

  compile_mode: 'latency'
  debug: False
  # core_num: 2
  optimize_level: 'O3'

```

#### X3 Multi-core BPU Usage Instructions

Because there are 2 BPU cores in X3, there are single-core model and dual-core model scenarios in BPU usage. Please refer to the document [Tips and Suggestions for Reasonable Use of X3 Multi-core BPU](https://developer.horizon.ai/forumDetail/136488103547258549) for notes on using the multi-core BPU.

#### Fixed-point .bin Model Usage Instructions on the Board with Multiple Batches

- 1. When converting models, configure the batch_size through the input_batch in the YAML configuration file;
- 2. When inputting the bin model on the board, assuming the original model has a dimension of 1x3x224x224, modify the input_batch to 10, that is, using the dimension of 10x3x224x224 as an example:
- Prepare data:

    Image data: Set "aligned_shape = valid_shape", and then prepare the 10 images one by one in the order by writing them into the allocated memory space;

    FeatureMap data: Pad the data according to aligned_shape, and then prepare the 10 sets of data one by one in the order by writing them into the allocated memory space. The model inference process is consistent with that of the single-batch model.