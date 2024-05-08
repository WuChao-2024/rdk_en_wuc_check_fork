---
sidebar_position: 1
---
# 2.1 Network Configuration

This section mainly introduces the methods for modifying the wired and wireless network configurations of the development board.

## Wired Network {#config_ethnet}

<iframe src="//player.bilibili.com/player.html?aid=700903305&bvid=BV1rm4y1E73q&cid=1196557461&page=11" scrolling="no" border="0" frameborder="no" framespacing="0" width="100%" height="500" allowfullscreen="true"> </iframe>

The default wired network configuration of the development board uses static IP configuration, and the initial IP address is `192.168.1.10`. Users can switch between static and DHCP modes by the following methods.

### Modifying Static IP Configuration
The development board's static network configuration is saved in the `/etc/network/interfaces` file. By modifying the `address`, `netmask`, `gateway`, and other fields, the static IP configuration can be modified. `metric` is the network priority configuration, setting it to `700` is to lower the priority of the wired network. When both wired and wireless networks are enabled, the wireless network will be prioritized. For example:

```shell
sudo vim /etc/network/interfaces
```

```shell
# interfaces(5) file used by ifup(8) and ifdown(8)
# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d
auto eth0
iface eth0 inet static
    address 192.168.1.10
    netmask 255.255.255.0
    gateway 192.168.1.1 
    metric 700
```

After the modification is completed, enter the command `sudo restart_network` on the command line to make the configuration take effect.

### Modifying DHCP Configuration
DHCP (Dynamic Host Configuration Protocol) is usually applied in local area network environments. Its main function is centralized management and allocation of IP addresses, allowing hosts in the network environment to dynamically obtain IP addresses, gateway addresses, DNS server addresses, and other information, thereby improving the utilization of addresses.

The development board's DHCP network configuration is saved in the `/etc/network/interfaces` file. By modifying the relevant configuration of eth0, the DHCP mode can be modified. For example:

```shell
sudo vim /etc/network/interfaces
```

```shell
source-directory /etc/network/interfaces.d
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet dhcp
metric 700
```

After modifying, enter the `sudo restart_network` command in the command line to make the configuration take effect.

### Modify MAC address configuration
If you need to modify the default MAC address of the development board, you can add `pre-up` configuration information in the `/etc/network/interfaces` file to specify the MAC address you need, for example:

```shell
sudo vim /etc/network/interfaces
```

```shell
# interfaces(5) file used by ifup(8) and ifdown(8)
# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d
auto eth0
iface eth0 inet static
    address 192.168.1.10
    netmask 255.255.255.0
    gateway 192.168.1.1 
    pre-up ifconfig eth0 hw ether 00:11:22:9f:51:27
```

After modifying, `reboot` to make the configuration take effect.

## Wireless Network

<iframe src="//player.bilibili.com/player.html?aid=700903305&bvid=BV1rm4y1E73q&cid=1196557610&page=12" scrolling="no" border="0" frameborder="no" framespacing="0" width="100%" height="500" allowfullscreen="true"> </iframe>

The development board integrates a 2.4GHz wireless WiFi module, which supports Soft AP and Station modes, and runs in Station mode by default. The following introduces how to use the two modes.

### Station Mode
In Station mode, the development board as a client and accesses the router's wireless hotspot for internet connection.

- For users of Ubuntu Desktop version, you can click on the Wi-Fi icon in the upper right corner of the desktop, select the corresponding hotspot, and enter the password to complete the network configuration, as shown in the figure below:

![image-wifi-config](./image/network/image-wifi-config.jpeg)

- For users of Ubuntu Server version, you can complete the wireless network configuration through the command line, following these steps:

1. Use the `sudo nmcli device wifi rescan` command to scan for hotspots. If you get the following message, it means scanning is too frequent and you need to try again later:

    ```shell
    root@ubuntu:~# sudo nmcli device wifi rescan
    Error: Scanning not allowed immediately following previous scan.
    ```
2. Use the `sudo nmcli device wifi list` command to list the scanned hotspots.
3. Use the `sudo wifi_connect "SSID" "PASSWD"` command to connect to the hotspot. If you get the following message, it means the network connection is successful:

    ```shell
    root@ubuntu:~# sudo wifi_connect "WiFi-Test" "12345678" 
    Device 'wlan0' successfully activated with 'd7468833-4195-45aa-aa33-3d43da86e1a7'.
    ```

:::tip
If you receive the following message after connecting to the hotspot, it means the hotspot is not found. You can execute the `sudo nmcli device wifi rescan` command to rescan and reconnect.
```shell
root@ubuntu:~# sudo wifi_connect "WiFi-Test" "12345678" 
Error: No network with SSID 'WiFi-Test' found.
```
:::

### Soft AP Mode

By default, the development board's wireless network runs in Station mode. To use the Soft AP mode, please follow the steps below for configuration.

1. Install `hostapd` and `isc-dhcp-server`

    ```shell
    sudo apt update
    sudo apt install hostapd
    sudo apt install isc-dhcp-server
    ```

2. Run the command `sudo vim /etc/hostapd.conf` to configure the `hostapd.conf` file, focusing on the following fields:

    ```shell
    interface=wlan0 # The network card used as an AP hotspot
    ssid=Sunrise # WiFi name
    wpa=2 # 0 for WPA, 2 for WPA2, usually 2
    wpa_key_mgmt=WPA-PSK # Encryption algorithm, usually WPA-PSK
    wpa_passphrase=12345678 # Password
    wpa_pairwise=CCMP # Encryption protocol, usually CCMP
    ```

    - For an open hotspot configuration, add the following content to the `hostapd.conf` file:

    ```shell
    interface=wlan0
    driver=nl80211
    ctrl_interface=/var/run/hostapd
    ssid=Sunrise
    channel=6
    ieee80211n=1
    hw_mode=g
    ignore_broadcast_ssid=0
    ```

    - For a hotspot with a password, add the following content to the `hostapd.conf` file:

    ```shell
    interface=wlan0
    driver=nl80211
    ctrl_interface=/var/run/hostapd
    ssid=Sunrise
    channel=6
    ieee80211n=1
    hw_mode=g
    ignore_broadcast_ssid=0
    wpa=2
    wpa_key_mgmt=WPA-PSK
    rsn_pairwise=CCMP
    wpa_passphrase=12345678
    ```
3. Configure the `isc-dhcp-server` file as follows:

    - Execute `sudo vim /etc/default/isc-dhcp-server` to modify the `isc-dhcp-server` file and add the following definition for the network interface:

    ```shell
    INTERFACESv4="wlan0"
    ```

    - Execute `sudo vim /etc/dhcp/dhcpd.conf` to modify the `dhcpd.conf` file and uncomment the following fields:

    ```shell
    authoritative;
    ```

    - Then, add the following configuration to the end of the `/etc/dhcp/dhcpd.conf` file:

    ```shell
    subnet 10.5.5.0 netmask 255.255.255.0 { #network and subnet mask
    range 10.5.5.100 10.5.5.254;#IP range available
    option subnet-mask 255.255.255.0; #subnet mask
    option routers 10.5.5.1;#default gateway
    option broadcast-address 10.5.5.31;#broadcast address
    default-lease-time 600;#default lease time in seconds
    max-lease-time 7200;#maximum lease time in seconds
    }
    ```

4. Stop the `wpa_supplicant` service and restart `wlan0`

    ```bash
    systemctl stop wpa_supplicant

    ip addr flush dev wlan0
    sleep 0.5
    ifconfig wlan0 down
    sleep 1
    ifconfig wlan0 up
    ```

5. Start the `hostapd` service as follows:
    - Execute the command `sudo hostapd -B /etc/hostapd.conf`
    ```bash
    root@ubuntu:~# sudo hostapd -B /etc/hostapd.conf
    Configuration file: /etc/hostapd.conf
    Using interface wlan0 with hwaddr 08:e9:f6:af:18:26 and ssid "sunrise"
    wlan0: interface state UNINITIALIZED->ENABLED
    wlan0: AP-ENABLED
    ```
    - Configure the IP and subnet of wireless interface `wlan0` using the `ifconfig` command, make sure it matches the configuration in the third step

    ```bash
    sudo ifconfig wlan0 10.5.5.1 netmask 255.255.255.0
    ```

    - Finally, start the `dhcp` server. Clients connecting to the hotspot will be assigned an IP address from `10.5.5.100` to `10.5.5.255`

    ```bash
    sudo ifconfig wlan0 10.5.5.1 netmask 255.255.255.0
    sudo systemctl start isc-dhcp-server
    sudo systemctl enable isc-dhcp-server
    ```

6. Connect to the hotspot on the development board, for example, `sunrise`

    ![image-20220601203025803](./image/network/image-20220601203025803.png)  

7. If you need to switch back to `Station` mode, you can do it as follows:
    ```bash
    # Stop hostapd
    killall -9 hostapd
    
    # Clear the address of wlan0
    ip addr flush dev wlan0
    sleep 0.5
    ifconfig wlan0 down
    sleep 1
    ifconfig wlan0 up
    
    # Restart wpa_supplicant
    systemctl restart wpa_supplicant
    
    # Connect to the hotspot, for specific operation, please refer to the previous section "Wireless Network"
    wifi_connect "WiFi-Test" "12345678"
    ```

## DNS Server

<iframe src="//player.bilibili.com/player.html?aid=700903305&bvid=BV1rm4y1E73q&cid=1196557655&page=13" scrolling="no" border="0" frameborder="no" framespacing="0" width="100%" height="500" allowfullscreen="true"> </iframe>

DNS (Domain Name Server) is a server that converts domain names to their corresponding IP addresses.

The DNS configuration on the development board is managed through the `/etc/systemd/resolved.conf` file. Users can modify this file to configure DNS settings. The steps are as follows:
1. Modify the `resolved.conf` file and add the DNS server address, for example:

    ```bash
    DNS=8.8.8.8 114.114.114.114
    ```

2. Enable DNS configuration using the following commands:

   ```bash
   sudo systemctl restart systemd-resolved
   sudo systemctl enable systemd-resolved
   sudo mv /etc/resolv.conf  /etc/resolv.conf.bak
   sudo ln -s /run/systemd/resolve/resolv.conf /etc/
   ```