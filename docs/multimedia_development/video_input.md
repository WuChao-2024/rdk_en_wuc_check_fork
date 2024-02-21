---
sidebar_position: 4
---
# 7.4 Video Input
## Overview
The Video Input (VIN) module functions by receiving video data through the MIPI Rx interface. VIN passes the received data to the next module, VPS, and can also store it in a designated memory area. During this process, VIN can process the received raw video image data to achieve video data acquisition.

### Concepts

- Video Input Device
The video input device primarily refers to the SIF (System Interconnect Framework) and image data interface. Its main function is to receive image data outputted by camera modules and directly output it to the ISP (Image Signal Processor) module for image processing, either offline or online.

- Video Input PIPE
The Video Input PIPE (ISP) is bound to the device backend and is responsible for image processing, hard-core function configuration, and supports multi-context.

- Lens Distortion Correction (LDC)
LDC is mainly responsible for correcting images affected by lens surface curvature, as certain low-end lenses can cause image distortion. It requires correcting the image based on the degree of distortion.

- DIS (Digital Image Stabilization)
The DIS module calculates the current image's displacement vector in various axis directions by comparing it with the previous two frames using different degrees of freedom of the anti-shake algorithm. It then corrects the current image based on the displacement vector, thus achieving an anti-shake effect.

- DWE (Distortion and Image Stabilization)
DWE integrates LDC and DIS together, including distortion correction by LDC and statistical results of DIS.

## Function Description

VIN is divided into four parts in software, as shown in the following diagram.

![image-20220329195124946](./image/video_input/image-20220329195124946.png)

### Video Input Device

SIF primarily functions to receive image data outputted by camera modules and directly output it to the ISP module for image processing, either offline or online. Mipi: supports RAW8/RAW10/RAW12/RAW14/RAW16 or YUV422 8bit/10bit. DVP interface: RAW8/RAW10/RAW12/RAW14/RAW16 or YUV422 8bit/10bit. It can support up to 8 sensor inputs.

### Video Input PIPE

ISP is primarily responsible for image processing, hard-core function configuration, and supports multi-context, with a maximum of 8 inputs. It mainly performs pipeline processing on the image data and outputs YUV image format to the channel. The PIPE also includes the functionality of DIS and LDC.

### Video Physical Channels

VIN's PIPE contains 2 physical channels. Physical channel 0 refers to the data processed by ISP going to DDR, or passed to the next level module VPS through DDR. Physical channel 1 refers to the data processed by ISP going online to VPS. Please refer to the "System Control" chapter for the binding relationship between VIN and VPS.### Binding Relationship

For the binding relationship between VIN and VPS, please refer to the "System Control" chapter HB_SYS_SetVINVPSMode.


### API Reference

```c
int HB_MIPI_SetBus(MIPI_SENSOR_INFO_S *snsInfo, uint32_t busNum);
int HB_MIPI_SetPort(MIPI_SENSOR_INFO_S *snsInfo, uint32_t port);
int HB_MIPI_SensorBindSerdes(MIPI_SENSOR_INFO_S *snsInfo, uint32_t serdesIdx, uint32_t serdesPort);
int HB_MIPI_SensorBindMipi(MIPI_SENSOR_INFO_S *snsInfo, uint32_t mipiIdx);
int HB_MIPI_SetExtraMode(MIPI_SENSOR_INFO_S *snsInfo, uint32_t ExtraMode);
int HB_MIPI_InitSensor(uint32_t DevId, MIPI_SENSOR_INFO_S *snsInfo);
int HB_MIPI_DeinitSensor(uint32_t DevId);
int HB_MIPI_ResetSensor(uint32_t DevId);
int HB_MIPI_UnresetSensor(uint32_t DevId);
int HB_MIPI_EnableSensorClock(uint32_t mipiIdx);
int HB_MIPI_DisableSensorClock(uint32_t mipiIdx);
int HB_MIPI_SetSensorClock(uint32_t mipiIdx, uint32_t snsMclk);
int HB_MIPI_ResetMipi(uint32_t mipiIdx);
int HB_MIPI_UnresetMipi(uint32_t mipiIdx);
int HB_MIPI_SetMipiAttr(uint32_t mipiIdx, MIPI_ATTR_S mipiAttr);
int HB_MIPI_Clear(uint32_t mipiIdx);
int HB_MIPI_ReadSensor(uint32_t devId, uint32_t regAddr, char *buffer, uint32_t size);
int HB_MIPI_WriteSensor(uint32_t devId, uint32_t regAddr, char *buffer, uint32_t size);
int HB_MIPI_GetSensorInfo(uint32_t devId, MIPI_SENSOR_INFO_S *snsInfo);
int HB_MIPI_SwSensorFps(uint32_t devId, uint32_t fps);
int HB_VIN_SetMipiBindDev(uint32_t devId, uint32_t mipiIdx);
int HB_VIN_GetMipiBindDev(uint32_t devId, uint32_t *mipiIdx);
int HB_VIN_SetDevAttr(uint32_t devId, const VIN_DEV_ATTR_S *stVinDevAttr);
int HB_VIN_GetDevAttr(uint32_t devId, VIN_DEV_ATTR_S *stVinDevAttr);
int HB_VIN_SetDevAttrEx(uint32_t devId, const VIN_DEV_ATTR_EX_S *stVinDevAttrEx);
int HB_VIN_GetDevAttrEx(uint32_t devId, VIN_DEV_ATTR_EX_S *stVinDevAttrEx);
int HB_VIN_EnableDev(uint32_t devId);
int HB_VIN_DisableDev(uint32_t devId);
int HB_VIN_DestroyDev(uint32_t devId);
int HB_VIN_SetDevBindPipe(uint32_t devId, uint32_t pipeId);
int HB_VIN_GetDevBindPipe(uint32_t devId, uint32_t *pipeId);
int HB_VIN_CreatePipe(uint32_t pipeId, const VIN_PIPE_ATTR_S *stVinPipeAttr);
int HB_VIN_DestroyPipe(uint32_t pipeId);
int HB_VIN_StartPipe(uint32_t pipeId);
int HB_VIN_StopPipe(uint32_t pipeId);
int HB_VIN_EnableChn(uint32_t pipeId, uint32_t chnId);
int HB_VIN_DisableChn(uint32_t pipeId, uint32_t chnId);
int HB_VIN_SetChnLDCAttr(uint32_t pipeId, uint32_t chnId, const VIN_LDC_ATTR_S *stVinLdcAttr);
int HB_VIN_GetChnLDCAttr(uint32_t pipeId, uint32_t chnId, VIN_LDC_ATTR_S *stVinLdcAttr);
int HB_VIN_SetChnDISAttr(uint32_t pipeId, uint32_t chnId, const VIN_DIS_ATTR_S *stVinDisAttr);
int HB_VIN_GetChnDISAttr(uint32_t pipeId, uint32_t chnId, VIN_DIS_ATTR_S *stVinDisAttr);
```c
int HB_MIPI_SetBus(MIPI_SENSOR_INFO_S *snsInfo, uint32_t busNum);
```

### HB_MIPI_SetBus
【Function Declaration】
```c
int HB_MIPI_SetBus(MIPI_SENSOR_INFO_S *snsInfo, uint32_t busNum);
```
【Description】
> Set the bus number of the sensor.

【Parameter Description】

| Parameter Name |       Description       | Input/Output |
| :------------: | :--------------------: | :----------: |
|    snsInfo     | Configuration of sensor |    Input     |
|    busNum      |         bus number      |    Input     |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|       0      |   Success   |
|     Non-zero |   Failure   |

【Note】
> None

【Reference Code】Please refer to the example of HB_MIPI_InitSensor/HB_MIPI_DeinitSensor.

### HB_MIPI_SetPort
【Function Declaration】
```c
int HB_MIPI_SetPort(MIPI_SENSOR_INFO_S *snsInfo, uint32_t port)
```
【Description】
> Set the port of the sensor, with values ranging from 0 to 7.

【Parameter Description】

| Parameter Name |        Description        | Input/Output |
| :------------: | :-----------------------: | :----------: |
|    snsInfo     | Configuration information of the sensor |    Input     |
|      port      |    The current port number of the sensor, ranging from 0 to 7   |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | :--------: |
|       0      |   Success  |
|    Non-0     |   Failure  |

【Note】
> None

【Reference Code】
> Please refer to the example of HB_MIPI_InitSensor/HB_MIPI_DeinitSensor.

### HB_MIPI_SensorBindSerdes
【Function Declaration】
```c
int HB_MIPI_SensorBindSerdes(MIPI_SENSOR_INFO_S *snsInfo, uint32_t serdesIdx, uint32_t serdesPort)
```
【Description】
> Set which serdes the sensor is bound to.

【Parameter Description】

|  Parameter Name   |                  Description                  | Input/Output |
| :---------------: | :------------------------------------------: | :----------: |
|     snsInfo       |          Configuration information of the sensor          |    Input     |
|    serdesIdx      |                   Serdes index, ranging from 0 to 1                  |    Input     |
|    serdesPort     |    Serdes port number: 954 (ranging from 0 to 1) or 960 (ranging from 0 to 3)  |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | :--------: |
| ExtraMode | DOL2或DOL3下的工作模式 | 输入 |

【返回值】

| 返回值 |  描述 |
|:-----:|:----:|
|   0   |  成功 |
|  非0  |  失败 |

【注意事项】
> 无

【参考代码】
> 请参见HB_MIPI_InitSensor举例| ExtraMode | Select the working mode | 1. Single DOL2, value is 0<br /> 2. DOL2 divided into two linear modes, one value is 1, the other value is 2<br /> 3. Single DOL3, value is 0<br /> 4. One DOL2 (value is 1) + one linear (value is 4)<br /> 5. DOL3 divided into three linear modes, one value is 2, one value is 3, one value is 4 |

【Return Value】

| Return Value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Notes】
> None

【Reference Code】
> Please refer to the examples of HB_MIPI_InitSensor/HB_MIPI_DeinitSensor

### HB_MIPI_InitSensor/HB_MIPI_DeinitSensor
【Function Declaration】
```c
int HB_MIPI_InitSensor (uint32_t DevId, MIPI_SENSOR_INFO_S  *snsInfo);
int HB_MIPI_DeinitSensor (uint32_t  DevId);
```
【Function Description】
> Initialize and release the resources generated by initialization of the sensor

【Parameter Description】

| Parameter Name |       Description        | Input/Output |
| :------: | :---------------: | :-------: |
|  devId   | Channel index, range 0~7 |   Input    |
| snsInfo  |    Sensor information    |   Input    |

【Return Value】

| Return Value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Notes】
> None

【Reference Code】
```c
    MIPI_SENSOR_INFO_S  snsInfo;
    MIPI_ATTR_S  mipiAttr;
    int DevId = 0, mipiIdx = 1;
    int bus = 1, port = 0, serdes_index = 0, serdes_port = 0;
    int ExtraMode= 0;

    memset(snsInfo, 0, sizeof(MIPI_SENSOR_INFO_S));
```memset(mipiAttr, 0, sizeof(MIPI_ATTR_S));
snsInfo.sensorInfo.bus_num = 0;
snsInfo.sensorInfo.bus_type = 0;
snsInfo.sensorInfo.entry_num = 0;
snsInfo.sensorInfo.sensor_name = "imx327";
snsInfo.sensorInfo.reg_width = 16;
snsInfo.sensorInfo.sensor_mode = NORMAL_M;
snsInfo.sensorInfo.sensor_addr = 0x36;

mipiAttr.dev_enable = 1;
mipiAttr.mipi_host_cfg.lane = 4;
mipiAttr.mipi_host_cfg.datatype = 0x2c;
mipiAttr.mipi_host_cfg.mclk = 24;
mipiAttr.mipi_host_cfg.mipiclk = 891;
mipiAttr.mipi_host_cfg.fps = 25;
mipiAttr.mipi_host_cfg.width = 1952;
mipiAttr.mipi_host_cfg.height = 1097;
mipiAttr.mipi_host_cfg->linelenth = 2475;
mipiAttr.mipi_host_cfg->framelenth = 1200;
mipiAttr.mipi_host_cfg->settle = 20;

HB_MIPI_SetBus(snsInfo, bus);
HB_MIPI_SetPort(snsinfo, port);
HB_MIPI_SensorBindSerdes(snsinfo, sedres_index, sedres_port);
HB_MIPI_SensorBindMipi(snsinfo, mipiIdx);
HB_MIPI_SetExtraMode(snsinfo, ExtraMode);
ret = HB_MIPI_InitSensor(DevId, snsInfo);
if (ret < 0) {
    printf("HB_MIPI_InitSensor error!\n");
    return ret;
}
ret = HB_MIPI_SetMipiAttr(mipiIdx, mipiAttr);
if (ret < 0) {
    printf("HB_MIPI_SetMipiAttr error! do sensorDeinit\n");
    HB_MIPI_SensorDeinit(DevId);
    return ret;
}
ret = HB_MIPI_ResetSensor(DevId);
if (ret < 0) {
    printf("HB_MIPI_ResetSensor error! do mipi deinit\n");
    HB_MIPI_DeinitSensor(DevId);
    HB_MIPI_Clear(mipiIdx);
    return ret;
}
ret = HB_MIPI_ResetMipi(mipiIdx);
if (ret < 0) {
    printf("HB_MIPI_ResetMipi error!\n");
    HB_MIPI_UnresetSensor(DevId);
    HB_MIPI_DeinitSensor(DevId);
    HB_MIPI_Clear(mipiIdx);```c
int HB_MIPI_EnableSensorClock(uint32_t mipiIdx);
int HB_MIPI_DisableSensorClock(uint32_t mipiIdx);
```

【功能描述】
> Function to enable/disable the sensor_clk.

【参数描述】

| 参数名称 |           描述            | 输入/输出 |
| :------: | :-----------------------: | :-------: |
| mipiIdx  | Mipi host 索引号，范围0~3 |   输入    |

【返回值】

| 返回值 | 描述 |
|:------:|:----:|
|    0   | 成功 |
|   非0  | 失败 |

【注意事项】
> 无

【参考代码】
> Please refer to the examples for HB_MIPI_InitSensor/HB_MIPI_DeinitSensor.【Return Values】

| Return Value | Description |
|:------------:|:-----------:|
|      0       |   Success   |
|     Non-zero    |   Failure   |

【Notes】
> Remove the crystal oscillator from the sub-board when using this interface.

【Reference Code】
> N/A

### HB_MIPI_SetSensorClock
【Function Declaration】
```c
int HB_MIPI_SetSensorClock(uint32_t mipiIdx, uint32_t snsMclk)
```
【Function Description】
> Set sensor_mclk.
> There are a total of 4 sensor_mclk, currently using sensor0_mclk and sensor1_mclk,
> mipi0 is connected to sensor_mclk1, mipi1 is connected to sensor_mclk0, and the hardware connection relationship is defined in dts.

【Parameter Description】

| Parameter Name |             Description             | Input/Output |
| :------------: | :---------------------------------: | :----------: |
|    mipiIdx     | Mipi host index number, range 0~3 |    Input     |
|    snsMclk     |             Unit: HZ              |     Input    |

【Return Values】

| Return Value | Description |
|:------------:|:-----------:|
|      0       |   Success   |
|   Non-zero    |   Failure   |

【Notes】
> Remove the crystal oscillator from the sub-board when using this interface.

【Reference Code】
> During initialization:
>> Set the sensor_mclk first and then enable it.
>> HB_MIPI_SetSensorClock(mipiIdx, 24000000);
>> HB_MIPI_EnableSensorClock(mipiIdx);

> During exit:
>> HB_MIPI_Clear(mipiIdx);
>> HB_MIPI_DeinitSensor(devId);HB_MIPI_DisableSensorClock(mipiIdx);

### HB_MIPI_ResetMipi/HB_MIPI_UnresetMipi
【Function Declaration】
```c
int HB_MIPI_ResetMipi(uint32_t mipiIdx);
int HB_MIPI_UnresetMipi(uint32_t mipiIdx);
```
【Description】
> Start and stop of mipi.

【Parameter Description】

| Parameter Name |          Description          | Input/Output |
| :------------: | :---------------------------: | :----------: |
|    mipiIdx     | Mipi host index, range: 0~3   |    Input     |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|       0      |   Success   |
|    Non-zero  |   Failure   |

【Note】
> None

【Reference Code】
> Please refer to the example of HB_MIPI_InitSensor/HB_MIPI_DeinitSensor

### HB_MIPI_SetMipiAttr
【Function Declaration】
```c
int HB_MIPI_SetMipiAttr(uint32_t mipiIdx, MIPI_ATTR_S mipiAttr);
```
【Description】
> Set the attributes of mipi, initialize host and dev.

【Parameter Description】

| Parameter Name |       Description       | Input/Output |
| :------------: | :--------------------: | :----------: |
|    mipiIdx     |  Mipi host index number |    Input     |
|    mipiAttr    |    Mipi bus attributes |    Input     |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|       0      |   Success   || size     |      数据大小     |   输入    |

【返回值】

| 返回值 |   描述   |
|:------:|:--------:|
|   0    |   成功   |
|  非0   |   失败   |

【注意事项】
> 无

【参考代码】
> 请参见HB_MIPI_InitSensor/HB_MIPI_DeinitSensor举例| Parameter Name | Description | Input/Output |
|:--------------:|:-----------:|:-----------:|
|    devId       | 设备ID      |    Input    |
|    regAddr     | 寄存器地址  |    Input    |
|    buffer      | 数据缓冲区  |    Input    |
|    size        | 写入的长度  |    Input    |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|      0       |    Success  |
|    Non-zero  |    Failure  |

【Note】
> 必须在HB_MIPI_InitSensor接口调用后才能使用

【Reference Code】
> Different sensors have different implementations. Taking imx327 as an example:
```c
    int i;
    char buffer[] = {0x34, 0x56};
    char rev_buffer[30] = {0};
    printf("HB_MIPI_InitSensor end\n");
    ret = HB_MIPI_ReadSensor(devId, 0x3018, rev_buffer,  2);
    if(ret < 0) {
        printf("HB_MIPI_ReadSensor error\n");
    }
    for(i = 0; i < strlen(rev_buffer); i++) {
        printf("rev_buffer[%d] 0x%x  \n", i, rev_buffer[i]);
    }
    ret = HB_MIPI_WriteSensor(devId, 0x3018, buffer, 2);
    if(ret < 0) {
        printf("HB_MIPI_WriteSensor error\n");
    }
    ret = HB_MIPI_ReadSensor(devId, 0x3018, rev_buffer, 2);
    if(ret < 0) {
        printf("HB_MIPI_ReadSensor error\n");
    }
    for(i = 0; i < strlen(rev_buffer); i++) {
        printf("rev_buffer[%d] 0x%x  \n", i, rev_buffer[i]);
    }
```

### HB_MIPI_WriteSensor
【Function Declaration】
```c
int HB_MIPI_WriteSensor (uint32_t devId, uint32_t regAddr, char *buffer, uint32_t size)
```
【Function Description】
> Write sensor registers through I2C

【Parameter Description】

| Parameter Name | Description | Input/Output |
|:--------------:|:-----------:|:-----------:|
|    devId       | Device ID   |    Input    |
|    regAddr     | Register Address |    Input    |
|    buffer      | Data Buffer |    Input    |
|    size        | Size of write |    Input    |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|      0       |    Success  |
|    Non-zero  |    Failure  |

【Note】
> This function can only be used after the HB_MIPI_InitSensor interface is called.| :------: | :---------------: | :-------: |
|  devId   | Channel index, range 0~7 |   Input    |
| regAddr  |    Register address     |   Input    |
|  buffer  |  Address to store data   |   Input    |
|   size   |     Length of data to write      |   Input    |

【Return Value】

| Return Value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Notes】
> Must be called after the HB_MIPI_InitSensor interface

【Reference Code】
> Please refer to the example of HB_MIPI_ReadSensor

### HB_MIPI_GetSensorInfo
【Function Declaration】
```c
int HB_MIPI_GetSensorInfo(uint32_t devId, MIPI_SENSOR_INFO_S *snsInfo)
```
【Function Description】
> Get sensor-related configuration information

【Parameter Description】

| Parameter Name |       Description        | Input/Output |
| :------: | :---------------: | :-------: |
|  devId   | Channel index, range 0~7 |   Input    |
| snsInfo  |    Sensor information     |   Output    |

【Return Value】

| Return Value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Notes】
> Must be called after the HB_MIPI_InitSensor interface

【Reference Code】
```c
    MIPI_SENSOR_INFO_S *snsinfo = NULL;
    snsinfo = malloc(sizeof(MIPI_SENSOR_INFO_S));
    if(snsinfo == NULL) {
        printf("malloc error\n");
``````c
return -1;
    }
    memset(snsinfo, 0, sizeof(MIPI_SENSOR_INFO_S));
    ret = HB_MIPI_GetSensorInfo(devId, snsinfo);
    if(ret < 0) {
        printf("HB_MIPI_InitSensor error!\n");
        return ret;
    }
```

### HB_MIPI_SwSensorFps
【Function Declaration】
```c
int HB_MIPI_SwSensorFps(uint32_t devId, uint32_t fps)
```
【Description】
> Switch the frame rate of the sensor.

【Parameter Description】

| Parameter Name |               Description               |  Input/Output |
| :------------: | :------------------------------------: | :-----------: |
|     devId      | Channel index, range 0~7 |     Input     |
|      fps       |           Frame rate of the sensor           |     Input     |

【Return Value】

|  Return Value  | Description |
| :------------: | :--------: |
|       0        |   Success  |
| Non-zero value |   Failure  |

【Notes】
> Must be called after the HB_MIPI_InitSensor interface.

【Reference Code】
>No reference code available.

### HB_VIN_SetMipiBindDev/HB_VIN_GetMipiBindDev
【Function Declaration】
```c
int HB_VIN_SetMipiBindDev(uint32_t devId, uint32_t mipiIdx)
int HB_VIN_GetMipiBindDev(uint32_t devId, uint32_t *mipiIdx)
```
【Description】
> Set the binding between mipi and dev, specify which mipi_host the dev uses.

【Parameter Description】

| Parameter Name |             Description              |  Input/Output |
| :------------: | :---------------------------------: | :-----------: |
|     devId      | Channel index, range 0~7|     Input     |
|    mipiIdx    |  MIPI index |     Input/Output    |

【Return Value】

|  Return Value  | Description |
| :------------: | :--------: |
|       0        |   Success  |
| Non-zero value |   Failure  || :------: | :---------------------: | :-------: |
|  devId   | Corresponding channel index, range 0~7 |   Input    |
|mipiIdx|Mipi_host index| Input|

【Return Value】

| Return value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Notes】
> None

【Reference Code】
> Please refer to the example of HB_VIN_CreatePipe/HB_VIN_DestroyPipe

### HB_VIN_SetDevAttr/HB_VIN_GetDevAttr
【Function Declaration】
```c
int HB_VIN_SetDevAttr(uint32_t devId,  const VIN_DEV_ATTR_S *stVinDevAttr)
int HB_VIN_GetDevAttr(uint32_t devId, VIN_DEV_ATTR_S *stVinDevAttr)
```
【Function Description】
> Set and get the attributes of the device

【Parameter Description】

|   Parameter Name   |          Description           |             Input/Output             |
| :----------: | :---------------------: | :-------------------------------: |
|    devId     | Corresponding channel index, range 0~7 |               Input                |
| stVinDevAttr |       Device channel attributes       | Input, output when calling HB_VIN_GetDevAttr |

【Return Value】

| Return value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Notes】
> When splitting DOL3 into multiple channels, in the case of multiple processes: the first process needs to be run for at least 1 second before the second process.
> Additionally, HB_VIN_SetDevAttr is not supported after calling HB_VIN_DestroyDev.
>
> If "SIF_IOC_BIND_GROUT ioctl failed" error occurs, it is generally because the previous call to pipeid did not exit before being called again.

【Reference Code】
> Please refer to the example of HB_VIN_CreatePipe/HB_VIN_DestroyPipe

### HB_VIN_SetDevAttrEx/HB_VIN_GetDevAttrEx【Function Declaration】
```c
int HB_VIN_SetDevAttrEx(uint32_t devId, const VIN_DEV_ATTR_EX_S *stVinDevAttrEx)
int HB_VIN_GetDevAttrEx(uint32_t devId, VIN_DEV_ATTR_EX_S *stVinDevAttrEx)
```
【Description】
> Set or get the extended attributes of the device

【Parameter Description】

| Parameter Name |             Description              | Input/Output |
| :------------: | :----------------------------------: | :----------: |
|     devId      | Channel index, range: 0~7            |    Input     |
| stVinDevAttrEx | Extended attributes of the device    |  Input; Output when calling HB_VIN_GetDevAttr  |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|      0       |    Success  |
|   Non-zero   |    Failed   |

【Note】
> This interface is not supported at present

【Reference Code】
> None

### HB_VIN_EnableDev/HB_VIN_DisableDev
【Function Declaration】
```c
int HB_VIN_EnableDev(uint32_t devId);
int HB_VIN_DisableDev(uint32_t devId);
```
【Description】
> Enable or disable the dev module

【Parameter Description】

| Parameter Name |               Description               |  Input/Output  |
| :------------: | :------------------------------------: | :------------: |
|     devId      | Corresponding input for each route, 0~7 |     Input      |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|      0       |    Success  |
|   Non-zero   |    Failed   |【Notes】
> None

【Reference code】
> Please refer to the example of HB_VIN_CreatePipe/HB_VIN_DestroyPipe

### HB_VIN_DestroyDev
【Function Declaration】
```c
int HB_VIN_DestroyDev(uint32_t devId)
```
【Function Description】
> Destroy the dev module and release resources.

【Parameter Description】

| Parameter |       Description       | Input/Output |
| :-------: | :--------------------: | :----------: |
|   devId   | Corresponds to each input, range: 0~7 |     Input    |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|      0       |   Success   |
|   Non-zero   |   Failure   |

【Notes】
> None

【Reference code】
> Please refer to the example of HB_VIN_CreatePipe/HB_VIN_DestroyPipe

### HB_VIN_SetDevBindPipe/HB_VIN_GetDevBindPipe
【Function Declaration】
```c
int HB_VIN_SetDevBindPipe(uint32_t devId, uint32_t pipeId)
int HB_VIN_GetDevBindPipe(uint32_t devId, uint32_t *pipeId)
```
【Function Description】
> Set the binding between the chn output of the dev and the chn input of the pipe.
> Set the binding between the chn input of the pipe and the chn output of the pipe.

【Parameter Description】

|  Parameter  |       Description       | Input/Output |
| :---------: | :--------------------: | :----------: |
|   devId     | Corresponds to each input, range: 0~7 |     Input    |
|   pipeId    | Corresponds to each input, same as above |     Input    |【Return Value】

| Return Value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Notes】
> HB_VIN_GetDevBindPipe interface is not implemented yet.

【Reference Code】
> Please refer to the examples of HB_VIN_CreatePipe/HB_VIN_DestroyPipe.

### HB_VIN_CreatePipe/HB_VIN_DestroyPipe

【Function Declaration】
```c
int HB_VIN_CreatePipe(uint32_t pipeId, const VIN_PIPE_ATTR_S * stVinPipeAttr);
int HB_VIN_DestroyPipe(uint32_t pipeId);
```

【Function Description】
> Create pipe, destroy pipe.

【Parameter Description】

| Parameter Name |         Description          | Input/Output |
| :------: | :-------------------: | :-------: |
|  pipeId  | Corresponding to each input, range from 0 to 7 |   Input    |
|stVinPipeAttr|Pointer describing the pipe attributes|Input|

【Return Value】

| Return Value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Notes】
> None

【Reference Code】
```c
    VIN_DEV_ATTR_S  stVinDevAttr;
    VIN_PIPE_ATTR_S  stVinPipeAttr;
    VIN_DIS_ATTR_S   stVinDisAttr;
    VIN_LDC_ATTR_S  stVinLdcAttr;
    MIPI_SNS_TYPE_E sensorId = 1;
    MIPI_SENSOR_INFO_S  snsInfo;
    MIPI_ATTR_S  mipiAttr;
    MIPI_SNS_TYPE_E sensorId = 1;
```int PipeId = 0;
int DevId = 0, mipiIdx = 1;
int ChnId = 1, bus = 1, port = 0, serdes_index = 0, serdes_port = 0;

memset(snsInfo, 0, sizeof(MIPI_SENSOR_INFO_S));
memset(mipiAttr, 0, sizeof(MIPI_ATTR_S));
memset(stVinDevAttr, 0, sizeof(VIN_DEV_ATTR_S));
memset(stVinPipeAttr, 0, sizeof(VIN_PIPE_ATTR_));
memset(stVinDisAttr, 0, sizeof(VIN_DIS_ATTR_S));
memset(stVinLdcAttr, 0, sizeof(VIN_LDC_ATTR_S));
snsInfo.sensorInfo.bus_num = 0;
snsInfo.sensorInfo.bus_type = 0;
snsInfo.sensorInfo.entry_num = 0;
snsInfo.sensorInfo.sensor_name = "imx327";
snsInfo.sensorInfo.reg_width = 16;
snsInfo.sensorInfo.sensor_mode = NORMAL_M;
snsInfo.sensorInfo.sensor_addr = 0x36;

mipiAttr.dev_enable = 1;
mipiAttr.mipi_host_cfg.lane = 4;
mipiAttr.mipi_host_cfg.datatype = 0x2c;
mipiAttr.mipi_host_cfg.mclk = 24;
mipiAttr.mipi_host_cfg.mipiclk = 891;
mipiAttr.mipi_host_cfg.fps = 25;
mipiAttr.mipi_host_cfg.width = 1952;
mipiAttr.mipi_host_cfg.height = 1097;
mipiAttr.mipi_host_cfg->linelenth = 2475;
mipiAttr.mipi_host_cfg->framelenth = 1200;
mipiAttr.mipi_host_cfg->settle = 20;
stVinDevAttr.stSize.format = 0;
stVinDevAttr.stSize.width = 1952;
stVinDevAttr.stSize.height = 1097;
stVinDevAttr.stSize.pix_length = 2;
stVinDevAttr.mipiAttr.enable = 1;
stVinDevAttr.mipiAttr.ipi_channels =  1;
stVinDevAttr.mipiAttr.enable_frame_id = 1;
stVinDevAttr.mipiAttr.enable_mux_out = 1;
stVinDevAttr.DdrIspAttr.enable = 1;
stVinDevAttr.DdrIspAttr.buf_num = 4;
stVinDevAttr.DdrIspAttr.raw_feedback_en = 0;
stVinDevAttr.DdrIspAttr.data.format = 0;
stVinDevAttr.DdrIspAttr.data.width = 1952;
stVinDevAttr.DdrIspAttr.data.height = 1907;
stVinDevAttr.DdrIspAttr.data.pix_length = 2;
stVinDevAttr.outIspAttr.isp_enable = 1;
stVinDevAttr.outIspAttr.dol_exp_num = 4;
stVinDevAttr.outIspAttr.enable_flyby = 0;
stVinDevAttr.outDdrAttr.enable = 1;
stVinDevAttr.outDdrAttr.mux_index = 0;
stVinDevAttr.outDdrAttr.buffer_num = 10;stVinDevAttr.outDdrAttr.raw_dump_en = 0;
    stVinDevAttr.outDdrAttr.stride = 2928;
    stVinDevAttr.outIpuAttr.enable_flyby = 0;

    stVinPipeAttr.ddrOutBufNum = 8;
    stVinPipeAttr.pipeDmaEnable = 1;
    stVinPipeAttr.snsMode = 3;
    stVinPipeAttr.stSize.format = 0;
    stVinPipeAttr.stSize.width = 1920;
    stVinPipeAttr.stSize.height = 1080;
    stVinDisAttr.xCrop.rg_dis_start = 0;
    stVinDisAttr.xCrop.rg_dis_end = 1919;
    stVinDisAttr.yCrop.rg_dis_start = 0;
    stVinDisAttr.yCrop.rg_dis_end = 1079
    stVinDisAttr.disHratio = 65536;
    stVinDisAttr.disVratio = 65536;
    stVinDisAttr.disPath.rg_dis_enable = 0;
    stVinDisAttr.disPath.rg_dis_path_sel = 1;
    stVinDisAttr.picSize.pic_w = 1919;
    stVinDisAttr.picSize.pic_h = 1079;
    stVinLdcAttr->ldcEnable = 0;
    stVinLdcAttr->ldcPath.rg_h_blank_cyc = 32;
    stVinLdcAttr->yStartAddr = 524288;
    stVinLdcAttr->cStartAddr = 786432;
    stVinLdcAttr->picSize.pic_w = 1919;
    stVinLdcAttr->picSize.pic_h = 1079;
    stVinLdcAttr->lineBuf = 99;
    stVinLdcAttr->xParam.rg_algo_param_a = 1;
    stVinLdcAttr->xParam.rg_algo_param_b = 1;
    stVinLdcAttr->yParam.rg_algo_param_a = 1;
    stVinLdcAttr->yParam.rg_algo_param_b = 1;
    stVinLdcAttr->xWoi.rg_length = 1919;
    stVinLdcAttr->xWoi.rg_start = 0;
    stVinLdcAttr->yWoi.rg_length = 1079;
    stVinLdcAttr->yWoi.rg_start = 0;

    ret = HB_VIN_CreatePipe(PipeId, pipeInfo);
    if(ret < 0) {
        printf("HB_VIN_CreatePipe t error!\n");
        HB_VIN_DestroyPipe(PipeId);
        return ret;
    }
    ret = HB_VIN_SetMipiBindDev(pipeId, mipiIdx);
    if(ret < 0) {
        printf("HB_VIN_SetMipiBindDev error!\n");
        HB_VIN_DestroyPipe(PipeId);
        return ret;
    }
    ret = HB_VIN_SetDevVCNumber(pipeId, deseri_port);
    if(ret < 0) {
printf("HB_MIPI_SetMipiAttr error!\n");
        HB_MIPI_DeInitSensor(devId);
        HB_VIN_DestroyPipe(PipeId);
        return ret;
    }
    ret = HB_MIPI_StartSensor(devId);
    if(ret < 0) {
        printf("HB_MIPI_StartSensor error!\n");
        HB_MIPI_DeInitSensor(devId);
        HB_VIN_DestroyPipe(PipeId);
        return ret;
    }
    ret = HB_VIN_StartDev(DevId);
    if(ret < 0) {
        printf("HB_VIN_StartDev error!\n");
        HB_MIPI_StopSensor(devId);
        HB_MIPI_DeInitSensor(devId);
        HB_VIN_DestroyPipe(PipeId);
        return ret;
    }
    ret = HB_VIN_StartPipe(PipeId);
    if(ret < 0) {
        printf("HB_VIN_StartPipe error!\n");
        HB_VIN_StopDev(DevId);
        HB_MIPI_StopSensor(devId);
        HB_MIPI_DeInitSensor(devId);
        HB_VIN_DestroyPipe(PipeId);
        return ret;
    }
    ret = HB_VIN_StartChn(PipeId, ChnId);
    if(ret < 0) {
        printf("HB_VIN_StartChn error!\n");
        HB_VIN_StopPipe(PipeId);
        HB_VIN_StopDev(DevId);
        HB_MIPI_StopSensor(devId);
        HB_MIPI_DeInitSensor(devId);
        HB_VIN_DestroyPipe(PipeId);
        return ret;
    }
    printf("HB_VIN_StartChn successfully!\n");

    return ret;printf("HB_MIPI_SetMipiAttr 错误！进行摄像头反初始化\n");
        HB_MIPI_SensorDeinit(sensorId);
        HB_VIN_DestroyPipe(PipeId);
        return ret;
    }

    ret = HB_VIN_EnableChn(PipeId, ChnId );
    if(ret < 0) {
        printf("HB_VIN_EnableChn 错误！\n");
        HB_MIPI_DeinitSensor(DevId );
        HB_MIPI_Clear(mipiIdx);
        HB_VIN_DestroyDev(pipeId);
        HB_VIN_DestroyChn(pipeId, ChnId);
        HB_VIN_DestroyPipe(pipeId);
        return ret;
    }
    ret = HB_VIN_StartPipe(PipeId);
    if(ret < 0) {
        printf("HB_VIN_StartPipe 错误！\n");
        HB_MIPI_DeinitSensor(DevId );
        HB_MIPI_Clear(mipiIdx);
        HB_VIN_DisableChn(pipeId, ChnId);
        HB_VIN_DestroyDev(pipeId);
        HB_VIN_DestroyChn(pipeId, ChnId);
        HB_VIN_DestroyPipe(pipeId);
        return ret;
    }
    ret = HB_VIN_EnableDev(DevId);
    if(ret < 0) {
        printf("HB_VIN_EnableDev 错误！\n");
        HB_MIPI_DeinitSensor(DevId );
        HB_MIPI_Clear(mipiIdx);
        HB_VIN_DisableChn(pipeId, ChnId);
        HB_VIN_StopPipe(pipeId);
        HB_VIN_DestroyDev(pipeId);
        HB_VIN_DestroyChn(pipeId, ChnId);
        HB_VIN_DestroyPipe(pipeId);
        return ret;
    }
    ret = HB_MIPI_ResetSensor(DevId );
    if(ret < 0) {
        printf("HB_MIPI_ResetSensor 错误！进行摄像头反初始化\n");
        HB_MIPI_DeinitSensor(DevId );
        HB_MIPI_Clear(mipiIdx);
        HB_VIN_DisableDev(pipeId);
        HB_VIN_StopPipe(pipeId);
        HB_VIN_DisableChn(pipeId, ChnId);
        HB_VIN_DestroyDev(pipeId);
        HB_VIN_DestroyChn(pipeId, ChnId);
        HB_VIN_DestroyPipe(pipeId);```c
return ret;
}
ret = HB_MIPI_ResetMipi(mipiIdx);
if (ret < 0) {
    printf("HB_MIPI_ResetMipi error!\n");
    HB_MIPI_UnresetSensor(DevId);
    HB_MIPI_DeinitSensor(DevId);
    HB_MIPI_Clear(mipiIdx);
    HB_VIN_DisableDev(pipeId);
    HB_VIN_StopPipe(pipeId);
    HB_VIN_DisableChn(pipeId, ChnId);
    HB_VIN_DestroyDev(pipeId);
    HB_VIN_DestroyChn(pipeId, ChnId);
    HB_VIN_DestroyPipe(pipeId);
    return ret;
}

HB_MIPI_UnresetSensor(DevId);
HB_MIPI_UnresetMipi(mipiIdx);
HB_VIN_DisableDev(PipeId);
HB_VIN_StopPipe(PipeId);
HB_VIN_DisableChn(PipeId, ChnId);
HB_MIPI_DeinitSensor(DevId);
HB_MIPI_Clear(mipiIdx);
HB_VIN_DestroyDev(DevId);
HB_VIN_DestroyChn(PipeId, ChnId);
HB_VIN_DestroyPipe(PipeId);
```

### HB_VIN_StartPipe/HB_VIN_StopPipe
【Function Declaration】
```c
int HB_VIN_StartPipe(uint32_t pipeId);
int HB_VIN_StopPipe(uint32_t pipeId);
```
【Function Description】
> Start or stop the pipe.

【Parameter Description】

| Parameter |                 Description                  | Input/Output |
| :-------: | :-----------------------------------------: | :----------: |
|  pipeId   | For each input, range is from 0 to 7 (inclusive) |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | :---------: |
|      0       |    Success  |
|    Non-zero  |    Failed   |【Note】
> None

【Reference Code】
> Please refer to the example of HB_VIN_CreatePipe/HB_VIN_DestroyPipe

### HB_VIN_EnableChn/HB_VIN_DisableChn
【Function Declaration】
```c
int HB_VIN_EnableChn(uint32_t pipeId, uint32_t chnId);
int HB_VIN_DisableChn(uint32_t pipeId, uint32_t chnId);
```
【Description】
> Enable or disable the channel of the pipe

【Parameter Description】

| Parameter Name |           Description            | Input/Output |
| :------------: | :-----------------------------: | :----------: |
|    pipeId      | Corresponds to each input, 0~7  |    Input     |
|     chnId      |            Input 1              |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | :---------: |
|       0      |   Success   |
|     Non-zero     |   Failure   |

【Note】
> None

【Reference Code】
> Please refer to the example of HB_VIN_CreatePipe/HB_VIN_DestroyPipe

### HB_VIN_SetChnLDCAttr/HB_VIN_GetChnLDCAttr
【Function Declaration】
```c
int HB_VIN_SetChnLDCAttr(uint32_t pipeId, uint32_t chnId,const VIN_LDC_ATTR_S *stVinLdcAttr);
int HB_VIN_GetChnLDCAttr(uint32_t pipeId, uint32_t chnId, VIN_LDC_ATTR_S*stVinLdcAttr);
```
【Description】
> Set and get the attributes of LDC

【Parameter Description】

| Parameter Name |           Description            |         Input/Output         |
| :------------: | :-----------------------------: | :--------------------------: |
|    pipeId      | Corresponds to each input, 0~7  |            Input             ||    chnId     |         1          |          input           |
| stVinLdcAttr |  ldc attribute info  | input, output when getting attribute |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|       0      |   Success   |
|     Non-0    |   Failure   |

【Notes】
> LDC has the function of adjusting the data timing sent to the IPU. When the VIN_ISP and VPS modules are in online mode, the LDC parameters must be configured through this interface, otherwise the VPS will be abnormal. The LDC parameter configuration does not affect the VIN_ISP and VPS modules in offline mode.

【Reference Code】
> Please refer to the examples of HB_VIN_CreatePipe/HB_VIN_DestroyPipe

### HB_VIN_SetChnDISAttr/HB_VIN_GetChnDISAttr
【Function Declaration】
```c
int HB_VIN_SetChnDISAttr(uint32_t pipeId, uint32_t chnId, const VIN_DIS_ATTR_S *stVinDisAttr);
int HB_VIN_GetChnDISAttr(uint32_t pipeId, uint32_t chnId, VIN_DIS_ATTR_S *stVinDisAttr);
```
【Function Description】
> Set and get the attributes of DIS

【Parameter Description】

|    Parameter Name    |       Description       |        Input/Output        |
| :------------------: | :---------------------: | :------------------------: |
|       pipeId         | Corresponds to each input, range from 0 to 7 |          Input           |
|        chnId         |           1             |          Input           |
|    stVinDisAttr      |   dis attribute info    | Input, output when getting attribute |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|       0      |   Success   |
|     Non-0    |   Failure   |

【Notes】
> None

【Reference Code】
> Please refer to the examples of HB_VIN_CreatePipe/HB_VIN_DestroyPipe

### HB_VIN_SetChnAttr
【Function Declaration】
```c
int HB_VIN_SetChnAttr(uint32_t pipeId, uint32_t chnId);
【Function Description】
> Set the properties of chn

【Parameter Description】

| Parameter Name |          Description           | Input/Output |
| :------------: | :----------------------------: | :----------: |
|    pipeId      | Corresponds to each input, range 0~7 |    Input    |
|    chnId       |            Input 1 only            |    Input    |

【Return Value】

| Return Value | Description |
| :----------: | :---------: |
|      0       |   Success   |
|    Non-0     |   Failure   |

【Notes】
> The properties of LDC and DIS are actually set in this interface. HB_VIN_SetChnLDCAttr and HB_VIN_SetChnDISAttr are only used to assign values to the properties. This chn refers to one of the output chn of isp, and its value is fixed as 1.

【Reference Code】
> Please refer to the example of HB_VIN_CreatePipe/HB_VIN_DestroyPipe

### HB_VIN_DestroyChn
【Function Declaration】
```c
int HB_VIN_DestroyChn(uint32_t pipeId, uint32_t chnId)
```
【Function Description】
> Destroy chn

【Parameter Description】

| Parameter Name |          Description           | Input/Output |
| :------------: | :----------------------------: | :----------: |
|    pipeId      | Corresponds to each input, range 0~7 |    Input    |
|    chnId       |            Input 1 only            |    Input    |

【Return Value】

| Return Value | Description |
| :----------: | :---------: |
|      0       |   Success   |
|    Non-0     |   Failure   |

【Notes】
> Currently, HB_VIN_SetChnAttr is not supported after HB_VIN_DestroyChn.

【Reference Code】Please refer to HB_VIN_CreatePipe/HB_VIN_DestroyPipe for examples.

### HB_VIN_GetChnFrame/HB_VIN_ReleaseChnFrame
【Function Declaration】
```c
int HB_VIN_GetChnFrame(uint32_t pipeId, uint32_t chnId, void *pstVideoFrame, int32_t millSec);
int HB_VIN_ReleaseChnFrame(uint32_t pipeId, uint32_t chnId, void *pstVideoFrame);
```
【Function Description】
> Get data from the pipe chn.

【Parameter Description】

|   Parameter Name    |                                                                Description                                                                | Input/Output |
| :-----------: | :--------------------------------------------------------------------------------------------------------------------------------: | :-------: |
|    pipeId     |                                                       Corresponds to each input, range: 0~7                                                        |   Input    |
|     chnId     |                                                             Input 0 is sufficient                                                              |   Input    |
| pstVideoFrame |                                                              Data information                                                              |   Output    |
|    millSec    | Timeout parameter millSec<br/>Set to -1 for blocking interface;<br/>Set to 0 for non-blocking interface;<br/>Set to a value greater than 0 for timeout waiting time, in milliseconds (ms)                     |   Input    |

【Return Value】

| Return Value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Note】
> This interface is used to get the image after ISP processing.

【Reference Code】
> Please refer to HB_VIN_CreatePipe/HB_VIN_DestroyPipe for examples.

### HB_VIN_GetDevFrame/HB_VIN_ReleaseDevFrame
【Function Declaration】
```c
int HB_VIN_GetDevFrame(uint32_t devId, uint32_t chnId, void *videoFrame, int32_t millSec);
int HB_VIN_ReleaseDevFrame(uint32_t devId, uint32_t chnId, void *buf);
```
【Function Description】
> Get data processed by sif chn, chn is 0.

【Parameter Description】

| Parameter Name  |                                                                Description                                                                | Input/Output |
| :-------: | :--------------------------------------------------------------------------------------------------------------------------------: | :-------: |
|   devId   |                                                       Corresponds to each input, range: 0~7                                                        |   Input    |
|   chnId   |                                                             Input 0 is sufficient                                                              |   Input    |
| videoFrame |                                                              Data information                                                              |   Output    |
|  millSec  | Timeout parameter millSec<br/>Set to -1 for blocking interface;<br/>Set to 0 for non-blocking interface;<br/>Set to a value greater than 0 for timeout waiting time, in milliseconds (ms)  |   Input    |【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|      0       |   Success   |
|    Non-zero  |   Failure   |

【Notes】
> This interface is used to obtain the image processed by SIF. Raw images can be dumped when using sif-offline-isp.
Applicable scenarios:
>>VIN_OFFLINE_VPS_ONLINE
>>VIN_OFFLINE_VPS_OFFINE
>>VIN_SIF_OFFLINE_ISP_OFFLINE_VPS_ONLINE

In addition, raw images can also be dumped when sif-online-isp simultaneously sends sif to ddr. Applicable scenarios:
>>VIN_SIF_ONLINE_DDR_ISP_DDR_VPS_ONLINE
>>VIN_SIF_ONLINE_DDR_ISP_ONLINE_VPS_ONLINE

【Reference Code】
```c
    typedef struct {
        uint32_t frame_id;
        uint32_t plane_count;
        uint32_t xres[MAX_PLANE];
        uint32_t yres[MAX_PLANE];
        char *addr[MAX_PLANE];
        uint32_t size[MAX_PLANE];
    } raw_t;
    typedef struct {
        uint8_t ctx_id;
        raw_t raw;
    } dump_info_t;
    dump_info_t dump_info = {0};
    hb_vio_buffer_t *sif_raw = NULL;
    int pipeId = 0;
    sif_raw = (hb_vio_buffer_t *) malloc(sizeof(hb_vio_buffer_t));
    memset(sif_raw, 0, sizeof(hb_vio_buffer_t));

    ret = HB_VIN_GetDevFrame(pipeId, 0, sif_raw, 2000);
    if (ret < 0) {
        printf("HB_VIN_GetDevFrame error!!!\n");
    } else {
        if (sif_raw->img_info.planeCount == 1) {
            dump_info.ctx_id = info->group_id;
            dump_info.raw.frame_id = sif_raw->img_info.frame_id;
            dump_info.raw.plane_count = sif_raw->img_info.planeCount;
            dump_info.raw.xres[0] = sif_raw->img_addr.width;
            dump_info.raw.yres[0] = sif_raw->img_addr.height;
            dump_info.raw.addr[0] = sif_raw->img_addr.addr[0];
```dump_info.raw.size[0] = size;
            printf("pipe(%d)dump normal raw frame id(%d),plane(%d)size(%d)\n",
                dump_info.ctx_id, dump_info.raw.frame_id,
                dump_info.raw.plane_count, size);
        } else if (sif_raw->img_info.planeCount == 2) {
            dump_info.ctx_id = info->group_id;
            dump_info.raw.frame_id = sif_raw->img_info.frame_id;
            dump_info.raw.plane_count = sif_raw->img_info.planeCount;
            for (int i = 0; i < sif_raw->img_info.planeCount; i ++) {
                dump_info.raw.xres[i] = sif_raw->img_addr.width;
                dump_info.raw.yres[i] = sif_raw->img_addr.height;
                dump_info.raw.addr[i] = sif_raw->img_addr.addr[i];
                dump_info.raw.size[i] = size;
            }
            if(sif_raw->img_info.img_format == 0) {
                printf("pipe(%d)dump dol2 raw frame id(%d),plane(%d)size(%d)\n",
                    dump_info.ctx_id, dump_info.raw.frame_id,
                    dump_info.raw.plane_count, size);
                }
            } else if (sif_raw->img_info.planeCount == 3) {
                dump_info.ctx_id = info->group_id;
                dump_info.raw.frame_id = sif_raw->img_info.frame_id;
                dump_info.raw.plane_count = sif_raw->img_info.planeCount;
                for (int i = 0; i < sif_raw->img_info.planeCount; i ++) {
                    dump_info.raw.xres[i] = sif_raw->img_addr.width;
                    dump_info.raw.yres[i] = sif_raw->img_addr.height;
                    dump_info.raw.addr[i] = sif_raw->img_addr.addr[i];
                    dump_info.raw.size[i] = size;
                }
                printf("pipe(%d)dump dol3 raw frame id(%d),plane(%d)size(%d)\n",
                dump_info.ctx_id, dump_info.raw.frame_id,
                dump_info.raw.plane_count, size);
            } else {
                printf("pipe(%d)raw buf planeCount wrong !!!\n", info->group_id);
            }
            for (int i = 0; i < dump_info.raw.plane_count; i ++) {
                if(sif_raw->img_info.img_format == 0) {
                    sprintf(file_name, "pipe%d_plane%d_%ux%u_frame_%03d.raw",
                            dump_info.ctx_id,
                            i,
                            dump_info.raw.xres[i],
                            dump_info.raw.yres[i],
                            dump_info.raw.frame_id);
                    dumpToFile(file_name,  dump_info.raw.addr[i], dump_info.raw.size[i]);
                }
            }
            if(sif_raw->img_info.img_format == 8) {
                sprintf(file_name, "pipe%d_%ux%u_frame_%03d.yuv",
                        dump_info.ctx_id,
                        dump_info.raw.xres[i],
                        dump_info.raw.yres[i],
                        dump_info.raw.frame_id);dump_info.raw.yres[i],
                        dump_info.raw.frame_id);
                dumpToFile2plane(file_name, sif_raw->img_addr.addr[0],
                    sif_raw->img_addr.addr[1], size, size/2);
            }
        }
        ret = HB_VIN_ReleaseDevFrame(pipeId, 0, sif_raw);
        if (ret < 0) {
            printf("HB_VIN_ReleaseDevFrame error!!!\n");
        }
        free(sif_raw);
        sif_raw = NULL;
    }

    int dumpToFile(char *filename, char *srcBuf, unsigned int size)
    {
        FILE *yuvFd = NULL;
        char *buffer = NULL;

        yuvFd = fopen(filename, "w+");
        if (yuvFd == NULL) {
            vio_err("ERRopen(%s) fail", filename);
            return -1;
        }
        buffer = (char *)malloc(size);
        if (buffer == NULL) {
            vio_err(":malloc file");
            fclose(yuvFd);
            return -1;
        }
        memcpy(buffer, srcBuf, size);
        fflush(stdout);
        fwrite(buffer, 1, size, yuvFd);
        fflush(yuvFd);
        if (yuvFd)
            fclose(yuvFd);
        if (buffer)
        free(buffer);
        vio_dbg("filedump(%s, size(%d) is successed\n", filename, size);
        return 0;
    }
    int dumpToFile2plane(char *filename, char *srcBuf, char *srcBuf1,
                        unsigned int size, unsigned int size1)
    {
        FILE *yuvFd = NULL;
        char *buffer = NULL;

        yuvFd = fopen(filename, "w+");
        if (yuvFd == NULL) {
            vio_err("open(%s) fail", filename);return -1;
        }
        buffer = (char *)malloc(size + size1);
        if (buffer == NULL) {
            vio_err("ERR:malloc file");
            fclose(yuvFd);
            return -1;
        }
        memcpy(buffer, srcBuf, size);
        memcpy(buffer + size, srcBuf1, size1);
        fflush(stdout);
        fwrite(buffer, 1, size + size1, yuvFd);
        fflush(yuvFd);
        if (yuvFd)
            fclose(yuvFd);
        if (buffer)
            free(buffer);
        vio_dbg("filedump(%s, size(%d) is successed\n", filename, size);
        return 0;
    }
```

### HB_VIN_SendPipeRaw
【Function Declaration】
```c
int HB_VIN_SendPipeRaw(uint32_t pipeId, void *pstVideoFrame，int32_t millSec)
```
【Function Description】
> Interface to send raw data for ISP processing.

【Parameter Description】

| Parameter Name |                                                                                                                                                                          Description                                                                                                                                                                           | Input/Output |
| :------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----------: |
|    pipeId      |                                                                                                                            Corresponding to each input, in the range of 0~7                                                                                                                             |    Input     |
| pstVideoFrame  |                                                                                                                         Information about the raw data to be sent back                                                                                                                                                                                          |    Input     |
|   millSec      | Timeout parameter millSec<br/>When set to -1, it is a blocking interface;<br/>When set to 0, it is a non-blocking interface;<br/>When set to a value greater than 0, it is a timeout waiting time.<br/>The unit of the timeout time is milliseconds (ms).                                                                                                               |    Input     |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|       0      |   Success   |
|     Non-zero |   Failure   |

【Note】
> None

【Reference Code】
```c
    return -1;
        }
        buffer = (char *)malloc(size + size1);
        if (buffer == NULL) {
            vio_err("ERR:malloc file");
            fclose(yuvFd);
            return -1;
        }
        memcpy(buffer, srcBuf, size);
        memcpy(buffer + size, srcBuf1, size1);
        fflush(stdout);
        fwrite(buffer, 1, size + size1, yuvFd);
        fflush(yuvFd);
        if (yuvFd)
            fclose(yuvFd);
        if (buffer)
            free(buffer);
        vio_dbg("filedump(%s, size(%d) is successed\n", filename, size);
        return 0;
    }
```int HB_VIN_CtrlPipeMirror(uint32_t pipeId, uint32_t mirrorNum, uint32_t mirror);
【功能描述】
> 控制pipe（ISP）的镜像功能

【参数描述】

|   参数名称    |           描述           | 输入/输出 |
| :-----------: | :----------------------: | :------: |
|    pipeId     |   对应每路输入，范围0~7   |   输入   |
|   mirrorNum   |  后续可能复用，目前不用   |   输入   |
|    mirror     | 镜像方式控制，参见EN_WI |   输入   |

【返回值】

| 返回值 |     描述     |
| :----: | :----------: |
|   0    |     成功     |
|   非0   | 非0失败代码 |

【注意事项】
> 无

【参考代码】
```c
HB_VIN_CtrlPipeMirror(0, 1, 1); //控制pipe 0 启用第 1 路镜像功能
``````c
int HB_VIN_InitLens(uint32_t pipeId, uint8_t calibFlag);
```
【Function Description】
> Initialize the lens.

【Parameter Description】

| Parameter Name |        Description         | Input/Output |
| :------------: | :------------------------: | :----------: |
|    pipeId      | Corresponding to each input, range from 0 to 7 |   Input      |
|   calibFlag    |   0 to disable calibration, non-zero to enable calibration   |   Input      |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|      0       |    Success  |
|   Non-zero   |   Failure   |

【Note】
> The calibration flag is used to enable or disable the lens calibration.【Function Declaration】
```c
int HB_VIN_InitLens(uint32_t pipeId, VIN_LENS_FUNC_TYPE_E lensType, const VIN_LENS_CTRL_ATTR_S *lenCtlAttr)
```
【Description】
> Motor driver initialization.

【Parameter Description】

| Parameter Name |             Description             |  Input/Output |
| :------------: | :---------------------------------: | :-----------: |
|    pipeId      | Corresponding to each input stream, ranging from 0~7 |    Input      |
|   lensType     | Type of motor function, AF, Zoom function |    Input      |
|  lenCtlAttr    |           Control attribute          |    Input      |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|       0      |   Success   |
|    Non-zero  |   Failure   |

【Notes】
> Invoke the interface once if using AF, if using both AF and Zoom functions, call the initialization twice. Call if needed, but it is not recommended to call if not used.

【Reference Code】
> None

### HB_VIN_DeinitLens
【Function Declaration】
```c
int HB_VIN_DeinitLens(uint32_t pipeId)
```
【Description】
> Motor exit

【Parameter Description】

| Parameter Name |             Description              |  Input/Output |
| :------------: | :----------------------------------: | :-----------: |
|    pipeId      | Corresponding to each input stream, ranging from 0~7 |    Input      |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|       0      |   Success   |
|    Non-zero  |   Failure   |

【Notes】Please translate the Chinese parts in the following content into English, while maintaining the original format and content:
> None

【Reference code】
> None

### HB_VIN_RegisterDisCallback
【Function declaration】
```c
int HB_VIN_RegisterDisCallback(uint32_t pipeId, VIN_DIS_CALLBACK_S *pstDISCallback)
```
【Function description】
> Register dis callback

【Parameter description】

| Parameter name |        Description        | Input/Output |
| :------------: | :-----------------------: | :----------: |
|    pipeId      | Corresponds to each input, range 0~7 |    Input     |
| pstDISCallback |         Callback interface         |    Input     |

【Return value】

| Return value |   Description   |
|:------------:|:---------------:|
|       0      |     Success     |
|     Non-0    |     Failure     |

【Note】
> None

【Reference code】
> None

### HB_VIN_SetDevVCNumber/HB_VIN_GetDevVCNumber
【Function declaration】
```c
int HB_VIN_SetDevVCNumber(uint32_t devId, uint32_t vcNumber);
int HB_VIN_GetDevVCNumber(uint32_t devId, uint32_t *vcNumber);
```
【Function description】
> Set and get the vc_index of the dev, which MIPI vc to use.

【Parameter description】

| Parameter name |        Description        |      Input/Output       |
| :------------: | :-----------------------: | :---------------------: |
|     devId      | Corresponds to each input, range 0~7 |         Input           |
|   vcNumber     | Corresponds to the vc of MIPI, range 0~3 | Input, output when getting |

【Return value】| Return Value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Notes】
> None

【Reference Code】
> None

### HB_VIN_AddDevVCNumber
【Function Declaration】
```c
int HB_VIN_AddDevVCNumber(uint32_t devId, uint32_t vcNumber)
```
【Function Description】
> Set the vc_index of dev, which vc to use for MIPI.

【Parameter Description】

| Parameter Name |          Description           | Input/Output |
| :------: | :---------------------: | :-------: |
|  devId   | Corresponds to each route input vc, range 0~7 |   Input    |
| vcNumber |  Corresponds to the vc of MIPI, range 0~3   |   Input    |

【Return Value】

| Return Value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Notes】
> When using linear mode, this interface is not used. When using DOL2 mode, set vcNumber to 1 for this interface. When using DOL3 mode, call HB_VIN_AddDevVCNumber twice, pass 0 and 1 respectively for vcNumber.

【Reference Code】
> DOL2 for one route
> Initialization Order:
> 1) Bind dev0 to mipi0
> HB_VIN_SetMipiBindDev(0, 0)
> 2) Bind virtual channel 0 of mipi0 to dev0
> HB_VIN_SetDevVCNumber(0, 0)
> 3) Bind virtual channel 1 of mipi0 to dev0
> HB_VIN_AddDevVCNumber(0, 1);
> 4) Bind dev0 to ISP pipe0 respectively
> HB_VIN_SetDevBindPipe(0, 0)
```c
    ret = HB_SYS_SetVINVPSMode(pipeId, vin_vps_mode);
```if (ret < 0) {
        printf("HB_SYS_SetVINVPSMode%d error!\n", vin_vps_mode);
        return ret;
    }
    ret = HB_VIN_CreatePipe(pipeId, pipeinfo);   // isp init
    if (ret < 0) {
        printf("HB_MIPI_InitSensor error!\n");
        return ret;
    }
    ret = HB_VIN_SetMipiBindDev(pipeId, mipiIdx);
    if (ret < 0) {
        printf("HB_VIN_SetMipiBindDev error!\n");
        return ret;
    }
    ret = HB_VIN_SetDevVCNumber(pipeId, deseri_port);
    if (ret < 0) {
        printf("HB_VIN_SetDevVCNumber error!\n");
        return ret;
    }
    ret = HB_VIN_AddDevVCNumber(pipeId, vc_num);
    if (ret < 0) {
        printf("HB_VIN_AddDevVCNumber error!\n");
        return ret;
    }
    ret = HB_VIN_SetDevAttr(pipeId, devinfo);
    if (ret < 0) {
        printf("HB_MIPI_InitSensor error!\n");
        return ret;
    }
    ret = HB_VIN_SetPipeAttr(pipeId, pipeinfo);
    if (ret < 0) {
        printf("HB_VIN_SetPipeAttr error!\n");
        goto pipe_err;
    }
    ret = HB_VIN_SetChnDISAttr(pipeId, 1, disinfo);
    if (ret < 0) {
        printf("HB_VIN_SetChnDISAttr error!\n");
        goto pipe_err;
    }
    ret = HB_VIN_SetChnLDCAttr(pipeId, 1, ldcinfo);
    if (ret < 0) {
        printf("HB_VIN_SetChnLDCAttr error!\n");
        goto pipe_err;
    }
    ret = HB_VIN_SetChnAttr(pipeId, 1);
    if (ret < 0) {
        printf("HB_VIN_SetChnAttr error!\n");
        goto chn_err;
    }
    HB_VIN_SetDevBindPipe(pipeId, pipeId);### HB_VIN_SetDevMclk

【Function Declaration】
```c
int HB_VIN_SetDevMclk(uint32_t devId, uint32_t devMclk, uint32_t vpuMclk);
```

【Function Description】
> Set the sif mclk and vpu clk.

【Parameter Description】

| Parameter Name |      Description      | Input/Output |
| :------------: | :-------------------: | :----------: |
|     devId      | Each input corresponds to a device, range 0~7 |    Input     |
|    devMclk     |   Sif mclk settings, refer to SIF MCLK   |  Input, unit: KHz  |
|    vpuMclk     |   Vpu clk settings, refer to VPU CLK   |  Input, unit: KHz  |

【Return Value】

| Return Value | Description |
|:------------:|:-----------:|
|       0      |   Success   |
|     Non-zero    |   Failure   |

【Notes】
> None

【Reference Code】
> None

### HB_VIN_GetChnFd

【Function Declaration】
```c
int HB_VIN_GetChnFd(uint32_t pipeId, uint32_t chnId)
```

【Function Description】
> Get the fd of the channel.

【Parameter Description】

| Parameter Name |      Description       | Input/Output |
| :------------: | :--------------------: | :----------: |
|     pipeId     | Each input corresponds to a pipeline, range 0~7 |    Input     |
|     chnId      |        Channel number, 0       |    Input     |

【Return Value】

| Return Value | Description |
| :----------: | :---------: |
| 参数名称 |            描述            | 输入/输出 |
| :------: | :------------------------: | :-------: |
|  devId   | Corresponding to each input, range 0~7 |   input   |

【返回值】

| 返回值 | 描述 |
|:------:|:----:|
|    0   | 成功 |
|   非0  | 失败 |

【注意事项】
> 无

【参考代码】
> 暂无【Return Value】

| Return Value | Description |
|:------:|:----:|
|    0   | Success |
|   Non-zero  | Failure |

【Notes】
> The call must be made after HB_VIN_SetDevAttrEx. The HB_VIN_SetDevAttrEx interface is used to set some attribute values of MD.

【Reference Code】
```c
    VIN_DEV_ATTR_EX_S devAttr;
    devAttr. path_sel = 0;
    devAttr. roi_top = 0;
    devAttr. roi_left = 0;
    devAttr. roi_width = 1280;
    devAttr. roi_height = 640;
    devAttr. grid_step = 128;
    devAttr. grid_tolerance =10;
    devAttr. threshold = 10;
    devAttr. weight_decay = 128;
    devAttr. precision = 0;
    ret = HB_VIN_SetDevAttrEx(pipeId, devexinfo);
    if(ret < 0) {
        printf("HB_VIN_SetDevAttrEx error!\n");
        return ret;
    }
    ret = HB_VIN_EnableDevMd(pipeId);
    if(ret < 0) {
        printf("HB_VIN_EnableDevMd error!\n");
        return ret;
    }
```
A thread is started below to call HB_VIN_MotionDetect to detect and disable MD function when receiving MD interrupt using HB_VIN_DisableDevMd.
```c
    int md_func(work_info_t * info)
    {
        int ret = 0;
        int pipeId = info->group_id;
        ret =  HB_VIN_MotionDetect(pipeId);
        if (ret < 0) {
            printf("HB_VIN_MotionDetect error!!! ret %d \n", ret);
        } else {
            HB_VIN_DisableDevMd(pipeId);
            printf("HB_VIN_DisableDevMd success!!! ret %d \n", ret);
        }
        return ret;
    }
```typedef enum HB_MIPI_SENSOR_MODE_E
{
    MIPI_SENSOR_MODE_RGB        = 0x0,              /* RGB */
    MIPI_SENSOR_MODE_YUV        = 0x1,              /* YUV */
    MIPI_SENSOR_MODE_BUTT
} MIPI_SENSOR_MODE_E;
```
【功能描述】
> sensor输出模式

【成员说明】
- RGB输出
- YUV输出```typedef enum HB_MIPI_SENSOR_MODE_E
{
    NORMAL_M             = 0x0,
    DOL2_M               = 0x1,
    DOL3_M               = 0x2,
    PWL_M                = 0x3,
} MIPI_SENSOR_MODE_E;

【Function Description】
> Sensor working modes

【Member Description】
> Linear mode, DOL2 mode, DOL3 mode, PWL mode

### MIPI_DESERIAL_INFO_T
【Structure Definition】
```c
typedef struct HB_MIPI_DESERIAL_INFO_T {
    int bus_type;
    int bus_num;
    int deserial_addr;
    int physical_entry;
    char *deserial_name;
} MIPI_DESERIAL_INFO_T;
```
【Function Description】
> Defines the attributes for serdes initialization

【Member Description】

|      Member      | Meaning                                       |
| :--------------: | :-------------------------------------------- |
|    bus_type      | Bus type, 0 for i2c, 1 for spi                 |
|    bus_num       | Bus number, determined by the specific hardware diagram, currently using 5 |
| deserial_addr    | Serdes address                                |
| physical_entry   | Reserved                                      |
| deserial_name    | Serdes name                                   |

### MIPI_SNS_INFO_S
【Structure Definition】
```c
typedef struct HB_MIPI_SNS_INFO_S {
    int port;
    int dev_port;
    int bus_type;
    int bus_num;
    int fps;
    int resolution;
    int sensor_addr;
    int serial_addr;
``````c
typedef struct HB_MIPI_SENSOR_INFO_S {
    int    deseEnable;
    MIPI_INPUT_MODE_E  inputMode;
    MIPI_DESERIAL_INFO_T deserialInfo;
    MIPI_SNS_INFO_S  sensorInfo;
} MIPI_SENSOR_INFO_S;

typedef struct MIPI_SNS_INFO_S {
    int entry_index;
    MIPI_SENSOR_MODE_E sensor_mode;
    int reg_width;
    char *sensor_name;
    int extra_mode;
    int deserial_index;
    int deserial_port;
    int gpio_num;
    int gpio_pin[GPIO_NUM];
    int gpio_level[GPIO_NUM];
    MIPI_SPI_DATA_S spi_info;
} MIPI_SNS_INFO_S;
```

【Function Description】
> Defines the attribute information for initializing the sensor.

【Member Description】

|   Member   | Meaning                                               |
| :--------: | :---------------------------------------------------- |
|   port     | Logical index of the current sensor, starting from 0. |
| dev_port   | Driver node for operating each sensor.                |
| bus_type   | Bus type, with 0 for i2c and 1 for spi.               |
|  bus_num   | Bus number, determined according to the hardware schematics of the board, defaulting to i2c5. |
|    fps     | Frame rate.                                           |
| resolution | Resolution of the sensor.                             |
| sensor_addr | Sensor address.                                       |
| serial_addr | Serdes address inside the sensor.                      |
| entry_index | Mipi index used by the sensor.                         |
| sensor_mode | Working mode of the sensor, with 1 for normal, 2 for dol2, and 3 for dol3. |
| reg_width   | Address width of the register.                         |
| sensor_name | Name of the sensor.                                   |
| extra_mode   | Distinguishing characteristics of the sensor, to be implemented in the specific sensor driver. |
| deserial_index | The serdes to which the sensor belongs.                |
| deserial_port  | The port of the serdes to which the sensor belongs.     |
| gpio_num   | GPIO pins used by some sensors for power on/off.       |
| gpio_pin   | GPIO pins being operated. GPIO_NUM is the number of GPIO pins used. |
| gpio_level  | Initial effective value. For example, if the pin needs to be pulled down first and then pulled up, this value should be 0; if pulled up first and then pulled down, this value should be 1. |
| spi_info    | Sensor spi information. Some sensors are accessed via the spi bus. |

### MIPI_SENSOR_INFO_S
【Structure Definition】
```c
typedef struct HB_MIPI_SENSOR_INFO_S {
    int    deseEnable;
    MIPI_INPUT_MODE_E  inputMode;
    MIPI_DESERIAL_INFO_T deserialInfo;
    MIPI_SNS_INFO_S  sensorInfo;
} MIPI_SENSOR_INFO_S;
```【Function Description】
> Defines the property information for initializing dev.

【Member Description】

|    Member    | Meaning             |
| :----------: | :------------------- |
|  deseEnable  | Whether the sensor has serdes |
|  inputMode   | The way the sensor is connected |
| deserialInfo | Information about the serdes |
|  sensorInfo  | Information about the sensor |

### MIPI_HOST_CFG_S
【Structure Definition】
```c
typedef struct HB_MIPI_HOST_CFG_S {
    uint16_t  lane;
    uint16_t  datatype;
    uint16_t  mclk;
    uint16_t  mipiclk;
    uint16_t  fps;
    uint16_t  width;
    uint16_t  height;
    uint16_t  linelenth;
    uint16_t  framelenth;
    uint16_t  settle;
    uint16_t  channel_num;
    uint16_t  channel_sel[4];
} MIPI_HOST_CFG_S;
```
【Function Description】
> Defines the initialization parameters for mipi.

【Member Description】

|     Member     | Meaning                                |
| :------------: | :-------------------------------------- |
|      lane      | Number of lanes, 0 ~ 4                  |
|    datatype    | Data format, see DATA TYPE               |
|      mclk      | Mipi module main clock, currently fixed at 24MHZ |
|    mipiclk     | Total mipi bit rate output by the sensor, in Mbits per second |
|      fps       | Actual frame rate output by the sensor  |
|     width      | Actual width output by the sensor       |
|     height     | Actual height output by the sensor      |
|   linelenth    | Total line length output by the sensor including blanking |
|   framelenth   | Total number of lines output by the sensor including blanking |
|     settle     | Actual Ttx-zero + Ttx-prepare time output by the sensor (in clock units) |
|  channel_num   | Number of virtual channels used         |
| channel_sel[4] | Stores the value of each virtual channel |### MIPI_ATTR_S
【Structure Definition】
```c
typedef struct HB_MIPI_ATTR_S {
    MIPI_HOST_CFG_S mipi_host_cfg;
    uint32_t  dev_enable;
} MIPI_ATTR_S;
```
【Function Description】
> Defines the parameters for initializing MIPI.

【Member Description】

|  Member   |        Meaning          |
| :-------: | :--------------------- |
| mipi_host_cfg | Structure of MIPI host attributes |
| dev_enable | Whether the MIPI dev is enabled, 1 for enable, 0 for disable |

### MIPI_SPI_DATA_S
【Structure Definition】
```c
typedef struct HB_MIPI_SPI_DATA_S {
    int spi_mode;
    int spi_cs;
    uint32_t spi_speed;
} MIPI_SPI_DATA_S;
```
【Function Description】
> Defines the spi information related to the sensor.

【Member Description】

|   Member   |        Meaning       |
| :--------: | :------------------ |
| spi_mode | SPI mode of operation |
| spi_cs | SPI chip select |
| spi_speed | SPI transmission speed |

### VIN_DEV_SIZE_S
【Structure Definition】
```c
typedef struct HB_VIN_DEV_SIZE_S {
    uint32_t  format;
    uint32_t  width;
    uint32_t  height;
    uint32_t  pix_length;
} VIN_DEV_SIZE_S;
```
【Function Description】
> Defines the properties for initializing the dev.【Member Description】

| Member | Meaning |
| :----: | :----- |
| format | Pixel format. format=0 represents raw8~raw16, depending on the pixel_lenght to determine whether it is raw8 or raw16. |
|  width | Data width. |
| height | Data height. |
| pix_length | Length of each pixel point. |

### VIN_MIPI_ATTR_S
【Structure Definition】
```c
typedef struct HB_VIN_MIPI_ATTR_S {
    uint32_t  enable;
    uint32_t  ipi_channels;
    uint32_t  ipi_mode;
    uint32_t  enable_mux_out;
    uint32_t  enable_frame_id;
    uint32_t  enable_bypass;
    uint32_t  enable_line_shift;
    uint32_t  enable_id_decoder;
    uint32_t  set_init_frame_id;
    uint32_t  set_line_shift_count;
    uint32_t  set_bypass_channels;
    uint32_t  enable_pattern;
} VIN_MIPI_ATTR_S;
```
【Function Description】
> Define the initialization information for dev mipi.

【Member Description】

|       Member       | Meaning |
| :----------------: | :------ |
|      enable        | Enable mipi, 0 means disable, 1 means enable. |
|   ipi_channels     | ipi_channels represents how many channels are used, starting from 0. If set to 2, it means channels 0 and 1 are used. |
|     ipi_mode       | When DOL2 is divided into two linear modes or DOL3 is divided into one DOL2 mode and one linear mode, or divided into three linear modes, this value is assigned as 2 or 3. |
|   enable_mux_out   | Enable mux selection output. |
|  enable_frame_id   | Whether to enable frameid. |
|   enable_bypass    | Whether to enable bypass. |
| enable_line_shift  | Unused. |
| enable_id_decoder  | Unused. |
| set_init_frame_id  | Initial frame id value, usually 1. |
| set_line_shift_count | Unused. |
| set_bypass_channels  | Unused. |
|  enable_pattern    | Whether to enable test pattern. |

### VIN_DEV_INPUT_DDR_ATTR_S
【Structure Definition】```c
typedef struct HB_VIN_DEV_INPUT_DDR_ATTR_S {
    uint32_t stride;
    uint32_t buf_num;
    uint32_t raw_feedback_en;
    VIN_DEV_SIZE_S data;
} VIN_DEV_INPUT_DDR_ATTR_S;
```
【Function Description】
> Defines the input information of the dev for offline and raw feedback scenarios.

【Member Description】

| Member          | Description                                                                                              |
| :-------------: | :------------------------------------------------------------------------------------------------------- |
| stride          | Hardware stride that matches the format. For example, if it is 12-bit, stride = width x 1.5. If it is 10-bit, stride = width x 1.25, and so on.    |
| buf_num         | Number of buffers to store raw feedback data.                                                           |
| raw_feedback_en | Enables raw feedback mode. Cannot be enabled at the same time as offline mode, and is used independently. |
| data            | Data format, see VIN_DEV_SIZE_S.                                                                         |

### VIN_DEV_OUTPUT_DDR_S
【Structure Definition】
```c
typedef struct HB_VIN_DEV_OUTPUT_DDR_S {
    uint32_t stride;
    uint32_t buffer_num;
    uint32_t frameDepth
} VIN_DEV_OUTPUT_DDR_S;
```
【Function Description】
> Defines the initialization information for dev output to DDR.

【Member Description】

| Member      | Description                                                               |
| :---------: | :------------------------------------------------------------------------ |
| stride      | Hardware stride that matches the format. Currently, it is 12-bit 1952x1.5. |
| buffer_num  | Number of buffers for dev output to DDR.                                   |
| frameDepth  | Maximum number of frames that can be get. buffer_num is the total number of buffers, and it is recommended that the maximum value of frameDepth is ddrOutBufNum - 4. |

### VIN_DEV_OUTPUT_ISP_S
【Structure Definition】
```c
typedef struct HB_VIN_DEV_OUTPUT_ISP_S {
    uint32_t dol_exp_num;
    uint32_t enable_dgain;
    uint32_t set_dgain_short;
    uint32_t set_dgain_medium;
    uint32_t set_dgain_long;
    uint32_t short_maxexp_lines;
```
【Function Description】
> Defines the output information of the dev for ISP.

【Member Description】

| Member               | Description                                                       |
| :------------------: | :---------------------------------------------------------------- |
| dol_exp_num          | DOL exposure number.                                              |
| enable_dgain         | Enable digital gain.                                              |
| set_dgain_short      | Short exposure digital gain setting.                               |
| set_dgain_medium     | Medium exposure digital gain setting.                              |
| set_dgain_long       | Long exposure digital gain setting.                                |
| short_maxexp_lines   | Maximum exposure lines for short exposure.                         |typedef struct HB_VIN_DEV_ATTR_S {
    VIN_DEV_SIZE_S        stSize;
    union
    {
        VIN_MIPI_ATTR_S  mipiAttr;
        VIN_DVP_ATTR_S   dvpAttr;
    };
    VIN_DEV_INPUT_DDR_ATTR_S DdrIspAttr;
    VIN_DEV_OUTPUT_DDR_S outDdrAttr;
    VIN_DEV_OUTPUT_ISP_S outIspAttr;
} VIN_DEV_ATTR_S;


【Description】
> Defines the initialization attributes for dev.


【Members】
|        Member         | Description                                                                                          |
| :-------------------: | :--------------------------------------------------------------------------------------------------- |
|   VIN_DEV_SIZE_S      | stSize input data                                                                                    |
| VIN_DEV_INTF_MODE_E | enIntfMode the input interface mode for sif(dev), either mipi or dvp, currently both are mipi   |
|     DdrIspAttr      | Input attribute configuration of isp(pipe), for offline or re-injection                            |
|     outDdrAttr      | Configuration of sif(dev) output to ddr                                                             |
|     outIspAttr      | Initialization information for dev output to pipe                                                 || outIspAttr | Some attribute settings from sif to isp |
| --- | --- |

### VIN_DEV_ATTR_EX_S
【Structure Definition】
```c
typedef struct HB_VIN_DEV_ATTR_EX_S {
    uint32_t path_sel;
    uint32_t roi_top;
    uint32_t roi_left;
    uint32_t roi_width;
    uint32_t roi_height;
    uint32_t grid_step;
    uint32_t grid_tolerance;
    uint32_t threshold;
    uint32_t weight_decay;
    uint32_t precision;
} VIN_DEV_ATTR_EX_S;
```
【Function Description】
> Define md related information

【Member Description】

| Member | Meaning |
| --- | --- |
| path_sel | 0: sif-isp path; 1: sif-ipu path |
| roi_top | Y coordinate of the ROI |
| roi_left | X coordinate of the ROI |
| roi_width | Length of the ROI, must be an integral multiple of step |
| roi_height | Width of the ROI, must be an integral multiple of step |
| grid_step | Width and height of each block in the motion detect area. It must be a power of 2, and the valid range is 4~128. |
| grid_tolerance | Threshold for comparing the difference between two frames of each block. When the difference exceeds this threshold, it is considered as different. |
| threshold | When the number of blocks in the ROI region selected for motion detection exceeds this threshold, a mot_det interrupt is issued. |
| weight_decay | When updating the ref buffer with a new frame, it is not a complete replacement of the previous frame data, but a weighted average of the current frame and the previous frame. Mot_det_wgt_decay is the weight of the current frame, and the weight of the previous frame is (256-mot_det_wgt_decay). |
| precision | The number of decimal places to retain in the calculation of each block. The valid range is 1~4. |

### VIN_PIPE_SENSOR_MODE_E
【Structure Definition】
```c
typedef enum HB_VIN_PIPE_SENSOR_MODE_E {
    SENSOR_NORMAL_MODE = 1,
    SENSOR_DOL2_MODE,
    SENSOR_DOL3_MODE,
    SENSOR_DOL4_MODE,
    SENSOR_PWL_MODE,
    SENSOR_INVALID_MODE
} VIN_PIPE_SENSOR_MODE_E;
```
【Function Description】
> Sensor working mode> 定义pipe calib 数据信息

【成员说明】

|  成员  | 含义       |
| :----: | :--------- |
|  mode  | 模式       |
| lname  | 标志位名称 |> Loading sensor calibration data

[Member Description]

| Member | Meaning                            |
| :----: | :--------------------------------- |
|  mode  | Whether to enable sensor calibration data loading |
| lname  | Corresponding calibration library used           |

### VIN_PIPE_ATTR_S
[Structure Definition]
```c
typedef struct HB_VIN_PIPE_ATTR_S {
    uint32_t  ddrOutBufNum;
    uint32_t  frameDepth;
    VIN_PIPE_SENSOR_MODE_E snsMode;
    VIN_PIPE_SIZE_S stSize;
    VIN_PIPE_CFA_PATTERN_E cfaPattern;
    uint32_t   temperMode;
    uint32_t   ispBypassEn;
    uint32_t   ispAlgoState;
    uint32_t   ispAfEn;s
    uint32_t   bitwidth;
    uint32_t   startX;
    uint32_t   startY;
    VIN_PIPE_CALIB_S calib;
} VIN_PIPE_ATTR_S;
```
[Function Description]
> Defines the attributes of the pipe.

[Member Description]

|   Member  |  Meaning                                      |
| :-------: | :-------------------------------------------- |
| ddrOutBufNum | Width of the data, can be 8, 10, 12, 14, 16  |
| frameDepth  | Maximum number of frames to get. The value of frameDepth should be at most ddrOutBufNum - 3.  |
|  snsMode   | Sensor working mode                           |
|   stSize   | Sensor data information, see 17               |
| cfaPattern | Data format layout, consistent with the sensor |
| temperMode | Temper mode, 0 means disabled, 2 means enabled |
| BypassEnable | Whether to enable ISP bypass                        |
| ispAlgoState | Whether to start 3a algorithm library, 1 means enabled, 0 means disabled |
|  bitwidth  | Bit width, valid values are 8, 10, 12, 14, 16, 20 |
|   startX   | X offset relative to the origin                 |
|   startY   | Y offset relative to the origin                 |
|   calib    | Whether to enable sensor calibration data loading, 1 means enabled, 0 means disabled |

### VIN_LDC_PATH_SEL_S
[Structure Definition]```c
typedef struct HB_VIN_LDC_PATH_SEL_S {
    uint32_t rg_y_only:1;
    uint32_t rg_uv_mode:1;
    uint32_t rg_uv_interpo:1;
    uint32_t reserved1:5;
    uint32_t rg_h_blank_cyc:8;
    uint32_t reserved0:16;
} VIN_LDC_PATH_SEL_S;
```
【Function Description】
> Defines the LDC attribute information

【Member Description】

|   Member    | Meaning   |
| :---------: | :-------- |
|  rg_y_only  | Output type |
| rg_uv_mode  | Output type |
|rg_uv_interpo| For turning |
|rg_h_blank_cyc| For turning |

### VIN_LDC_PICSIZE_S
【Structure Definition】
```c
typedef struct HB_VIN_LDC_PICSIZE_S {
    uint16_t pic_w;
    uint16_t pic_h;
} VIN_LDC_PICSIZE_S;
```
【Function Description】
> Defines the LDC width and height input information

【Member Description】

|  Member | Meaning |
| :-----: | :------ |
|  pic_w  | Set the size to -1 if the output size is 1920. For example, set it to 1919 if the ISP output is 1920. |
|  pic_h  | Do not change any settings other than size, ldc, and dis parts. |

### VIN_LDC_ALGOPARAM_S
【Structure Definition】
```c
typedef struct HB_VIN_LDC_ALGOPARAM_S {
    uint16_t rg_algo_param_b;
    uint16_t rg_algo_param_a;
} VIN_LDC_ALGOPARAM_S;
```
【Function Description】
> Defines the LDC attribute information【Member Description】

|      Member       | Meaning           |
| :-------------: | :------------- |
| rg_algo_param_b | Parameter needs tuning |
| rg_algo_param_a | Parameter needs tuning |

### VIN_LDC_OFF_SHIFT_S
【Structure Definition】
```c
typedef struct HB_VIN_LDC_OFF_SHIFT_S {
    uint32_t rg_center_xoff:8;
    uint32_t rg_center_yoff:8;
    uint32_t reserved0:16;
} VIN_LDC_OFF_SHIFT_S;
```
【Function Description】
> Defines LDC attribute information

【Member Description】

|      Member      | Meaning         |
| :------------: | :----------- |
| rg_center_xoff | Processing area adjustment |
| rg_center_yoff | Processing area adjustment |

### VIN_LDC_WOI_S
【Structure Definition】
```c
typedef struct HB_VIN_LDC_WOI_S {
    uint32_t rg_start:12;
    uint32_t reserved1:4;
    uint32_t rg_length:12;
    uint32_t reserved0:4;
}VIN_LDC_WOI_S;
```
【Function Description】
> Defines LDC attribute information

【Member Description】

|   Member    | Meaning         |
| :-------: | :----------- |
| rg_start  | Processing area adjustment |
| rg_length | Processing area adjustment |

### VIN_LDC_ATTR_S
【Structure Definition】
```ctypedef struct HB_VIN_LDC_ATTR_S {
    uint32_t         ldcEnable;
    VIN_LDC_PATH_SEL_S  ldcPath;
    uint32_t yStartAddr;
    uint32_t cStartAddr;
    VIN_LDC_PICSIZE_S  picSize;
    uint32_t lineBuf;
    VIN_LDC_ALGOPARAM_S xParam;
    VIN_LDC_ALGOPARAM_S yParam;
    VIN_LDC_OFF_SHIFT_S offShift;
    VIN_LDC_WOI_S   xWoi;
    VIN_LDC_WOI_S   yWoi;
} VIN_LDC_ATTR_S;

【Function Description】
> Define LDC attribute information

【Member Description】

| Member     | Description    |
| :--------: | :------------- |
| ldcEnable  | Whether LDC is enabled |
|  ldcPath   | Output type    |
| yStartAddr | Iram address used |
| cStartAddr | Iram address used |
|  picSize   | Input size     |
|  lineBuf   | Set to 99      |
|   xParam   | Parameters need tuning |
|   yParam   | Parameters need tuning |
|  offShift  | Processing region correction |
|    xWoi    | Processing region correction |
|    yWoi    | Processing region correction |

### VIN_DIS_PICSIZE_S
【Structure Definition】
```c
typedef struct HB_VIN_DIS_PICSIZE_S {
    uint16_t pic_w;
    uint16_t pic_h;
} VIN_DIS_PICSIZE_S;
```
【Function Description】
> Define DIS attribute information

【Member Description】

| Member | Description |
| :---: | :--- |
| pic_w | Size that needs to be set to -1 smaller than the input size, if the ISP outputs 1920, then set 1919 here |
| pic_h | Size that needs to be set to -1 smaller than the input size |### VIN_DIS_PATH_SEL_S
【Structure Definition】
```c
typedef struct HB_VIN_DIS_PATH_SEL_S {
    uint32_t rg_dis_enable:1;
    uint32_t rg_dis_path_sel:1;
    uint32_t reserved0:30;
} VIN_DIS_PATH_SEL_S;
```
【Function Description】
> Defines DIS attribute information

【Member Description】

|    Member    | Meaning  |
| :----------: | :------- |
| rg_dis_enable | Output type |
| rg_dis_path_sel | Output type |

### VIN_DIS_CROP_S
【Structure Definition】
```c
typedef struct HB_VIN_DIS_CROP_S {
    uint16_t rg_dis_start;
    uint16_t rg_dis_end;
} VIN_DIS_CROP_S;
```
【Function Description】
> Defines DIS attribute information

【Member Description】

|    Member    | Meaning  |
| :----------: | :------- |
| rg_dis_start | Processing area correction |
| rg_dis_end | Processing area correction |

### VIN_DIS_CALLBACK_S
【Structure Definition】
```c
typedef struct HB_VIN_DIS_CALLBACK_S {
    void (*VIN_DIS_DATA_CB) (uint32_t pipeId, uint32_t event,
    VIN_DIS_MV_INFO_S *disData, void *userData);
} VIN_DIS_CALLBACK_S;
```
【Function Description】
> Defines the callback interface for DIS

【Member Description】|    Member    |     Meaning           |
| :-----------:| :----------------------|
| VIN_DIS_DATA_CB | Callback function, returns data to the user after receiving it |

### VIN_DIS_MV_INFO_S
【Structure definition】
```c
typedef struct HB_VIN_DIS_MV_INFO_S {
    int  gmvX;
    int  gmvY;
    int  xUpdate;
    int  yUpdate;
} VIN_DIS_MV_INFO_S;
```

【Functional description】
> Defines the information of coordinate movement

【Member description】

|    Member    |     Meaning                                                                                                     |
| :-----------:| :---------------------------------------------------------------------------------------------------------------|
|    gmvX      | Absolute coordinates, the amount of movement in the x-axis relative to the camera center. If the camera is firmly fixed, gmv is the movement relative to the fixed position.       |
|    gmvY      | Absolute coordinates, the amount of movement in the y-axis relative to the camera center.                      |
|    xUpdate   | Relative quantity, the amount of movement in the x-axis relative to the previous frame. Update only considers the movement of the camera shake in the previous frame, regardless of where it is locked. (If the previous frame is in a fixed position, update is the same as gmv, but this only happens in the first frame of continuous shaking). |
|    yUpdate   | Relative quantity, the amount of movement in the y-axis relative to the previous frame.                         |

### VIN_DIS_ATTR_S
【Structure definition】
```c
typedef struct HB_VIN_DIS_ATTR_S {
    VIN_DIS_PICSIZE_S picSize;
    VIN_DIS_PATH_SEL_S disPath;
    uint32_t disHratio;
    uint32_t disVratio;
    VIN_DIS_CROP_S xCrop;
    VIN_DIS_CROP_S yCrop;
} VIN_DIS_ATTR_S;
```
【Functional description】
> Defines the DIS property information

【Member description】

|    Member    |     Meaning           |
| :-----------:| :----------------------|
|   picSize    | Input data width and height |
|   disPath    | Output type |
|  disHratio   | Set to 65536 || disVrati  | Set to 65536  |
|   xCrop   | Processing area correction |
|   yCrop   | Processing area correction |

### VIN_LENS_FUNC_TYPE_E
【Structure Definition】
```c
typedef enum HB_VIN_LENS_FUNC_TYPE_E {
    VIN_LENS_AF_TYPE = 1,
    VIN_LENS_ZOOM_TYPE,
    VIN_LENS_INVALID,
} VIN_LENS_FUNC_TYPE_E;
```
【Function Description】
> Motor function

【Member Description】
- AF: Auto focus, change focus distance
- ZOOM: Zoom, change focal length

### VIN_LENS_CTRL_ATTR_S
【Structure Definition】
```c
typedef struct HB_VIN_LENS_CTRL_ATTR_S {
    uint16_t port;
    VIN_LENS_MOTOR_TYPE_E motorType;
    uint32_t maxStep;
    uint32_t initPos;
    uint32_t minPos;
    uint32_t maxPos;
    union {
        struct {
            uint16_t pwmNum;
            uint32_t pwmDuty;
            uint32_t pwmPeriod;
        } pwmParam;
        struct {
            uint16_t pulseForwardNum;
            uint16_t pulseBackNum;
            uint32_t pulseDuty;
            uint32_t pulsePeriod;
        } pulseParam;
        struct {
            uint16_t i2cNum;
            uint32_t i2cAddr;
        } i2cParam;
        struct {
            uint16_t gpioA1;
            uint16_t gpioA2;
            uint16_t gpioB1;```c
typedef struct HB_VIN_LENS_CTRL_ATTR_S {
    uint8_t port;
    VIN_LENS_MOTOR_TYPE_E motorType;
    uint32_t maxStep;
    uint32_t initPos;
    uint32_t minPos;
    uint32_t maxPos;
    uint8_t pwmNum;
    uint32_t pwmDuty;
    uint32_t pwmPeriod;
    uint8_t pulseForwardNum;
    uint8_t pulseBackNum;
    uint32_t pulseDuty;
    uint32_t pulsePeriod;
    uint8_t i2cNum;
    uint8_t i2cAddr;
    uint16_t gpioA1;
    uint16_t gpioA2;
    uint16_t gpioB1;
    uint16_t gpioB2;
} VIN_LENS_CTRL_ATTR_S;

typedef enum HB_VIN_LENS_MOTOR_TYPE_E {
    VIN_LENS_PWM_TYPE = 0,
    VIN_LENS_PULSE_TYPE,
    VIN_LENS_I2C_TYPE,
    VIN_LENSSPI_TYPE,
    VIN_LENS_GPIO_TYPE
} VIN_LENS_MOTOR_TYPE_E;
```

【Function Description】
> Define the pipe attribute information

【Member Description】

|   Member  |              Meaning             |
|:---------:|:-------------------------------:|
|    port   | Corresponding to each input and pipeId |
| motorType | Motor driver type, see VIN_LENS_MOTOR_TYPE_E for details |
|  maxStep  | Maximum steps of the motor |
|  initPos  | Initial position of the motor |
|  minPos   | Minimum position of the motor |
|  maxPos   | Maximum position of the motor |
|  pwmNum   | Motor control pwm device number |
| pwmDuty   | Motor control pwm duty cycle |
| pwmPeriod | Motor control pwm frequency |
|pulseForwardNum| Motor control forward control pulse device number |
| pulseBackNum  | Motor control backward control pulse device number |
|  pulseDuty   | Motor control pulse duty cycle |
| pulsePeriod  | Motor control pulse frequency |
|  i2cNum  | Motor control I2C device number |
| i2cAddr  | Motor control I2C address |
|  gpioA1  | Motor control a+ gpio number |
|  gpioA2  | Motor control a- gpio number |
|  gpioB1  | Motor control b+ gpio number |
|  gpioB2  | Motor control b- gpio number |

### VIN_LENS_MOTOR_TYPE_E
【Structure Definition】
```c
typedef enum HB_VIN_LENS_MOTOR_TYPE_E {
    VIN_LENS_PWM_TYPE = 0,
    VIN_LENS_PULSE_TYPE,
    VIN_LENS_I2C_TYPE,
    VIN_LENSSPI_TYPE,
    VIN_LENS_GPIO_TYPE
} VIN_LENS_MOTOR_TYPE_E;
```
【Function Description】
> Motor driver types, including the above types.

【Member Description】
- PWM drive, pulse number drive, I2C communication control, SPI communication control, GPI pin timing control.
Due to hardware environment factors, only GPIO mode has been tested and verified.### DATA TYPE

| Data | Type Description                               |
| :--: | :--------------------------------------------- |
| 0x28 | RAW6                                           |
| 0x29 | RAW7                                           |
| 0x2A | RAW8                                           |
| 0x2B | RAW10                                          |
| 0x2C | RAW12                                          |
| 0x2D | RAW14                                          |
| 0x2E | Reserved                                       |
| 0x18 | YUV 420 8-bit                                  |
| 0x19 | YUV 420 10-bit                                 |
| 0x1A | Legacy YUV420 8-bit                            |
| 0x1B | Reserved                                       |
| 0x1C | YUV 420 8-bit(Chroma Shifted Pixel Sampling)   |
| 0x1D | YUV 420 10-bit(Chroma Shifted Pixel Sampling)) |
| 0x1E | YUV 422 8-bit                                  |
| 0x1F | YUV 422 10-bit                                 |

### SIF MCLK

| ISP Application       | SIF_MCLK(MHz) |
| :------------------- | :-----------: |
| 8M 30fps input       |     326.4     |
| 2M 30fps 2-channel TDM |    148.36     |
| 2M 30fps 1-channel input |    102.00     |
| 8M DOL2 30fps        |    544.00     |
| 2M 15fps 4-channel TDM |    148.36     |

### VPU CLK

| VPU Application | Encoding  | VPU_BCLK/VPU_CCLK(MHz) |
| :---------- | :---: | :--------------------: |
| 8M@30fps    |  AVC  |         326.4          |
|             | HEVC  |          408           |
| 2M*4@30fps  |  AVC  |          544           |
|             | HEVC  |          544           |
| 2M @30fps   |  AVC  |          204           |
|             | HEVC  |          204           |

## Error Codes

The VIN error codes are shown in the table below:

|   Error Code   | Macro Definition                           | Description                   |
| :--------: | :------------------------------- | :--------------------------- |
| -268565505 | HB_ERR_VIN_CREATE_PIPE_FAIL      | Failed to create PIPE         |
| -268565506 | HB_ERR_VIN_SIF_INIT_FAIL         | Failed to initialize DEV(Sif) |
| -268565507 | HB_ERR_VIN_DEV_START_FAIL        | Failed to start DEV(Sif)      || -268565508 | HB_ERR_VIN_PIPE_START_FAIL       | Failed to start ISP               |
| -268565509 | HB_ERR_VIN_CHN_UNEXIST           | Channel does not exist                    |
| -268565510 | HB_ERR_VIN_INVALID_PARAM         | Invalid interface parameter                 |
| -268565511 | HB_ERR_VIN_ISP_INIT_FAIL         | Failed to initialize ISP                |
| -268565512 | HB_ERR_VIN_ISP_FRAME_CORRUPTED   | Frame corrupted, ISP driver may have dropped it |
| -268565513 | HB_ERR_VIN_CHANNEL_INIT_FAIL     | Failed to initialize two chn channels in ISP   |
| -268565514 | HB_ERR_VIN_DWE_INIT_FAIL         | Failed to initialize DWE                |
| -268565515 | HB_ERR_VIN_SET_DEV_ATTREX_FAIL   | Failed to initialize SIF extended attributes        |
| -268565516 | HB_ERR_VIN_LENS_INIT_FAIL        | Failed to initialize lens               |
| -268565517 | HB_ERR_VIN_SEND_PIPERAW_FAIL     | Failed to send SIF raw data back      |
| -268565518 | HB_ERR_VIN_NULL_POINT            | VIN module has a null pointer              |
| -268565519 | HB_ERR_VIN_GET_CHNFRAME_FAIL     | Failed to obtain data from ISP        |
| -268565520 | HB_ERR_VIN_GET_DEVFRAME_FAIL     | Failed to obtain data from SIF        |
| -268565521 | HB_ERR_VIN_MD_ENABLE_FAIL        | Failed to enable MotionDetect         |
| -268565522 | HB_ERR_VIN_MD_DISABLE_FAIL       | Failed to disable MotionDetect         |
| -268565523 | HB_ERR_VIN_SWITCH_SNS_TABLE_FAIL | Failed to switch SNS table between linear and DOL ISP modes    |

## Reference code
For VIN module sample code examples, please refer to [get_sif_data](./multimedia_samples#get_sif_data) and [get_isp_data](./multimedia_samples#get_isp_data).