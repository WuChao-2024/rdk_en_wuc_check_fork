# Camera Usage

The RDK Ultra development kit provides two 15-pin MIPI CSI interfaces, `CAM0` and `CAM2`, which can support the connection of the imx219 camera included in the kit. When connecting the camera ribbon cable, make sure the blue side is facing up. In addition, the sample program has implemented automatic detection of the camera, so users do not need to worry about the corresponding relationship between the CAM interface and the camera.

The development board is equipped with the `mipi_camera.py` program to test the data path of the MIPI camera. This sample program will real-time capture the image data from the MIPI camera, then run the target detection algorithm, and finally output the fused image data and detection results via the HDMI interface.

- Running method: Execute the program with the following command

  ```bash
  sunrise@ubuntu:~$ cd /app/pydev_demo/03_mipi_camera_sample/
  sunrise@ubuntu:/app/pydev_demo/03_mipi_camera_sample$ sudo python3 ./mipi_camera.py 
  ```

- Expected result: After the program is executed, the monitor will display the camera image and the results of the target detection algorithm (target type, confidence) in real time.