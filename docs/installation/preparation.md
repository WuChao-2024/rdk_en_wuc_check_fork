---
sidebar_position: 1
---
# 1.1 Preparation

```mdx-code-block
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
```

Before using the RDK X3 development board, the following preparations need to be made.

## Development Preparation

### **Power Supply**

<Tabs groupId="rdk-type">
<TabItem value="x3" label="RDK X3">

The RDK X3 development board is powered by a USB Type C interface. It requires a power adapter that supports **5V/3A** to power the board. It is recommended to use the recommended power adapter model in the [Basic Accessories List](/hardware_development/rdk_x3/accessory#basic_accessories) section.

</TabItem>

<TabItem value="x3md" label="RDK X3 Module">

The RDK X3 Module is powered through the power interface on the carrier board. The [official carrier board](http://localhost:3000/documents_rdk/hardware_development/rdk_x3_module/interface) is powered through a DC interface. It is recommended to use the **12V/2A** adapter recommended in the certified accessories list.

</TabItem>

</Tabs>

:::caution

Please do not power the development board through the USB interface of a computer, as it may cause abnormal power failure and repeated restarts due to insufficient power supply.

For more troubleshooting, please refer to the [Common Questions](../category/common_questions) section.

:::



### **Storage** 
<Tabs groupId="rdk-type">
<TabItem value="x3" label="RDK X3">The RDK X3 development board uses a Micro SD card as the system boot medium, and it is recommended to use a storage card with a capacity of at least 8GB to meet the storage requirements of the Ubuntu system and application software.

</TabItem>

<TabItem value="x3md" label="RDK X3 Module">

The RDK X3 Module has onboard eMMC (optional) and supports booting the system from both eMMC and SD cards.

</TabItem>

</Tabs>



### **Display** 
<Tabs groupId="rdk-type">
<TabItem value="x3" label="RDK X3">

The RDK X3 development board supports HDMI display interface, and connects the development board and monitor via HDMI cable to support graphical desktop display.

</TabItem>

<TabItem value="x3md" label="RDK X3 Module">

The RDK X3 Module supports HDMI display interface, and connects the official carrier board and monitor via HDMI cable to support graphical desktop display.

</TabItem>

</Tabs>



### **Network Connection**
<Tabs groupId="rdk-type">
<TabItem value="x3" label="RDK X3">

The RDK X3 development board supports Ethernet and Wi-Fi network interfaces, and users can use either interface for network connection.

</TabItem><TabItem value="x3md" label="RDK X3 Module">

The RDK X3 Module supports two types of network interfaces: Ethernet and Wi-Fi (optional). Users can achieve network connectivity through either interface.

</TabItem>

</Tabs>



## **Frequently Asked Questions**  

Here are some common issues when using the development board for the first time:

- **<font color='Blue'>Power on failure</font>**: Please ensure that the recommended power adapter is used for [power supply](#power_supply); please also ensure that the Micro SD card or eMMC of the development board has been flashed with the Ubuntu system image.
- **<font color='Blue'>No response from USB Host interface</font>**: Please make sure that no data cable is connected to the Micro USB interface of the development board.
- **<font color='Blue'>Hot-plugging storage card during usage</font>**: The development board does not support hot-plugging of Micro SD storage cards. If an accidental operation occurs, please restart the development board.



## **Important Notices**

- Do not plug and unplug any devices other than USB, HDMI, and Ethernet cables when they are powered on.
- The Type C USB interface of RDK X3 is only used for power supply.
- Use USB Type C power cables from reputable brands; otherwise, power supply abnormalities may occur, leading to system power failure.



:::tip

For more problem-solving, please refer to the [Frequently Asked Questions](../category/common_questions) section, and you can also visit the [Horizon Developer Forum](https://developer.horizon.cc/forum) for assistance.

:::