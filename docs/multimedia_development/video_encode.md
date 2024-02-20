# 7.9 Video Encoding
## Overview
The video encoding module implements hardware encoding protocols such as H.264/H.265/JPEG/MJPEG. This module supports real-time encoding of multiple channels, with each channel being independent. Common use cases include single-channel recording, multi-channel recording, single-channel VIO video streaming, multi-channel VIO video streaming, recording + VIO video streaming, etc.

## Function Description

### Basic Specifications

The encoding specifications supported by X3 are as follows:

![image-20220329224946556](./image/video_encode/image-20220329224946556.png)

H.264/H.265 protocol encoding performance is as follows:

- H.264 decoding supports a maximum resolution of 8192 x 8192, with a minimum resolution of 256 x 128, and a minimum decoding resolution of 32 x 32.
- H.265 decoding supports a maximum resolution of 8192 x 8192, with a minimum resolution of 256 x 128, and a minimum decoding resolution of 8 x 8.
- The stride of H.264/H.265 is aligned to 32 bytes, while the width and height are aligned to 8 bytes. If they are not aligned, it is recommended to use VIDEO_CROP_INFO_S to perform corresponding cropping.
- Both H.264/H.265 have real-time multi-stream encoding capabilities.
- The highest capability supports 4K@60fps.
- ROI encoding with QP map (allows users to select regions of interest in the picture, after enabling ROI function, important or moving regions will be encoded with high-quality lossless coding, while the bitrate and image quality of regions that do not move or are not selected will be reduced, achieving standard definition video compression, or even not transmitting this part of the video)
- Supports rotation and mirroring.
- Multi-instance processing, up to 32 instances.

JPEG protocol encoding capabilities are as follows:
- Encoding and decoding resolution range from 16 x 16 to 32768 x 32768.
- MJPEG and JPEG stride are aligned to 32 bytes, width is aligned to 16 bytes, and height is aligned to 8 bytes.
- For YUV 4:2:0 format (e.g. NV12), the highest capability is 4K@30fps.
- JPEG Baseline and Extended sequential ISO/IEC 10918-1.
- Supports one or three color components, each component can have 8-bit or 12-bit sampling.
- Supports YUV 4:0:0, 4:2:0, 4:2:2, 4:4:0, and 4:4:4 color formats.
- Supports encoding and decoding ROI.
- Supports slice encoding.
- Supports rotation and mirroring.
- Multi-instance, with a maximum support of 64 instances.

### Encoding and Decoding Channels
An encoding and decoding channel refers to a specific type of encoding and decoding instance. The user parameters, configuration, and resources of different encoding and decoding channels can be independent of each other, allowing for multiple channels of video encoding and decoding with different specifications to cover various business scenarios.

### Bitrate Control
Bitrate control mainly refers to the control of encoding bitrate. Bitrate control is for continuous video encoding streams, and for a changing scene, if you want to achieve stable image quality, the encoding bitrate will fluctuate. If you want to achieve stable encoding bitrate, the image quality will fluctuate. X3 supports the following bitrate control methods for H.264, H.265, and MJPEG protocols:

- H.264/H.265 supports CBR, VBR, AVBR, FixQp, and QpMap five types of bitrate control modes for encoding channels.
- MJPEG encoding channel supports FixQp bitrate control mode.

CBR can ensure a stable overall encoding bitrate.

VBR ensures a stable image quality during encoding.AVBR considers both bitrate and image quality, generating a bitrate and image quality relatively stable bitstream;

FixQp fixes the QP value for each I frame, P frame, and B frame;

QPMAP assigns a QP value for each block in a frame, where the block size is 16x16 for H264 and 32x32 for H265.

For CBR and AVBR, the encoder internally finds a suitable QP value for each frame image to ensure a constant bitrate.

The encoder supports three levels of rate control internally, which are frame level, CTU/MB level, and subCTU/subMB level. The frame level control mainly generates a QP value for each frame image based on the target bitrate to ensure a constant bitrate; the CTU/MB level control generates a QP value for each block based on the target bitrate of each 64x64 CTU or 16x16 MB, which can achieve better bitrate control, but frequent QP value adjustments may cause unstable image quality; the subCTU/subMB level control generates a QP value for each 32x32 subCTU or 8x8 subMB, with complex blocks receiving higher QP values and static blocks receiving lower QP values, because the human eye is more sensitive to static regions compared to complex areas. The detection of complex and static regions mainly relies on internal hardware modules. This level of control is mainly for improving subjective image quality while ensuring a constant bitrate, and it results in higher SSIM scores but lower PSNR scores.

CBR, VBR, and AVBR can enable QPMAP, and the actual value for each block region is obtained by the following formula:

MQP is the value in the ROI map, RQP is the value obtained by the internal bitrate control of the encoder, and ROIAvaQP is the average QP value in the ROI map.

### GOP Structure

The GOP structure table can define a set of periodic GOP structures that will be used throughout the encoding process. The elements in a single structure table are shown in the following table. It is possible to specify the reference frames for this image. If the reference frames specified for the frames following the IDR frame are the data frames before the IDR frame, the encoder will automatically handle this situation so that they do not reference other frames. Users do not need to be concerned about this situation. When defining a custom GOP structure, users need to specify the number of structure tables. A maximum of 8 structure tables can be defined, and the order of the structure tables needs to be arranged in decoding order.

| Element        | Description                                                  |
| :------------- | :----------------------------------------------------------- |
| Type           | Slice type (I, P or B)                                       |
| POC            | Display order of the frame within a GOP, ranging from 1 to GOP size |
| QPoffset       | A quantization parameter of the picture in the custom GOP     |
| NUM_REF_PIC_L0 | Flag to use multi-reference picture for P picture. It is valid only if PIC_TYPE is P |
| temporal_id    | Temporal layer of the frame. A frame cannot predict from a frame with a higher temporal ID (0~6) |
| 1st_ref_POC    | The POC of the 1st reference picture of L0                   |
| 2nd_ref_POC    | The POC of the 1st reference picture of L1 in case that Type is equal to B. The POC of the 2nd reference picture of L0 in case that Type is equal to P. Note that reference_L1 can have the same POC as reference in B slice. But for compression efficiency, it is recommended that reference_L1 have a different POC from reference_L0. |

#### GOP Predefined Structures

The following table provides 8 predefined GOP structures.

| Index | GOP Structure | Low Delay (encoding order and display order are the same) | GOP Size | Encoding Order | Minimum Source Frame Buffer | Minimum Decoded Picture Buffer | Intra Period (I Frame Interval) Requirement |
| :---: | :-----------: | :-------------------------------------------------------: | :------: | :------------: | :-------------------------: | :---------------------------: | :-----------------------------------------: |
|   1   |       I       |                             Yes                             |    1     |  I0-I1-I2…    |              1              |               1               |                                             |
|   2   |       P       |                             Yes                             |    1     |  P0-P1-P2…    |              1              |               2               |                                             |
|   3   |       B       |                             Yes                             |    1     |  B0-B1-B2…    |              1              |               3               |                                             |
|   4   |      BP       |                              No                             |    2     | B1-P0-B3-P2…  |              4              |               3               |               Multiple of 2               |
|   5   |     BBBP      |                              No                             |    4     | B2-B1-B3-P0…  |              7              |               4               |               Multiple of 4               |
|   6   |     PPPP      |                             Yes                             |    4     | P0-P1-P2-P3…  |              1              |               2               |                                             |
|   7   |     BBBB      |                             Yes                             |    4     | B0-B1-B2-B3…  |              1              |               3               |                                             |
|   8   |   BBBBBBBB    |                              No                             |    8     |B3-B2-B4-B1-B6-B5-B7-B0…|          12          |              5              |               Multiple of 8               |

Where: [image available for reference, not shown here]- GOP Preset1
  - Only I frames, no inter-reference frames
  - Low latency
  ![VENC_GOP_preset1](./image/video_encode/ss_venc_gop_preset1.png)
  
- GOP Preset2
  - Only I frames and P frames
  - P frames reference two forward reference frames
  - Low latency
  ![VENC_GOP_preset2](./image/video_encode/ss_venc_gop_preset2.png)
  
- GOP Preset3
  - Only I frames and B frames
  - B frames reference two forward reference frames
  - Low latency
  ![VENC_GOP_preset3](./image/video_encode/ss_venc_gop_preset3.png)
  
- GOP Preset4
  - I frames, P frames, and B frames
  - P frames reference two forward reference frames
  - B frames reference one forward reference frame and one backward reference frame
  ![VENC_GOP_preset4](./image/video_encode/ss_venc_gop_preset4.png)
  
- GOP Preset5
  - I frames, P frames, and B frames
  - P frames reference two forward reference frames
  - B frames reference one forward reference frame and one backward reference frame, where the backward reference frame can be a P frame or a B frame
  ![VENC_GOP_preset5](./image/video_encode/ss_venc_gop_preset5.png)
  
- GOP Preset 6
  - Only I frames and P frames
  - P frames reference two forward reference frames
  - Low latency
  ![VENC_GOP_preset6](./image/video_encode/ss_venc_gop_preset6.png)
  
- GOP Preset 7
  - Only I frames and B frames
  - B frames reference two forward reference frames
  - Low latency
  ![VENC_GOP_preset7](./image/video_encode/ss_venc_gop_preset7.png)
  
- GOP Preset 8
  - Only I frames and B frames
  - B frames reference one forward reference frame and one backward reference frame
  ![VENC_GOP_preset8](./image/video_encode/ss_venc_gop_preset8.png)

#### Relationship between GOP and I frame period
The following figure shows the relationship between GOP structure and I frame period.

![VENC_GOP_i-frame](./image/video_encode/ss_venc_gop_i-frame.png)### ROI

The implementation of ROI encoding is similar to QPMAP, and users need to set the QP value for each block according to the raster scan direction. The following figure shows an example of ROI map for H265. For H264 encoding, the size of each block is 16x16, while in H265, it is 32x32. In the ROI map table, each QP value occupies one byte, ranging from 0 to 51.

ROI encoding can work together with CBR and AVBR. When CBR or AVBR is not enabled, the actual QP value for each block region is the value specified in the ROI map. When CBR or AVBR is enabled, the actual value for each block region is obtained by the following formula:

MQP is the value in the ROI map, RQP is the value obtained by the encoder's internal rate control, and ROIAvaQP is the average QP value in the ROI map.

### Intra Refresh
Intra Refresh mode improves fault tolerance by periodically inserting intra-coded MB/CTUs into non-I frames. It provides more repair points for the decoder to avoid image corruption caused by temporal errors. Users can specify the number of continuous rows, columns, or step size of MB/CTUs to force the encoder to insert intra-coded units. Users can also specify the size of intra-coded units, which will be determined internally by the encoder.

### Long-term reference frame
Users can specify the period of long-term reference frames and the cycle of referring long-term reference frames, as shown in the following figure.

### Smart background encoding
In video surveillance scenarios, the background is often static. Therefore, it is desired that the encoder can either ignore the background region or use less bitrate to encode it when detecting a background region. In actual scenarios, due to the presence of noise in the camera image, it is not easy to detect the background region. In many cases, the ISP needs to notify the encoder when it detects a background region, which consumes additional bandwidth and system computing resources.

H264 and H265 encoding provide integrated smart background encoding modes inside the codec. This mode fully utilizes internal hardware modules and on-the-fly processing, without consuming additional bandwidth and system resources. The following figure shows the working mode of background detection. In the smart background encoding mode, the internal hardware module compares each block unit with the corresponding block unit of the reference frame to determine whether the block is part of the background.

For background region judgment, users can set the maximum pixel difference value (recommended value 8) and the average pixel difference value (recommended value 1). Users can also adjust the Lambda parameter to influence the mode selection in encoding. When a background region is detected, the encoder internally increases the corresponding Lambda value for each block unit, making the encoder more likely to use ignore mode to encode the block unit. For Lambda control, users can set lambdaQP (recommended value 32) and deltaQP (recommended value 3), and the final Lambda value is calculated according to the following formula:

QP_TO_LAMBDA_TABLE is the Lambda conversion table, which is also used for Lambda conversion in non-background regions.

It should be noted that Smart background encoding does not work when ROI encoding is enabled. The amount of bandwidth saved by this mode is closely related to the set bitrate and I-frame interval. The larger the bitrate and I-frame interval, the more bandwidth can be saved. In addition, in this mode, frames with better image quality can be set as long-term reference frames to improve the quality of the background image and save bitrate.

### Frame skip setting
Users can use the interface to set the encoding mode of the next input image as the skip mode. This mode is only valid for non-I frames. In skip mode, the encoder internally ignores the input frame and uses the reconstructed frame of the previous frame to generate the reconstruction frame of the current input. The input frame is then encoded as a P frame.

## API Reference
```C
HB_VENC_CreateChn: Create an encoding channel.
HB_VENC_DestroyChn: Destroy an encoding channel.
HB_VENC_ResetChn: Reset an encoding channel.
HB_VENC_StartRecvFrame: Start the encoding channel to receive input images.
HB_VENC_StopRecvFrame: Stop the encoding channel from receiving input images.
HB_VENC_SetChnAttr: Set the encoding attributes of an encoding channel.
HB_VENC_GetChnAttr: Get the encoding attributes of an encoding channel.
HB_VENC_GetStream: Get the encoded stream.
HB_VENC_ReleaseStream: Release the stream buffer.
HB_VENC_SendFrame: Support the user to send raw images for encoding.
HB_VENC_RequestIDR: Request an IDR frame.
HB_VENC_SetRoiAttr: Set the ROI encoding configuration of an encoding channel.
HB_VENC_GetRoiAttr: Get the ROI encoding configuration of an encoding channel.HB_VENC_SetH264SliceSplit: Set slice splitting configuration for H.264 encoding.
HB_VENC_GetH264SliceSplit: Get slice splitting configuration for H.264 encoding.
HB_VENC_SetH264IntraPred: Set frame intra-prediction configuration for H.264 encoding.
HB_VENC_GetH264IntraPred: Get frame intra-prediction configuration for H.264 encoding.
HB_VENC_SetH264Trans: Set transform and quantization configuration for H.264 encoding.
HB_VENC_GetH264Trans: Get transform and quantization configuration for H.264 encoding.
HB_VENC_SetH264Entropy: Set entropy coding configuration for H.264 encoding.
HB_VENC_GetH264Entropy: Get entropy coding configuration for H.264 encoding.
HB_VENC_SetH264Dblk: Set deblocking configuration for H.264 encoding.
HB_VENC_GetH264Dblk: Get deblocking configuration for H.264 encoding.
HB_VENC_SetH264Vui: Set VUI configuration for H.264 encoding.
HB_VENC_GetH264Vui: Get VUI configuration for H.264 encoding.
HB_VENC_SetH265Vui: Set VUI parameters for H.265 encoding channel.
HB_VENC_GetH265Vui: Get VUI configuration for H.265 encoding channel.
HB_VENC_SetRcParam: Set advanced parameters for channel bitrate control.
HB_VENC_GetRcParam: Get advanced parameters for channel bitrate control.
HB_VENC_SetRefParam: Set advanced skip frame reference parameters for H.264/H.265 encoding channels.
HB_VENC_GetRefParam: Get advanced skip frame reference parameters for H.264/H.265 encoding channels.
HB_VENC_SetH265SliceSplit: Set slice splitting configuration for H.265 encoding.
HB_VENC_GetH265SliceSplit: Get slice splitting configuration for H.265 encoding.
HB_VENC_SetH265PredUnit: Set PU configuration for H.265 encoding.
HB_VENC_GetH265PredUnit: Get PU configuration for H.265 encoding.
HB_VENC_SetH265Trans: Set transform and quantization configuration for H.265 encoding.
HB_VENC_GetH265Trans: Get transform and quantization configuration for H.265 encoding.
HB_VENC_SetH265Dblk: Set deblocking configuration for H.265 encoding.
HB_VENC_GetH265Dblk: Get deblocking configuration for H.265 encoding.
HB_VENC_SetH265Sao: Set SAO configuration for H.265 encoding.
HB_VENC_GetH265Sao: Get SAO configuration for H.265 encoding.
HB_VENC_GetIntraRefresh: Get parameters for P frame refreshing Islice.
HB_VENC_SetIntraRefresh: Set parameters for P frame refreshing Islice.
HB_VENC_SetCuPrediction: Set tendency for CU mode prediction.
HB_VENC_GetCuPrediction: Get configuration for CU mode prediction.
HB_VENC_GetFd: Get device file handle for encoding channel.
HB_VENC_CloseFd: Close device file handle for encoding channel.
HB_VENC_QueryStatus: Query status of encoding channel.
HB_VENC_InserUserData: Insert user data.
HB_VENC_SendFrameEx: Send raw image and QpMap table for encoding.| :------: | :-------------------------------------------------------------------------------------------------------------- | :-------: |
|   VeChn    | Encoding channel number <br/>Value range: [0, VENC_MAX_CHN_NUM). <br/>H264/H265 supports up to 32 channels, JPEG/MJPEG supports up to 64 channels. |   Input    |
|  pstAttr  | Pointer to encoding channel attributes                                                                                     |   Input    |

【Return Value】

| Return Value |                             Description |
| :----------: | :---------------------------------------|
|      0       |                                     Success |
|   Non-zero  |                           Failure, see error code. |

【Notes】
> None

【Reference Code】
> Reference code for HB_VENC_GetStream function

### HB_VENC_DestroyChn
【Function Declaration】
```C
int32_t HB_VENC_DestroyChn(VENC_CHN VeChn);
```
【Function Description】
> Destroy the encoding channel

【Parameter Description】

| Parameter Name |                                          Description | Input/Output |
| :------------: | :--------------------------------------------------- | :----------: |
|     VeChn      | Encoding channel number <br/>Value range: [0, VENC_MAX_CHN_NUM) |   Input    |

【Return Value】

| Return Value |                            Description |
| :----------: | :--------------------------------------|
|      0       |                                    Success |
|   Non-zero  |                           Failure, see error code. |

【Notes】
> None

【Reference Code】
> Reference code for HB_VENC_GetStream function

### HB_VENC_ResetChn
【Function Declaration】
```C
int32_t HB_VENC_ResetChn(VENC_CHN VeChn);
```
【Function Description】【函数声明】
```C
int32_t HB_VENC_StopRecvFrame(VENC_CHN VeChn);
```
【功能描述】
> 停止编码通道接收输入图像。

【参数描述】

| 参数名称 | 描述                                             | 输入/输出 |
| :------: | :----------------------------------------------- | :-------: |
|  VeChn   | 编码通道号。<br/>取值范围：[0, VENC_MAX_CHN_NUM) |   输入    |

【返回值】

| 返回值 |               描述 |
| :----: | :-----------------|
|   0    |               成功 |
|  非0   | 失败，参见错误码。 |

【注意事项】
> 需要在HB_VENC_SetChnAttr设置完通道属性后，才能调用。

【参考代码】
> HB_VENC_GetStream参考代码【Function Declaration】
```C
int32_t HB_VENC_StopRecvFrame(VENC_CHN VeChn);
```
【Description】
> Stop the encoding channel from receiving input images.

【Parameter Description】

| Parameter | Description                                            | Input/Output |
| :-------: | :----------------------------------------------------- | :----------: |
|   VeChn   | Encoding channel number.<br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |

【Return Value】

| Return Value |            Description |
| :----------: | :---------------------|
|      0       |           Success    |
|    non-zero  | Failure, see error code for details. |

【Note】
> None

【Reference Code】
> Reference code for HB_VENC_GetStream

### HB_VENC_SetChnAttr
【Function Declaration】
```C
int32_t HB_VENC_SetChnAttr(VENC_CHN VeChn, const VENC_CHN_ATTR_S *pstChnAttr);
```
【Description】
> Set the encoding attributes of the encoding channel.

【Parameter Description】

|  Parameter Name | Description                                            | Input/Output |
| :-------------: | :----------------------------------------------------- | :----------: |
|     VeChn       | Encoding channel number.<br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |
|   pstChnAttr    | Pointer to the encoding channel attributes           |    Input     |

【Return Value】

| Return Value |            Description |
| :----------: | :---------------------|
|      0       |           Success    |
|    non-zero  | Failure, see error code for details. |

【Note】
> The channel needs to be created first using HB_VENC_CreateChn.【参考代码】
> Reference code for HB_VENC_GetStream

### HB_VENC_GetChnAttr
【Function Declaration】
```C
int32_t HB_VENC_GetChnAttr(VENC_CHN VeChn, VENC_CHN_ATTR_S *pstChnAttr);
```
【Function Description】
> Get the encoding attributes of the encoding channel.

【Parameter Description】

|  Parameter Name  | Description                                       |  Input/Output  |
| :--------------: | :------------------------------------------------ | :------------: |
|      VeChn       | Encoding channel number.<br/>Value range: [0, VENC_MAX_CHN_NUM) |     Input      |
|   pstChnAttr     | Pointer to encoding channel attributes            |     Input      |

【Return Value】

|  Return Value  |      Description     |
| :------------: | :------------------: |
|       0        |        Success       |
|  Non-zero      |    Failure. Refer to error code.  |

【Notes】
> None

【Reference code】
> Reference code for HB_VENC_GetStream

### HB_VENC_GetStream
【Function Declaration】
```C
int32_t HB_VENC_GetStream(VENC_CHN VeChn, VIDEO_STREAM_S *pstStream, int32_t s32MilliSec);
```
【Function Description】
> Get the encoding stream.

【Parameter Description】

|  Parameter Name   | Description                                                                                     |  Input/Output  |
| :---------------: | :--------------------------------------------------------------------------------------------- | :------------: |
|      VeChn        | Encoding channel number.<br/>Value range: [0, VENC_MAX_CHN_NUM)                               |     Input      |
|    pstStream      | Pointer to the stream structure                                                                |     Input      |
|    s32MilliSec    | Timeout for getting the stream.<br/>Value range: [-1, + ∞ )<br/> -1: Block.<br/> 0: Non-block.<br/> Greater than 0: Timeout duration. |     Input      |

【Return Value】| Return Value | Description       |
| :----------: | :---------------- |
|      0       | Success           |
|    Non-zero  | Failure, see error code. |

【Notes】
> None

【Reference Code】
```C
    VENC_CHN VeChn = 0;
    int32_t s32Ret = 0;
    int32_t Width = 640;
    int32_t Height = 480;
    FILE *inFile;

    char *inputFileName = "./venc/yuv/input_640x480_yuv420p.yuv";
    inFile = fopen(inputFileName, "rb");
    ASSERT_NE(inFile, nullptr);

    char* mmz_vaddr[10];
    int32_t i = 0;
    for (i=0;i<10;i++) {
        mmz_vaddr[i] = NULL;
    }
    uint64_t mmz_paddr[10];
    memset(mmz_paddr, 0, sizeof(mmz_paddr));

    int32_t mmz_size = Width * Height * 3 / 2;

    VP_CONFIG_S struVpConf;
    memset(&struVpConf, 0x00, sizeof(VP_CONFIG_S));
    struVpConf.u32MaxPoolCnt = 32;
    HB_VP_SetConfig(&struVpConf);

    s32Ret = HB_VP_Init();
    if (s32Ret != 0) {
        printf("vp_init fail s32Ret = %d !\n",s32Ret);
    }

    for (i = 0; i < 10; i++) {
        s32Ret = HB_SYS_Alloc(&mmz_paddr[i], (void **)&mmz_vaddr[i], mmz_size);
        if (s32Ret == 0) {
            printf("mmzAlloc paddr = 0x%x, vaddr = 0x%x i = %d \n", mmz_paddr[i], mmz_vaddr[i],i);
        }
    }

    int32_t s32ReadLen = 0;
    for (i = 0; i < 10; i++) {
        s32ReadLen = fread(mmz_vaddr[i], 1, mmz_size, inFile);printf("s32ReadLen = %d !!!!!\n", s32ReadLen);
    if (s32ReadLen == 0) {
        printf("read over !!!\n");
    }
}
/* if (inFile) fclose(inFile); */

VENC_CHN_ATTR_S m_VencChnAttr;
memset(&m_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
m_VencChnAttr.stVencAttr.enType = PT_H264;
m_VencChnAttr.stVencAttr.u32PicWidth = Width;
m_VencChnAttr.stVencAttr.u32PicHeight = Height;
m_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
m_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
m_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;
m_VencChnAttr.stVencAttr.stAttrH264.h264_profile = 0;
m_VencChnAttr.stVencAttr.stAttrH264.h264_level = 0;
m_VencChnAttr.stGopAttr.u32GopPresetIdx = 2;
m_VencChnAttr.stGopAttr.s32DecodingRefreshType = 2;
m_VencChnAttr.stRcAttr.enRcMode = VENC_RC_MODE_H264CBR;
VENC_RC_ATTR_S *pstRcParam = &(m_VencChnAttr.stRcAttr);
s32Ret = HB_VENC_GetRcParam(VeChn, pstRcParam);
pstRcParam->stH264Cbr.u32BitRate = 3000;
pstRcParam->stH264Cbr.u32FrameRate = 30;
pstRcParam->stH264Cbr.u32IntraPeriod = 30;
pstRcParam->stH264Cbr.u32VbvBufferSize = 3000;
s32Ret = HB_VENC_CreateChn(VeChn, &m_VencChnAttr);

HB_VENC_SetChnAttr(VeChn, &m_VencChnAttr);  // config

VENC_RECV_PIC_PARAM_S pstRecvParam;
pstRecvParam.s32RecvPicNum = 0;  // unchangable
s32Ret = HB_VENC_StartRecvFrame(VeChn, &pstRecvParam);
VIDEO_FRAME_S pstFrame;
VIDEO_STREAM_S pstStream;
memset(&pstFrame, 0, sizeof(VIDEO_FRAME_S));
memset(&pstStream, 0, sizeof(VIDEO_STREAM_S));

pstFrame.stVFrame.width = Width;
pstFrame.stVFrame.height = Height;
pstFrame.stVFrame.size = mmz_size;

int32_t offset = Width * Height;
for (i=0;i<10;i++) {
    pstFrame.stVFrame.phy_ptr[0] = mmz_paddr[i];
    pstFrame.stVFrame.phy_ptr[1] = mmz_paddr[i] + offset;
    pstFrame.stVFrame.phy_ptr[2] = mmz_paddr[i] + offset * 5 / 4;
    pstFrame.stVFrame.vir_ptr[0] = mmz_vaddr[i];
    pstFrame.stVFrame.vir_ptr[1] = mmz_vaddr[i] + offset;
    pstFrame.stVFrame.vir_ptr[2] = mmz_vaddr[i] + offset * 5 / 4;\# If i is equal to 9
if (i == 9) {
    pstFrame.stVFrame.frame_end = HB_TRUE;
}

s32Ret = HB_VENC_SendFrame(VeChn, &pstFrame, 3000);
usleep(300000);

s32Ret = HB_VENC_GetStream(VeChn, &pstStream, 3000);
EXPECT_EQ(s32Ret, (int32_t)0);
printf("i = %d   pstStream.pstPack.size = %d !!!!!\n", i, pstStream.pstPack.size);
s32Ret = HB_VENC_ReleaseStream(VeChn, &pstStream);
}

s32Ret = HB_VENC_StopRecvFrame(VeChn);
s32Ret = HB_VENC_DestroyChn(VeChn);
for (i = 0; i < 10; i++) {
    s32Ret = HB_SYS_Free(mmz_paddr[i], mmz_vaddr[i]);
    if (s32Ret == 0) {
        printf("mmzFree paddr = 0x%x, vaddr = 0x%x i = %d \n", mmz_paddr[i],
            mmz_vaddr[i], i);
    }
}
s32Ret = HB_VP_Exit();
if (s32Ret == 0) printf("vp exit ok!\n");
printf("GetStream_Test\n");
if (inFile) fclose(inFile);

### HB_VENC_ReleaseStream
【Function Declaration】
```C
int32_t HB_VENC_ReleaseStream(VENC_CHN VeChn, VIDEO_STREAM_S *pstStream);
```
【Function Description】
> Release stream buffer.

【Parameter Description】

| Parameter | Description                                        | Input/Output |
| :-------: | :------------------------------------------------- | :----------: |
|   VeChn   | Encoding channel number. <br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |
| pstStream | Pointer of stream structure                       |    Input     |

【Return Value】

| Return Value |            Description |
| :----------: | :-------------------- |
|      0       |            Success |
|   Non-zero   | Fail, see error code |

【Notes】Please translate the following Chinese parts into English, while keeping the original format and content:

> None

【Reference Code】
> HB_VENC_GetStream reference code

### HB_VENC_SendFrame
【Function Declaration】
```C
int32_t HB_VENC_SendFrame(VENC_CHN VeChn, VIDEO_FRAME_S *pstFrame ,int32_t s32MilliSec);
```
【Function Description】
> Supports sending original images for encoding.

【Parameter Description】

| Parameter | Description                                                                                            | Input/Output |
| :-------: | :---------------------------------------------------------------------------------------------------- | :----------: |
|   VeChn   | Encoding channel number.<br/>Range: [0, VENC_MAX_CHN_NUM)                                              |    Input     |
| pstFrame  | Pointer to the structure of the original image information.                                            |    Input     |
|s32MilliSec| Timeout for obtaining the bitstream.<br/>Range: [-1, +∞)<br/>-1: Block.<br/> 0: Non-block.<br/> >0: Timeout.|    Input     |

【Return Value】

| Return Value |                Description |
| :----------: | :------------------------ |
|      0       |            Success        |
|   Non-zero   | Failure, see error code.  |

【Notes】
> None

【Reference Code】
> HB_VENC_GetStream reference code

### HB_VENC_RequestIDR
【Function Declaration】
```C
int32_t HB_VENC_RequestIDR(VENC_CHN VeChn);
```
【Function Description】
> Requests an IDR frame.

【Parameter Description】

| Parameter | Description                                                                                           | Input/Output |
| :-------: | :---------------------------------------------------------------------------------------------------- | :----------: |
|   VeChn   | Encoding channel number.<br/>Range: [0, VENC_MAX_CHN_NUM)                                             |    Input     |

【Return Value】| Parameter |         Description        | Input/Output |
| :-------: | :----------------------- | :----------: |
|  VeChn    | 编码通道号                |     Input    |
| pstRoiAttr | 感兴趣区域编码配置参数    |     Input    |

【返回值】
- 返回0表示成功。
- 非0表示失败，参见错误码。| :--------: | :----------------------------------------------- | :-------: |
|   VeChn    | Coding channel number.<br/>Value range: [0, VENC_MAX_CHN_NUM) |   Input    |
| pstRoiAttr | ROI region parameters                                      |   Input    |

【Return Value】

| Return Value |               Description |
| :----: | :-----------------|
|   0    |               Success |
|  Non-zero   | Failure, see error code. |

【Notes】
> None

【Reference Code】
> Reference code for HB_VENC_GetRoiAttr

### HB_VENC_GetRoiAttr
【Function Declaration】
```C
int32_t HB_VENC_GetRoiAttr(VENC_CHN VeChn, VENC_ROI_ATTR_S *pstRoiAttr);
```
【Function Description】
> Get the encoding configuration of the regions of interest for the coding channel.

【Parameter Description】

|  Parameter Name  | Description                                             | Input/Output |
| :--------: | :----------------------------------------------- | :-------: |
|   VeChn    | Coding channel number.<br/>Value range: [0, VENC_MAX_CHN_NUM) |   Input    |
| pstRoiAttr | Configuration of the corresponding ROI region                                |   Output    |

【Return Value】

| Return Value |               Description |
| :----: | :-----------------|
|   0    |               Success |
|  Non-zero   | Failure, see error code. |

【Notes】
> None

【Reference Code】
```C
    VENC_CHN VeChn = 0;
    int32_t s32Ret = 0;
    int32_t Width = 1920;
    int32_t Height = 1080;
    VENC_ROI_ATTR_S pstRoiAttrTest1;
    memset(&pstRoiAttrTest1, 0, sizeof(VENC_ROI_ATTR_S));
``````C
int32_t HB_VENC_SetH264SliceSplit(VENC_CHN VeChn, const VENC_H264_SLICE_SPLIT_S *pstSliceSplit);
```

【Function Description】
> Set the slice split configuration for H.264 encoding.

【Parameter Description】

|   Parameter    | Description                                   | Input/Output |
| :------------: | :-------------------------------------------- | :----------: |
|     VeChn      | Channel number for encoding.<br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |
| pstSliceSplit | Parameters for H.264 slice split in the bitstream |    Input     |

【Return Value】| Return Value | Description       |
| :----:       | :---------------  |
|   0          | Successful        |
|  Non-zero    | Failed, see error code |

【Notes】
> None

【Reference Code】
> HB_VENC_GetH264SliceSplit Reference Code

### HB_VENC_GetH264SliceSplit
【Function Declaration】
```C
int32_t HB_VENC_GetH264SliceSplit(VENC_CHN VeChn, VENC_H264_SLICE_SPLIT_S *pstSliceSplit);
```

【Function Description】
> Get the slice split configuration of H.264 encoding.

【Parameter Description】

|   Parameter Name    | Description                                        | Input/Output |
| :-----------:       | :-----------------------------------------------  | :-------:    |
|     VeChn           | Encoding channel number.<br/>Range: [0, VENC_MAX_CHN_NUM)      |   Input       |
| pstSliceSplit       | H.264 stream slice split parameters                 |   Output      |

【Return Value】

| Return Value | Description       |
| :----:       | :---------------  |
|   0          | Successful        |
|  Non-zero    | Failed, see error code |

【Notes】
> None

【Reference Code】
```C
    VENC_CHN VeChn = 0;
    int32_t Width = 1920;
    int32_t Height = 1080;
    int32_t s32Ret = 0;

    VENC_H264_SLICE_SPLIT_S pstSliceSplit1;
    memset(&pstSliceSplit1, 0, sizeof(VENC_H264_SLICE_SPLIT_S));
    VENC_CHN_ATTR_S m_VencChnAttr;
    memset(&m_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
    m_VencChnAttr.stVencAttr.enType = PT_H264;
    m_VencChnAttr.stVencAttr.u32PicWidth = Width;
``````C
m_VencChnAttr.stVencAttr.u32PicHeight = Height;
m_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
m_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
m_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;
m_VencChnAttr.stVencAttr.stAttrH264.h264_profile = 0;
m_VencChnAttr.stVencAttr.stAttrH264.h264_level = 0;
m_VencChnAttr.stGopAttr.u32GopPresetIdx = 2;
m_VencChnAttr.stGopAttr.s32DecodingRefreshType = 2;
m_VencChnAttr.stRcAttr.enRcMode = VENC_RC_MODE_H264CBR;
VENC_RC_ATTR_S *pstRcParam = &(m_VencChnAttr.stRcAttr);
s32Ret = HB_VENC_GetRcParam(VeChn, pstRcParam);
pstRcParam->stH264Cbr.u32BitRate = 3000;
pstRcParam->stH264Cbr.u32FrameRate = 30;
pstRcParam->stH264Cbr.u32IntraPeriod = 30;
pstRcParam->stH264Cbr.u32VbvBufferSize = 3000;
s32Ret = HB_VENC_CreateChn(VeChn, &m_VencChnAttr);
HB_VENC_SetChnAttr(VeChn, &m_VencChnAttr);  // config

pstSliceSplit1.h264_slice_mode = HB_TRUE;
pstSliceSplit1.h264_slice_arg = 10;
pstSliceSplit1.slice_loop_filter_across_slices_enabled_flag = HB_TRUE;
s32Ret = HB_VENC_SetH264SliceSplit(VeChn, &pstSliceSplit1);

VENC_H264_SLICE_SPLIT_S pstSliceSplit2;
memset(&pstSliceSplit2, 0, sizeof(VENC_H264_SLICE_SPLIT_S));
s32Ret = HB_VENC_GetH264SliceSplit(VeChn, &pstSliceSplit2);
s32Ret = HB_VENC_DestroyChn(VeChn);
```【Attention】
> None

【Reference Code】
> Reference code for HB_VENC_GetH264IntraPred

### HB_VENC_GetH264IntraPred
【Function Declaration】
```C
int32_t HB_VENC_GetH264IntraPred(VENC_CHN VeChn, VENC_H264_INTRA_PRED_S *pstH264IntraPred);
```
【Function Description】
> Get the frame intra prediction configuration for H.264 encoding.

【Parameter Description】

|  Name  |              Description             | Input/Output |
| :----: | :---------------------------------: | :----------: |
| VeChn  |      Encoding channel number.       |    Input     |
| pstH264IntraPred | Frame intra prediction configuration for H.264 protocol encoding. |    Output    |

【Return Value】

| Return Value |                 Description                 |
| :----------: | :-----------------------------------------: |
|       0      |                  Success                    |
|   Non-zero   | Failed, see error code for more information. |

【Attention】
> None

【Reference Code】
```C
    int32_t s32Ret = 0;
    VENC_CHN VeChn = 0;
    int32_t Width = 1920;
    int32_t Height = 1080;

    VENC_H264_INTRA_PRED_S pstH264IntraPred1;
    memset(&pstH264IntraPred1, 0, sizeof(VENC_H264_INTRA_PRED_S));

    VENC_CHN_ATTR_S m_VencChnAttr;
    memset(&m_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
    m_VencChnAttr.stVencAttr.enType = PT_H264;
    m_VencChnAttr.stVencAttr.u32PicWidth = Width;
    m_VencChnAttr.stVencAttr.u32PicHeight = Height;
    m_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
    m_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
    m_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;
```    s32Ret = HB_VENC_SetH264Trans(VeChn, &pstH264Trans);Please translate the Chinese parts in the content below into English, while keeping the original format and content:

```C
VENC_CHN VeChn = 0;
int32_t Width = 1920;
int32_t Height = 1080;

VENC_H264_TRANS_S pstH264Trans1;
memset(&pstH264Trans1, 0, sizeof(VENC_H264_TRANS_S));
VENC_CHN_ATTR_S m_VencChnAttr;
memset(&m_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
m_VencChnAttr.stVencAttr.enType = PT_H264;
m_VencChnAttr.stVencAttr.u32PicWidth = Width;
m_VencChnAttr.stVencAttr.u32PicHeight = Height;
m_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
m_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
m_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;
m_VencChnAttr.stVencAttr.stAttrH264.h264_profile = 0;
m_VencChnAttr.stVencAttr.stAttrH264.h264_level = 0;
m_VencChnAttr.stGopAttr.u32GopPresetIdx = 2;
m_VencChnAttr.stGopAttr.s32DecodingRefreshType = 2;
m_VencChnAttr.stRcAttr.enRcMode = VENC_RC_MODE_H264CBR;
VENC_RC_ATTR_S *pstRcParam = &(m_VencChnAttr.stRcAttr);
s32Ret = HB_VENC_GetRcParam(VeChn, pstRcParam);
pstRcParam->stH264Cbr.u32BitRate = 3000;
pstRcParam->stH264Cbr.u32FrameRate = 30;
pstRcParam->stH264Cbr.u32IntraPeriod = 30;
pstRcParam->stH264Cbr.u32VbvBufferSize = 3000;

s32Ret = HB_VENC_CreateChn(VeChn, &m_VencChnAttr);
HB_VENC_SetChnAttr(VeChn, &m_VencChnAttr);
pstH264Trans1.chroma_cb_qp_offset = 5;
pstH264Trans1.chroma_cr_qp_offset = 5;
pstH264Trans1.transform_8x8_enable = HB_TRUE;
pstH264Trans1.user_scaling_list_enable = 1;
s32Ret = HB_VENC_SetH264Trans(VeChn, &pstH264Trans1);
VENC_H264_TRANS_S pstH264Trans2;
memset(&pstH264Trans2, 0, sizeof(VENC_H264_TRANS_S));
s32Ret = HB_VENC_GetH264Trans(VeChn, &pstH264Trans2);
s32Ret = HB_VENC_DestroyChn(VeChn);
```

### HB_VENC_GetH264Trans
【Function Declaration】
```C
int32_t HB_VENC_GetH264Trans(VENC_CHN VeChn, VENC_H264_TRANS_S *pstH264Trans);
```
【Description】
> Get the transformation and quantization settings for H.264 encoding.

【Parameters】

| Parameter Name | Description                                                | Input/Output |
| :----------: | :----------------------------------------------- | :-------: |
|    VeChn     | Encoded channel number.<br/>Range: [0, VENC_MAX_CHN_NUM) |   Input    |
| pstH264Trans | Transformation and quantization properties of H.264 protocol encoding channel |   Output    |

【Return Value】

| Return Value |               Description |
| :----: | :-----------------|
|   0    |               Success |
|  Non-zero   | Failure, refer to the error code. |

【Notes】
> None

【Reference Code】
> Reference code for HB_VENC_SetH264Trans

### HB_VENC_SetH264Entropy
【Function Declaration】
```C
int32_t HB_VENC_SetH264Entropy(VENC_CHN VeChn, const VENC_H264_ENTROPY_S *pstH264EntropyEnc);
```
【Function Description】
> Set the entropy coding configuration of H.264 encoding.

【Parameter Description】

|     Parameter Name      | Description                                             | Input/Output |
| :---------------: | :----------------------------------------------- | :-------: |
|       VeChn       | Encoded channel number.<br/>Range: [0, VENC_MAX_CHN_NUM) |   Input    |
| pstH264EntropyEnc | Entropy coding mode of H.264 protocol encoding channel                   |   Input    |

【Return Value】

| Return Value |               Description |
| :----: | :-----------------|
|   0    |               Success |
|  Non-zero   | Failure, refer to the error code. |

【Notes】
> None

【Reference Code】
```C
    int32_t s32Ret = 0;
    VENC_CHN VeChn = 0;
    int32_t Width = 1920;
    int32_t Height = 1080;

    VENC_H264_ENTROPY_S pstH264EntropyEnc1;
````memset(&pstH264EntropyEnc1, 0, sizeof(VENC_H264_ENTROPY_S));`
`memset(&m_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));`
`m_VencChnAttr.stVencAttr.enType = PT_H264;`
`m_VencChnAttr.stVencAttr.u32PicWidth = Width;`
`m_VencChnAttr.stVencAttr.u32PicHeight = Height;`
`m_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;`
`m_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;`
`m_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;`
`m_VencChnAttr.stVencAttr.stAttrH264.h264_profile = 0;`
`m_VencChnAttr.stVencAttr.stAttrH264.h264_level = 0;`
`m_VencChnAttr.stGopAttr.u32GopPresetIdx = 2;`
`m_VencChnAttr.stGopAttr.s32DecodingRefreshType = 2;`
`m_VencChnAttr.stRcAttr.enRcMode = VENC_RC_MODE_H264CBR;`

`VENC_RC_ATTR_S *pstRcParam = &(m_VencChnAttr.stRcAttr);`
`s32Ret = HB_VENC_GetRcParam(VeChn, pstRcParam);`
`pstRcParam->stH264Cbr.u32BitRate = 3000;`
`pstRcParam->stH264Cbr.u32FrameRate = 30;`
`pstRcParam->stH264Cbr.u32IntraPeriod = 30;`
`pstRcParam->stH264Cbr.u32VbvBufferSize = 3000;`

`s32Ret = HB_VENC_CreateChn(VeChn, &m_VencChnAttr);`
`HB_VENC_SetChnAttr(VeChn, &m_VencChnAttr);`
`pstH264EntropyEnc1.u32EntropyEncMode = 0;`

`s32Ret = HB_VENC_SetH264Entropy(VeChn, &pstH264EntropyEnc1);`

`VENC_H264_ENTROPY_S pstH264EntropyEnc2;`
`memset(&pstH264EntropyEnc2, 0, sizeof(VENC_H264_ENTROPY_S));`
`s32Ret = HB_VENC_GetH264Entropy(VeChn, &pstH264EntropyEnc2);`

`s32Ret = HB_VENC_DestroyChn(VeChn);`

### HB_VENC_GetH264Entropy
【Function Declaration】
```C
int32_t HB_VENC_GetH264Entropy(VENC_CHN VeChn, VENC_H264_ENTROPY_S *pstH264EntropyEnc);
```
【Description】
> Get the entropy encoding configuration of H.264 encoding.

【Parameter Description】

| Parameter Name | Description                                    | Input/Output |
| :------------: | :--------------------------------------------- | :----------: |
|     VeChn      | Encoding channel number. <br/>Range: [0, VENC_MAX_CHN_NUM) |   Input    |
| pstH264EntropyEnc| Entropy encoding mode of H.264 protocol encoding channel |    Output    |

【Return Value】

| Return Value | Description |
| :----------: | :----------|
|   Return | Description |
| :----: | :---------|
|   0    |   Success |
|  Non-zero   | Failed, see error code. |

【Notes】
> None

【Reference Code】
> Reference code for HB_VENC_SetH264Entropy

### HB_VENC_SetH264Dblk
【Function Declaration】
```C
int32_t HB_VENC_SetH264Dblk(VENC_CHN VeChn, const VENC_H264_DBLK_S *pstH264Dblk);
```
【Description】
> Sets the deblocking configuration for H.264 encoding.

【Parameter Description】

|  Parameter Name   | Description                                             | Input/Output |
| :---------: | :----------------------------------------------- | :-------: |
|    VeChn    | Encoding channel number.<br/>Value range: [0, VENC_MAX_CHN_NUM) |   Input    |
| pstH264Dblk | Deblocking parameters for the H.264 protocol encoding channel |   Input    |

【Return Value】

| Return Value |               Description |
| :----: | :-----------------|
|   0    |   Success |
|  Non-zero   | Failed, see error code. |

【Notes】
> None

【Reference Code】
```C
    int32_t s32Ret = 0;
    VENC_CHN VeChn = 0;
    int32_t Width = 1920;
    int32_t Height = 1080;

    VENC_H264_DBLK_S pstH264Dblk1;
    memset(&pstH264Dblk1, 0, sizeof(VENC_H264_DBLK_S));
    VENC_CHN_ATTR_S m_VencChnAttr;
    memset(&m_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
    m_VencChnAttr.stVencAttr.enType = PT_H264;
    m_VencChnAttr.stVencAttr.u32PicWidth = Width;
    m_VencChnAttr.stVencAttr.u32PicHeight = Height;
    m_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
    m_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
HB_VENC_GetH264Dblk
【Function Declaration】
```C
int32_t HB_VENC_GetH264Dblk(VENC_CHN VeChn, VENC_H264_DBLK_S *pstH264Dblk);
```
【Function Description】
> Get the deblocking configuration of H.264 encoding.

【Parameter Description】

|   Parameter Name   |                      Description                     | Input/Output |
| :----------------: | :--------------------------------------------------: | :----------: |
|       VeChn        |    Encoding channel number.<br/>Value range: [0, VENC_MAX_CHN_NUM) |    Input    |
|   pstH264Dblk  | Deblocking parameters of H.264 protocol encoding channel  |   Output    |

【Return Value】

| Return Value |                           Description                          |
| :----------: | :-----------------------------------------------------------: |
|       0      |                            Success                            |
|   Non-zero   | Failed, see error code for details. |

【Precautions】
> None### HB_VENC_SetH264Vui
【Function Declaration】
```C
int32_t HB_VENC_SetH264Vui(VENC_CHN VeChn, const VENC_H264_VUI_S *pstH264Vui);
```
【Function Description】
> Set the VUI configuration for H.264 encoding.

【Parameter Description】

| Parameter Name | Description                                              | Input/Output |
| :------------: | :------------------------------------------------------- | :----------: |
|     VeChn      | Encoding channel number.<br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |
|   pstH264Vui   | Vui parameters of the H.264 protocol encoding channel    |    Input     |

【Return Value】

| Return Value | Description   |
| :----------: | :------------ |
|      0       | Success       |
|   Non-zero   | Failure, see error codes. |

【Notes】
> The Vui parameters are static and can only be called before HB_VENC_SetChnAttr.

【Reference Code】
```C
    int32_t s32Ret = 0;
    VENC_CHN VeChn = 0;
    int32_t Width = 1920;
    int32_t Height = 1080;

    VENC_H264_VUI_S pstH264Vui1;
    memset(&pstH264Vui1, 0, sizeof(VENC_H264_VUI_S));
    VENC_CHN_ATTR_S m_VencChnAttr;
    memset(&m_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
    m_VencChnAttr.stVencAttr.enType = PT_H264;
    m_VencChnAttr.stVencAttr.u32PicWidth = Width;
    m_VencChnAttr.stVencAttr.u32PicHeight = Height;
    m_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
    m_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
    m_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;
    m_VencChnAttr.stVencAttr.stAttrH264.h264_profile = 0;
    m_VencChnAttr.stVencAttr.stAttrH264.h264_level = 0;
    m_VencChnAttr.stGopAttr.u32GopPresetIdx = 2;
    m_VencChnAttr.stGopAttr.s32DecodingRefreshType = 2;
    m_VencChnAttr.stRcAttr.enRcMode = VENC_RC_MODE_H264CBR;
``````C
int32_t HB_VENC_SetH265Vui(VENC_CHN VeChn, const VENC_H265_VUI_S *pstH265Vui);
```
【功能描述】
> 设置 H.265 编码的 VUI 配置。

【参数描述】

|   参数名称   | 描述                                             | 输入/输出 |
| :----------: | :----------------------------------------------- | :-------: |
|    VeChn     | 编码通道号。<br/>取值范围：[0, VENC_MAX_CHN_NUM) |   输入    |
| pstH265Vui | H.265 协议编码通道的 Vui 参数                    |   输入    |

【返回值】

| 返回值 |               描述 |
| :----: | :-----------------|
|   0    |               成功 |
|  非0   | 失败，参见错误码。 |

【注意事项】
> 无

【参考代码】
> 无```C
int32_t HB_VENC_SetH265Vui(VENC_CHN VeChn, const VENC_H265_VUI_S *pstH265Vui);
```
【Function Description】
> Set the VUI configuration for the H.265 protocol encoding channel

【Parameter Description】

|   Parameter Name   |                    Description                     | Input/Output |
| :----------------: | :------------------------------------------------: | :----------: |
|       VeChn        |          Encoding channel number.<br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |
|     pstH265Vui     |        Vui parameter for the H.265 protocol encoding channel         |    Input     |

【Return Value】

| Return Value |                   Description                      |
| :----------: | :------------------------------------------------: |
|       0      |                   Success                          |
|     Non-0    |            Failure, refer to the error code         |

【Notes】
> None

【Reference Code】
```C
    int32_t s32Ret = 0;
    VENC_CHN VeChn = 0;
    int32_t Width = 1920;
    int32_t Height = 1080;

    VENC_H265_VUI_S pstH265Vui1;
    memset(&pstH265Vui1, 0, sizeof(VENC_H265_VUI_S));
    VENC_CHN_ATTR_S m_VencChnAttr;
    memset(&m_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
    m_VencChnAttr.stVencAttr.enType = PT_H265;
    m_VencChnAttr.stVencAttr.u32PicWidth = Width;
    m_VencChnAttr.stVencAttr.u32PicHeight = Height;
    m_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
    m_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
    m_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;
    m_VencChnAttr.stGopAttr.u32GopPresetIdx = 2;
    m_VencChnAttr.stGopAttr.s32DecodingRefreshType = 2;
    m_VencChnAttr.stRcAttr.enRcMode = VENC_RC_MODE_H265CBR;
    VENC_RC_ATTR_S *pstRcParam = &(m_VencChnAttr.stRcAttr);
    s32Ret = HB_VENC_GetRcParam(VeChn, pstRcParam);
    pstRcParam->stH265Cbr.u32BitRate = 3000;
    pstRcParam->stH265Cbr.u32FrameRate = 30;
    pstRcParam->stH265Cbr.u32IntraPeriod = 30;
    pstRcParam->stH265Cbr.u32VbvBufferSize = 3000;
    s32Ret = HB_VENC_CreateChn(VeChn, &m_VencChnAttr);
```|  参数名称   |               描述                 | 输入/输出 |
| :---------: | :------------------------------- | :-------: |
|   VeChn     | 编码通道号。<br/>取值范围：[0, VENC_MAX_CHN_NUM) |   输入    |
| pstRcParam  | 编码通道的码率控制高级参数         |   输入    |
【返回值】

| 返回值 |               描述 |
| :----: | :-----------------|
|   0    |               成功 |
|  非0   | 失败，参见错误码。 |

【注意事项】
> 无

【参考代码】
```C
VENC_RC_ATTR_S stRcParam;
memset(&stRcParam, 0, sizeof(VENC_RC_ATTR_S));
HB_VENC_GetRcParam(VeChn, &stRcParam);
// 修改stRcParam的相关参数
s32Ret = HB_VENC_SetRcParam(VeChn, &stRcParam);
```| Parameter Name | Description                                       | Input/Output |
| :------------: | :------------------------------------------------ | :----------: |
|    VeChn       | Encoding channel number.<br/>Value Range: [0, VENC_MAX_CHN_NUM) |   Input   |
|  pstRcParam    | Advanced parameters of the encoding channel's rate controller   |   Input   |

【Return Value】

| Return Value | Description |
| :----------: | :---------- |
|      0       |    Success   |
|   Non-zero   | Failure, see error codes. |

【Note】
> None

【Reference Code】

### HB_VENC_GetRcParam
【Function Declaration】
```C
int32_t HB_VENC_GetRcParam(VENC_CHN VeChn, VENC_RC_ATTR_S *pstRcParam);
```
【Function Description】
> Get advanced parameters of the rate controller for the channel.

【Parameter Description】

| Parameter Name | Description                                       | Input/Output |
| :------------: | :------------------------------------------------ | :----------: |
|    VeChn       | Encoding channel number.<br/>Value Range: [0, VENC_MAX_CHN_NUM) |   Input   |
|  pstRcParam    | Advanced parameters of the encoding channel's rate controller   |   Input   |

【Return Value】

| Return Value | Description |
| :----------: | :---------- |
|      0       |    Success   |
|   Non-zero   | Failure, see error codes. |

【Note】
> None

【Reference Code】

### HB_VENC_SetRefParam
【Function Declaration】
```C
int32_t HB_VENC_SetRefParam(VENC_CHN VeChn, const VENC_REF_PARAM_S *pstRefParam);
```
【Function Description】> Set advanced frame skipping reference parameters for H.264/H.265 encoding channel.

【Parameter Description】

|  Parameter Name  | Description                                                      | Input/Output |
| :--------------: | :--------------------------------------------------------------- | :-----------: |
|      VeChn       | Encoding channel number.<br/>Value range: [0, VENC_MAX_CHN_NUM) |    Input      |
|  pstRefParam     | Advanced frame skipping reference parameters for H.264/H.265 encoding channel  |    Input      |

【Return Value】

| Return Value |        Description        |
| :----------: | :------------------------ |
|       0      |          Success          |
|   Non-zero   |    Failure, see error code    |

【Notes】
> None

【Reference Code】
```C
    int32_t s32Ret = 0;
    VENC_CHN VeChn = 0;
    int32_t Width = 1920;
    int32_t Height = 1080;

    VENC_REF_PARAM_S pstRefParam_test1;
    memset(&pstRefParam_test1, 0x00, sizeof(VENC_REF_PARAM_S));
    VENC_CHN_ATTR_S m_VencChnAttr;
    memset(&m_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
    m_VencChnAttr.stVencAttr.enType = PT_H264;
    m_VencChnAttr.stVencAttr.u32PicWidth = Width;
    m_VencChnAttr.stVencAttr.u32PicHeight = Height;
    m_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
    m_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
    m_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;
    m_VencChnAttr.stVencAttr.stAttrH264.h264_profile = 0;
    m_VencChnAttr.stVencAttr.stAttrH264.h264_level = 0;
    m_VencChnAttr.stGopAttr.u32GopPresetIdx = 2;
    m_VencChnAttr.stGopAttr.s32DecodingRefreshType = 2;
    m_VencChnAttr.stRcAttr.enRcMode = VENC_RC_MODE_H264CBR;
    VENC_RC_ATTR_S *pstRcParam = &(m_VencChnAttr.stRcAttr);
    s32Ret = HB_VENC_GetRcParam(VeChn, pstRcParam);
    pstRcParam->stH264Cbr.u32BitRate = 3000;
    pstRcParam->stH264Cbr.u32FrameRate = 30;
    pstRcParam->stH264Cbr.u32IntraPeriod = 30;
    pstRcParam->stH264Cbr.u32VbvBufferSize = 3000;
    s32Ret = HB_VENC_CreateChn(VeChn, &m_VencChnAttr);

    pstRefParam_test1.use_longterm = HB_TRUE;
```| 参数名称   | 描述                                             | 输入/输出 |
| :---------: | :----------------------------------------------- | :-------: |
|    VeChn    | 编码通道号。<br/>取值范围：[0, VENC_MAX_CHN_NUM) |   输入    |
| bEnableIDR | 是否使能 IDR 帧。<br/>取值范围：HB_TRUE（启用），HB_FALSE（禁用） |   输入    |

【返回值】

| 返回值 |               描述 |
| :----: | :-----------------|
|   0    |               成功 |
|  非0   | 失败，参见错误码。 |

【注意事项】
> 无

【参考代码】
```C
HB_VENC_EnableIDR(VeChn, HB_TRUE);
```【Return Value】

| Return Value | Description |
| :----: | :-----------------|
|   0    |   Success |
|  Non-zero   |  Failure, see error code. |

【Notes】
> None

【Code Reference】
> None

### HB_VENC_SetH265SliceSplit
【Function Declaration】
```C
int32_t HB_VENC_SetH265SliceSplit(VENC_CHN VeChn, const VENC_H265_SLICE_SPLIT_S *pstSliceSplit);
```
【Function Description】
> Set the slice split configuration of H.265 encoding.

【Parameter Description】

|   Parameter Name   | Description                                     | Input/Output |
| :------------: | :--------------------------------------------- | :----------: |
|     VeChn      | Channel number of the encoding.<br/>Value range: [0, VENC_MAX_CHN_NUM) |    Input     |
| pstSliceSplit  | Slice split parameters of H.265 bitstream        |    Input     |

【Return Value】

| Return Value | Description |
| :----: | :-----------------|
|   0    |   Success |
|  Non-zero   |  Failure, see error code. |

【Notes】
> None

【Code Reference】
```C
    int32_t s32Ret = 0;
    VENC_CHN VeChn = 0;
    int32_t Width = 1920;
    int32_t Height = 1080;

    VENC_H265_SLICE_SPLIT_S pstSliceSplit1;
    memset(&pstSliceSplit1, 0, sizeof(VENC_H265_SLICE_SPLIT_S));
    VENC_CHN_ATTR_S m_VencChnAttr;
    memset(&m_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
    m_VencChnAttr.stVencAttr.enType = PT_H265;
```m_VencChnAttr.stVencAttr.u32PicWidth = Width;
m_VencChnAttr.stVencAttr.u32PicHeight = Height;
m_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
m_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
m_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;
m_VencChnAttr.stGopAttr.u32GopPresetIdx = 2;
m_VencChnAttr.stGopAttr.s32DecodingRefreshType = 2;
m_VencChnAttr.stRcAttr.enRcMode = VENC_RC_MODE_H265CBR;
VENC_RC_ATTR_S *pstRcParam = &(m_VencChnAttr.stRcAttr);
s32Ret = HB_VENC_GetRcParam(VeChn, pstRcParam);
pstRcParam->stH265Cbr.u32BitRate = 3000;
pstRcParam->stH265Cbr.u32FrameRate = 30;
pstRcParam->stH265Cbr.u32IntraPeriod = 30;
pstRcParam->stH265Cbr.u32VbvBufferSize = 3000;
s32Ret = HB_VENC_CreateChn(VeChn, &m_VencChnAttr);

HB_VENC_SetChnAttr(VeChn, &m_VencChnAttr);
pstSliceSplit1.h265_dependent_slice_arg = 1;
pstSliceSplit1.h265_dependent_slice_mode = 1;
pstSliceSplit1.h265_independent_slice_arg = 1;
pstSliceSplit1.h265_independent_slice_mode = 1;
s32Ret = HB_VENC_SetH265SliceSplit(VeChn, &pstSliceSplit1);

VENC_H265_SLICE_SPLIT_S pstSliceSplit2;
memset(&pstSliceSplit2, 0, sizeof(VENC_H265_SLICE_SPLIT_S));
s32Ret = HB_VENC_GetH265SliceSplit(VeChn, &pstSliceSplit2);
s32Ret = HB_VENC_DestroyChn(VeChn);

### HB_VENC_GetH265SliceSplit
【Function Declaration】
```C
int32_t HB_VENC_GetH265SliceSplit(VENC_CHN VeChn, VENC_H265_SLICE_SPLIT_S *pstSliceSplit);
```
【Function Description】
> Get the H.265 encoding slice split configuration.

【Parameter Description】

|  Parameters |                      Description                    | Input/Output |
| :---------: | :------------------------------------------------: | :----------: |
|   VeChn     |     Encoding channel number.<br/>Value range: [0, VENC_MAX_CHN_NUM) |    Input     |
| pstSliceSplit |   H.265 stream slice split parameters              |     Output    |

【Return Value】

| Return Value | Description |
| :----------: | :---------: |
|      0       |   Success   |
|    Non-zero  |     Failure, see error code.    |【Attention】
> None

【Reference Code】
> Reference code for HB_VENC_SetH265SliceSplit

### HB_VENC_SetH265PredUnit
【Function Declaration】
```C
int32_t HB_VENC_SetH265PredUnit(VENC_CHN VeChn, const VENC_H265_PU_S *pstPredUnit);
```
【Function Description】
> Set the PU configuration for H.265 encoding

【Parameter Description】

| Parameter Name | Description                                      | Input/Output |
| :------------: | :---------------------------------------------- | :----------: |
|    VeChn       | Encoding channel number.<br/>Value range: [0, VENC_MAX_CHN_NUM) |   Input      |
| pstPredUnit    | PU configuration for H.265 protocol encoding    |   Input      |

【Return Value】

| Return Value |           Description |
| :----------: | :------------------- |
|      0       |           Success    |
| Non-zero value| Failure, see error code. |

【Attention】
> None

【Reference Code】
```C
    int32_t s32Ret = 0;
    VENC_CHN VeChn = 0;
    int32_t Width = 1920;
    int32_t Height = 1080;

    VENC_H265_PU_S pstPredUnit1;
    memset(&pstPredUnit1, 0, sizeof(VENC_H265_PU_S));

    VENC_CHN_ATTR_S m_VencChnAttr;
    memset(&m_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
    m_VencChnAttr.stVencAttr.enType = PT_H265;
    m_VencChnAttr.stVencAttr.u32PicWidth = Width;
    m_VencChnAttr.stVencAttr.u32PicHeight = Height;
    m_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
    m_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
    m_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;
```m_VencChnAttr.stGopAttr.u32GopPresetIdx = 2;
m_VencChnAttr.stGopAttr.s32DecodingRefreshType = 2;
m_VencChnAttr.stRcAttr.enRcMode = VENC_RC_MODE_H265CBR;
VENC_RC_ATTR_S *pstRcParam = &(m_VencChnAttr.stRcAttr);
s32Ret = HB_VENC_GetRcParam(VeChn, pstRcParam);
pstRcParam->stH265Cbr.u32BitRate = 3000;
pstRcParam->stH265Cbr.u32FrameRate = 30;
pstRcParam->stH265Cbr.u32IntraPeriod = 30;
pstRcParam->stH265Cbr.u32VbvBufferSize = 3000;
s32Ret = HB_VENC_CreateChn(VeChn, &m_VencChnAttr);

pstPredUnit1.constrained_intra_pred_flag = 1;
pstPredUnit1.intra_nxn_enable = 0;
pstPredUnit1.max_num_merge = 1;
pstPredUnit1.strong_intra_smoothing_enabled_flag = 1;

s32Ret = HB_VENC_SetH265PredUnit(VeChn, &pstPredUnit1);

VENC_H265_PU_S pstPredUnit2;
memset(&pstPredUnit2, 0, sizeof(VENC_H265_PU_S));
s32Ret = HB_VENC_GetH265PredUnit(VeChn, &pstPredUnit2);
HB_VENC_SetChnAttr(VeChn, &m_VencChnAttr);
s32Ret = HB_VENC_DestroyChn(VeChn);

### HB_VENC_GetH265PredUnit
【Function Declaration】
```C
int32_t HB_VENC_GetH265PredUnit(VENC_CHN VeChn, VENC_H265_PU_S *pstPredUnit);
```
【Function Description】
> Get PU configuration for H.265 encoding

【Parameter Description】

|   Parameter Name   |                  Description                  | Input/Output |
| :----------------: | :-------------------------------------------: | :----------: |
|       VeChn        |      Channel number for encoding.<br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |
|    pstPredUnit     | PU configuration for H.265 encoding channel  |    Output    |

【Return Value】

| Return Value |       Description        |
| :----------: | :----------------------: |
|      0       |         Success          |
|    Non-zero  |      Failure, see error code.    |

【Precautions】
> None【参考代码】

> HB_VENC_SetH265PredUnit Reference Code

### HB_VENC_SetH265Trans
【Function Declaration】
```C
int32_t HB_VENC_SetH265Trans(VENC_CHN VeChn, const VENC_H265_TRANS_S *pstH265Trans);
```
【Function Description】
> Set the transformation and quantization configuration of H.265 encoding.

【Parameter Description】

|   Parameter Name   | Description                                        | Input/Output |
| :----------------: | :------------------------------------------------- | :----------: |
|       VeChn        | Encoding channel number.<br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |
|   pstH265Trans   | Transformation and quantization configuration of H.265 protocol encoding channel |    Input     |

【Return Value】

| Return Value |               Description |
| :----------: | :----------------------- |
|       0      |               Success    |
|   Non-zero   | Failure, see error code. |

【Precautions】
> None

【Reference Code】
```C
    int32_t s32Ret = 0;
    VENC_CHN VeChn = 0;
    int32_t Width = 1920;
    int32_t Height = 1080;

    VENC_H265_TRANS_S pstH265Trans1;
    memset(&pstH265Trans1, 0, sizeof(VENC_H265_TRANS_S));
    VENC_CHN_ATTR_S m_VencChnAttr;
    memset(&m_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
    m_VencChnAttr.stVencAttr.enType = PT_H265;
    m_VencChnAttr.stVencAttr.u32PicWidth = Width;
    m_VencChnAttr.stVencAttr.u32PicHeight = Height;
    m_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
    m_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
    m_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;
    m_VencChnAttr.stGopAttr.u32GopPresetIdx = 2;
    m_VencChnAttr.stGopAttr.s32DecodingRefreshType = 2;
    m_VencChnAttr.stRcAttr.enRcMode = VENC_RC_MODE_H265CBR;
    VENC_RC_ATTR_S *pstRcParam = &(m_VencChnAttr.stRcAttr);
    s32Ret = HB_VENC_GetRcParam(VeChn, pstRcParam);
```Set the deblocking filter parameters for H.265 encoding.

【参数描述】

|   Parameter   |                          Description                          | Input/Output |
| :-----------: | :----------------------------------------------------------: | :----------: |
|    VeChn      |                Channel ID for encoding.<br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |
|  pstH265Dblk  | Deblocking filter parameters for H.265 encoding |    Input     |

【返回值】

| Return value |                          Description                          |
| :----------: | :----------------------------------------------------------: |
|      0       |                            Success                             |
|    Non-0     |                     Failure, see error code                     |

【注意事项】
> None

【参考代码】
> There is no example provided for this function> Set deblocking configuration for H.265 encoding.

【Parameter Description】

|  Parameter Name  | Description                            | Input/Output |
| :--------------: | :------------------------------------- | :----------: |
|     VeChn        | Encoding channel number.<br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |
|  pstH265Dblk     | Deblocking configuration for H.265 protocol encoding channel |    Input     |

【Return Value】

| Return Value |             Description               |
| :----------: | :----------------------------------- |
|      0       |             Success                   |
|    Non-zero  | Failure, see error code.              |

【Note】
> None

【Reference Code】
```C
    int32_t s32Ret = 0;
    VENC_CHN VeChn = 0;
    int32_t Width = 1920;
    int32_t Height = 1080;

    VENC_H265_DBLK_S pstH265Dblk1;
    memset(&pstH265Dblk1, 0, sizeof(VENC_H265_DBLK_S));
    VENC_CHN_ATTR_S m_VencChnAttr;
    memset(&m_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
    m_VencChnAttr.stVencAttr.enType = PT_H265;
    m_VencChnAttr.stVencAttr.u32PicWidth = Width;
    m_VencChnAttr.stVencAttr.u32PicHeight = Height;
    m_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
    m_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
    m_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;
    m_VencChnAttr.stGopAttr.u32GopPresetIdx = 2;
    m_VencChnAttr.stGopAttr.s32DecodingRefreshType = 2;
    m_VencChnAttr.stRcAttr.enRcMode = VENC_RC_MODE_H265CBR;
    VENC_RC_ATTR_S *pstRcParam = &(m_VencChnAttr.stRcAttr);
    s32Ret = HB_VENC_GetRcParam(VeChn, pstRcParam);
    pstRcParam->stH265Cbr.u32BitRate = 3000;
    pstRcParam->stH265Cbr.u32FrameRate = 30;
    pstRcParam->stH265Cbr.u32IntraPeriod = 30;
    pstRcParam->stH265Cbr.u32VbvBufferSize = 3000;

    s32Ret = HB_VENC_CreateChn(VeChn, &m_VencChnAttr);

    HB_VENC_SetChnAttr(VeChn, &m_VencChnAttr);
    pstH265Dblk1.slice_beta_offset_div2 = 3;
```pstH265Sao | H.265 协议编码通道的 SAO 配置                |   输入    |

【返回值】

| 返回值 |               描述 |
| :----: | :-----------------|
|   0    |               成功 |
|  非0   | 失败，参见错误码。 |

【注意事项】
> 无

【参考代码】
> 无| pstH265Sao | Sao configuration for H.265 protocol encoded channel                    |   Input    |

【Return Value】

| Return Value |               Description |
| :----: | :-----------------|
|   0    |               Success |
|  Non-zero   | Failure, see error code. |

【Notes】
> None

【Reference Code】
```C
    int32_t s32Ret = 0;
    VENC_CHN VeChn = 0;
    int32_t Width = 1920;
    int32_t Height = 1080;

    VENC_H265_SAO_S pstH265Sao1;
    memset(&pstH265Sao1, 0, sizeof(VENC_H265_SAO_S));

    VENC_CHN_ATTR_S m_VencChnAttr;
    memset(&m_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
    m_VencChnAttr.stVencAttr.enType = PT_H265;
    m_VencChnAttr.stVencAttr.u32PicWidth = Width;
    m_VencChnAttr.stVencAttr.u32PicHeight = Height;
    m_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
    m_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
    m_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;
    m_VencChnAttr.stGopAttr.u32GopPresetIdx = 2;
    m_VencChnAttr.stGopAttr.s32DecodingRefreshType = 2;
    m_VencChnAttr.stRcAttr.enRcMode = VENC_RC_MODE_H265CBR;
    VENC_RC_ATTR_S *pstRcParam = &(m_VencChnAttr.stRcAttr);
    s32Ret = HB_VENC_GetRcParam(VeChn, pstRcParam);
    pstRcParam->stH265Cbr.u32BitRate = 3000;
    pstRcParam->stH265Cbr.u32FrameRate = 30;
    pstRcParam->stH265Cbr.u32IntraPeriod = 30;
    pstRcParam->stH265Cbr.u32VbvBufferSize = 3000;

    s32Ret = HB_VENC_CreateChn(VeChn, &m_VencChnAttr);
    pstH265Sao1.sample_adaptive_offset_enabled_flag = 1;
    s32Ret = HB_VENC_SetH265Sao(VeChn, &pstH265Sao1);

    VENC_H265_SAO_S pstH265Sao2;
    memset(&pstH265Sao2, 0, sizeof(VENC_H265_SAO_S));
    s32Ret = HB_VENC_GetH265Sao(VeChn, &pstH265Sao2);
    HB_VENC_SetChnAttr(VeChn, &m_VencChnAttr);
    s32Ret = HB_VENC_DestroyChn(VeChn);
```### HB_VENC_GetH265Sao
【Function declaration】
```C
int32_t HB_VENC_GetH265Sao(VENC_CHN VeChn, VENC_H265_SAO_S *pstH265Sao);
```
【Function description】
> Get the SAO configuration of H.265 encoding.

【Parameter description】

| Parameter name | Description                                          | Input/Output |
| :------------: | :--------------------------------------------------- | :----------: |
|    VeChn       | Encoding channel number.<br/>Valid values: [0, VENC_MAX_CHN_NUM) |   Input      |
|  pstH265Sao    | SAO configuration for H.265 protocol encoding channel |   Output     |

【Return value】

| Return value |        Description       |
| :----------: | :---------------------- |
|     0        |        Success           |
|   Non-zero   |    Failure, see error codes. |

【Notes】
> None

【Reference code】
> Reference code for HB_VENC_SetH265Sao

### HB_VENC_SetIntraRefresh
【Function declaration】
```C
int32_t HB_VENC_SetIntraRefresh(VENC_CHN VeChn, const HB_VENC_INTRA_REFRESH_S *pstIntraRefresh);
```
【Function description】
> Set the parameters for refreshing P frames by inserting Islice.

【Parameter description】

| Parameter name | Description                                          | Input/Output |
| :------------: | :--------------------------------------------------- | :----------: |
|    VeChn       | Encoding channel number.<br/>Valid values: [0, VENC_MAX_CHN_NUM) |   Input      |
| pstIntraRefresh| Islice refreshing parameters                         |   Input      |

【Return value】

| Return value |        Description       |
| :----------: | :---------------------- |
|     0        |        Success           |
|   Non-zero   |    Failure, see error codes. |This function is used to get the intra refresh settings of a specified video encoding channel.

【参数说明】
- VeChn: 视频编码通道号
- pstIntraRefresh: 指向保存获取到的参数信息的结构体指针

【返回值】
- 0: 成功
- 非0: 失败> Get parameters of P frame brushing Islice.

【Parameter Description】

| Parameter Name | Description                                         | Input/Output |
| :------------: | :-------------------------------------------------- | :----------: |
|     VeChn      | Encoding channel number.<br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |
| pstIntraRefresh   | Parameters for brushing Islice                      |    Output    |

【Return Value】

| Return Value | Description |
| :----------: | :---------- |
|      0       | Success     |
|    Non-zero  | Failure, see error code. |

【Notes】
> None

【Reference Code】
> Reference code for HB_VENC_SetIntraRefresh

### HB_VENC_SetCuPrediction
【Function Declaration】
```C
int32_t HB_VENC_SetCuPrediction(VENC_CHN VeChn, const VENC_CU_PREDICTION_S * pstCuPrediction);
```
【Function Description】
> Set the tendency of CU mode prediction.

【Parameter Description】

| Parameter Name | Description                                         | Input/Output |
| :------------: | :-------------------------------------------------- | :----------: |
|     VeChn      | Encoding channel number.<br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |
| pstCuPrediction   | Parameters for selecting the tendency of CU mode     |    Input    |

【Return Value】

| Return Value | Description |
| :----------: | :---------- |
|      0       | Success     |
|    Non-zero  | Failure, see error code. |

【Notes】
> None

【Reference Code】
```C
    int32_t s32Ret = 0;
``````C
VENC_CU_PREDICTION_S pstCuPrediction2;
memset(&pstCuPrediction2, 0, sizeof(VENC_CU_PREDICTION_S));
s32Ret = HB_VENC_GetCuPrediction(VeChn, &pstCuPrediction2);
```| pstCuPrediction | Tendency parameter for CU mode selection | Output |

【Return Value】

| Return Value | Description |
| :----: | :-----------------|
|   0    | Success |
|  Non-zero   | Failure, see error code. |

【Note】
> None

【Reference Code】
> Reference code for HB_VENC_SetCuPrediction

### HB_VENC_SetJpegParam
【Function Declaration】
```C
int32_t HB_VENC_SetJpegParam(VENC_CHN VeChn, const VENC_JPEG_PARAM_S * pstJpegParam);
```
【Description】
> Set the advanced parameters for JPEG protocol encoding channel.

【Parameter Description】

|   Parameter Name   | Description                                             | Input/Output |
| :----------: | :----------------------------------------------- | :-------: |
|    VeChn     | Encoding channel number.<br/>Value range: [0, VENC_MAX_CHN_NUM) |   Input    |
| pstJpegParam | Pointer to the encoding channel attributes                                 |   Input    |

【Return Value】

| Return Value | Description |
| :----: | :-----------------|
|   0    | Success |
|  Non-zero   | Failure, see error code. |

【Note】
> None

【Reference Code】
> Reference code for HB_VENC_SetJpegParam

### HB_VENC_GetJpegParam
【Function Declaration】
```C
int32_t HB_VENC_GetJpegParam(VENC_CHN VeChn, VENC_JPEG_PARAM_S * pstJpegParam);
```
【Description】
> Get the advanced parameter settings for JPEG protocol encoding channel.【Parameter Description】

|   Parameter Name   | Description                                             | Input/Output |
| :----------------: | :------------------------------------------------------ | :----------: |
|      VeChn         | Channel number of the encoding.<br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |
|   pstJpegParam     | Pointer to the encoding channel attributes                 |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | :--------- |
|      0       | Success     |
|   Non-zero   | Failure, see error code |

【Note】
> None

【Reference Code】
> Reference code for HB_VENC_SetJpegParam

### HB_VENC_SetMjpegParam
【Function Declaration】
```C
int32_t HB_VENC_SetJpegParam(VENC_CHN VeChn, const VENC_MJPEG_PARAM_S * pstMjpegParam);
```
【Description】
> Set advanced parameters of MJPEG protocol encoding channel.

【Parameter Description】

|   Parameter Name    | Description                                             | Input/Output |
| :-----------------: | :------------------------------------------------------ | :----------: |
|       VeChn         | Channel number of the encoding.<br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |
|   pstMjpegParam     | Pointer to the encoding channel attributes                 |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | :--------- |
|      0       | Success     |
|   Non-zero   | Failure, see error code |

【Note】
> None

【Reference Code】
```C
    int32_t s32Ret = 0;
    VENC_CHN VeChn0 = 0;
```VENC_CHN VeChn1 = 1;

    int32_t Width = 1920;
    int32_t Height = 1080;
    VENC_JPEG_PARAM_S pstJpegParam;
    VENC_MJPEG_PARAM_S pstMjpegParam;
    memset(&pstJpegParam, 0, sizeof(VENC_JPEG_PARAM_S));
    memset(&pstMjpegParam, 0, sizeof(VENC_MJPEG_PARAM_S));

    VENC_CHN_ATTR_S m0_VencChnAttr;
    memset(&m0_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
    m0_VencChnAttr.stVencAttr.enType = PT_JPEG;
    m0_VencChnAttr.stVencAttr.u32PicWidth = Width;
    m0_VencChnAttr.stVencAttr.u32PicHeight = Height;
    m0_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
    m0_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
    m0_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;
    m0_VencChnAttr.stVencAttr.enPixelFormat = pixFmt;
    m0_VencChnAttr.stVencAttr.u32BitStreamBufferCount = 1;
    m0_VencChnAttr.stVencAttr.u32FrameBufferCount = 2;
    m0_VencChnAttr.stVencAttr.bExternalFreamBuffer = HB_TRUE;
    m0_VencChnAttr.stVencAttr.stAttrJpeg.dcf_enable = HB_FALSE;
    m0_VencChnAttr.stVencAttr.stAttrJpeg.quality_factor = 0;
    m0_VencChnAttr.stVencAttr.stAttrJpeg.restart_interval = 0;
    m0_VencChnAttr.stVencAttr.u32BitStreamBufSize = 4096*1096;
    VENC_CHN_ATTR_S m1_VencChnAttr;
    memset(&m1_VencChnAttr, 0, sizeof(VENC_CHN_ATTR_S));
    m1_VencChnAttr.stVencAttr.enType = PT_MJPEG;
    m1_VencChnAttr.stVencAttr.u32PicWidth = Width;
    m1_VencChnAttr.stVencAttr.u32PicHeight = Height;
    m1_VencChnAttr.stVencAttr.enMirrorFlip = DIRECTION_NONE;
    m1_VencChnAttr.stVencAttr.enRotation = CODEC_ROTATION_0;
    m1_VencChnAttr.stVencAttr.stCropCfg.bEnable = HB_FALSE;
    m1_VencChnAttr.stVencAttr.enPixelFormat = pixFmt;
    m1_VencChnAttr.stVencAttr.u32BitStreamBufferCount = 1;
    m1_VencChnAttr.stVencAttr.u32FrameBufferCount = 2;
    m1_VencChnAttr.stVencAttr.bExternalFreamBuffer = HB_TRUE;
    m1_VencChnAttr.stVencAttr.stAttrJpeg.dcf_enable = HB_FALSE;
    m1_VencChnAttr.stVencAttr.stAttrJpeg.quality_factor = 0;
    m1_VencChnAttr.stVencAttr.stAttrJpeg.restart_interval = 0;
    m1_VencChnAttr.stVencAttr.u32BitStreamBufSize = 4096*1096;

    s32Ret = HB_VENC_CreateChn(VeChn0, &m0_VencChnAttr);
    s32Ret = HB_VENC_CreateChn(VeChn1, &m1_VencChnAttr);
    HB_VENC_SetJpegParam(VeChn0, &pstJpegParam);
    HB_VENC_GetJpegParam(VeChn0, &pstJpegParam);
    HB_VENC_SetMjpegParam(VeChn1, &pstMjpegParam);
    HB_VENC_GetMjpegParam(VeChn1, &pstMjpegParam);
    s32Ret = HB_VENC_DestroyChn(VeChn0);
    s32Ret = HB_VENC_DestroyChn(VeChn1);### HB_VENC_GetMjpegParam
【Function Declaration】
```C
int32_t HB_VENC_GetMjpegParam(VENC_CHN VeChn, VENC_MJPEG_PARAM_S *pstMjpegParam);
```
【Function Description】
> Get advanced parameter settings of MJPEG protocol encoding channel.

【Parameter Description】

| Parameter Name | Description                                               | Input/Output |
| :------------: | :-------------------------------------------------------- | :-----------: |
|     VeChn      | Encoding channel number. <br/>Range: [0, VENC_MAX_CHN_NUM) |     Input     |
| pstMjpegParam  | Pointer to the attributes of encoding channel             |     Input     |

【Return Value】

| Return Value | Description     |
| :----------: | :-------------- |
|      0       | Success         |
|     Non-0     | Failed, see error code |

【Notes】
> None

【Reference Code】
> Reference code of HB_VENC_SetMjpegParam

### HB_VENC_GetFd
【Function Declaration】
```C
int32_t HB_VENC_GetFd(VENC_CHN VeChn, int32_t *fd);
```
【Function Description】
> Get the device file handle corresponding to the encoding channel.

【Parameter Description】

| Parameter Name | Description                                               | Input/Output |
| :------------: | :-------------------------------------------------------- | :-----------: |
|     VeChn      | Encoding channel number. <br/>Range: [0, VENC_MAX_CHN_NUM) |     Input     |
|       fd       | Return encoding channel file handle                       |     Input     |

【Return Value】

| Return Value | Description     |
| :----------: | :-------------- |
|      0       | Success         ||  HB_VENC_CloseFd  |
【Function Declaration】
```C
int32_t HB_VENC_GetFd(VENC_CHN VeChn, int32_t fd)
```【Function Description】
> Close the device file handle corresponding to the encoding channel.

【Parameter Description】

| Parameter Name | Description                                       | Input/Output |
| :------------: | :------------------------------------------------ | :----------: |
|    VeChn       | Encoding channel number.<br/>Value range: [0, VENC_MAX_CHN_NUM) |     Input    |
|      fd        | Input encoding channel file handle                |     Input    |

【Return Value】

| Return Value |      Description    |
| :----------: | :------------------ |
|       0      |      Success        |
|     Non-zero | Failed, refer to error code. |

【Note】
> None

【Reference Code】
> Reference code for HB_VENC_GetFd

### HB_VENC_QueryStatus
【Function Declaration】
```C
int32_t HB_VENC_QueryStatus(VENC_CHN VeChn, , VENC_CHN_STATUS_S *pstStatus)
```
【Function Description】
> Get the status of the encoding channel.

【Parameter Description】

| Parameter Name | Description                                       | Input/Output |
| :------------: | :------------------------------------------------ | :----------: |
|    VeChn       | Encoding channel number.<br/>Value range: [0, VENC_MAX_CHN_NUM) |     Input    |
| pstStatus      | Pointer to the status of the encoding channel     |     Input    |

【Return Value】

| Return Value |      Description    |
| :----------: | :------------------ |
|       0      |      Success        |
|     Non-zero | Failed, refer to error code. |

【Note】
> None

【Reference Code】### HB_VENC_InserUserData
【Function Declaration】
```C
int32_t HB_VENC_InserUserData(VENC_CHN VeChn, uint8_t *pu8Data,
                            uint32_t u32Len)
```
【Function Description】
> Insert user data into encoding channel.

【Parameter Description】

| Parameter Name | Description                                                | Input/Output |
| :------------: | :-------------------------------------------------------- | :----------: |
|     VeChn      | Encoding channel number.<br/>Value Range: [0, VENC_MAX_CHN_NUM) |     Input    |
|    pu8Data     | Pointer to the user data                                  |     Input    |
|     u32Len     | Length of the user data                                   |     Input    |

【Return Value】

| Return Value |       Description      |
| :----------: | :--------------------- |
|      0       |        Success         |
|     Non-0    | Failure, see error code.|

【Notes】
> None

【Reference Code】

### HB_VENC_SetChnParam
【Function Declaration】
```C
int32_t HB_VENC_SetChnParam(VENC_CHN VeChn, const VENC_CHN_PARAM_S *pstChnParam)
```
【Function Description】
> Set frame rate control parameters for the encoding channel.

【Parameter Description】

|  Parameter Name  | Description                                                | Input/Output |
| :--------------: | :-------------------------------------------------------- | :----------: |
|      VeChn       | Encoding channel number.<br/>Value Range: [0, VENC_MAX_CHN_NUM) |     Input    |
|   pstChnParam    | Frame rate control parameters                             |     Input    |

【Return Value】

| Return Value |       Description      |
| :----------: | :--------------------- |
|      0       |        Success         |
|     Non-0    | Failure, see error code. |【Notice】
>  N/A

【Reference Code】
> N/A

### HB_VENC_GetChnParam
【Function Declaration】
```C
int32_t HB_VENC_GetChnParam(VENC_CHN VeChn, VENC_CHN_PARAM_S *pstChnParam)
```
【Function Description】
> Get frame rate control parameters of the encoding channel.

【Parameter Description】

|  Parameter Name  |                   Description                        |   Input/Output   |
| :--------------: | :-------------------------------------------------- | :--------------: |
|      VeChn       |        Encoding channel number.<br/>Range: [0, VENC_MAX_CHN_NUM)     |       Input       |
|   pstChnParam    |        Frame rate control parameters        |      Output       |

【Return Value】

| Return Value |                   Description                    |
| :----------: | :---------------------------------------------- |
|      0       |                     Success                      |
|   Non-zero   |              Failure, see error code.              |

【Notice】
>  N/A

【Reference Code】
> N/A

### HB_VENC_SetModParam
【Function Declaration】
```C
int32_t HB_VENC_SetModParam(VENC_CHN VeChn, const VENC_PARAM_MOD_S *pstModParam)
```
【Function Description】
> Set whether VPS, SPS, PPS, and IDR of the encoding channel are output in one frame.

【Parameter Description】

|  Parameter Name  |                   Description                        |   Input/Output   |
| :--------------: | :-------------------------------------------------- | :--------------: |
|      VeChn       |        Encoding channel number.<br/>Range: [0, VENC_MAX_CHN_NUM)     |       Input       |
|   pstModParam    |        Pointer to ModParam                |       Input       |【Return Value】

| Return Value | Description |
| :----------: | :---------- |
|     0        | Success     |
|   Non-zero   | Failure, see error code. |

【Note】

> None

【Reference Code】

### HB_VENC_GetModParam
【Function Declaration】
```C
int32_t HB_VENC_GetModParam(VENC_CHN VeChn, VENC_PARAM_MOD_S *pstModParam)
```
【Function Description】
> Get whether the encoding channel VPS, SPS, PPS, IDR output in one frame.

【Parameter Description】

|   Parameter Name   | Description                                    | Input/Output |
| :---------------:  | :--------------------------------------------  | :-----------:|
|       VeChn        | Encoding channel number. <br/>Range: [0, VENC_MAX_CHN_NUM) |    Input     |
|    pstModParam     | Pointer to ModParam                            |   Output     |

【Return Value】

| Return Value | Description |
| :----------: | :---------- |
|     0        | Success     |
|   Non-zero   | Failure, see error code. |

【Note】

> None

【Reference Code】

### HB_VENC_SendFrameEx
【Function Declaration】
```C
int32_t HB_VENC_SendFrameEx(VENC_CHN VeChn, const USER_FRAME_INFO_S *pstFrame, int32_t s32MilliSec)
```
【Function Description】
> User sends the original image and its QpMap table for encoding.

【Parameter Description】

|   Parameter Name   | Description                                    | Input/Output || :---------: | :----------------------------------------------- | :-------: |
|    VeChn    | Channel number for encoding. <br/>Value range: [0, VENC_MAX_CHN_NUM) |   Input    |
|  pstFrame   | Pointer to the structure of original image information.                           |   Input    |
| s32MilliSec | Timeout                                     |   Input    |

【Return Value】

| Return Value |               Description |
| :----: | :-----------------|
|   0    |               Success |
|  Non-zero   | Failure, see error code. |

【Notes】
> None

【Reference Code】

### HB_VENC_SetAverageQp
【Function Declaration】
```C
int32_t HB_VENC_SetAverageQp(VENC_CHN VeChn, int averageQp)
```
【Functional Description】
> Set relative Qpmap averageQp.

【Parameter Description】

| Parameter Name  | Description                                             | Input/Output |
| :-------: | :----------------------------------------------- | :-------: |
|   VeChn   | Channel number for encoding. <br/>Value range: [0, VENC_MAX_CHN_NUM) |   Input    |
| averageQp | Relative QPMAP averageqp                              |   Input    |

【Return Value】

| Return Value |               Description |
| :----: | :-----------------|
|   0    |               Success |
|  Non-zero   | Failure, see error code. |

【Notes】
> None

【Reference Code】

### HB_VENC_GetAverageQp
【Function Declaration】
```C
int32_t HB_VENC_GetAverageQp(VENC_CHN VeChn, int *averageQp)
```
【Functional Description】> Obtain the relative QPmap average QP.

[Parameter Description]

| Parameter Name | Description                                     | Input/Output |
| :-------------:| :---------------------------------------------- | :----------: |
|    VeChn       | Encoding channel number.<br/>Value range: [0, VENC_MAX_CHN_NUM) |   Input    |
|  averageQp     | Relative QPmap average QP                      |   Output    |

[Return Value]

| Return Value |           Description |
| :----------: | :------------------- |
|      0       |         Success      |
|   Non-zero   |    Failure. See the error code for details. |

[Note]
> None

[Sample Code]

### HB_VENC_Set3DNRParam
[Function Declaration]
```C
int32_t HB_VENC_Set3DNRParam(VENC_CHN VeChn, VENC_3DNR_PARAMS *param)
```
[Function Description]
> Set H265 3DNR parameters.

[Parameter Description]

| Parameter Name | Description                                     | Input/Output |
| :-------------:| :---------------------------------------------- | :----------: |
|     VeChn      | Encoding channel number.<br/>Value range: [0, VENC_MAX_CHN_NUM) |   Input    |
|     param      | Pointer to 3DNR parameters                        |   Input    |

[Return Value]

| Return Value |           Description |
| :----------: | :------------------- |
|      0       |         Success      |
|   Non-zero   |    Failure. See the error code for details. |

[Note]
> None

[Sample Code]

### HB_VENC_Get3DNRParam
[Function Declaration]【Function Description】
```C
int32_t HB_VENC_Get3DNRParam(VENC_CHN VeChn, VENC_3DNR_PARAMS *param)
```
【Description】
> Get the H265 3DNR parameters.

【Parameter Description】

| Parameter Name | Description                                              | Input/Output |
| :------------: | :------------------------------------------------------- | :----------: |
|     VeChn      | Encoding channel number. <br/>Value range: [0, VENC_MAX_CHN_NUM) |     Input    |
|     param      | 3DNR parameter pointer                                   |     Input    |

【Return Value】

| Return Value | Description |
| :----------: | :--------- |
|      0       |   Success   |
|     non-zero     | Failure, see error code |

【Notes】
> None.

【Reference Code】

## Data Structure
Variables in the structure cannot be adjusted dynamically and need to be set before HB_VENC_SetChnAttr. Variables that can be set dynamically can be set at any time.

### HB_PIXEL_FORMAT_E
【Description】
> Definition of the enumeration of encoder input image types.

【Structure Definition】
```C
typedef enum HB_PIXEL_FORMAT_E {
    HB_PIXEL_FORMAT_NONE = -1,
    HB_PIXEL_FORMAT_YUV420P,
    HB_PIXEL_FORMAT_NV12,
    HB_PIXEL_FORMAT_NV21,
    HB_PIXEL_FORMAT_YUV422P,
    HB_PIXEL_FORMAT_NV16,
    HB_PIXEL_FORMAT_NV61,
    HB_PIXEL_FORMAT_YUYV422,
    HB_PIXEL_FORMAT_YVYU422,
    HB_PIXEL_FORMAT_UYVY422,
    HB_PIXEL_FORMAT_VYUY422,
    HB_PIXEL_FORMAT_YUV444,
    HB_PIXEL_FORMAT_YUV444P,
    HB_PIXEL_FORMAT_NV24,
    HB_PIXEL_FORMAT_NV42,
    HB_PIXEL_FORMAT_YUV440P,
```HB_PIXEL_FORMAT_YUV400,
    HB_PIXEL_FORMAT_TOTAL,
} PIXEL_FORMAT_E;

### PAYLOAD_TYPE_E
【Description】
> Defines the enumeration of encoder types.

【Structure Definition】
```C
typedef enum {
    PT_PCMU = 0,
    PT_1016 = 1,
    PT_G721 = 2,
    PT_GSM = 3,
    PT_G723 = 4,
    PT_DVI4_8K = 5,
    PT_DVI4_16K = 6,
    PT_LPC = 7,
    PT_PCMA = 8,
    PT_G722 = 9,
    PT_S16BE_STEREO = 10,
    PT_S16BE_MONO = 11,
    PT_QCELP = 12,
    PT_CN = 13,
    PT_MPEGAUDIO = 14,
    PT_G728 = 15,
    PT_DVI4_3 = 16,
    PT_DVI4_4 = 17,
    PT_G729 = 18,
    PT_G711A = 19,
    PT_G711U = 20,
    PT_G726 = 21,
    PT_G729A = 22,
    PT_LPCM = 23,
    PT_CelB = 25,
    PT_JPEG = 26,
    PT_CUSM = 27,
    PT_NV = 28,
    PT_PICW = 29,
    PT_CPV = 30,
    PT_H261 = 31,
    PT_MPEGVIDEO = 32,
    PT_MPEG2TS = 33,
    PT_H263 = 34,
    PT_SPEG = 35,
    PT_MPEG2VIDEO = 36,
    PT_AAC = 37,
    PT_WMA9STD = 38,
```PT_HEAAC = 39,
    PT_PCM_VOICE = 40,
    PT_PCM_AUDIO = 41,
    PT_AACLC = 42,
    PT_MP3 = 43,
    PT_ADPCMA = 49,
    PT_AEC = 50,
    PT_X_LD = 95,
    PT_H264 = 96,
    PT_D_GSM_HR = 200,
    PT_D_GSM_EFR = 201,
    PT_D_L8 = 202,
    PT_D_RED = 203,
    PT_D_VDVI = 204,
    PT_D_BT656 = 220,
    PT_D_H263_1998 = 221,
    PT_D_MP1S = 222,
    PT_D_MP2P = 223,
    PT_D_BMPEG = 224,
    PT_MP4VIDEO = 230,
    PT_MP4AUDIO = 237,
    PT_VC1 = 238,
    PT_JVC_ASF = 255,
    PT_D_AVI = 256,
    PT_DIVX3 = 257,
    PT_AVS = 258,
    PT_REAL8 = 259,
    PT_REAL9 = 260,
    PT_VP6 = 261,
    PT_VP6F = 262,
    PT_VP6A = 263,
    PT_SORENSON = 264,
    PT_H265 = 265,
    PT_MAX = 266,
    PT_AMR = 1001,
    PT_MJPEG = 1002,
    PT_AMRWB = 1003,
    PT_BUTT
} PAYLOAD_TYPE_E;

【Member Description】

### HB_ROTATION_E
【Description】
> Define the rotation angle enumeration.

【Structure Definition】
```C
typedef enum HB_CODEC_ROTATION_S {
    CODEC_ROTATION_0 = 0,```CODEC_ROTATION_90 = 1,
    CODEC_ROTATION_180 = 2,
    CODEC_ROTATION_270 = 3,
    ROTATION_BUTT
} CODEC_ROTATION_E;
```
【Member explanation】

|       Member        |       Meaning       |
| :-----------------: | :-----------------: |
|  CODEC_ROTATION_0   | No rotation, 0 degrees rotation. |
|  CODEC_ROTATION_90  |     90 degrees rotation.      |
| CODEC_ROTATION_180  |     180 degrees rotation.     |
| CODEC_ROTATION_270  |     270 degrees rotation.     |

### MIRROR_FLIP_E
【Description】
> Defines an enumeration of mirror flip methods.

【Structure definition】
```C
typedef enum HB_MIRROR_FLIP_E {
    DIRECTION_NONE = 0,
    VERTICAL = 1,
    HORIZONTAL = 2,
    HOR_VER = 3,
    DIRECTION_BUTT,
} MIRROR_FLIP_E;
```
【Member explanation】

|    Member    |        Meaning       |
| :----------: | :------------------: |
| DIRECTION_NONE |    No mirror operation    |
|  HORIZONTAL   | Mirror operation along the horizontal direction |
|   VERTICAL    | Mirror operation along the vertical direction |
|   HOR_VER     | Mirror operation along both horizontal and vertical directions |

### HB_VENC_H264_PROFILE_E
【Description】
> Defines H264 profile enumeration.

【Structure definition】
```C
typedef enum HB_VENC_H264_PROFILE_E {
    HB_H264_PROFILE_UNSPECIFIED,
    HB_H264_PROFILE_BP,
    HB_H264_PROFILE_MP,
    HB_H264_PROFILE_EXTENDED,
    HB_H264_PROFILE_HP,
```HB_H264_PROFILE_HIGH10,
	HB_H264_PROFILE_HIGH422,
	HB_H264_PROFILE_HIGHT444
} VENC_H264_PROFILE_E;

### HB_VENC_H264_LEVEL
【Description】
> Defines the H264 level enumeration.

【Structure Definition】
```C
typedef enum HB_VENC_H264_LEVEL {
	HB_H264_LEVEL_UNSPECIFIED,
	HB_H264_LEVEL1 = 10,
	HB_H264_LEVEL1b = 9,
	HB_H264_LEVEL1_1 = 11,
	HB_H264_LEVEL1_2 = 12,
	HB_H264_LEVEL1_3 = 13,
	HB_H264_LEVEL2 = 20,
	HB_H264_LEVEL2_1 = 21,
	HB_H264_LEVEL2_2 = 22,
	HB_H264_LEVEL3 = 30,
	HB_H264_LEVEL3_1 = 31,
	HB_H264_LEVEL3_2 = 32,
	HB_H264_LEVEL4 = 40,
	HB_H264_LEVEL4_1 = 41,
	HB_H264_LEVEL4_2 = 42,
	HB_H264_LEVEL5 = 50,
	HB_H264_LEVEL5_1 = 51,
	HB_H264_LEVEL5_2 = 52,
} HB_H264_LEVEL_E;
```

### HB_VENC_H265_LEVEL
【Description】
> Defines the H265 level enumeration.

【Structure Definition】
```C
typedef enum HB_VENC_H265_LEVEL {
	HB_H265_LEVEL_UNSPECIFIED,
	HB_H265_LEVEL1 = 30,
	HB_H265_LEVEL2 = 60,
	HB_H265_LEVEL2_1 = 63,
	HB_H265_LEVEL3 = 90,
	HB_H265_LEVEL3_1 = 93,
	HB_H265_LEVEL4 = 120,
	HB_H265_LEVEL4_1 = 123,
	HB_H265_LEVEL5 = 150,
```typedef struct HB_VENC_ATTR_H265_S {
    VENC_H265_PROFILE_E h265_profile;
    HB_H265_LEVEL_E h265_level;
} VENC_ATTR_H265_S;
```
【成员说明】

|     成员      |             含义              |
| :-----------: | :---------------------------: |
| h265_profile  | H265 profile，不可动态配置。  |
|  h265_level   |  H265 level，不可动态配置。   |typedef struct HB_VENC_ATTR_H265_S {
    HB_BOOL main_still_picture_profile_enable;
    int32_t s32h265_tier;
    HB_BOOL transform_skip_enabled_flag;
    uint32_t lossless_mode;
    uint32_t tmvp_Enable;
    uint32_t wpp_Enable;
    HB_H265_LEVEL_E h265_level;
} VENC_ATTR_H265_S;

【Member Description】

|               Member                |                         Meaning                          |
| :-------------------------------: | :---------------------------------------------------: |
| main_still_picture_profile_enable |  Enable H265 main still picture profile, not dynamically configurable.  |
|           s32h265_tier            |           Set H265 tier information, not dynamically configurable.           |
|    transform_skip_enabled_flag    | Whether to enable transform skip for intra CU, not dynamically configurable.  |
|           lossless_mode           |           Enable lossless encoding mode, not dynamically configurable.            |
|            tmvp_Enable            | Enable temporal motion vector prediction, not dynamically configurable. |
|            wpp_Enable             |                Enable weighted prediction, not dynamically configurable.                |
|            h265_level             |               H265 level, not dynamically configurable.               |

### VENC_ATTR_MJPEG_S
【Description】
> Definition of MJPEG encoding attribute structure.

【Structure Definition】
```C
typedef struct HB_VENC_ATTR_MJPEG_S {
    uint32_t restart_interval;
    HB_BOOL huff_table_valid;
	uint8_t huff_luma_dc_bits[16];
	uint8_t huff_luma_dc_val[16];
	uint8_t huff_luma_ac_bits[16];
	uint8_t huff_luma_ac_val[256];
	uint8_t huff_chroma_dc_bits[16];
	uint8_t huff_chroma_ac_bits[16];
	uint8_t huff_chroma_dc_val[16];
	uint8_t huff_chroma_ac_val[256];
	HB_BOOL extended_sequential;
} VENC_ATTR_MJPEG_S;
```

【Member Description】

|        Member         |                           Meaning                            |
| :-----------------: | :-------------------------------------------------------: |
|  restart_interval   | Specify the number of MCU included in an independent scan sequence, not dynamically configurable. |
|  huff_table_valid   |             Whether to enable huffman table, not dynamically configurable.             |
|  huff_luma_dc_bits  |        Huffman Luma DC bit length table, not dynamically configurable.        ||        Member         |                              Meaning                              |
| :-------------------: | :---------------------------------------------------------------: |
|     dcf_enable        |              Whether to enable dcf, cannot be dynamically configured.              |
|  restart_interval     | Number of MCU included in an independent scan sequence, cannot be dynamically configured.   |
|   quality_factor      | Quality factor, the larger the value, the lower the compression ratio, the smaller the encoding quality loss, can be dynamically configured. |
|  huff_table_valid     |               Whether to enable Huffman table, cannot be dynamically configured.               |
|  huff_luma_dc_bits    |          Huffman luminance DC bit length table, cannot be dynamically configured.           |
|  huff_luma_dc_val     |           Huffman luminance DC huffvalue table, cannot be dynamically configured.           |
|  huff_luma_ac_bits    |          Huffman luminance AC bit length table, cannot be dynamically configured.          |
|  huff_luma_ac_val     |           Huffman luminance AC huffvalue table, cannot be dynamically configured.           |
| huff_chroma_dc_bits   |          Huffman chroma DC bit length table, cannot be dynamically configured.          |
| huff_chroma_ac_bits   |          Huffman chroma AC bit length table, cannot be dynamically configured.           |
| huff_chroma_dc_val    |           Huffman chroma DC huffvalue table, cannot be dynamically configured.           |
| huff_chroma_ac_val    |           Huffman chroma AC huffvalue table, cannot be dynamically configured.           |
| extended_sequential   |              12-bit mode, cannot be dynamically configured.              |【Description】
> Define the structure of the encoder properties.

【Structure Definition】
```C
typedef struct HB_VENC_ATTR_S {
    PAYLOAD_TYPE_E enType;
    uint32_t u32PicWidth;
    uint32_t u32PicHeight;
    PIXEL_FORMAT_E enPixelFormat;
    uint32_t u32FrameBufferCount;
    uint32_t u32BitStreamBufferCount;
    HB_BOOL bExternalFreamBuffer;
    uint32_t u32BitStreamBufSize;
    CODEC_ROTATION_E enRotation;
    MIRROR_FLIP_E enMirrorFlip;
    VIDEO_CROP_INFO_S stCropCfg;
    HB_BOOL bEnableUserPts;
    uint32_t vlc_buf_size;
    int32_t s32BufJoint;
    int32_t s32BufJointSize;
    union {
        VENC_ATTR_H264_S stAttrH264;
        VENC_ATTR_H265_S stAttrH265;
        VENC_ATTR_MJPEG_S stAttrMjpeg;
        VENC_ATTR_JPEG_S stAttrJpeg;
    };
} VENC_ATTR_S;
```

【Member Description】

|       Member       |                            Meaning                            |
| :----------------: | :------------------------------------------------------------: |
|       enType       |    Encoding protocol type, cannot be configured dynamically.    |
|    u32PicWidth     |     Encoded image width, cannot be configured dynamically.     |
|    u32PicHeight    |    Encoded image height, cannot be configured dynamically.     |
|   enPixelFormat   |       Pixel format, cannot be configured dynamically.          |
| u32FrameBufferCount |  Number of input framebuffer buffers, cannot be configured dynamically. |
| u32BitStreamBufferCount | Number of output bitstream buffers, cannot be configured dynamically. |
| bExternalFreamBuffer | Use user allocated input buffer, cannot be configured dynamically. |
| u32BitStreamBufSize | Size of the output bitstream buffer, cannot be configured dynamically. |
|    enRotation     |         Rotation property, cannot be configured dynamically.         |
|   enMirrorFlip    |         Mirror property, cannot be configured dynamically.         |
|     stCropCfg     |         Crop configuration, cannot be configured dynamically.         |
|   bEnableUserPts   |       Whether to use user pts, cannot be configured dynamically.        |
|    vlc_buf_size     |          Set the vlc buffer size for encoding task, cannot be configured dynamically.          |
|    s32BufJoint     |      Whether to use continuous memory cache for multiple frames, cannot be configured dynamically.       |
|   s32BufJointSize  |        Size of continuous memory used, range: 4M-50M        |
| stAttrH264/stAttrMjpeg/<br/>stAttrJpeg/stAttrH265 |    Encoder properties of a certain protocol, cannot be configured dynamically.    |### VENC_RC_MODE_E
[Description]
> Enumeration of RC modes.

[Structure Definition]
```C
typedef enum HB_VENC_RC_MODE_E {
    VENC_RC_MODE_NONE = -1,
    VENC_RC_MODE_H264CBR = 1,
    VENC_RC_MODE_H264VBR,
    VENC_RC_MODE_H264AVBR,
    VENC_RC_MODE_H264FIXQP,
    VENC_RC_MODE_H264QPMAP,
    VENC_RC_MODE_H265CBR,
    VENC_RC_MODE_H265VBR,
    VENC_RC_MODE_H265AVBR,
    VENC_RC_MODE_H265FIXQP,
    VENC_RC_MODE_H265QPMAP,
    VENC_RC_MODE_MJPEGFIXQP,
    VENC_RC_MODE_BUTT,
} VENC_RC_MODE_E;
```
[Member Description]

|          Member          |       Meaning       |
| :----------------------: | :----------------: |
|  VENC_RC_MODE_H264CBR    |   H264 CBR mode.   |
|  VENC_RC_MODE_H264VBR    |   H264 VBR mode.   |
|  VENC_RC_MODE_H264AVBR   |  H264 AVBR mode.   |
| VENC_RC_MODE_H264FIXQP   |  H264 Fixqp mode.  |
| VENC_RC_MODE_H264QPMAP   | H.264 QPMAP mode.  |
| VENC_RC_MODE_MJPEGFIXQP  | MJPEG Fixqp mode.  |
|  VENC_RC_MODE_H265CBR    |   H265 CBR mode.   |
|  VENC_RC_MODE_H265VBR    |   H265 VBR mode.   |
|  VENC_RC_MODE_H265AVBR   |   H265 VBR mode.   |
| VENC_RC_MODE_H265FIXQP   |  H265 Fixqp mode.  |
| VENC_RC_MODE_H265QPMAP   |  H265 QPMAP mode.  |

### VENC_H264_CBR_S
[Description]
> Definition of H.264 encoding channel CBR attribute structure.

[Structure Definition]
```C
typedef struct HB_VENC_H264_CBR_S {
    uint32_t u32IntraPeriod;
    uint32_t u32IntraQp;
    uint32_t u32BitRate;
    uint32_t u32FrameRate;
    uint32_t u32InitialRcQp;
```uint32_t u32BitRate;
    uint32_t u32InitialRcQp;
    uint32_t u32VbvBufferSize;
    HB_BOOL bMbLevelRcEnable;
    uint32_t u32MaxIQp;
    uint32_t u32MinIQp;
    uint32_t u32MaxPQp;
    uint32_t u32MinPQp;
    uint32_t u32MaxBQp;
    uint32_t u32MinBQp;
    HB_BOOL bHvsQpEnable;
    int32_t s32HvsQpScale;
    uint32_t u32MaxDeltaQp;
    HB_BOOL bQpMapEnable;
} VENC_H264_CBR_S;

【Member Description】

|       Member       |Meaning|
| :--------------: | :---------------------: |
|  u32IntraPeriod  |The interval between I frames, dynamically configurable.|
|    u32IntraQp    |The QP value of I frames, dynamically configurable. The smaller the value, the better the image quality.|
|    u32BitRate    |The target average bit rate, in kbps, dynamically configurable.|
|   u32FrameRate   |The target frame rate, in fps, dynamically configurable.|
|  u32InitialRcQp  |The initial QP value for rate control. If the value is not within the range [0,51], the encoder will determine the initial value internally, and it cannot be dynamically configured.|
| u32VbvBufferSize |The actual size of the VBV buffer space in bits is bit_rate * vbv_buffer_size / 1000 (kb). The size of this buffer affects the image encoding quality and rate control accuracy. When the buffer is small, the rate control accuracy is high, but the image encoding quality is poor. When the buffer is large, the image encoding quality is high, but the rate fluctuates greatly. Dynamically configurable. |
| bMbLevelRcEnable |H264 rate control can work at the macroblock level, which can achieve higher precision rate control, but it will reduce the image encoding quality. This mode cannot work together with ROI encoding. When ROI encoding is enabled, this function is automatically disabled. Not dynamically configurable.|
|    u32MaxIQp     |The maximum QP value of I frames, dynamically configurable.|
|    u32MinIQp     |The minimum QP value of I frames, dynamically configurable.|
|    u32MaxPQp     |The maximum QP value of P frames, dynamically configurable.|
|    u32MinPQp     |The minimum QP value of P frames, dynamically configurable.|
|    u32MaxBQp     |The maximum QP value of B frames, dynamically configurable.|
|    u32MinBQp     |The minimum QP value of B frames, dynamically configurable.|
|   bHvsQpEnable   |H264 rate control can work at the sub-macroblock level, which can adjust the QP value of sub-macroblocks and improve the subjective image quality. Dynamically configurable.|
|  s32HvsQpScale   |Valid when hvs_qp_enable is enabled, this value represents the QP scaling factor. Dynamically configurable.|
|  u32MaxDeltaQp   |Valid when hvs_qp_enable is enabled, specifies the maximum deviation range of HVS qp value. Dynamically configurable.|
|   bQpMapEnable   |Whether to enable Qp map, dynamically configurable.|

Note: The rate control module calculates the bit rate. If the bit rate is smaller than the set bit rate, it will decrease the QP value. If the QP value is smaller than qpmin, it cannot be adjusted, resulting in the image not achieving the expected quality. If the bit rate is larger than the set bit rate, it will increase the QP value. If the QP value is larger than qpmax, it cannot be adjusted, and the bit rate will always be larger than the set bit rate, unable to achieve the set bit rate./*** Struct definition ***/
typedef struct HB_VENC_H264_AVBR_S
{
    uint32_t u32IntraPeriod;
    uint32_t u32IntraQp;
    uint32_t u32BitRate;
    uint32_t u32FrameRate;
    uint32_t u32InitialRcQp;
    uint32_t u32VbvBufferSize;
    HB_BOOL bMbLevelRcEnable;
    uint32_t u32MaxIQp;
    uint32_t u32MinIQp;
    uint32_t u32MaxPQp;
    uint32_t u32MinPQp;
    uint32_t u32MaxBQp;
    uint32_t u32MinBQp;
    HB_BOOL bHvsQpEnable;
    int32_t s32HvsQpScale;
    uint32_t u32MaxDeltaQp;
    HB_BOOL bQpMapEnable;
} VENC_H264_AVBR_S;

/*** Member Description ***/
| Member Name      | Meaning                      |
| :--------------: | :--------------------------: |
| u32IntraPeriod   | I-frame interval, dynamically configurable. |
| u32IntraQp       | QP value for I-frame, dynamically configurable. |
| u32BitRate       | Target average bitrate in kbps, dynamically configurable. |
| u32FrameRate     | Target frame rate in fps, dynamically configurable. |
| u32InitialRcQp   | Initial QP value for rate control. If the value is not within the range of [0,51], the encoder will determine the initial value internally. Cannot be dynamically configured. |
| u32VbvBufferSize | The actual size of the VBV buffer is calculated by bit_rate * vbv_buffer_size / 1000 (kb). The size of this buffer affects the image quality and the accuracy of rate control. When the buffer is small, the rate control accuracy is high, but the image quality is poor. When the buffer is large, the image quality is high but the rate fluctuation is large. Dynamically configurable. |
| bMbLevelRcEnable | The rate control of H.264 can work at the macroblock level. This mode can achieve higher accuracy rate control but sacrifices image quality. This mode cannot work together with ROI encoding. When ROI encoding is enabled, this function is automatically disabled. Cannot be dynamically configured. |
| u32MaxIQp        | Maximum QP value for I-frame, dynamically configurable. |
| u32MinIQp        | Minimum QP value for I-frame, dynamically configurable. ||         成员         |               含义                |
| :------------------: | :-------------------------------: |
|    u32IntraPeriod    |       I帧间隔，可动态配置。       |
|     u32FrameRate     | 目标帧率，单位是fps，可动态配置。 |
|  u32QpMapArrayCount  |        QP值数组的长度。          |
|    u32QpMapArray     |          QP值数组，可动态配置。   ||       Member       |                                        Meaning                                         |
| :----------------: | :-----------------------------------------------------------------------------------: |
|   u32IntraPeriod   |                             I-frame interval, configurable dynamically.                              |
|    u32FrameRate    |                              Target frame rate in fps, configurable dynamically.                               |
|   u32QpMapArray    |                             Specify the QP map table. Each macroblock in H264 is 16x16 and requires a QP value. Each QP value takes up one byte and is sorted in a raster scan direction. Configurable dynamically. |
| u32QpMapArrayCount |                               Specify the size of the QP map table, configurable dynamically.                                |

### VENC_H265_CBR_S
【Description】
> Define CBR attribute structure for H.265 encoding channel.

【Structure Definition】
```C
typedef struct HB_VENC_H265_CBR_S {
    uint32_t u32IntraPeriod;
    uint32_t u32IntraQp;
    uint32_t u32BitRate;
    uint32_t u32FrameRate;
    uint32_t u32InitialRcQp;
    uint32_t u32VbvBufferSize;
    HB_BOOL bCtuLevelRcEnable;
    uint32_t u32MaxIQp;
    uint32_t u32MinIQp;
    uint32_t u32MaxPQp;
    uint32_t u32MinPQp;
    uint32_t u32MaxBQp;
    uint32_t u32MinBQp;
    HB_BOOL bHvsQpEnable;
    int32_t s32HvsQpScale;
    uint32_t u32MaxDeltaQp;
    HB_BOOL bQpMapEnable;
} VENC_H265_CBR_S;
```
【Member Description】

|       Member       |                                          Meaning                                           |
| :----------------: | :--------------------------------------------------------------------------------------: |
|  u32IntraPeriod    |                                 I-frame interval, configurable dynamically.                                  |
|    u32IntraQp      |                                    QP value for I-frame, configurable dynamically.                                    |
|    u32BitRate      |                          Target average bit rate in kbps, configurable dynamically.                          |
|   u32FrameRate     |                                 Target frame rate in fps, configurable dynamically.                                  |
|  u32InitialRcQp    |                    Initial QP value for rate control. If the value is not in the range [0,51], the encoder will decide the initial value internally. Not configurable dynamically.                    |
| u32VbvBufferSize   | The actual space size of the VBV buffer is bit_rate * vbv_buffer_size / 1000 (kb), and this buffer size affects the image quality and rate control precision. A smaller buffer size will result in better rate control accuracy but poorer image quality, while a larger buffer size will provide higher image quality but larger rate fluctuations. Configurable dynamically. |
|bMbLevelRcEnable|The rate control for H264 can work at the macroblock level, which can achieve higher precision rate control but sacrifices image encoding quality. This mode cannot work together with ROI encoding. When ROI encoding is enabled, this function is automatically disabled. Configurable dynamically.|
|u32MaxIQp|Maximum QP value for I-frame, configurable dynamically.|
|u32MinIQp|Minimum QP value for I-frame, configurable dynamically.|
|u32MaxPQp|Maximum QP value for P-frame, configurable dynamically.|
|u32MinPQp|Minimum QP value for P-frame, configurable dynamically.|
|u32MaxBQp|Maximum QP value for B-frame, configurable dynamically.|
|u32MinBQp|Minimum QP value for B-frame, configurable dynamically.||bHvsQpEnable|H.264 bitrate control can work at the sub-macroblock level, adjusting the QP values of the sub-macroblocks to improve subjective image quality. It can be dynamically configured.|
|s32HvsQpScale|Valid when hvs_qp_enable is enabled. This value represents the QP scaling factor and can be dynamically configured.|
|u32MaxDeltaQp|Valid when hvs_qp_enable is enabled. Specifies the maximum deviation range of the HVS qp value and can be dynamically configured.|
|bQpMapEnable|Whether to enable Qp map. It can be dynamically configured.|

### VENC_H265_VBR_S
【Description】
> Defines the VBR attribute structure for H.265 encoding channel.

【Structure Definition】
```C
typedef struct HB_VENC_H265_VBR_S {
    uint32_t u32IntraPeriod;
    uint32_t u32IntraQp;
    uint32_t u32FrameRate;
    HB_BOOL bQpMapEnable;
} VENC_H265_VBR_S;
```
【Member Description】

|     Member     |           Description           |
| :------------: | :-------------------------------: |
| u32IntraPeriod |     Intra frame period, can be dynamically configured.     |
|   u32IntraQp   |       QP value of intra frame, can be dynamically configured.      |
|  u32FrameRate  |         Frame rate, can be dynamically configured.          |
|  bQpMapEnable  |   Whether to enable Qp map, can be dynamically configured.   |

### VENC_H265_AVBR_S
【Description】
> Defines the AVBR attribute structure for H.265 encoding channel.

【Structure Definition】
```C
typedef struct HB_VENC_H265_AVBR_S {
    uint32_t u32IntraPeriod;
    uint32_t u32IntraQp;
    uint32_t u32BitRate;
    uint32_t u32FrameRate;
    uint32_t u32InitialRcQp;
    uint32_t u32VbvBufferSize;
    HB_BOOL bCtuLevelRcEnable;
    uint32_t u32MaxIQp;
    uint32_t u32MinIQp;
    uint32_t u32MaxPQp;
    uint32_t u32MinPQp;
    uint32_t u32MaxBQp;
    uint32_t u32MinBQp;
    HB_BOOL bHvsQpEnable;
    int32_t s32HvsQpScale;
    uint32_t u32MaxDeltaQp;
``````C
【描述】
> 定义 H.265 编码通道 Qpmap 属性结构。

【结构定义】
```C
typedef struct HB_VENC_H265_QPMAP_S {
    uint32_t u32MaxQp;
    uint32_t u32MinQp;
    HB_BOOL bQpMapEnable;
} VENC_H265_QPMAP_S;
```

【成员说明】

|      成员      |              含义               |
| :------------: | :-----------------------------: |
|   u32MaxQp     | Qpmap映射的最大QP值，可动态配置。 |
|   u32MinQp     | Qpmap映射的最小QP值，可动态配置。 |
| bQpMapEnable   |    是否使能Qp map，可动态配置。   |
```【Description】
Define the QPMAP attribute structure for H.265 encoding channel.

【Structure Definition】
```C
typedef struct HB_VENC_H265_QPMAP_S {
    uint32_t u32IntraPeriod;
    uint32_t u32FrameRate;
    unsigned char * u32QpMapArray;
    uint32_t u32QpMapArrayCount;
} VENC_H265_QPMAP_S;
```
【Member Explanation】

|      Member      |                                                    Meaning                                                     |
| :--------------: | :-----------------------------------------------------------------------------------------------------------: |
| u32IntraPeriod   |                                          I-frame interval, can be dynamically configured.                                          |
|  u32FrameRate    |                                    Target frame rate, in fps, can be dynamically configured.                                    |
| u32QpMapArray    | Specify QP map table. The macroblock size of H.264 is 16x16, and each macroblock needs to be assigned a QP value. Each QP value occupies one byte, and the order is sorted in a raster scan direction. Can be dynamically configured. |
| u32QpMapArrayCount |                     Specify the size of the QP map table, can be dynamically configured.                      |

### VENC_MJPEG_FIXQP_S
【Description】
Define the Fixqp attribute structure for MJPEG encoding channel.

【Structure Definition】
```C
typedef struct HB_VENC_MJPEG_FIXQP_S {
    uint32_t u32FrameRate;
    uint32_t u32QualityFactort;
} VENC_MJPEG_FIXQP_S;
```
【Member Explanation】

|       Member       |                                                   Meaning                                                   |
| :----------------: | :--------------------------------------------------------------------------------------------------------: |
|   u32FrameRate     |                                    Target frame rate, in fps, can be dynamically configured.                                    |
| u32QualityFactort  | Quantification factor. When this value is 100, the image quality loss of the encoded image is minimum but the compression ratio is low. When this value is 1, the image quality loss is greater but the compression ratio is high. Can be dynamically configured. |

### VENC_RC_ATTR_S
【Description】
Define the rate control attributes for encoding channel.

【Structure Definition】
```C
typedef struct HB_VENC_RC_ATTR_S {
    VENC_RC_MODE_E enRcMode;
    union {
        VENC_H264_CBR_S stH264Cbr;
        VENC_H264_VBR_S stH264Vbr;
```VENC_H264_AVBR_S stH264AVbr;
        VENC_H264_FIXQP_S stH264FixQp;
        VENC_H264_QPMAP_S stH264QpMap;
        VENC_MJPEG_FIXQP_S stMjpegFixQp;
        VENC_H265_CBR_S stH265Cbr;
        VENC_H265_VBR_S stH265Vbr;
        VENC_H265_AVBR_S stH265AVbr;
        VENC_H265_FIXQP_S stH265FixQp;
        VENC_H265_QPMAP_S stH265QpMap;
    };
} VENC_RC_ATTR_S;
```
【Member Explanation】

|     Member     |                Meaning                |
| :----------: | :---------------------------------: |
|   enRcMode   |       RC mode, not dynamically configurable.       |
|  stH264Cbr   |  H.264 protocol coding channel Cbr mode attribute.  |
|  stH264Vbr   |  H.264 protocol coding channel Vbr mode attribute.  |
|  stH264AVbr  | H.264 protocol coding channel AVbr mode attribute.  |
| stH264FixQp  | H.264 protocol coding channel Fixqp mode attribute. |
| stH264QpMap  | H.264 protocol coding channel QpMap mode attribute. |
| stMjpegFixQp | Mjpeg protocol coding channel Fixqp mode attribute. |
|  stH265Cbr   |  .265 protocol coding channel Cbr mode attribute.   |
|  stH265Vbr   |  H.265 protocol coding channel Vbr mode attribute.  |
|  stH265AVbr  | H.265 protocol coding channel AVbr mode attribute.  |
| stH265FixQp  | H.265 protocol coding channel Fixqp mode attribute. |
| stH265QpMap  | H.265 protocol coding channel QpMap mode attribute. |

### VENC_GOP_PICTURE_CUSTOM_S
【Description】
> Defines the data structure of the custom GOP structure table.

【Structure Definition】
```C
typedef struct HB_VENC_GOP_PICTURE_CUSTOM_S {
    uint32_t u32PictureType;
    int32_t s32PocOffset;
    uint32_t u32PictureQp;
    int32_t s32NumRefPictureL0;
    int32_t s32RefPocL0;
    int32_t s32RefPocL1;
    uint32_t u32TemporalId;
} VENC_GOP_PICTURE_CUSTOM_S;
```
【Member Explanation】

|        Member        |                                                   Meaning                                                   |
| :----------------: | :------------------------------------------------------------------------------------------------------: |
|   u32PictureType   |                                       Frame type of the image, not dynamically configurable.                                       ||          成员          |               含义               |
| :--------------------: | :------------------------------: |
|     s32PocOffset       | 图像的POC值，不可动态配置。 |
|     u32PictureQp       |  图像的QP值，不可动态配置。 |
| s32NumRefPictureL0 | 当前图像参考的L0的帧数量，只有当pic_type=1时，该值有效，不可动态配置。 |
|     s32RefPocL0      | 当前图像的L0参考帧的POC值，不可动态配置。|
|     s32RefPocL1      | 当pic_type=2，表示当前图像的L1参考帧的POC值；当pic_type=1，表示当前图像的L0参考帧的POC值，不可动态配置。 |
|     u32TemporalId     | 图像的temporal id，不可动态配置。 |
typedef struct HB_VENC_CHN_ATTR_S {
    VENC_ATTR_S stVencAttr;
    VENC_RC_ATTR_S stRcAttr;
    VENC_GOP_ATTR_S stGopAttr;
} VENC_CHN_ATTR_S;

【Member Description】

|    Member    |          Meaning          |
| :--------: | :---------------------: |
| stVencAttr |      Encoder Attributes       |
|  stRcAttr  |    Rate Control Attributes     |
| stGopAttr  | Structure of Gop Mode Type    |

### VENC_JPEG_PARAM_S
【Description】
> Defines the advanced parameters structure for JPEG protocol encoding channel.

【Structure Definition】
```C
typedef struct HB_VENC_JPEG_PARAM_S {
    uint32_t u32Qfactor;
    uint8_t  u8LumaQuantTable[64];
    uint8_t u8ChromaQuantTable[64];
    uint16_t u16LumaQuantEsTable[64];
    uint16_t u16ChromaQuantEsTable[64];
    uint32_t u32RestartInterval;
    VIDEO_CROP_INFO_S stCropCfg;
} VENC_JPEG_PARAM_S;
```
【Member Description】

|         Member          |                               Meaning                               |
| :-------------------: | :--------------------------------------------------------------: |
|      u32Qfactor       |   Refer to RFC2435 protocol for specific meaning, default value is 90. Range: [1, 99].   |
|   u8LumaQuantTable    |              8-bit Y Quantization Table. Range: [0, 255].               |
|  u8ChromaQuantTable   |             8-bit CbCr Quantization Table. Range: [0, 255].             |
|  u16LumaQuantEsTable  |              12-bit Y Quantization Table. Range: [0, 255].              |
| u16ChromaQuantEsTable |            12-bit CbCr Quantization Table. Range: [0, 255].             |
|  u32RestartInterval   | u32RestartInterval: [0, (picwidth+15)>>4 x(picheight+15)>>4 x 2] |
|       stCropCfg       |                           Crop Configuration Parameters                           |

### VENC_MJPEG_PARAM_S
【Description】
> Defines the advanced parameters structure for MJPEG protocol encoding channel.

【Structure Definition】
```C
typedef struct HB_VENC_MJPEG_PARAM_S {
    uint8_t  u8LumaQuantTable [64];
```typedef struct HB_VENC_INTRA_REFRESH_S
{
    HB_BOOL bRefreshEnable;
    VENC_INTRA_REFRESH_MODE_E enIntraRefreshMode;
【描述】
> 定义H265去块滤波参数。

【结构定义】
```C
typedef struct HB_VENC_H265_DBLK_S
{
    uint32_t disable_deblocking_filter_idc;
    int32_t slice_beta_offset_div2;
    int32_t slice_tc_offset_div2;
} VENC_H265_DBLK_S;
```
【成员说明】

|             成员              |                                含义                                 |
| :---------------------------: | :-----------------------------------------------------------------: |
| disable_deblocking_filter_idc | 取值范围：[0, 2], 默认值 0，具体含义请参见 H.265 协议，可动态配置。 |
|    slice_beta_offset_div2     | 取值范围：[-6, 6], 默认值 0，具体含义请参见 H.265 协议，可动态配置。 |
|     slice_tc_offset_div2      | 取值范围：[-6, 6], 默认值 0，具体含义请参见 H.265 协议，可动态配置。 |{
    uint32_t aspect_ratio_info_present_flag;
    uint32_t aspect_ratio_idc;
    uint32_t sar_width;
    uint32_t sar_height;
    uint32_t overscan_info_present_flag;
    uint32_t overscan_appropriate_flag;
    uint32_t video_signal_type_present_flag;
    uint32_t video_format;
    uint32_t video_full_range_flag;
    uint32_t colour_description_present_flag;
    uint32_t colour_primaries;
    uint32_t transfer_characteristics;
    uint32_t matrix_coefficients;
    uint32_t chroma_loc_info_present_flag;
    uint32_t chroma_sample_loc_type_top_field;
    uint32_t chroma_sample_loc_type_bottom_field;
    uint32_t timing_info_present_flag;
    VENC_VUI_H264_TIME_INFO_S timing_info;
    uint32_t nal_hrd_parameters_present_flag;
    uint32_t vcl_hrd_parameters_present_flag;
    uint32_t low_delay_hrd_flag;
    uint32_t pic_struct_present_flag;
    uint32_t bitstream_restriction_flag;
    uint32_t motion_vectors_over_pic_boundaries_flag;
    uint32_t max_bytes_per_pic_denom;
    uint32_t max_bits_per_mb_denom;
    uint32_t log2_max_mv_length_horizontal;
    uint32_t log2_max_mv_length_vertical;
    uint32_t num_reorder_frames;
    uint32_t max_dec_frame_buffering;
}VENC_H264_VUI_S;
```
【成员说明】

|              成员               |                             含义                             |
| :----------------------------: | :----------------------------------------------------------: |
|  aspect_ratio_info_present_flag  |           Indicate the presence of aspect ratio info.           |
|            aspect_ratio_idc            | Specify the aspect ratio. |
|              sar_width               |     Specify the width of the sample aspect ratio.     |
|             sar_height              |    Specify the height of the sample aspect ratio.    |
|  overscan_info_present_flag  |         Indicate the presence of overscan info.         |
|   overscan_appropriate_flag   |    Indicate whether overscan should be deployed.    |
|  video_signal_type_present_flag  |        Indicate the presence of video signal type info.        |
|            video_format            |            Specify the format of the video signal.            |
|    video_full_range_flag    |          Specify the range of the digitized video.          |
|  colour_description_present_flag  |     Indicate the presence of colour description info.     |
|       colour_primaries        |      Specify the chromaticity coordinates of the source primaries.      |
| transfer_characteristics  | Indicate the transfer characteristics of the source picture. |
|     matrix_coefficients    | Specify the matrix coefficients used in deriving luma and chroma signals. |
|chroma_loc_info_present_flag| Indicate the presence of chroma sample location info. |
|chroma_sample_loc_type_top_field| Specify the chromaticity sample location for the top field. |
|chroma_sample_loc_type_bottom_field| Specify the chromaticity sample location for the bottom field. |
|timing_info_present_flag| Indicate the presence of HRD timing and buffering parameters. |
|timing_info| Specify the HRD timing and buffering parameters. |
|nal_hrd_parameters_present_flag| Indicate the presence of NAL HRD parameters. |
|vcl_hrd_parameters_present_flag| Indicate the presence of VCL HRD parameters. |
|low_delay_hrd_flag| Specify whether the HRD buffer delay is low or not. |
|pic_struct_present_flag| Indicate the presence of pic_struct syntax. |
|bitstream_restriction_flag| Indicate the presence of bitstream restriction parameters. |
|motion_vectors_over_pic_boundaries_flag| Indicate whether motion vectors extend beyond picture boundaries. |
|max_bytes_per_pic_denom| Specify the maximum number of bytes occupied by a picture. |
|max_bits_per_mb_denom| Specify the maximum number of bits occupied by a macroblock. |
|log2_max_mv_length_horizontal| Specify the maximum absolute value of a horizontal motion vector component. |
|log2_max_mv_length_vertical| Specify the maximum absolute value of a vertical motion vector component. |
|num_reorder_frames| Specify the number of frame reordering delay. |
|max_dec_frame_buffering| Specify the value of max_dec_frame_buffering. |{
    VENC_VUI_H264_TIME_INFO_S stVuiTimeInfo;
}VENC_H264_VUI_S;
```
【Member Description】

|     Member      | Meaning  |
| :-----------: | :---: |
| stVuiTimeInfo | H264 Timing parameters |

### VENC_VUI_H265_TIME_INFO_S
【Description】
> Defines H265 Timing parameters.

【Struct Definition】
```C
typedef struct HB_VENC_VUI_H265_TIME_INFO_S
{
    uint32_t num_units_in_tick;
    uint32_t time_scale;
    uint32_t num_ticks_poc_diff_one_minus1;
}VENC_VUI_H265_TIME_INFO_S;
```
【Member Description】

|             Member              |               Meaning               |
| :---------------------------: | :------------------------------: |
|       num_units_in_tick       | Based on H265 specifications, cannot be dynamically set. |
|          time_scale           | Based on H265 specifications, cannot be dynamically set. |
| num_ticks_poc_diff_one_minus1 | Based on H265 specifications, cannot be dynamically set. |

### VENC_H265_VUI_S
【Description】
> Defines Vui structure for H.264 protocol encoding channel.

【Struct Definition】
```C
typedef struct HB_VENC_H265_VUI_S
{
    VENC_VUI_H265_TIME_INFO_S stVuiTimeInfo;
}VENC_H265_VUI_S;
```
【Member Description】

|     Member      |      Meaning       |
| :-----------: | :-------------: |
| stVuiTimeInfo | H265 Timing parameters |

### VENC_H265_SAO_S
【Description】
|                成员                 |                                        含义                                        |
| :---------------------------------: | :--------------------------------------------------------------------------------: |
| h265_independent_slice_mode | 独立 slice 分割模式，可动态配置 |
| h265_independent_slice_arg | 独立 slice 参数，可动态配置，代表一个 slice 宏块个数，从左上开始，64x64的像素，定义一个宏块，图像被划分成一个个宏块，进行编码，宏块最大值(h+63)/64 *（w+63）/64 |
| h265_dependent_slice_mode | 依赖 slice 分割模式，可动态配置 |
| h265_dependent_slice_arg | 依赖 slice 参数，可动态配置，代表一个 slice 宏块个数，从左上开始，64x64的像素，定义一个宏块，图像被划分成一个个宏块，进行编码，宏块最大值(h+63)/64 *（w+63）/64 ||              Member               |                                   Meaning                                    |
| :-------------------------------: | :---------------------------------------------------------------------------: |
| h265_independent_slice_mode       |                  Independent slice encoding mode<br/>0: Disabled<br/>1: Enabled<br/>Can be dynamically configured.                  |
| h265_independent_slice_arg        |              Size of independent slice, in coding CTUs, range [0, 2^16-1]<br/>Can be dynamically configured.               |
| h265_dependent_slice_mode         | Non-independent slice encoding mode<br/>0: Disabled<br/>1: Slice unit is coding CTU<br/>2: Slice unit is byte<br/>Can be dynamically configured. |
| h265_dependent_slice_arg          |     Size of non-independent slice, range [0, 2^16-1],<br/>Can be dynamically configured.      |

### VENC_H264_INTRA_PRED_S
【Description】
> Defines the structure of intra prediction for H.264 protocol encoding channel.

【Structure Definition】
```C
typedef struct HB_VENC_H264_INTRA_PRED_S
{
    uint32_t constrained_intra_pred_flag;
} VENC_H264_INTRA_PRED_S;
```
【Member Description】

|              Member               |                         Meaning                              |
| :-------------------------------: | :---------------------------------------------------------: |
| constrained_intra_pred_flag      | Default: 0.<br/>Range: 0 or 1.<br/>Can be dynamically configured. |

### VENC_H265_PU_S
【Description】
> Defines the structure of PU parameters for H.265 protocol encoding channel.

【Structure Definition】
```C
typedef struct HB_VENC_H265_PU_S
{
    uint32_t intra_nxn_enable;
    uint32_t max_num_merge;
    uint32_t constrained_intra_pred_flag;
    uint32_t strong_intra_smoothing_enabled_flag;
} VENC_H265_PU_S;
```
【Member Description】

|                                            Member                                             |                       Meaning                       |
| :-----------------------------------------------------------------------------------------: | :-------------------------------------------------: |
|                                      intra_nxn_enable                                       |   Enable intra NxN PUs in intra CUs, can be dynamically configured    |
|                                        max_num_merge                                        |   Specify number of merge candidates in RDO, can be dynamically configured   |
|                                 constrained_intra_pred_flag                                 | Default: 0<br/>Range: 0 or 1<br/>Can be dynamically configured |
| strong_intra_smoothing_enabled_flag<br/>Default: 0<br/>Range: 0 or 1<br/>Can be dynamically configured   |

### VENC_H264_TRANS_S
【Description】
> Defines H264 transform parameters.【Structure Definition】
```C
typedef struct HB_VENC_H264_TRANS_S {
    uint32_t transform_8x8_enable;
    int32_t chroma_cb_qp_offset;
    int32_t chroma_cr_qp_offset;
    uint32_t user_scaling_list_enable;
    uint8_t scaling_list_4x4[HB_VENC_SL_MATRIX_NUM][16];
    uint8_t scaling_list_8x8[2][64];
} VENC_H264_TRANS_S;
```
【Member Description】

|         Member        |                  Meaning                   |
| :-------------------: | :----------------------------------------: |
| transform_8x8_enable  |  Enable 8x8 transform, dynamically configurable. |
| chroma_cb_qp_offset   | Specify the QP offset of cb component, dynamically configurable. |
| chroma_cr_qp_offset   | Specify the QP offset of cr component, dynamically configurable. |
| user_scaling_list_enable | Enable user-specified scaling list, not dynamically configurable. |
| scaling_list_4x4 | Specify the coefficients of 4x4 blocks, each element has 16 coefficients, not dynamically configurable. |
| scaling_list_8x8 | Specify the coefficients of 8x8 blocks, each element has 64 coefficients, not dynamically configurable. |

### VENC_H265_TRANS_S
【Description】
> Define H265 Transform parameters.

【Structure Definition】
```C
typedef struct HB_VENC_H265_TRANSFORM_PARAMS {
    int32_t chroma_cb_qp_offset;
    int32_t chroma_cr_qp_offset;
    uint32_t user_scaling_list_enable;
    uint8_t scaling_list_4x4[HB_VENC_SL_MATRIX_NUM][16];
    uint8_t scaling_list_8x8[HB_VENC_SL_MATRIX_NUM][64];
    uint8_t scaling_list_16x16[HB_VENC_SL_MATRIX_NUM][64];
    uint8_t scaling_list_32x32[2][64];
    uint8_t scaling_list_dc_16x16[HB_VENC_SL_MATRIX_NUM];
    uint8_t scaling_list_dc_32x32[2];
} VENC_H265_TRANS_S;
```
【Member Description】

|         Member        |                  Meaning                   |
| :-------------------: | :----------------------------------------: |
| chroma_cb_qp_offset   | Specify the QP offset of cb component, dynamically configurable. |
| chroma_cr_qp_offset   | Specify the QP offset of cr component, dynamically configurable. |
| user_scaling_list_enable | Enable user-specified scaling list, not dynamically configurable. |
| scaling_list_4x4 | Specify the coefficients of 4x4 blocks, each element has 16 coefficients, not dynamically configurable. |
| scaling_list_8x8 | Specify the coefficients of 8x8 blocks, each element has 64 coefficients, not dynamically configurable. ||             成员              |                      含义                       |
| :---------------------------: | :---------------------------------------------: |
|     mode_decision_enable;     | Enable mode decision, dynamically configurable. |
|       pu04_delta_rate;        |    4x4 block cost delta, dynamically configurable.    |
|       pu08_delta_rate;        |    8x8 block cost delta, dynamically configurable.    |
|       pu16_delta_rate;        |   16x16 block cost delta, dynamically configurable.   |
|       pu32_delta_rate;        |   32x32 block cost delta, dynamically configurable.   |【Translation】
| pu04_intra_planar_delta_rate; | Frame intra planar rate delta under intra prediction mode, configurable dynamically. |
| pu04_intra_dc_delta_rate;   | Frame intra dc rate delta under intra prediction mode, configurable dynamically.   |
| pu04_intra_angle_delta_rate;  | Frame intra angle rate delta under intra prediction mode, configurable dynamically. |
| pu08_intra_planar_delta_rate; | Frame intra planar rate delta under intra prediction mode, configurable dynamically. |
| pu08_intra_dc_delta_rate;   | Frame intra dc rate delta under intra prediction mode, configurable dynamically.   |
| pu08_intra_angle_delta_rate;  | Frame intra angle rate delta under intra prediction mode, configurable dynamically. |
| pu16_intra_planar_delta_rate; | Frame intra planar rate delta under intra prediction mode, configurable dynamically. |
| pu16_intra_dc_delta_rate;   | Frame intra dc rate delta under intra prediction mode, configurable dynamically.   |
| pu16_intra_angle_delta_rate;  | Frame intra angle rate delta under intra prediction mode, configurable dynamically. |
| pu32_intra_planar_delta_rate; | Frame intra planar rate delta under intra prediction mode, configurable dynamically. |
| pu32_intra_dc_delta_rate;   | Frame intra dc rate delta under intra prediction mode, configurable dynamically.   |
| pu32_intra_angle_delta_rate;  | Frame intra angle rate delta under intra prediction mode, configurable dynamically. |
| cu08_intra_delta_rate;     | Inter frame CU8x8 intra rate delta, configurable dynamically.  |
| cu08_inter_delta_rate;     | Inter frame CU8x8 inter rate delta, configurable dynamically.  |
| cu08_merge_delta_rate;     | Inter frame CU8x8 merge rate delta, configurable dynamically.  |
| cu16_intra_delta_rate;     | Inter frame CU16x16 intra rate delta, configurable dynamically.  |
| cu16_inter_delta_rate;     | Inter frame CU16x16 inter rate delta, configurable dynamically.  |
| cu16_merge_delta_rate;     | Inter frame CU16x16 merge rate delta, configurable dynamically.  |
| cu32_intra_delta_rate;     | Inter frame CU32x32 intra rate delta, configurable dynamically.  |
| cu32_inter_delta_rate;     | Inter frame CU32x32 inter rate delta, configurable dynamically.  |
| cu32_merge_delta_rate;     | Inter frame CU32x32 merge rate delta, configurable dynamically.  |

### VIDEO_CROP_INFO_S
【Description】
> Defines the cropping parameters of the video channel.

【Structure Definition】
```C
typedef struct HB_VIDEO_CROP_INFO_S
{
    HB_BOOL bEnable;
    CODEC_RECT_S stRect;
}VIDEO_CROP_INFO_S;
```
【Member Description】

|  Member   |                             Meaning                             |
| :-------: | :------------------------------------------------------------: |
|  bEnable  |              Whether to enable cropping.<br/>Value range: [HB_FALSE, HB_TRUE]              |
|   stRect  | The cropped area, where s32X and s32Y are aligned to 8 bytes, u32Width and u32Height for H.264/H.265 are aligned to 2 bytes, and u32Width and u32Height for MJPEG/JPEG are aligned to 1 byte. |

### VIDEO_FRAME_PACK_S
【Description】
> Defines the structure of a video frame.

【Structure Definition】
```C
typedef struct HB_VIDEO_FRAME_PACK_S {
    hb_char* vir_ptr[3];
    uint64_t phy_ptr[3];
```|   stFrameInfo   |  视频帧信息  |
| stJpegInfo | JPEG图像信息 ||    total_mb_in_frame_display    |      显示帧总MB块数量      |
|         display_rect         |         显示矩形信息         |
|       display_width;        |          显示宽度          |
|         display_height         |         显示高度         |
|         decoded_rect        |         解码矩形信息         |
|    aspect_rate_info     |        宽高比信息       |
|       frame_rate_numerator        |          帧率分子          |
|        frame_rate_denominator          |         帧率分母         |
|         display_poc          |         显示POC         |
|         decoded_poc          |         解码POC         |
|         error_reason          |         错误原因         |
|        warn_info         |         警告信息         |
|        sequence_no          |         序列号         |
|         temporal_id          |         视频帧时域ID         |
|         output_flag          |         输出标志         |
|         ctu_size          |         CTU大小         |

### JPEG_FRAME_INFO_S
【描述】
> 定义JPEG图像帧信息结构体。

【结构定义】
```C
typedef struct HB_JPEG_FRAME_INFO_S {
    int32_t width;
    int32_t height;
    int32_t image_quality;
    int32_t aspect_rate_info;
} HB_JPEG_FRAME_INFO_S;
```
【成员说明】

|       成员       |       含义       |
| :--------------: | :--------------: |
|      width       |      宽度       |
|      height      |      高度       |
|  image_quality   |      图像质量      |
| aspect_rate_info |     宽高比信息    || total_mb_in_frame_display |      Total number of MB blocks in the frame display      |
|       display_rect        |                 Display area                 |
|       display_width       |                 Display width                |
|      display_height       |                 Display height               |
|       decoded_rect        |                 Decoded area                |
|     aspect_rate_info      |                 Aspect ratio information                |
|   frame_rate_numerator    |                 Numerator part of frame rate fraction                |
|  frame_rate_denominator   |                 Denominator part of frame rate fraction                |
|        display_poc        |                 Image display order                |
|        decoded_poc        |                 Image decoding order                |
|       error_reason        |                 Decoding error information                |
|         warn_info         |                 Decoding warning information                |
|        sequence_no        |                 Image number, incremented by 1 per frame                |
|        temporal_id        |                 Temporal ID in custom GOP                |
|        output_flag        |                 Flag indicating whether to output                |
|         ctu_size          |                 CTU size                |

### VIDEO_FRAME_INFO_JPEG_S
【Description】
> Defines the structure for video frame information.

【Structure Definition】
```C
typedef struct HB_VIDEO_FRAME_INFO_JPEG_S {
    int32_t decode_result;
    int32_t frame_display_index;
    uint64_t stream_start_addr;
    int32_t stream_size;
    int32_t err_rst_idx;
    int32_t err_pos_x;
    int32_t err_pos_y;
    int32_t display_width;
    int32_t display_height;
} VIDEO_FRAME_INFO_JPEG_S;
```
【Member Description】

|         Member         |                           Meaning                           |
| :------------------: | :------------------------------------------------------: |
|    decode_result;    |                         Decoding result                         |
| frame_display_index; |                        Frame display index                        |
|  stream_start_addr;  |                       Stream start address                       |
|     stream_size;     |                         Stream size                         |
|     err_rst_idx;     | JPEG error restart index, available after decode_result returns success  |
|      err_pos_x;      | JPEG error MCU position X, available after decode_result returns success |
|      err_pos_y;      | JPEG error MCU position Y, available after decode_result returns success |
|    display_width;    |                         Display width                         |
|   display_height;    |                         Display height                         |

### VIDEO_STREAM_PACK_S【Description】
> Defines the stream buffer information for video streams.

【Structure Definition】
```C
typedef struct HB_VIDEO_PACK_S {
    hb_char* vir_ptr;
    uint64_t phy_ptr;
    uint32_t size;
    uint64_t pts;
    uint32_t fd;
    uint32_t src_idx;
    HB_BOOL stream_end;
} VIDEO_STREAM_PACK_S;
```
【Member Description】

|   Member    |           Meaning           |
| :---------: | :-------------------------: |
|  vir_ptr    | Frame buffer virtual address pointer |
|  phy_ptr    |    Frame buffer physical address    |
|    size     |    Total size of the frame buffer    |
|    pts      |           Frame timestamp           |
|     fd      |         Buffer file handle          |
|  src_idx    |             Index number            |
| stream_end  |     Last segment of the data stream   |

### VIDEO_STREAM_INFO_S
【Description】
> Defines additional information for H264/H265 output streams.

【Structure Definition】
```C
typedef struct HB_VIDEO_STREAM_INFO_S {
    HB_BOOL frame_index;
    uint64_t frame_start_addr;
    int32_t frame_size;
    int32_t nalu_type;
    uint32_t slice_idx;
    uint32_t slice_num;
    uint32_t dependent_slice_num;
    uint32_t independent_slice_num;
    uint32_t pic_skipped;
    uint32_t intra_block_num;
    uint32_t skip_block_num;
    uint32_t avg_mb_qp;
    uint32_t enc_pic_byte;
    int32_t enc_gop_pic_idx;
    int32_t enc_pic_poc;
    uint32_t enc_src_idx;
```uint32_t enc_pic_cnt; // Encoded picture count
int32_t enc_error_reason; // Encoding error reason
int32_t enc_warn_info; // Encoding warning information
uint32_t frame_cycle; // Frame cycle for encoding
uint32_t temporal_id; // Temporal ID for output stream
uint32_t longterm_ref_type; // Long-term reference frame type for output stream

【Member Description】

|       Member       |                                   Meaning                                    |
| :----------------: | :--------------------------------------------------------------------------: |
|  frame_start_addr  |                           Start address of the frame stream                            |
|     frame_size     |                                  Size of the frame stream                                   |
|    frame_index     |                               Index of the reconstructed frame                              |
|     nalu_type      |                                   NALU type in H.264                                    |
|     slice_idx      |                                 Slice index in H.264                                  |
|     slice_num      |                             Number of slices (H.264)                             |
| dependent_slice_num|                       Number of non-independent slices (H.265)                       |
|independent_slice_num|                        Number of independent slices (H.265)                       |
|    pic_skipped     |                          Flag indicating whether the frame is skipped                           |
|  intra_block_num   |                               Number of intra blocks in the frame                                |
|   skip_block_num   |                               Number of skipped blocks in the frame                               |
|      avg_mb_qp     |                          Average macroblock quantization parameter                           |
|    enc_pic_byte    |                      Size of the encoded image in bytes                     |
|  enc_gop_pic_idx   |                          GOP index of the encoded image                           |
|    enc_pic_poc     |                           POC (Picture Order Count) value of the encoded image                           |
|    enc_src_idx     |                      Buffer index of the encoded image                      |
|    enc_pic_cnt     |                          Number of encoded images                           |
| enc_error_reason   |                             Encoding error information                             |
|  enc_warn_info    |                            Encoding warning information                             |
|    frame_cycle     |                           Cycle for encoding one frame                            |
|    temporal_id     |                                    Temporal layer ID for output stream                                   |
| longterm_ref_type  |            Frame type for output stream, where bit1 and bit0 are valid            |
|                     |  bit1 = 1 indicates long-term reference frame, bit0 = 1 indicates reference long-term reference frame  |

### VIDEO_STREAM_INFO_JPEG_S
【Description】
> Defines additional information for MJPEG/JPEG output stream.

【Structure Definition】
```C
typedef struct VIDEO_STREAM_INFO_JPEG_S {
    uint64_t frame_start_addr;
    int32_t frame_size;
    uint32_t slice_idx;
    uint32_t slice_num;
    uint32_t frame_cycle;
} VIDEO_STREAM_INFO_JPEG_S;
```
【Member Description】|     Member      |                   Meaning                   |
| :-------------: | :-----------------------------------------: |
| frame_start_addr |          Start address of the bitstream          |
|   frame_size    |            Size of the bitstream            |
|    slice_idx    |           Index of the slice           |
|    slice_num    |           Number of slices           |
|   frame_cycle   |          Cycle of encoding one frame          |

### VIDEO_STREAM_S
【Description】
> Defines the structure of video frame stream.

【Structure Definition】
```C
typedef struct HB_VIDEO_STREAM_S
{
    VIDEO_STREAM_PACK_S pstPack;
    union
    {
        VIDEO_STREAM_INFO_S stStreamInfo;
        VIDEO_STREAM_INFO_JPEG_S stJpegInfo;
    };
}VIDEO_STREAM_S;
```
【Member Description】

|    Member    |         Meaning          |
| :----------: | :----------------------: |
|   pstPack    | Structure of the frame stream package |
| stStreamInfo | Characteristics information of the bitstream |
|  stJpegInfo  | Characteristics information of the bitstream |

### VENC_RECV_PIC_PARAM_S
【Description】
> Defines the structure of number of frames continuously received and encoded by the encoding channel.

【Structure Definition】
```C
typedef struct HB_VENC_RECV_PIC_PARAM_S
{
    int32_t s32RecvPicNum;
}VENC_RECV_PIC_PARAM_S;
```
【Member Description】

|    Member     |                   Meaning                   |
| :-----------: | :-----------------------------------------: |
| s32RecvPicNum | Number of frames continuously received and encoded by the encoding channel. Range: [-1,0)∪(0,∞] |### VENC_REF_PARAM_S
【Description】
> Defines the structure of the reference parameters for the encoder.

【Structure Definition】
```C
typedef struct HB_VENC_REF_PARAM_S{
    uint32_t use_longterm;
    uint32_t longterm_pic_period;
    uint32_t longterm_pic_using_period;
} VENC_REF_PARAM_S;
```
【Member Description】

| Member                   | Meaning                                 |
| -----------------------  | --------------------------------------- |
| use_longterm             | Enables long-term reference mode, not dynamically configurable. |
| longterm_pic_period      | Long-term reference picture period, dynamically configurable. |
| longterm_pic_using_period| Long-term reference picture usage period, dynamically configurable. |

### VENC_USER_RC_ATTR_S
【Description】
> Defines the structure of the user frame information.

【Structure Definition】
```C
typedef struct HB_VENC_USER_RC_ATTR_S {
    HB_BOOL qp_map_valid;
    unsigned char *qp_map_array;
    uint32_t qp_map_array_count;
} VENC_USER_RC_ATTR_S;
```
【Member Description】

| Member               | Meaning                  |
| -------------------- | ------------------------ |
| qp_map_valid         | Whether to enable QP map. |
| qp_map_array	       | Pointer to the QP map table. |
| qp_map_array_count   | Length of the QP map table. |

### USER_FRAME_INFO_S
【Description】
> Defines the structure of the user frame information.

【Structure Definition】
```C
typedef struct HB_USER_FRAME_INFO_S{
    VIDEO_FRAME_S stUserFrame;
    VENC_USER_RC_ATTR_S stUserRcInfo;} USER_FRAME_INFO_S;
```
【Member Explanation】

|     Member     |     Meaning     |
| :----------: | :----------: |
| stUserFrame  |    Image frame    |
| stUserRcInfo | User RC information. |

### VENC_PARAM_MOD_S
【Description】
> Define frame rate control parameters for encoding channels.

【Struct Definition】
```C
typedef struct HB_VENC_PARAM_MOD_S {
    uint32_t u32OneStreamBuffer;
} VENC_PARAM_MOD_S;
```
【Member Explanation】

|        Member        |                       Meaning                        |
| :----------------: | :-----------------------------------------------: |
| u32OneStreamBuffer | Whether VPS, SPS, PPS, IDR are output in one frame<br/>Default: one frame output. |

### VENC_FRAME_RATE_S
【Description】
> Define frame rate control parameters for encoding channels.

【Struct Definition】
```C
typedef struct HB_VENC_FRAME_RATE_S {
    int32_t s32InputFrameRate;
    int32_t s32OutputFrameRate;
} VENC_FRAME_RATE_S;
```
【Member Explanation】

|        Member        |                 Meaning                  |
| :----------------: | :-----------------------------------: |
| s32InputFrameRate  |               Input frame rate                |
| s32OutputFrameRate | Output frame rate, range: [1- s32InputFrameRate） |

### VENC_CHN_PARAM_S
【Description】
> Define encoding channel parameters.

【Struct Definition】
```C
typedef struct HB_VENC_CHN_PARAM_S {
```C
typedef struct HB_VENC_CHN_PARAM_S {
    VENC_FRAME_RATE_S stFrameRate;
} VENC_CHN_PARAM_S;
```
【Member Description】

|   Member    |      Meaning     |
|:-----------:|:-----------------:|
| stFrameRate | Frame rate control parameters, can be dynamically set |

### VENC_ROI_ATTR_S
【Description】
> Defines the information of regions of interest for encoding.

【Structure Definition】
```C
typedef struct HB_VENC_ROI_ATTR_S {
    uint32_t roi_enable;
    uint8_t* roi_map_array;
    uint32_t roi_map_array_count;
} VENC_ROI_ATTR_S;
```
【Member Description】

|       Member       |              Meaning               |
|:------------------:|:----------------------------------:|
|    roi_enable      | Enable ROI region, cannot be dynamically configured |
|   roi_map_array    | ROI region Qp array, can be dynamically configured |
| roi_map_array_count| Number of ROI region Qp arrays, cannot be dynamically configured |

### VENC_CHN_STATUS_S
【Description】
> Defines the structure for encoding channel status.

【Structure Definition】
```C
typedef struct HB_VENC_CHN_STATUS_S {
    uint32_t cur_input_buf_cnt;
    uint64_t cur_input_buf_size;
    uint64_t cur_output_buf_cnt;
    uint64_t cur_output_buf_size;
    uint32_t left_recv_frame;
    uint32_t left_enc_frame;
    uint32_t total_input_buf_cnt;
    uint32_t total_output_buf_cnt;
    int32_t pipeline;
    int32_t channel_port_id;
} VENC_CHN_STATUS_S;
```
【Member Description】

|       Member       |          Meaning          |
|nr_noise_sigmaCb|Cb分量噪声标准偏差|
|nr_noise_sigmaCr|Cr分量噪声标准偏差|## Error Codes
The error codes for VENC are as follows:

| Error Code   |                Macro Definition | Description        |
| :----------: | -----------------------------: | ------------------: |
| -268958720   |               HB_ERR_VENC_UNKNOWN | Unknown error      |
| -268958721   |             HB_ERR_VENC_NOT_FOUND | VENC channel not found |
| -268958722   |             HB_ERR_VENC_OPEN_FAIL | Failed to open VENC channel |
| -268958723   |      HB_ERR_VENC_RESPONSE_TIMEOUT | No response from VENC channel |
| -268958724   |             HB_ERR_VENC_INIT_FAIL | Failed to initialize VENC module |
| -268958725   |HB_ERR_VENC_OPERATION_NOT_ALLOWED | Operation not allowed |
| -268958726   |                 HB_ERR_VENC_NOMEM | Insufficient VENC memory |
| -268958727   |       HB_ERR_VENC_NO_FREE_CHANNEL | No available VENC channel |
| -268958728   |         HB_ERR_VENC_ILLEGAL_PARAM | Invalid parameter |
| -268958729   |         HB_ERR_VENC_INVALID_CHNID | Invalid channel ID |
| -268958730   |           HB_ERR_VENC_INVALID_BUF | Invalid buffer block |
| -268958731   |           HB_ERR_VENC_INVALID_CMD | Invalid command |
| -268958732   |          HB_ERR_VENC_WAIT_TIMEOUT | Wait timeout |
| -268958733   |   HB_ERR_VENC_FILE_OPERATION_FAIL | Operation failed |
| -268958734   |       HB_ERR_VENC_PARAMS_SET_FAIL | Failed to set parameters |
| -268958735   |       HB_ERR_VENC_PARAMS_GET_FAIL | Failed to retrieve parameters |
| -268958736   |                 HB_ERR_VENC_EXIST | VENC channel already exists |
| -268958737   |               HB_ERR_VENC_UNEXIST | VENC channel does not exist |
| -268958738   |              HB_ERR_VENC_NULL_PTR | Null pointer |
| -268958739   |             HB_ERR_VENC_UNSUPPORT | Not supported |

## Reference Code
You can refer to the sample code for VENC in [sample_video_codec](./multimedia_samples#sample_video_codec).