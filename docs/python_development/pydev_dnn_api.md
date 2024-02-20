# 4.4 Model Inference Interface Description

## Overview

The Python version of the `pyeasy_dnn` model inference module is pre-installed on the Ubuntu system of the development board. It loads the model and creates a `Model` object to complete model inference and data parsing.

The module inference process can be divided into three steps: loading the model, image inference, and data parsing. The code example is as follows:

```python
from hobot_dnn import pyeasy_dnn as dnn

#create model object
models = model.load('./model.bin')

#do inference with image
outputs = models[0].forward(image)

for item in outputs:
    output_array.append(item.buffer)
post_process(output_array)
```

## Model Object{#model}

The Model object is created when loading the model, and includes members and methods such as `inputs`, `outputs`, and `forward`. The details are as follows:

### inputs

<font color='Blue'>[Function Description]</font>

Returns the tensor input information of the model, and specifies the specific input by index. For example, `inputs[0]` represents the 0th group of inputs.

<font color='Blue'>[Function Declaration]</font>

```python
Model.inputs(tuple(pyDNNTensor))
```

<font color='Blue'>[Parameter Description]</font>

| Parameter  | Definition |
| ---------- | ---------- |
| index | Index of the input tensor. |

<font color='Blue'>[Usage]</font>```python
def print_properties(pro):
    print("tensor type:", pro.tensor_type)
    print("data type:", pro.dtype)
    print("layout:", pro.layout)
    print("shape:", pro.shape)

models = dnn.load('../models/fcos_512x512_nv12.bin')
input = models[0].inputs[0]

print_properties(input.properties)
```

<font color='Blue'>【Return Value】</font>  

Return an object of type `pyDNNTensor`, with the following description:

| Parameter Name | Description |
| ------ | ----- |
| properties  | Represents the properties of the tensor  |
| buffer    | Represents the data in the tensor, in numpy format |
| name    | Represents the name in the tensor |

<font color='Blue'>【Notes】</font>  

None

### outputs

<font color='Blue'>【Description】</font>  

Return the tensor output information of the model, specifying the specific output by index, for example: outputs[0] represents the first output.

<font color='Blue'>【Function Declaration】</font>  

```python
Model.outputs(tuple(pyDNNTensor))
```

<font color='Blue'>【Parameter Description】</font>  

| Parameter Name      | Definition Description                  |
| ----------- | ------------------------ |
| index | Represents the index of the output tensor |

<font color='Blue'>【Usage】</font>  

```python
def print_properties(pro):
    print("tensor type:", pro.tensor_type)print("data type:", pro.dtype)
print("layout:", pro.layout)
print("shape:", pro.shape)

models = dnn.load('../models/fcos_512x512_nv12.bin')
output = models[0].outputs[0]

print_properties(output.properties)```

<font color='Blue'>【Return Value】</font>  

Returns an object of type `pyDNNTensor`, with the following description:

| Parameter Name | Description |
| ------ | ----- |
| properties  | Represents the properties of the tensor  |
| buffer    | Represents the data in the tensor, in numpy format |
| name    | Represents the name of the tensor |

<font color='Blue'>【Note】</font>  

None


### forward

<font color='Blue'>【Function Description】</font>  

Performs inference on the model with the specified input.

<font color='Blue'>【Function Signature】</font>  

```python
Model.forward(args &args, kwargs &kwargs)
```

<font color='Blue'>【Parameter Description】</font>  

| Parameter Name      | Definition                  | Range |
| ----------- | ------------------------ | ------- |
| args | Input data for inference | numpy: single model input, list[numpy, numpy, ...]: for multiple model inputs |
| kwargs | core_id, indicates the core id for model inference | 0: automatically allocated, 1: core0, 2: core1 |
| kwargs | priority, indicates the priority for the current model inference task | Range: 0 to 255. The higher the value, the higher the priority |

<font color='Blue'>【Usage】</font>  

```python
img = cam.get_img(2, 512, 512)img = np.frombuffer(img, dtype=np.uint8)
outputs = models[0].forward(img)

<font color='Blue'>【Return Value】</font>  

Returns the 'outputs' object.


<font color='Blue'>【Note】</font>  

N/A

## Sample Code
You can check the chapter [Model Inference Example](./pydev_dnn_demo) for more details.