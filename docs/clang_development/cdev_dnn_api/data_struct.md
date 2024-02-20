# Data Types and Data Structures

## Version Information Class

``HB_DNN_VERSION_MAJOR``


    #define HB_DNN_VERSION_MAJOR 1U

DNN major version number.

``HB_DNN_VERSION_MINOR``


    #define HB_DNN_VERSION_MINOR 1U

DNN minor version number.

``HB_DNN_VERSION_PATCH``



    #define HB_DNN_VERSION_PATCH 0U

DNN patch version number.

:::info Note

  Please note that the version numbers of the version information types in this section may vary with each release. The version numbers provided here are for reference only. Please refer to the release materials you have obtained for the actual version.
:::

## Model Class

``HB_DNN_TENSOR_MAX_DIMENSIONS``



    #define HB_DNN_TENSOR_MAX_DIMENSIONS 8

The maximum dimensions of a tensor are set to ``8``.

``HB_DNN_INITIALIZE_INFER_CTRL_PARAM``#define HB_DNN_INITIALIZE_INFER_CTRL_PARAM(param) \
    {                                                 \
        (param)->bpuCoreId = HB_BPU_CORE_ANY;         \
        (param)->dspCoreId = HB_DSP_CORE_ANY;         \
        (param)->priority = HB_DNN_PRIORITY_LOWEST;   \
        (param)->more = false;                        \
        (param)->customId = 0;                        \
        (param)->reserved1 = 0;                       \
        (param)->reserved2 = 0;                       \
    }

Initialize control parameters.

``hbPackedDNNHandle_t``

typedef void *hbPackedDNNHandle_t;

DNN handle, pointing to packed multiple models.

``hbDNNHandle_t``

typedef void *hbDNNHandle_t;

DNN handle, pointing to a single model.

``hbDNNTaskHandle_t``

typedef void *hbDNNTaskHandle_t;

Task handle, pointing to a task.

``hbDNNTensorLayout``

typedef enum {
  HB_DNN_LAYOUT_NHWC = 0,
  HB_DNN_LAYOUT_NCHW = 2,
  HB_DNN_LAYOUT_NONE = 255,
} hbDNNTensorLayout;

Layout of the tensor. "NHWC" stands for Number, Height, Width, and Channel.

+ Members| Member Name                   | Description                           |
|-------------------------------|---------------------------------------|
| ``HB_DNN_IMG_TYPE_Y``             | Tensor type for image with only Y channel.           |
| ``HB_DNN_IMG_TYPE_NV12``       | Tensor type for image in NV12 format.            |
| ``HB_DNN_IMG_TYPE_NV12_SEPARATE`` | Tensor type for image with separate Y and UV channels. |
| ``HB_DNN_IMG_TYPE_YUV444``        | Tensor type for image in YUV444 format.        |
| ``HB_DNN_IMG_TYPE_RGB``           | Tensor type for image in RGB format.           |
| ``HB_DNN_IMG_TYPE_BGR``           | Tensor type for image in BGR format.           |
| ``HB_DNN_TENSOR_TYPE_S4``         | Tensor type for signed 4-bit data.                |
| ``HB_DNN_TENSOR_TYPE_U4``         | Tensor type for unsigned 4-bit data.                || Member Name        | Description                                                 |
|--------------------|-------------------------------------------------------------|
| ``shiftLen``       | 移位数据的长度。                                            |
| ``shiftData``      | 存储移位数据的数组。                                        || Member Name    | Description          |
|----------------|----------------------|
| ``shiftLen``   | Length of shift data.   |
| ``shiftData``  | Address of shift data. |

``hbDNNQuantiScale``

    typedef struct {
      int32_t scaleLen;
      float *scaleData;
      int32_t zeroPointLen;
      int8_t *zeroPointData;
    } hbDNNQuantiScale;

Scaling data for quantization/dequantization.

**For input:** If the collected floating-point data is ``data[i]``, the corresponding scaling data is ``scale[i]``, and the zero-point offset data is ``zeroPoint[i]``, then the input inference data is: :math:`g((data[i] / scale[i]) + zeroPoint[i])`, where: :math:`g(x) = clip(nearbyint(x))`, rounded using fesetround(FE_TONEAREST) method, truncated to: U8: :math:`g(x)∈[0, 255]`, S8: :math:`g(x)∈[-128, 127]`;

**For output:** If the inference result is ``data[i]``, the corresponding scaling data is ``scale[i]``, and the zero-point offset data is ``zeroPoint[i]``, then the final inference result is: :math:`(data[i] - zeroPoint[i])* scale[i]`.

:::caution Caution

  The value of ``scaleLen`` is determined by the (de)quantization method of data ``data`` in a ``per-axis`` or ``per-tensor`` manner.
  When the data ``data`` is (de)quantized in a ``per-tensor`` manner, ``scaleLen`` is equal to ``1``, and the value of ``quantizeAxis`` is not important;
  otherwise, ``scaleLen`` is equal to the size of the ``quantizeAxis`` dimension of the data ``data``. ``zeroPointLen`` is the same as ``scaleLen``.
:::

+ Members

    | Member Name    | Description          |
    |----------------|----------------------|
    | ``scaleLen``   | Length of scaling data.   |
    | ``scaleData``  | Address of scaling data.  |
    | ``zeroPointLen``   | Length of zero-point offset data.  |
    | ``zeroPointData``  | Address of zero-point offset data. |

``hbDNNQuantiType``

    typedef enum {
      NONE, 
      SHIFT,
      SCALE,
    } hbDNNQuantiType;

Quantization/dequantization type for fixed-point floating-point conversion.
``NONE`` represents no need to process data; ``SHIFT`` type corresponds to quantization/dequantization parameters stored in the struct ``hbDNNQuantiShift``, ``SCALE`` corresponds to quantization/dequantization parameters stored in the struct ``hbDNNQuantiScale``.+ Members

    |Member             |Description         |
    |-------------------|--------------------|
    |``NONE``           |No quantization.    |
    |``SHIFT``          |Quantization type is ``SHIFT``.|
    |``SCALE``          |Quantization type is ``SCALE``.|

``hbDNNTensorProperties``

    typedef struct {
      hbDNNTensorShape validShape;
      hbDNNTensorShape alignedShape;
      int32_t tensorLayout;
      int32_t tensorType;
      hbDNNQuantiShift shift;
      hbDNNQuantiScale scale;
      hbDNNQuantiType quantiType;
      int32_t quantizeAxis;
      int32_t alignedByteSize;
      int32_t stride[HB_DNN_TENSOR_MAX_DIMENSIONS];
    } hbDNNTensorProperties;

Information of a tensor.

The ``alignedShape`` is the shape of the tensor after alignment, obtained from the model information.
After preparing the input data, the ``alignedShape`` needs to match the actual shape of the tensor input.

+ Members

    |Member             |Description         |
    |-------------------|--------------------|
    |``validShape``     |Shape of the valid content of the tensor.|
    |``alignedShape``   |Shape of the aligned content of the tensor.|
    |``tensorLayout``   |Layout of the tensor.|
    |``tensorType``     |Type of the tensor.|
    |``shift``          |Quantization shift.|
    |``scale``          |Quantization scale.|
    |``quantiType``     |Quantization type.|
    |``quantizeAxis``   |Quantization axis, only valid for per-axis quantization.|
    |``alignedByteSize``|Memory size of the aligned content of the tensor.|
    |``stride``         |Stride for each dimension of the tensor.

:::info Note

The tensor information obtained through the interface is required by the model. You can modify the corresponding tensor information based on the actual input, but currently only modifications to ``alignedShape`` and ``tensorType`` are allowed, and they must meet the requirements.

``alignedShape``:1. If you are preparing input based on "alignedShape", there is no need to modify "alignedShape".

2. If you are preparing input based on "validShape", you need to change "alignedShape" to "validShape", and the inference library will perform padding operations on the data.

"tensorType":

When inferring a model that takes NV12 input, you can modify the "tensorType" attribute of the tensor to "HB_DNN_IMG_TYPE_NV12" or "HB_DNN_IMG_TYPE_NV12_SEPARATE" based on actual situation.

"hbDNNTaskPriority":

typedef enum {
  HB_DNN_PRIORITY_LOWEST = 0,
  HB_DNN_PRIORITY_HIGHEST = 255,
  HB_DNN_PRIORITY_PREEMP = HB_DNN_PRIORITY_HIGHEST,
} hbDNNTaskPriority;

Task priority configuration, providing default parameters.

"hbDNNTensor":

typedef struct {
  hbSysMem sysMem[4];
  hbDNNTensorProperties properties;
} hbDNNTensor;

Tensor used to store input and output information. For "NV12_SEPARATE" type tensors, 2 "hbSysMem" are required, while others require 1.

+ Members

|Member Name     |Description       |
|-----------|----------------|
| "sysMem"      |     Memory to store the tensor.|
| "properties"  |     Information of the tensor.|

"hbDNNRoi":

typedef struct {
  int32_t left;
  int32_t top;
  int32_t right;
  int32_t bottom;
} hbDNNRoi;

Region of interest of a rectangle. :math:`W∈[left, right], H∈[top, bottom]`.

+ Members

|Member Name     |Description       || Member     | Description                           |
|------------|---------------------------------------|
| HB_BPU_CORE_ANY    | Any BPU core                          |
| HB_BPU_CORE_0      | BPU core 0                            |
| HB_BPU_CORE_1      | BPU core 1                            |

``hbDSPCore``

    typedef enum {
      HB_DSP_CORE_ANY = 0,
      HB_DSP_CORE_0 = (1 << 0),
      HB_DSP_CORE_1 = (1 << 1)
    } hbDSPCore;

DSP核枚举。

+ 成员

|成员名称     |描述       |
|-----------|----------------|
| HB_DSP_CORE_ANY    | 任一DSP核       |
| HB_DSP_CORE_0      | DSP核0       |
| HB_DSP_CORE_1      | DSP核1       || Member Name         | Description     |
|--------------------|----------------|
| ``HB_BPU_CORE_ANY`` | Any BPU core.  |
| ``HB_BPU_CORE_0``   | BPU core 0.    |
| ``HB_BPU_CORE_1``   | BPU core 1.    |

``hbDSPCore``

    typedef enum {
      HB_DSP_CORE_ANY = 0,
      HB_DSP_CORE_0 = (1 << 0),
      HB_DSP_CORE_1 = (1 << 1)
    } hbDSPCore;

Enumeration of DSP cores.

+ Members

| Member Name         | Description     |
|--------------------|----------------|
| ``HB_DSP_CORE_ANY`` | Any DSP core.  |
| ``HB_DSP_CORE_0``   | DSP core 0.    |
| ``HB_DSP_CORE_1``   | DSP core 1.    |

``hbSysMem``

    typedef struct {
      uint64_t phyAddr;
      void *virAddr;
      uint32_t memSize;
    } hbSysMem;

Structure for system memory, used for allocating system memory.

+ Members

| Member Name         | Description     |
|--------------------|----------------|
| ``phyAddr``         | Physical address.  |
| ``virAddr``         | Virtual address.  |
| ``memSize``         | Memory size.  |

``hbSysMemFlushFlag``

    typedef enum {
      HB_SYS_MEM_CACHE_INVALIDATE = 1,
      HB_SYS_MEM_CACHE_CLEAN = 2
    } hbSysMemFlushFlag;Synchronization parameters for system memory and cache. There is a cache between the CPU and memory, which can cause unsynchronized content between the cache and memory. In order to always get the latest data, we need to update the data in the cache from memory before CPU reading, and update the data in memory from the cache after CPU writing.

![hbSysMemFlushFlag](./image/cdev_dnn_api/hbSysMemFlushFlag.png)


+ Members

    |Member Name    |Description       |
    |-----------|----------------|
    | ``HB_SYS_MEM_CACHE_INVALIDATE``  | Synchronize the memory to the cache, used before CPU reading.     |
    | ``HB_SYS_MEM_CACHE_CLEAN``       | Synchronize the cache data to the memory, used after CPU writing. |

## Pre-processing Class


``HB_DNN_INITIALIZE_RESIZE_CTRL_PARAM``

    #define HB_DNN_INITIALIZE_RESIZE_CTRL_PARAM(param)     \
      {                                                     \
        (param)->bpuCoreId = HB_BPU_CORE_ANY;              \
        (param)->resizeType = HB_DNN_RESIZE_TYPE_BILINEAR; \
        (param)->priority = HB_DNN_PRIORITY_LOWEST;        \
        (param)->reserved1 = 0;                             \
        (param)->reserved2 = 0;                             \
        (param)->reserved3 = 0;                             \
        (param)->reserved4 = 0;                             \
      }

Initialize control parameters.

``hbDNNResizeType``

    typedef enum {
      HB_DNN_RESIZE_TYPE_BILINEAR = 0,
    } hbDNNResizeType;

``Resize`` type.

+ Members

    |Member Name     |Description       |
    |-----------|----------------|
    |``HB_DNN_RESIZE_TYPE_BILINEAR`` |  Resize type is bilinear interpolation.|

``hbDNNResizeCtrlParam``

    typedef struct {
      int32_t bpuCoreId;
      int32_t priority;
hbDNNResizeType resizeType;
      int32_t reserved1;
      int32_t reserved2;
      int32_t reserved3;
      int32_t reserved4;
    } hbDNNResizeCtrlParam;

Controls parameters of `Resize`.

+ Members

    |Member Name     |Description       |
    |-----------|----------------|
    |`bpuCoreId`  | BPU core ID.|
    |`priority`   | Task priority.|
    |`resizeType` | Resize type.|
    |`reserved1`  | Reserved field 1.|
    |`reserved2`  | Reserved field 2.|
    |`reserved3`  | Reserved field 3.|
    |`reserved4`  | Reserved field 4.|