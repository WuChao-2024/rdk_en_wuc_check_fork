---
sidebar_position: 2
---
# 2.2 System Updates
For system security and stability considerations, it is recommended for users to update the system using the `apt` command after the installation.

The software source list for the `apt` command is stored in the `/etc/apt/source.list` file, and it is necessary to update the package list with the `apt` command before installing software.

First, open the terminal command line and enter the following command:
```bash
sudo apt update
```
Next, upgrade all installed software packages to the latest version with the following command:
```bash
sudo apt full-upgrade
```

:::tip
It is recommended to use the `full-upgrade` option instead of the `upgrade` option, so that dependency packages will also be updated when related dependencies change.

When running the `sudo apt full-upgrade` command, the system will prompt for data download and disk space usage. However, `apt` does not check if there is enough disk space, so it is recommended for users to manually check with the `df -h` command. In addition, the deb files downloaded during the upgrade process will be saved in the `/var/cache/apt/archives` directory. Users can use the `sudo apt clean` command to delete cache files and free up disk space.
:::

After executing the `apt full-upgrade` command, it may be necessary to reinstall drivers, kernel files, and some system software. It is recommended for users to manually restart the device to apply the updates, using the following command:

```bash
sudo reboot
```