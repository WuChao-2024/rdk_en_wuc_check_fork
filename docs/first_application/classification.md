# 3.2 Image Classification Algorithm Example

<iframe src="//player.bilibili.com/player.html?aid=700903305&bvid=BV1rm4y1E73q&cid=1196558179&page=17" scrolling="no" border="0" frameborder="no" framespacing="0" width="100%" height="500" allowfullscreen="true"> </iframe>

The development board is installed with the program `test_mobilenetv1.py` for testing the functionality of the mobilenet v1 image classification algorithm. This program reads the static image `zebra_cls.jpg` as the input of the model, and outputs the classification result `cls id: 340 Confidence: 0.991851` in the command line terminal.


## Execution Method
Execute the program `test_mobilenetv1.py`

  ```bash
  sunrise@ubuntu:~$ cd /app/pydev_demo/01_basic_sample/
  sunrise@ubuntu:/app/pydev_demo/01_basic_sample$ sudo ./test_mobilenetv1.py
  ```

## Expected Effect
Output the predicted result of the image classification algorithm, id and confidence.

`zebra_cls.jpg` is an image of a zebra. According to the classification of the `ImageNet` dataset, the returned result id is 340, with a confidence of 0.991851.

```shell
========== Classification result ==========
cls id: 340 Confidence: 0.991851
```

![zebra_cls](./image/classification/zebra_cls.jpg)