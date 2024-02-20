sidebar_position: 6
---

# 7.6 Video Processing

## Overview
`VPS (Video Process System)` is a video processing system that supports image scaling, zooming, cropping, rotation, GDC correction, frame rate control, and pyramid image output.


## Function Description
### Basic Concepts
- Group

  The `VPS` provides the concept of groups to users, and each group time-sharing multiplexes the `IPU`, `GDC`, `PYM` hardware. Multiple `VPS groups` can be cascaded for use.

- Channel

  The channel of `VPS` represents an output of `VPS`. The output channels are mainly divided into ordinary image channels and pyramid image channels. The ordinary channel outputs the single-layer data after scaling, cropping, or rotating, and the pyramid channel outputs multi-layer pyramid scaled data.

### Function Description
![Func Description](./image/video_processing/ss_ch5_func_description.png)

The `VPS` can bind with other modules by calling the binding interface provided by [System Control](./system_control). The input can be bound with `VIN` and `VDEC` modules, and the output of `VPS` can be bound with `VOT` and `VENC` modules. The former is the input source of `VPS`, and the latter is the receiver of `VPS`. It can also be bound with another `VPS` to achieve more channels; support processing image data fed back by users. Users can manage `groups` through the `VPS` interface, each `group` can only bind with one input source, and each `channel` can bind with different modules. When `VPS` is bound with `VIN`, you need to call `HB_SYS_SetVINVPSMode` to configure the different modes between `VIN` and `VPS` online or offline.

![Func Description Topology](./image/video_processing/ss_ch5_func_description_topology.png)

The `VPS` hardware consists of one `IPU`, one `PYM`, and two `GDCs`. There are 7 output `channels` (chn0~chn6), chn0~chn4 can achieve downscales, chn5 can achieve upscale, chn0~chn5 can all achieve cropping (ROI), rotation, correction, and frame rate control, and chn6 is the pyramid online channel. The dashed box represents hardware reuse, and the gray blocks of `OSD` are CPU overlays, and the other three beige blocks are hardware overlays.
- Upscale Function:

  Size limitations are referred to in the table below

  Maximum 1.5x zoom in the horizontal direction, the width needs to be a multiple of 4, minimum 32x32, maximum 4096

  Maximum 1.5x zoom in the vertical direction, the height needs to be even, minimum 32x32, maximum 4096

  Only channel 5 supports upscale function

- Downscale Function:

  Size limitations are referred to in the table below

  Maximum 1/8 (greater than 1/8) reduction in the horizontal direction, minimum 32x32, maximum 4096

  Maximum 1/8 (greater than 1/8) reduction in the vertical direction, minimum 32x32, maximum 4096

  Channel 0 ~ channel 4 support downscale function

- The size limitations of each channel of the IPU are as follows:

| Scaler | FIFO (bytes) | Resolution (pixels) ||hb_err_t|HB_VPS_CreateGrp| (VPS_GRP_GRP grp_id, const VPS_GRP_ATTR_S* pstGrpAttr)|
|:-:|:-:|:-:|
|描述|创建VPS Group，并设置属性。|
|输入参数|grp_id|组ID，取值范围为0到[VPS_MAX_GRP_NUM-1]。|
||pstGrpAttr|指向VPS_GRP_ATTR_S结构体的指针，包含组的属性信息。|
|返回值|成功返回HB_SUCCESS，失败返回错误码。|```c
int HB_VPS_CreateGrp(int VpsGrp, const VPS_GRP_ATTR_S *grpAttr);
```

【Function Description】
> Create a VPS Group

【Parameter Description】

| Parameter Name | Description    | Input/Output |
| :------------: | :------------- | :----------: |
|     VpsGrp     | Group number   |    Input     |
|    grpAttr     | Group attribute pointer | Input |

【Return Value】

| Return Value | Description |
| :----------: | :---------- |
|      0       | Success |
|    Non-zero  | Failure |

【Notes】
> Up to 8 groups can be created in VPS; group attribute mainly includes the input width, height, and GDC buffer depth.

【Reference Code】
> VPS reference code

### HB_VPS_DestroyGrp
【Function Declaration】
```c
int HB_VPS_DestroyGrp(int VpsGrp);
```

【Function Description】
> Destroy a VPS Group

【Parameter Description】

| Parameter Name | Description    | Input/Output |
| :------------: | :------------- | :----------: |
|     VpsGrp     | Group number   |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | :---------- |
|      0       | Success |
|    Non-zero  | Failure |

【Notes】
> The group must have been created.【参考代码】
> No reference code

### HB_VPS_StartGrp
【Function Declaration】
```c
int HB_VPS_StartGrp(int VpsGrp);
```
【Function Description】
> Start VPS Group processing

【Parameter Description】

| Parameter Name | Description | Input/Output |
| :------------: | :---------- | :----------: |
|    VpsGrp      | Group number|    Input     |

【Return Value】

| Return Value | Description |
| :----------: | -----------:|
|      0       |    Success  |
|    Non-zero  |    Failure  |

【Note】
> The group must have been created

【参考代码】
> VPS reference code

### HB_VPS_StopGrp
【Function Declaration】
```c
int HB_VPS_StopGrp(int VpsGrp);
```
【Function Description】
> Stop VPS Group processing

【Parameter Description】

| Parameter Name | Description | Input/Output |
| :------------: | ----------- | :---------: |
|    VpsGrp      | Group number|

【Return Value】

| Return Value | Description |
| :----------: | -----------:|
|      0       |    Success  |
|    Non-zero  |    Failure  |【Note】
> The Group must have been created and already started.

【Reference Code】
> VPS Reference Code

### HB_VPS_GetGrpAttr
【Function Declaration】
```c
int HB_VPS_GetGrpAttr(int VpsGrp, VPS_GRP_ATTR_S *grpAttr);
```
【Function Description】
> Get the attributes of VPS Group.

【Parameter Description】

| Parameter Name | Description              | Input/Output |
| :------------: | :----------------------- | :----------: |
|    VpsGrp      | Group Number             |    Input     |
|    grpAttr     | Pointer to attribute struct |    Output    |

【Return Value】

| Return Value | Description |
| :----------: | ----------- |
|      0       | Success     |
|   Non-zero   | Failure     |

【Note】
> None

【Reference Code】
> None

### HB_VPS_SetGrpAttr
【Function Declaration】
```c
int HB_VPS_SetGrpAttr(int VpsGrp, const VPS_GRP_ATTR_S *grpAttr);
```
【Function Description】
> Set the attributes of VPS Group.

【Parameter Description】

| Parameter Name | Description              | Input/Output |
| :------------: | :----------------------- | :----------: |
|    VpsGrp      | Group Number             |    Input     |
|    grpAttr     | Pointer to attribute struct |    Input    |【Return Value】

| Return Value | Description |
| :----------: | ----------- |
|      0       | Success     |
|   Non-zero   | Failure     |

【Notes】

> No

【Reference Code】

> VPS Reference Code

### HB_VPS_SetGrpRotate
【Function Declaration】
```c
int HB_VPS_SetGrpRotate(int VpsGrp, ROTATION_E enRotation);
```
【Function Description】
> Set the rotation function for VPS Group, rotate all outputs of VPS

【Parameter Description】

|   Parameter Name   |  Description   | Input/Output |
| :----------------: | :------------ | :----------: |
|      VpsGrp        |   Group number |    Input     |
|    enRotation      |  Rotation parameter |   Input    |

【Return Value】

| Return Value | Description |
| :----------: | ----------- |
|      0       | Success     |
|   Non-zero   | Failure     |

【Notes】

> This interface needs to be called before HB_VPS_SetChnAttr, disable ChnRotate after enabling GroupRotate; isp binding ipu must be in offline mode

【Reference Code】

> VPS Reference Code

### HB_VPS_GetGrpRotate
【Function Declaration】
```c
int HB_VPS_GetGrpRotate(int VpsGrp, ROTATION_E *enRotation);
```
【Function Description】
> Get the rotation function property of VPS Group

【Parameter Description】int HB_VPS_SetGrpGdc(int VpsGrp, GDC_ATTR_S* pstGdcAttr);
```
【功能描述】
> 设置Gdc配置参数

【参数描述】

|  参数名称  |        描述       | 输入/输出 |
| :--------: | :--------------: | :-------: |
|   VpsGrp   |      Group号     |   输入    |
| pstGdcAttr | Gdc配置参数指针 |   输入    |

【返回值】

| 返回值 | 描述 |
| :----: | ---: |
|   0    | 成功 |
|  非0   | 失败 |

【注意事项】
> 无

【参考代码】
> 无int HB_VPS_SetGrpGdc(int VpsGrp, char* buf_addr, uint32_t buf_len, ROTATION_E enRotation)
```
【Function Description】
> Set the GDC correction function for VPS Group, so that all the outputs of VPS have correction effect.

【Parameter Description】

| Parameter Name | Description       | Input/Output |
| :-------------: | :---------------- | :----------: |
|    VpsGrp       | Group number      |    Input     |
|   buf_addr      | Correction file address |    Input     |
|   buf_len       | Correction file length |    Input     |
|  enRotation     | Rotation parameter |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | ----------: |
|       0      |   Success   |
|   Non-zero   |   Failure   |

【Note】
> This interface needs to be called before HB_VPS_SetChnAttr; For different lenses, different distortions, and different sizes, different correction bin files need to be passed in.

【Reference Code】
> VPS reference code

### HB_VPS_SendFrame
【Function Declaration】
```c
int HB_VPS_SendFrame(int VpsGrp, void* videoFrame, int ms);
```
【Function Description】
> Send data to VPS.

【Parameter Description】

| Parameter Name | Description                                                                                                                                                                                                  | Input/Output |
| :-------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------: |
|    VpsGrp       | Group number                                                                                                                                                                                                |    Input     |
|  videoFrame     | Image data pointer; VPS feedback data structure is hb_vio_buffer_t structure;                                                                                                                              |    Input     |
|       ms        | Timeout parameter ms set to -1 means blocking interface; 0 means non-blocking interface; greater than 0 means timeout waiting time, and the unit of timeout time is milliseconds (ms) |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | ----------: |
|       0      |   Success   |
|   Non-zero   |   Failure   |【Notice】
> None

【Reference Code】
> VPS reference code

### HB_VPS_SetChnAttr
【Function Declaration】
```c
int HB_VPS_SetChnAttr(int VpsGrp, int VpsChn, const VPS_CHN_ATTR_S *chnAttr);
```
【Function Description】
> Set the attributes of VPS channel (set the output size of a specific channel in IPU)

【Parameter Description】

| Parameter Name | Description       | Input/Output |
| :------------: | :---------------- | :----------: |
|     VpsGrp     | Group number      |    Input     |
|     VpsChn     | Channel number    |    Input     |
|    chnAttr     | Channel attribute |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | :---------: |
|      0       |   Success   |
|    Non-zero  |   Failure   |

【Notice】
> This interface supports dynamically configuring the output size of IPU. Dynamic configuration needs to call this interface after StartGrp. The new size for dynamic configuration cannot be larger than the initial configuration size. If you need to change from a smaller size to a larger size after starting, you need to call this interface twice before StartVps, passing the maximum size for the first time and the minimum size for the second time.

【Reference Code】
> VPS reference code

### HB_VPS_GetChnAttr
【Function Declaration】
```c
int HB_VPS_GetChnAttr(int VpsGrp, int VpsChn, VPS_CHN_ATTR_S *chnAttr);
```
【Function Description】
> Get the attributes of VPS channel

【Parameter Description】

| Parameter Name | Description       | Input/Output |
| :------------: | :---------------- | :----------: |
|     VpsGrp     | Group number      |    Input     |
|     VpsChn     | Channel number    |    Input     |
|    chnAttr     | Channel attribute |    Output    |【Return Value】

| Return Value | Description |
| :----------: | :---------: |
|      0       |  Successful |
|    Non-zero  |   Failed    |

【Notes】
> None

【Reference Code】
> None

### HB_VPS_EnableChn
【Function Declaration】
```c
int HB_VPS_EnableChn(int VpsGrp, int VpsChn);
```
【Function Description】
> Enable the VPS channel

【Parameter Description】

|  Parameter Name |   Description   |  Input/Output  |
| :-------------: | :-------------: | :------------: |
|     VpsGrp      |   Group number  |      Input     |
|     VpsChn      |   Channel number|      Input     |

【Return Value】

| Return Value | Description |
| :----------: | :---------: |
|      0       |  Successful |
|    Non-zero  |   Failed    |

【Notes】
> If the channel is not enabled, the GetChnFrame interface cannot obtain images.

【Reference Code】
> VPS reference code

### HB_VPS_DisableChn
【Function Declaration】
```c
int HB_VPS_DisableChn(int VpsGrp, int VpsChn);
```
【Function Description】
> Disable the VPS channel【函数声明】
```c
int HB_VPS_GetChnRotate(int VpsGrp, int VpsChn, ROTATION_E *penRotation);
```
【功能描述】
> 获取VPS通道图像固定角度旋转属性

【参数描述】

|  参数名称  |  描述    | 输入/输出 |
| :--------: | :------ | :-------: |
|   VpsGrp   | Group号  |   输入    |
|   VpsChn   | 通道号   |   输入    |
| penRotation | 旋转属性 |   输出    |

【返回值】

| 返回值 | 描述 |
| :----: | ---: |
|   0    | 成功 |
|  非0   | 失败 |

【注意事项】
> 无

【参考代码】
> VPS参考代码【Function Declaration】
```c
int HB_VPS_GetChnRotate(int VpsGrp, int VpsChn, ROTATION_E *enRotation);
```
【Function Description】
> Get the rotation property of the VPS channel image.

【Parameter Description】

|  Parameter Name | Description      | Input/Output |
| :-------------: | :--------------  | :----------: |
|    VpsGrp       | Group number     |    Input     |
|    VpsChn       | Channel number   |    Input     |
|  enRotation     | Rotation property|    Output    |

【Return Value】

| Return Value | Description |
| :----: | ---: |
|   0    | Success |
|  Non-zero  | Failure |

【Note】
> None

【Referenced Code】
> None

### HB_VPS_SetChnGdc
【Function Declaration】
```c
int HB_VPS_SetChnGdc(int VpsGrp, int VpsChn, char* buf_addr, uint32_t buf_len, ROTATION_E enRotation)
```
【Function Description】
> Set the GDC correction function for VPS channel.

【Parameter Description】

|  Parameter Name | Description         | Input/Output |
| :-------------: | :--------------     | :----------: |
|    VpsGrp       | Group number        |    Input     |
|    VpsChn       | Channel number      |    Input     |
|    buf_addr     | Correction file address |    Input     |
|    buf_len      | Correction file length  |    Input     |
|  enRotation     | Rotation parameter  |    Input     |

【Return Value】

| Return Value | Description |
| :----: | ---: |Please translate the Chinese parts in the following content into English, while keeping the original format and content:

| 0 | Success |
| Non-zero | Failed |

[Notes]
> This interface needs to be called after HB_VPS_SetChnAttr and supports up to two CHN corrections at the same time; different lenses, distortions, and sizes require different correction bin files to be passed in.

[Reference Code]
> VPS reference code

### HB_VPS_UpdateGdcSize
[Function Declaration]
```c
int HB_VPS_UpdateGdcSize(int VpsGrp, int VpsChn, uint16_t out_width, uint16_t out_height)
```
[Function Description]
> Set the VPS GDC correction output size (the GDC input and output sizes are normally the same, use this interface to change the GDC output size)

[Parameter Description]

| Parameter Name | Description | Input/Output |
| :--------: | :-------- | :-------: |
| VpsGrp | Group number | Input |
| VpsChn | Channel number | Input |
| out_width | Output width | Input |
| out_height | Output height | Input |

[Return Value]

| Return Value | Description |
| :----: | ---: |
| 0 | Success |
| Non-zero | Failed |

[Notes]
> This interface needs to be called after HB_VPS_SetChnGdc and HB_VPS_SetGrpGdc. The output size passed in needs to correspond to the correction bin file. The input size cannot be larger than the current GDC input size.

[Reference Code]
> Scene where the output size is inconsistent between the Group and GDC correction:
```c
    ret = HB_VPS_SetGrpGdc(grp_id, bin_buf, buf_len, degree);
    ret = HB_VPS_UpdateGdcSize(grp_id, 0, 1280, 720);
```
> Scene where the output size is inconsistent between the channel and GDC correction:
```c
    ret = HB_VPS_SetChnGdc(grp_id, chn_id, bin_buf, buf_len, degree);
    ret = HB_VPS_UpdateGdcSize(grp_id, 0, 1280, 720);
```

### HB_VPS_SetChnCrop
[Function Declaration]```c
int HB_VPS_SetChnCrop(int VpsGrp, int VpsChn, const VPS_CROP_INFO_S *cropInfo)
```
【Function Description】
> Set the cropping function of VPS Chn

【Parameter Description】

| Parameter Name | Description | Input/Output |
| :------------: | :--------- | :----------: |
|    VpsGrp      | Group number |   Input    |
|    VpsChn      | Channel number |   Input    |
|   cropInfo     | Cropping attribute |   Input    |

【Return Value】

|   Return Value   | Description |
| :--------------: | ----------: |
|        0         |  Success |
|       Non-zero       |  Failed |

【Notes】
> Need to be called after SetChnAttr; The ROI region passed in needs to be within the size range of the IPU input;

【Reference Code】
> VPS Reference Code

### HB_VPS_GetChnCrop
【Function Declaration】
```c
int HB_VPS_GetChnCrop(int VpsGrp, int VpsChn, VPS_CROP_INFO_S *cropInfo)
```
【Function Description】
> Get the fixed angle rotation of VPS Chn

【Parameter Description】

| Parameter Name | Description | Input/Output |
| :------------: | :--------- | :----------: |
|    VpsGrp      | Group number |   Input    |
|    VpsChn      | Channel number |   Input    |
|   cropInfo     | Cropping attribute |   Output    |

【Return Value】

|   Return Value   | Description |
| :--------------: | ----------: |
|        0         |  Success |
|       Non-zero       |  Failed |【注意事项】
> No

【参考代码】
> No

### HB_VPS_SetChnFrameRate
【Function Declaration】
```c
int HB_VPS_SetChnFrameRate(int VpsGrp, int VpsChn, FRAME_RATE_CTRL_S *frameRate)
```
【Description】
> Set the frame rate of the VPS channel.

【Parameter Description】

|   Parameter Name   | Description             | Input/Output |
| :----------------: | :---------------------- | :----------: |
|      VpsGrp        | Group number            |    Input     |
|      VpsChn        | Channel number          |    Input     |
| frameRate (struct) | Frame rate attribute    |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | ----------- |
|      0       | Success     |
|    Non-zero  | Failed      |

【注意事项】
> No

【参考代码】
> No

### HB_VPS_TriggerSnapFrame
【Function Declaration】
```c
int HB_VPS_TriggerSnapFrame(int VpsGrp, int VpsChn, uint32_t frameCnt)
```
【Description】
> Capture frames; mark frameCnt frames starting from the current frame.

【Parameter Description】

|  Parameter Name  | Description             | Input/Output |
| :--------------: | :---------------------- | :----------: |
|      VpsGrp      | Group number            |    Input     |
|      VpsChn      | Channel number          |    Input     |
|   frameCnt       | Number of captured frames|    Input     |【返回值】

| 返回值 | 描述     |
| :----: | -------: |
|   0    | Success |
|  Non-0 | Failure |

【注意事项】
> The function can only be called after initialization.

【参考代码】
> N/A

### HB_VPS_GetChnFrame
【函数声明】
```c
int HB_VPS_GetChnFrame(int VpsGrp, int VpsChn, void *videoFrame, int ms);
```
【功能描述】
> Get a processed image frame from the channel.

【参数描述】

|  参数名称  |                     描述                     | 输入/输出 |
| :--------: | :------------------------------------------: | :-------: |
|   VpsGrp   |                  Group number                |   Input   |
|   VpsChn   |                  Channel number              |   Input   |
| videoFrame |                 Image information             |   Output  |
|     ms     | Timeout parameter <br/>-1 for blocking interface;<br/>0 for non-blocking interface;<br/>larger than 0 for timeout waiting time in milliseconds (ms) |   Input   |

【返回值】

| 返回值 | 描述     |
| :----: | -------: |
|   0    | Success |
|  Non-0 | Failure |

【注意事项】
> The obtained image structure can be either a normal buffer structure (hb_vio_buffer_t) or a pyramid buffer structure (pym_buffer_t).

【参考代码】
> Reference code for VPS

### HB_VPS_GetChnFrame_Cond
【函数声明】
```c
int HB_VPS_GetChnFrame_Cond(int VpsGrp, int VpsChn, void *videoFrame, int ms, int time);
```
【功能描述】> Obtain a processed image frame from the channel if conditions are met.

【Parameter Description】

| Parameter Name | Description                                                                                                     | Input/Output |
| :------------: | :-------------------------------------------------------------------------------------------------------------- | :----------: |
|    VpsGrp      | Group number                                                                                                    |    Input     |
|    VpsChn      | Channel number                                                                                                  |    Input     |
|  videoFrame    | Image information                                                                                               |    Output    |
|       ms       | Timeout parameter <br/>When ms is set to -1, it is a blocking interface;<br/>When set to 0, it is a non-blocking interface;<br/>When greater than 0, it is the timeout waiting time in milliseconds (ms) |    Input     |
|      time      | Time condition: set to 0 to discard old frames starting from the current frame and wait for a new frame; other values are not supported        |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | :--------- |
|       0      | Success    |
|   Non-zero   | Failure    |

【Note】
> The obtained image structure is divided into normal BUF structure (hb_vio_buffer_t) and pyramid BUF structure (pym_buffer_t).

【Reference Code】
> VPS reference code

### HB_VPS_ReleaseChnFrame
【Function Declaration】
```c
int HB_VPS_ReleaseChnFrame(int VpsGrp, int VpsChn, void *videoFrame);
```
【Function Description】
> Release a frame of channel image.

【Parameter Description】

| Parameter Name | Description | Input/Output |
| :------------: | :------- | :--------: |
|      VpsGrp    | Group number |   Input    |
|     VpsChn     | Channel number |   Input    |
|   videoFrame   | Image information |   Input    |

【Return Value】

| Return Value | Description |
| :----------: | :--------- |
|       0      | Success    |
|   Non-zero   | Failure    |

【Note】
> None.【Reference Code】
> VPS reference code

### HB_VPS_SetPymChnAttr
【Function Declaration】
```c
int HB_VPS_SetPymChnAttr(int VpsGrp, int VpsChn, const VPS_PYM_CHN_ATTR_S *pymChnAttr);
```
【Function Description】
> Set pyramid channel attributes

【Parameter Description】

| Parameter Name | Description           | Input/Output |
| :------------: | :-------------------- | :----------: |
|    VpsGrp      | Group number          |    Input     |
|    VpsChn      | Channel number        |    Input     |
|  pymChnAttr    | Pyramid channel attributes pointer |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | ----------- |
|     0        | Success     |
|   Non-zero   | Failure     |

【Notes】
1) This interface supports dynamically configuring the output size of PYM roi layer. It needs to be called after StartGrp, and the new roi size configured dynamically cannot be larger than the size configured for the first initialization. If it is necessary to change from a smaller size to a larger size after startup, this interface needs to be called twice before StartVps, passing the maximum size the first time and the minimum size the second time.
2) This interface also supports dynamically configuring the input size of PYM, which is only valid during PYM feedback and supports changing the src size from large to small after StartGrp.

【Reference Code】
> VPS reference code

### HB_VPS_GetPymChnAttr
【Function Declaration】
```c
int HB_VPS_GetPymChnAttr(int VpsGrp, int VpsChn, VPS_PYM_CHN_ATTR_S *pymChnAttr);
```
【Function Description】
> Get pyramid channel attributes

【Parameter Description】

| Parameter Name | Description           | Input/Output |
| :------------: | :-------------------- | :----------: |
|    VpsGrp      | Group number          |    Input     |
|    VpsChn      | Channel number        |    Input     |
|  pymChnAttr    | Pyramid channel attributes pointer |    Output     |### HB_VPS_ChangePymUs
【Function Declaration】
```c
int HB_VPS_ChangePymUs(int VpsGrp, uint8_t us_num, uint8_t enable)
```
【Function Description】
> Enable or disable a certain layer of us in pym.

【Parameter Description】

| Parameter Name |  Description | Input/Output |
| :------: | ---------: | ---------: |
|  VpsGrp  |    Group number |       Input |
|  us_num  | Pyramid us layer |       Input |
|  enable  |     Is enable |       Input |

【Return Value】

| Return Value | Description |
| :----: | ---: |
|   0    | Success |

【Notes】
> None

【Reference Code】
> None

### HB_VPS_GetChnFd
【Function Declaration】
```c
int HB_VPS_GetChnFd(int VpsGrp, int VpsChn);
```
【Function Description】
> Get the device file descriptor corresponding to the VPS channel, and the obtained fd can be monitored by select. After select returns, the image can be directly obtained through the getChnFrame interface.

【Parameter Description】| Parameter Name | Description | Input/Output |
| :------------: | :--------- | :----------: |
|    VpsGrp     |   Group ID  |    Input     |
|    VpsChn     |  Channel ID |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | ---------: |
|   Positive   |   Success  |
|   Negative   |   Failure  |

【Notes】
> None

【Reference Code】
> None

### HB_VPS_CloseChnFd
【Function Declaration】
```c
int HB_VPS_CloseChnFd(void);
```
【Function Description】
> Close the fd of all channels in VPS.

【Parameter Description】
> None

【Return Value】

| Return Value | Description |
| :----------: | ---------: |
|      0       |   Success  |
|    Non-zero  |   Failure  |

【Notes】
> None

【Reference Code】
> None

### VPS Reference Code
```c
    grp_attr.maxW = 1280;
    grp_attr.maxH = 720;
    ret = HB_VPS_CreateGrp(grp_id, &grp_attr);

    grp_attr.maxW = 1920;
    grp_attr.maxH = 1080;
```ret = HB_VPS_SetGrpAttr(grp_id, &grp_attr);

ret = HB_VPS_SetGrpRotate(grp_id, ROTATION_90);
ret = HB_VPS_SetGrpGdc(grp_id, bin_buf, bin_len, ROTATION_90);
chn_attr.enScale = 1;
chn_attr.width = 1280;
chn_attr.height = 720;
chn_attr.frameDepth = 8;
ret = HB_VPS_SetChnAttr(grp_id, chn_id, &chn_attr);

chn_crop_info.en = 1;
chn_crop_info.cropRect.x = 0;
chn_crop_info.cropRect.y = 0;
chn_crop_info.cropRect.width = 1280;
chn_crop_info.cropRect.height = 720;
ret = HB_VPS_SetChnCrop(grp_id, chn_id, &chn_crop_info);

ret = HB_VPS_EnableChn(grp_id, chn_id);

ret = HB_VPS_SetChnRotate(grp_id, chn_id, ROTATION_90);

ret = HB_VPS_SetChnGdc(grp_id, chn_id, bin_buf, bin_len, ROTATION_90);

pym_chn_attr.timeout = 2000;
pym_chn_attr.ds_layer_en = 24;
pym_chn_attr.us_layer_en = 0;
pym_chn_attr.frame_id = 0;
pym_chn_attr.frameDepth = 8;
ret = HB_VPS_SetPymChnAttr(grp_id, pym_chn, &pym_chn_attr);

ret = HB_VPS_StartGrp(grp_id);

ret = HB_VPS_SendFrame(grp_id, feedback_buf, 1000);
ret = HB_VPS_GetChnFrame(grp_id, chn_id, &out_buf, 2000);
ret = HB_VPS_ReleaseChnFrame(grp_id, chn_id, &out_buf);
ret = HB_VPS_DisableChn(grp_id, chn_id);
ret = HB_VPS_StopGrp(grp_id);
ret = HB_VPS_DestroyGrp(grp_id);If only one module IPU is used, after creating the Group, you need to call HB_VPS_SetChnAttr. If multiple channels need to be output from IPU, then you need to call this interface multiple times.

![VPS GDC](./image/video_processing/ss_vps_gdc.png)

If only the GDC module is used, after creating the Group, you need to call HB_VPS_SetGrpGdc/Rotate interface.

![VPS PYM](./image/video_processing/ss_vps_pym.png)

If only the PYM module is used, after creating the Group, you need to call HB_VPS_SetPymChnAttr interface.

![VPS IPU_PYM](./image/video_processing/ss_vps_ipu_pym.png)

When IPU is the first module and PYM is the second module, after creating the Group, you need to call HB_VPS_SetChnAttr first and then call HB_VPS_SetPymChnAttr.

![VPS GDC_IPU](./image/video_processing/ss_vps_gdc_ipu.png)

When GDC comes before IPU, you need to call HB_VPS_SetGrpGdc/Rotate first and then call HB_VPS_SetChnAttr.

![VPS GDC_PYM](./image/video_processing/ss_vps_gdc_pym.png)

When GDC comes before PYM, you need to call HB_VPS_SetGrpGdc/Rotate first and then call HB_VPS_SetPymChnAttr.

![VPS IPU_GDC](./image/video_processing/ss_vps_ipu_gdc.png)

When IPU comes before GDC, you need to call HB_VPS_SetChnAttr first and then call HB_VPS_SetChnGdc/Rotate.

![VPS IPU_GDC_PYM](./image/video_processing/ss_vps_ipu_gdc_pym.png)

If IPU comes before GDC and then PYM, you need to call HB_VPS_SetChnAttr first, then call HB_VPS_SetChnGdc/Rotate, and finally call HB_VPS_SetPymChnAttr.

![VPS IPU_GDC+PYM](./image/video_processing/ss_vps_ipu_gdc+pym.png)

If multiple channels output from IPU need to be connected to GDC and PYM separately, then you need to call HB_VPS_SetChnAttr(chnA), HB_VPS_SetChnAttr(chnB), and then HB_VPS_SetChnGdc/Rotate(chnA), and finally HB_VPS_SetPymChnAttr(chnB).

![VPS IPU_GDC_PYM+GDC](./image/video_processing/ss_vps_ipu_gdc_pym+gdc.png)

You need to call HB_VPS_SetChnAttr(chnA), HB_VPS_SetChnAttr(chnB), then HB_VPS_SetChnGdc/Rotate(chnA), HB_VPS_SetChnGdc/Rotate(chnB), and finally HB_VPS_SetPymChnAttr(chnB).

![VPS IPU+GDC+PYM+GDC](./image/video_processing/ss_vps_ipu+gdc+pym+gdc.png)

You need to call HB_VPS_SetChnAttr(chnA), HB_VPS_SetChnAttr(chnB), HB_VPS_SetChnAttr(chnC), then HB_VPS_SetChnGdc/Rotate(chnA), HB_VPS_SetPymChnAttr(chnB), and HB_VPS_SetChnGdc/Rotate(chnC).

![VPS IPU_GDC_PYM_GDC](./image/video_processing/ss_vps_gdc_ipu_gdc_pym.png)

If all four modules in VPS need to be run together, you need to call HB_VPS_SetGrpGdc, HB_VPS_SetChnAttr(chnA), HB_VPS_SetChnRotate(chnA), and HB_VPS_SetPymChnAttr(chnA).

## Data Structure
### HB_VPS_GRP_ATTR_S
【Structure Definition】
```c```c
// Define the structure of VPS group attributes
typedef struct HB_VPS_GRP_ATTR_S {
    uint32_t    maxW;
    uint32_t    maxH;
    uint8_t     frameDepth;
    int         pixelFormat;
} VPS_GRP_ATTR_S;

【Function Description】
> Structure for VPS group attributes

【Member Description】
|   Member   |                        Description                        |
| :--------: | :-------------------------------------------------------: |
|    maxW    |               Maximum width of input image in VPS               |
|    maxH    |               Maximum height of input image in VPS             |
| frameDepth | Number of buffers allocated by Gdc. If VPS is bound with VOT, frameDepth should not be greater than 6. The actual number of input buffers for IAR is 8, and for GDC, it is frameDepth + 2. In IAR, the index sent by GDC (starting from 0) cannot be greater than or equal to 8. |
| pixelFormat |   Pixel format (VPS only supports nv12 format, current parameter reserved)   |

### HB_RECT_S
【Structure Definition】
```c
typedef struct HB_RECT_S {
    uint16_t    x;
    uint16_t    y;
    uint16_t    width;
    uint16_t    height;
} RECT_S;
```
【Function Description】
> Define a rectangular region

【Member Description】
|  Member  |  Description  |
| :------: | :-----------: |
|    x     | Starting x coordinate |
|    y     | Starting y coordinate |
|  width   |   Image width  |
|  height  |  Image height  |

### HB_VPS_CROP_INFO_S
【Structure Definition】
```c
typedef HB_VPS_CROP_INFO_S {
    bool        en;
    RECT_S      cropRect;
} VPS_CROP_INFO_S;
```
【Function Description】【Member Description】
|   Member   |                  Meaning                  |
| :--------: | :---------------------------------------: |
|    width   |           Width of the image output        |
|   height   |           Height of the image output       |

### HB_VPS_CHN_CROP_CFG_S
【Structure Definition】
```c
typedef struct HB_VPS_CHN_CROP_CFG_S {
    uint8_t             en;
    RECT_S              cropRect;
} VPS_CHN_CROP_CFG_S;
```
【Function Description】
> Structure for cropping configuration

【Member Description】
|   Member   |              Meaning               |
| :--------: | :---------------------------------: |
|     en     |     Whether cropping is enabled     |
|  cropRect  |         The area to be cropped      ||   new_height  |        高        |

### HB_VPS_SetChnCrop
【接口声明】
```c
int32_t HB_VPS_SetChnCrop(HB_VPS_CHN_ID_E channel,uint32_t x,uint32_t y,uint32_t width,uint32_t height,HB_ROTATION_E rotation);
```

【功能描述】
> 设置通道裁剪位置和尺寸

【参数说明】

|   参数    |                    含义                     |
| :-------: | :-----------------------------------------: |
|  channel  |               通道ID，枚举类型                |
|     x     |               裁剪起始横坐标                |
|     y     |               裁剪起始纵坐标                |
|   width   |                   裁剪宽度                  |
|  height   |                   裁剪高度                  |
| rotation  | 旋转角度，枚举类型（详情见HB_ROTATION_E说明） |

### HB_VPS_SetChnFrameRate
【接口声明】
```c
int32_t HB_VPS_SetChnFrameRate(HB_VPS_CHN_ID_E channel,uint32_t frame_rate);
```

【功能描述】
> 设置通道帧率

【参数说明】

|   参数    |       含义       |
| :-------: | :--------------: |
|  channel  |  通道ID，枚举类型 |
| frame_rate|     帧率值       ||       成员       |                含义                |
| :--------------: | :--------------------------------: |
|    frame_id     |              帧ID                 |
|   ds_uv_bypass   |         DS层YUV是否绕过          |
|    ds_layer_en   |            DS层使能位             |
|    us_layer_en   |           US层使能位              |
|   us_uv_bypass   |          US层YUV是否绕过          |
|     timeout      |              超时时间             |
|    frameDepth    |            帧深度设置            |
| dynamic_src_info |       动态源信息结构体            |
|  MAX_PYM_DS_NUM  |       DS层最大数目限制           |
|  MAX_PYM_US_NUM  |       US层最大数目限制           |
|    ds_info[]     |     DS层的金字塔缩放信息数组     |
|    us_info[]     |     US层的金字塔缩放信息数组     ||   Member   |      Meaning       |
| :--------: | :----------------: |
|  frame_id  |     Frame ID       |
| ds_uv_bypass |  DS layer UV bypass |
|  ds_layer_en  | DS layer enable levels (4~23) |
|  us_layer_en  | US layer enable levels (0~6)  |
| us_uv_bypass |  US layer UV bypass |
|  timeout   |     Timeout       |
| frameDepth |  Image queue length |
|   ds_info  |   DS scaling information |
|   us_info  |   US scaling information |

### HB_DIS_MV_INFO_S
【Structure Definition】
```c
typedef struct HB_DIS_MV_INFO_S {
    int    gmvX;
    int    gmvY;
    int    xUpdate;
    int    yUpdate;
} DIS_MV_INFO_S;
```
【Function Description】
> Offset information structure

【Member Description】

|   Member  |    Meaning    |
| :-------: | :-----------: |
|   gmvX    |  Horizontal offset value |
|   gmvY    |  Vertical offset value |
|  xUpdate  |     X update value   |
|  yUpdate  |     Y update value   |

## Error Codes

|     Error Code    |                  Macro Definition |            Description |
| :---------------: |:---------------------------------: | :--------------------- |
| -268,696,577 |      HB_ERR_VPS_INVALID_GROUPID |           Invalid group ID |
| -268,696,578 |               HB_ERR_VPS_BUFMGR |            Frame queue error |
| -268,696,579 |           HB_ERR_VPS_GROUP_FAIL |              Group failure |
| -268,696,580 |        HB_ERR_VPS_GROUP_UNEXIST |           Group does not exist |
| -268,696,581 |          HB_ERR_VPS_CHN_UNEXIST |            Channel does not exist |
| -268,696,582 |               HB_ERR_VPS_ROTATE |              Rotation failure |
| -268,696,583 |            HB_ERR_VPS_NULL_PARA |          Null parameter |
| -268,696,584 |              HB_ERR_VPS_BAD_ARG |           Invalid argument |
| -268,696,585 |          HB_ERR_VPS_UN_PREPARED |            Not ready |
| -268,696,586 |            HB_ERR_VPS_SENDFRAME |          Image injection failure |
| -268,696,587 |          HB_ERR_VPS_CHN_DISABLE |            Channel not enabled |
| -268,696,588 |               HB_ERR_VPS_TIMEOUT |             Timeout || -268,696,589 |   HB_ERR_VPS_CHN_FD | Failed to get channel file descriptor |
| -268,696,590 |   HB_ERR_VPS_SET_AFTER_START | Configuration not allowed after start |
| -268,696,591 |   HB_ERR_VPS_SET_BEFORE_START | Configuration not allowed before start |
| -268,696,592 |   HB_ERR_VPS_SET_AT_WRONG_TIME | Configuration not allowed at this time |
| -268,696,593 |   HB_ERR_VPS_UN_SUPPORT_SIZE | Unsupported size |
| -268,696,594 |   HB_ERR_VPS_FRAME_UNEXIST | Non-existent frame image |
| -268,696,595 |   HB_ERR_VPS_DEV_FRAME_DROP | Hardware frame drop |
| -268,696,596 |   HB_ERR_VPS_NOT_ENOUGH | Insufficient buffer frames |
| -268,696,597 |   HB_ERR_VPS_UN_SUPPORT_RATE | Unsupported frame rate |
| -268,696,598 |   HB_ERR_VPS_FRAME_RATE | Incorrect frame rate |

## Reference Code
For examples of VPS, please refer to [sample_vps](./multimedia_samples#sample_vps) and [sample_vps_zoom](./multimedia_samples#sample_vps_zoom).