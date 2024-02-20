# 7.3 System Control
## Overview
System control is used to initialize and deinitialize the entire media system, and establish relationships between modules through binding interfaces. It provides the VP (Video Pool) module for managing large blocks of physical memory allocation.

## Functional Description

### Video Pool

The VP (Video Pool) video pool provides large blocks of physical memory and management functions, and is responsible for memory allocation and recovery.
The video pool is composed of a group of physically contiguous and equally sized buffer blocks. It needs to be configured and initialized before use. The number of buffer pools and the size of buffer blocks can be configured according to the needs.

### Binding Relationship

![image-20220329183230983](./image/system_control/image-20220329183230983.png)

Note: The binding relationship between modules can be established using the HB_SYS_Bind interface. Once bound, the data processed by the data source will be automatically sent to the data sink.

### Operation Mode

**Online Mode:** The data between modules is directly transferred from the previous module to the next module through the internal bus without the need to read/write DDR. This can reduce latency and save DDR bandwidth.

**Offline Mode:** The data from the previous module is first written to DDR, and then the next module reads the data from DDR. When multiple sensors are connected, all connected sensors are processed offline.

| Mode  |      VIN_SIF and VIN_ISP      |        VIN_ISP and VPS         |       VIN_SIF and VPS        |
| :---: | :---------------------------: | :----------------------------: | :--------------------------: |
| Online |    SIF(RAW) --> ISP    |      ISP(YUV) --> VPS      |      SIF(YUV) --> VPS     |
| Offline | SIF(RAW) --> DDR --> ISP | ISP(YUV) --> DDR --> VPS | SIF(YUV) --> DDR --> ISP |

Note: The HB_SYS_SetVINVPSMode interface is used to set the operation mode between VIN and VPS.

## API Reference

- HB_SYS_Init: Initialize the media system (reserved).
- HB_SYS_Exit: Exclude the media system (reserved).
- HB_SYS_Bind: Bind the data source to the data receiver.
- HB_SYS_UnBind: Unbind the data source from the data receiver.
- HB_SYS_SetVINVPSMode: Set the operation mode between VIN and VPS modules. 
- HB_SYS_GetVINVPSMode: Get the operation mode between VIN and VPS modules for a specified pipeid.
- HB_VP_SetConfig: Set the properties of the Video Pool video pool.
- HB_VP_GetConfig: Get the properties of the Video Pool video pool.
- HB_VP_Init: Initialize the Video Pool video pool.
- HB_VP_Exit: Deinitialize the Video Pool video pool.
- HB_VP_CreatePool: Create a video buffer pool.
- HB_VP_DestroyPool: Destroy a video buffer pool.
- HB_VP_GetBlock: Get a buffer block.
- HB_VP_ReleaseBlock: Release an acquired buffer block.- HB_VP_PhysAddr2Block: Get the buffer block ID from the physical address of the buffer block.
- HB_VP_Block2PhysAddr: Get the physical address of a buffer block.
- HB_VP_Block2PoolId: Get the ID of the cache pool where a cache block is located.
- HB_VP_MmapPool: Map the user space virtual address for a video cache pool.
- HB_VP_MunmapPool: Unmap the user space virtual address for a video cache pool.
- HB_VP_GetBlockVirAddr: Get the user space virtual address of a cache block in a video cache pool.
- HB_VP_InquireUserCnt: Check if a buffer block is in use.
- HB_VP_SetAuxiliaryConfig: Set additional information for a video buffer pool.
- HB_SYS_Alloc: Allocate memory in user space.
- HB_SYS_Free: Free a memory block.
- HB_SYS_AllocCached: Allocate cached memory in user space.
- HB_SYS_CacheInvalidate: Invalidate the cache of the cached memory.
- HB_SYS_CacheFlush: Flush the cache of the cached memory.
- HB_VP_DmaCopy: Copy physical memory through DMA.

### HB_SYS_Init
【Function Declaration】
```c
int HB_SYS_Init(void);
```
【Function Description】
> Reserved interface, currently has no effect.

【Parameter Description】
> None

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|      0       |   Success   |
|     Non-zero |   Failure   |

【Notes】
> None

【Reference Code】
> None

### HB_SYS_Exit
【Function Declaration】
```c
int HB_SYS_Exit(void);
```
【Function Description】
> Reserved interface, currently has no effect.

【Parameter Description】
> None【Return Value】

| Returns | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Notes】
> None

【Reference Code】
> None

### HB_SYS_Bind
【Function Declaration】
```c
int HB_SYS_Bind(const SYS_MOD_S *pstSrcMod, const SYS_MOD_S *pstDstMod);
```
【Function Description】
> Establishes a binding relationship between VIN pipelines, channels, VPS groups/channels, VO channels, and VENC channels.

【Parameter Description】

| Parameter Name | Description | Input/Output |
| :-------: | :----------: | :-------: |
| pstSrcMod | Source module pointer |   Input    |
| pstDstMod | Destination module pointer |   Input    |

【Return Value】

| Returns | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Notes】
> None

【Reference Code】
> None

### HB_SYS_UnBind
【Function Declaration】
```c
int HB_SYS_UnBind(const SYS_MOD_S *pstSrcMod, const SYS_MOD_S *pstDstMod);
```
【Function Description】
> Unbinds the binding relationship between VIN pipelines, channels, VPS groups/channels, VO channels, and VENC channels.

【Parameter Description】int HB_SYS_GetVINVPSMode(int pipeId, SYS_VIN_VPS_MODE_E *pMode);
```
【功能描述】
> 获取VIN，VPS模块间的工作模式。

【参数描述】

| 参数名称 |       描述       | 输入/输出 |
| :------: | :--------------: | :-------: |
|  pipeId  |      Pipe号      |   输入    |
|  pMode   | VIN，VPS工作模式 |   输出    |

【返回值】

| 返回值 | 描述 |
|:------:|:----:|
|    0   | 成功 |
|   非0  | 失败 |

【注意事项】
> 无

【参考代码】
> 无int HB_SYS_GetVINVPSMode(int pipeId);
```
【Function Description】
> Get the working mode of the VIN, VPS module of the specified pipe ID.

【Parameter Description】

| Parameter Name | Description | Input/Output |
| :------------: | :---------: | :----------: |
|    pipeId      | Pipe number |    Input     |

【Return Value】

| Return Value |       Description       |
| :----------: | :---------------------: |
|     >=0      | SYS_VIN_VPS_MODE_E enum |
|      <0      |        Failed           |

【Notice】
> None

【Reference Code】
> None

Video Pool

### HB_VP_SetConfig
【Function Declaration】
```c
int HB_VP_SetConfig(VP_CONFIG_S *VpConfig);
```
【Function Description】
> Set the attributes of the Video Pool video buffer pool.

【Parameter Description】

| Parameter Name |          Description          | Input/Output |
| :------------: | :---------------------------: | :----------: |
|    vpConfig    | Pointer to video buffer pool properties |    Input     |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|      0       |    Success  |
|   Non-zero   |    Failed   |

【Notice】
> None【Reference Code】
> VideoPool Reference Code

### HB_VP_GetConfig
【Function Declaration】
```c
int HB_VP_GetConfig(VP_CONFIG_S *VpConfig);
```
【Description】
> Get the properties of the Video Pool video buffer pool.

【Parameter Description】

| Parameter Name |     Description     | Input/Output |
| :------------: | :-----------------: | :----------: |
|    vpConfig    | Video buffer pool property pointer |    Output    |

【Return Value】

| Return Value | Description |
| :----------: | :---------: |
|      0       |   Success   |
|    Non-zero  |   Failure   |

【Note】
> None

【Reference Code】
> None

### HB_VP_Init
【Function Declaration】
```c
int HB_VP_Init(void);
```
【Description】
> Initialize the video buffer pool.

【Parameter Description】
> None

【Return Value】

| Return Value | Description |
| :----------: | :---------: |
|      0       |   Success   |
|    Non-zero  |   Failure   |

【Note】
> It is necessary to call HB_VP_SetConfig to configure the cache pool properties before initializing the cache pool, otherwise it will fail.【参考代码】
> Reference code for VideoPool

### HB_VP_Exit
【Function Declaration】
```c
int HB_VP_Exit(void);
```
【Function Description】
> Uninitialize the video pool

【Parameter Description】
> None

【Return Value】

| Return Value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Notes】
> None

【参考代码】
> Reference code for VideoPool

### HB_VP_CreatePool
【Function Declaration】
```c
uint32_t HB_VP_CreatePool(VP_POOL_CONFIG_S *VpPoolCfg);
```
【Function Description】
> Create a video pool

【Parameter Description】

| Parameter | Description | Input/Output |
| :-------: | :--------------------: | :-------: |
| VpPoolCfg | Pointer to cache pool configuration attributes  |   Input    |

【Return Value】

|       Return Value        |       Description       |
| :-----------------: | :--------------: |
| Non-VP_INVALID_POOLID | Valid pool ID number |
|  VP_INVALID_POOLID  |  Failed to create pool  |

【Notes】【参考代码】
> Reference code for VideoPool

### HB_VP_DestroyPool
【Function Declaration】
```c
int HB_VP_DestroyPool(uint32_t Pool);
```
【Function Description】
> Destroy a video buffer pool

【Parameter Description】

| Parameter Name |     Description     | Input/Output |
| :------------: | :-----------------: | :----------: |
|      Pool      | ID of the pool     |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | :---------: |
|       0      |   Success   |
|    Non-zero  |   Failure   |

【Note】
> N/A

【参考代码】
> Reference code for VideoPool

### HB_VP_GetBlock
【Function Declaration】
```c
uint32_t HB_VP_GetBlock(uint32_t Pool, uint64_t u64BlkSize);
```
【Function Description】
> Obtain a buffer block

【Parameter Description】

|  Parameter Name   |    Description     | Input/Output |
| :---------------: | :----------------: | :----------: |
|       Pool        |     ID of pool     |    Input     |
|    u64BlkSize     |    Size of block   |    Input     |

【Return Value】

|    Return Value   |     Description    |### Translation
| :-----------------: | :------------: |
| Non-VP_INVALID_HANDLE | Valid buffer block id |
| VP_INVALID_HANDLE | Failed to get buffer block |

【Notes】
> u64BlkSize must be less than or equal to the buffer block size specified when creating the cache pool

【Reference code】
> VideoPool reference code

### HB_VP_ReleaseBlock
【Function declaration】
```c
int HB_VP_ReleaseBlock(uint32_t Block);
```
【Function description】
> Release a buffer block that has been acquired

【Parameter description】

| Parameter name | Description | Input/Output |
| :------: | :------: | :-------: |
|  Block   | Buffer block id |   Input    |

【Return value】

| Return value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failed |

【Notes】
> None

【Reference code】
> VideoPool reference code

### HB_VP_PhysAddr2Block
【Function declaration】
```c
uint32_t HB_VP_PhysAddr2Block(uint64_t u64PhyAddr);
```
【Function description】
> Get the buffer block id through the physical address of the buffer block

【Parameter description】

|  Parameter name  |      Description      | Input/Output |
| :--------: | :------------: | :-------: |
| u64PhyAddr | Physical address of the buffer block |   Input    |【返回值】

| Return Value | Description |
|:------------:|:-----------:|
|      0       |   Success   |
|     Non-zero      |   Failure   |

【注意事项】
> None

【参考代码】
> VideoPool reference code

### HB_VP_Block2PhysAddr
【函数声明】
```c
uint64_t HB_VP_Block2PhysAddr(uint32_t Block);
```
【功能描述】
> Get the physical address of a buffer block

【参数描述】

| Parameter Name | Description | Input/Output |
| :------------: | :---------: | :----------: |
|     Block      | Buffer block id |    Input     |

【返回值】

| Return Value |        Description        |
| :----------: | :-----------------------: |
|      0       |   Invalid return value    |
|   Non-zero    |    Valid physical address   |

【注意事项】
> None

【参考代码】
> VideoPool reference code

### HB_VP_Block2PoolId
【函数声明】
```c
uint32_t HB_VP_Block2PoolId(uint32_t Block);
```
【功能描述】
> Get the buffer pool id through the buffer block id

【参数描述】| Parameter Name | Description | Input/Output |
| :------------: | :---------: | :----------: |
|     Block      | Buffer block ID |    Input     |

【Return Value】

| Return Value |     Description      |
| :----------: | :------------------: |
|  Non-negative integer |  Valid buffer pool ID  |
|    Negative integer   |  Invalid buffer pool ID  |

【Note】
> None

【Reference Code】
> Reference code for VideoPool

### HB_VP_MmapPool
【Function Declaration】
```c
int HB_VP_MmapPool(uint32_t Pool);
```
【Function Description】
> Map user-space virtual address for a buffer pool

【Parameter Description】

| Parameter Name | Description | Input/Output |
| :------------: | :---------: | :----------: |
|     Pool       | Buffer pool ID |    Input     |

【Return Value】

| Return Value |     Description      |
| :----------: | :------------------: |
|       0      |         Success          |
|    Non-zero  |         Failure          |

【Note】
> None

【Reference Code】
> Reference code for VideoPool

### HB_VP_MunmapPool
【Function Declaration】
```c
int HB_VP_MunmapPool(uint32_t Pool);
```【Function Description】
> Remove user-mode mapping for a buffer pool

【Parameter Description】

| Parameter Name |      Description      | Input/Output |
| :------------: | :------------------: | :----------: |
|      Pool      | Buffer pool ID number |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | :---------: |
|       0      |   Success   |
|     Non-zero     |   Failure   |

【Notes】
> None

【Reference Code】
> Reference code for VideoPool

### HB_VP_GetBlockVirAddr
【Function Declaration】
```c
int HB_VP_GetBlockVirAddr(uint32_t Pool, uint64_t u64PhyAddr, void **ppVirAddr);
```
【Function Description】
> Get the user-mode virtual address of a cache block in a video buffer pool

【Parameter Description】

|  Parameter Name  |      Description       | Input/Output |
| :--------------: | :-------------------: | :----------: |
|       Pool       |   Buffer pool ID number  |    Input     |
|    u64PhyAddr    |   Buffer pool physical address |    Input     |
|    ppVirAddr    |   Buffer pool virtual address |    Output     |

【Return Value】

| Return Value | Description |
| :----------: | :---------: |
|       0      |   Success   |
|     Non-zero     |   Failure   |

【Notes】
> None

【Reference Code】
> Reference code for VideoPool### HB_VP_InquireUserCnt
【Function Declaration】
```c
int HB_VP_InquireUserCnt(uint32_t Block);
```
【Function Description】
> Check if the buffer block is being used.

【Parameter Description】

| Parameter Name |  Description | Input/Output |
| :------: | :------: | :-------: |
|  Block   | Buffer block ID |   Input    |

【Return Value】

|    Return Value     |   Description   |
| :-----------------: | :------: |
|  VP_INVALID_HANDLE  | Query failed |
| Non-VP_INVALID_HANDLE | Reference count |

【Note】
> None

【Reference Code】
> None

### HB_VP_SetAuxiliaryConfig
【Function Declaration】
```c
int HB_VP_SetAuxiliaryConfig (const VP_AUXILIARY_CONFIG_S *pstAuxiliaryConfig);
```
【Function Description】
> Set the auxiliary configuration of the video buffer pool.

【Parameter Description】

| Parameter Name |             Description             | Input/Output |
| :----------------: | :--------------------------: | :-------: |
| pstAuxiliaryConfig | Configuration structure for auxiliary information of video buffer pool |   Input    |

【Return Value】

| Return Value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Note】### HB_SYS_Alloc
【Function Declaration】
```c
int HB_SYS_Alloc(uint64_t *pu64PhyAddr, void **ppVirAddr, uint32_t u32Len);
```
【Description】
> Allocate memory in user mode.

【Parameter Description】

| Parameter Name | Description | Input/Output |
| :------------: | :---------: | :----------: |
|  pu64PhyAddr  |  Physical address pointer  |    Output    |
|   ppVirAddr   |    Pointer to virtual address    |    Output    |
|    u32Len    |    Size of memory allocation    |    Input    |

【Return Value】
| Return Value | Description |
|:------:|:----:|
|    0   | Success |
|  Non-zero  | Failure |

【Notes】
> Need to call HB_VP_Init to initialize video buffer pool.

【Sample Code】
```c
    ret = HB_SYS_Alloc(&paddr, &vaddr, 0x1000);
    if (ret == 0) {
        printf("Alloc paddr = 0x%x, vaddr = 0x%x\n", paddr, vaddr);
    }
    ret = HB_SYS_Free(paddr, vaddr);
    if (ret == 0) {
        printf("Free ok\n");
    }
```

### HB_SYS_AllocCached
【Function Declaration】
```c
int HB_SYS_AllocCached(uint64_t *pu64PhyAddr, void **ppVirAddr, uint32_t u32Len);
```
【Description】
> Allocate cached memory in user mode.【Parameter Description】

| Parameter Name |       Description        | Input/Output |
| :------------: | :----------------------: | :----------: |
|  pu64PhyAddr   |      Physical Address    |    Output    |
|   ppVirAddr    | Pointer to Virtual Address |    Output    |
|    u32Len      |    Size of Memory Block   |    Input     |

【Return Value】

| Return Value |  Description |
| :----------: | :----------: |
|       0      |     Success  |
|    Non-zero  |    Failure   |

【Note】
> Need to call HB_VP_Init to initialize the video buffer pool

【Reference Code】
> None

### HB_SYS_Free
【Function Declaration】
```c
int HB_SYS_Free(uint64_t u64PhyAddr, void *pVirAddr);
```
【Function Description】
> Free Memory Block

【Parameter Description】

| Parameter Name |    Description     | Input/Output |
| :------------: | :----------------: | :----------: |
|  u64PhyAddr    |    Physical Address  |    Input     |
|   pVirAddr     | Pointer to Virtual Address  |    Input     |

【Return Value】

| Return Value |  Description |
| :----------: | :----------: |
|       0      |     Success  |
|    Non-zero  |    Failure   |

【Note】
> None

【Reference Code】
> Refer to HB_SYS_Alloc|   非0  | 失败 |

【注意事项】
> 无

【参考代码】
> 无|   非0  |   Failed  |

【Notes】
> None

【Reference Code】
> None

### HB_VP_DmaCopy
【Function Declaration】
```c
int HB_VP_DmaCopy(void *dstPaddr, void *srcPaddr, uint32_t len);
```
【Function Description】
> Copy physical memory through DMA.

【Parameter Description】

| Parameter Name |     Description     | Input/Output |
| :------------: | :-----------------: | :----------: |
|   dstPaddr     | Destination address |    Input     |
|   srcPaddr     |    Source address   |    Input     |
|      len       |       Length        |    Input     |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|      0       |   Success   |
|   Non-zero   |   Failed    |

【Notes】
> dstPaddr and srcPaddr should be continuous physical addresses.

【Reference Code】
> None

## Data Type
### HB_SYS_MOD_ID_E
【Structure Definition】
```c
typedef enum HB_SYS_MOD_ID_E {
    HB_ID_SYS = 0,
    HB_ID_VIN,
    HB_ID_VOT,
    HB_ID_VPS,
    HB_ID_RGN,
    HB_ID_AIN,
    HB_ID_AOT,
    HB_ID_VENC,
```> 定义了VIN和VPS之间的工作模式。

【成员说明】

| 成员                                       | 含义                                       |
|------------------------------------------|--------------------------------------------|
| VIN_ONLINE_VPS_ONLINE                     | 在线模式：VIN和VPS都在线                    |
| VIN_ONLINE_VPS_OFFLINE                    | 在线模式：VIN在线，VPS离线                  |
| VIN_OFFLINE_VPS_ONLINE                    | 在线模式：VIN离线，VPS在线                  |
| VIN_OFFLINE_VPS_OFFINE                    | 离线模式：VIN和VPS都离线                    |
| VIN_SIF_VPS_ONLINE                        | 在线模式：SIF输入，VIN在线，VPS在线          |
| VIN_SIF_OFFLINE_ISP_OFFLINE_VPS_ONLINE    | 在线模式：SIF输入，VIN离线，ISP离线，VPS在线 |
| VIN_SIF_ONLINE_DDR_ISP_DDR_VPS_ONLINE     | 在线模式：SIF输入，DDR输入，ISP在线，VPS在线 |
| VIN_SIF_ONLINE_DDR_ISP_ONLINE_VPS_ONLINE  | 在线模式：SIF输入，DDR输入，ISP在线，VPS在线 |
| VIN_FEEDBACK_ISP_ONLINE_VPS_ONLINE        | 在线模式：其它模块反馈的ISP，ISP在线，VPS在线 |
| VIN_SIF_OFFLINE_VPS_OFFLINE               | 离线模式：SIF输入，VIN离线，VPS离线           |
| VIN_SIF_OFFLINE                           | 离线模式：SIF输入，VIN离线                  |> 表示VIN和VPS的在线与离线模式和VIN内部的工作模式。

[Member Explanation]

| Member                                   | Meaning                                                                                   |
| :--------------------------------------- | :------------------------------------------------------------------------------------- |
| VIN_ONLINE_VPS_ONLINE                    | VIN_SIF and VIN_ISP are online, VIN_ISP and VPS are online                                |
| VIN_ONLINE_VPS_OFFLINE                   | VIN_SIF and VIN_ISP are online, VIN_ISP is offline, VPS is offline                        |
| VIN_OFFLINE_VPS_ONLINE                   | VIN_SIF and VIN_ISP are offline, VIN_ISP is online, VPS is online                         |
| VIN_OFFLINE_VPS_OFFINE                   | VIN_SIF and VIN_ISP are offline, VIN_ISP and VPS are offline                              |
| VIN_SIF_VPS_ONLINE                       | VIN_SIF directly sends data online to VPS                                                 |
| VIN_SIF_OFFLINE_ISP_OFFLINE _VPS_ONLINE   | VIN_SIF and VIN_ISP are offline, VIN_ISP is online, VPS is online, VIN_ISP to DDR, generally used to dump VIN_ISP image |
| VIN_SIF_ONLINE_DDR_ISP_DDR _VPS_ONLINE    | VIN_SIF and VIN_ISP are online, VIN_SIF to DDR, VIN_ISP is offline, VPS is online         |
| VIN_SIF_ONLINE_DDR_ISP_ONL INE_VPS_ONLINE | VIN_SIF and VIN_ISP are online, VIN_ISP and VPS are online, VIN_SIF to DDR, generally used to dump VIN_SIF image |
| VIN_FEEDBACK_ISP_ONLINE _VPS_ONLINE       | VIN_SIF feeds back in raw mode                                                           |
| VIN_SIF_OFFLINE_VPS_OFFLINE              | VIN_SIF and VPS are offline, generally used for YUV to IPU                                |
| VIN_SIF_OFFLINE                          | VIN_SIF goes directly to DDR                                                              |

### HB_VP_POOL_CONFIG_S
[Structure Definition]
```c
typedef struct HB_VP_POOL_CONFIG_S {
    uint64_t u64BlkSize;
    uint32_t u32BlkCnt;
    uint32_t cacheEnable;
} VP_POOL_CONFIG_S;
```
[Function Description]
> Video buffer pool configuration structure

[Member Explanation]

|   Member    | Meaning               |
| :---------: | :--------------------- |
| u64BlkSize  | Size of buffer blocks  |
|  u32BlkCnt  | Number of blocks per pool |
| cacheEnable | Whether cache is enabled for the pool |

### HB_VP_CONFIG_S
[Structure Definition]
```c
struct HB_VP_CONFIG_S {
    uint32_t u32MaxPoolCnt;
    VP_POOL_CONFIG_S pubPool[VP_MAX_PUB_POOLS];
} VP_CONFIG_S;
```
[Function Description]
> Video buffer pool attribute structure

[Member Explanation]|    Member   | Meaning                  |
| :---------: | :----------------------- |
| u32MaxPoolCnt | Number of buffer pools that can be accommodated in the entire system |
|   pubPool   | Structure defining the properties of a public buffer pool           |

### HB_VP_AUXILIARY_CONFIG_S
【Structure Definition】
```c
typedef struct HB_VP_AUXILIARY_CONFIG_S {
    int u32AuxiliaryConfig;
} VP_AUXILIARY_CONFIG_S;
```
【Functional Description】
> Structure for configuring additional information for video buffer pools

【Member Description】

|     Member      | Meaning       |
| :-------------: | :------------ |
| AuxiliaryConfig | Additional information type |

### hb_vio_buffer_t
【Structure Definition】
```c
typedef struct hb_vio_buffer_s {
    image_info_t img_info;
    address_info_t img_addr;
} hb_vio_buffer_t;
```

【Functional Description】
> Structure for regular buffer information, representing one frame of image

【Member Description】

|    Member   | Meaning           |
| :---------: | :---------------- |
| img_info | Image data information |
| img_addr | Image address information |

### pym_buffer_t
【Structure Definition】
```c
typedef struct pym_buffer_s {
    image_info_t pym_img_info;
    address_info_t pym[6];
    address_info_t pym_roi[6][3];
    address_info_t us[6];
    char *addr_whole[HB_VIO_BUFFER_MAX_PLANES];
typedef struct image_info_s {
    uint16_t sensor_id;
    uint32_t pipeline_id;
    uint32_t frame_id;
    uint64_t time_stamp;
    struct timeval tv;
    int buf_index;
    int img_format;
    int fd[HB_VIO_BUFFER_MAX_PLANES];
    uint32_t size[HB_VIO_BUFFER_MAX_PLANES];
    uint32_t planeCount;
    uint32_t dynamic_flag;
    uint32_t water_mark_line;
    VIO_DATA_TYPE_E data_type;
    buffer_state_e state;
} image_info_t;
```
【Functional Description】
> Structure for image information

【Member Description】

|    Member    | Meaning                                                      |
| :----------: | :----------------------------------------------------------- |
|  sensor_id   | Sensor id                                                    |
| pipeline_id  | Corresponding data channel number                            |
|  frame_id    | Data frame number                                            |
| time_stamp   | HW time stamp, internal hardware time in SIF, updated every FS, not related to system time, generally used for synchronization |
|    tv        | Timeval structure                                            |
|  buf_index   | Buffer index                                                 |
| img_format   | Image format                                                 |
|     fd       | File descriptor array for each plane                         |
|    size      | Data size in each plane                                      |
| planeCount   | Number of planes                                             |
| dynamic_flag | Dynamic flag                                                 |
| water_mark_line | Water mark line                                           |
| data_type    | Enumeration type for VIO data type                           |
|    state     | Buffer state                                                 ||       tv        | System time of getting buffer in hal, the system time when sif is triggered in framestart      |
|    buf_index    | Index of the obtained buffer                                           |
|   img_format    | Image format                                                     |
|       fd        | Ion buffer file descriptor                                                   |
|      size       | Size of corresponding plane                                              |
|   planeCount    | Number of planes in the image                                       |
|  dynamic_flag   | Flag indicating dynamic size change                                             |
| water_mark_line | Water mark line information, not supported in XJ3                                      |
|    data_type    | Data type of the image                                             |
|      state      | State of the buffer, user state in the user layer                              |

### address_info_t
【Structure Definition】
```c
typedef struct address_info_s {
    uint16_t width;
    uint16_t height;
    uint16_t stride_size;
    char *addr[HB_VIO_BUFFER_MAX_PLANES];
    uint64_t paddr[HB_VIO_BUFFER_MAX_PLANES];
} address_info_t;
```
【Description】
> Structure for image address information

【Member Description】

|    Member     | Description                                       |
| :---------: | :----------------------------------------- |
|    width    | Width of the image data                               |
|   height    | Height of the image data                               |
| stride_size | Memory stride of the image data (actual width stored in memory) |
|    addr     | Virtual addresses, stored according to the number of yuv planes              |
|    paddr    | Physical addresses, stored according to the number of yuv planes              |

## Error Codes

|   Error code   |          Macro            |          Description          |
| :--------: | :----------------------: | :--------------------: |
| -268500032 |    VP_INVALID_BLOCKID    |       Invalid buffer block       |
| -268500033 |    VP_INVALID_POOLID     |       Invalid buffer pool       |
| -268500034 |    HB_ERR_VP_NOT_PERM    |       Operation not permitted       |
| -268500035 |    HB_ERR_VP_UNEXIST     |    Video buffer pool does not exist    |
| -268500036 |      HB_ERR_VP_BUSY      |        Buffer pool busy        |
| -268500037 |     HB_ERR_SYS_BUSY      |         System busy         |
| -268500038 | HB_ERR_SYS_ILLEGAL_PARAM |    Illegal parameter of system interface    |
| -268500039 |     HB_ERR_SYS_NOMEM     |  Failed to allocate memory in system interface  |
| -268500040 | HB_ERR_VP_ILLEGAL_PARAM  | Invalid parameter setting for buffer pool interface |