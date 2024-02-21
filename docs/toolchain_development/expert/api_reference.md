--- 
sidebar_position: 5 
---

# API Manual

## March

```python 
class horizon_plugin_pytorch.march.March 
```

BPU platform.

- **BAYES**: Bayes platform

- **BERNOULLI2**: Bernoulli2 platform

## qconfig

```python 
horizon_plugin_pytorch.quantization.get_default_qconfig(activation_fake_quant: Optional[str] = 'fake_quant', weight_fake_quant: Optional[str] = 'fake_quant', activation_observer: Optional[str] = 'min_max', weight_observer: Optional[str] = 'min_max', activation_qkwargs: Optional[Dict] = None, weight_qkwargs: Optional[Dict] = None) 
```

Get default qconfig.

**Parameters**

- **activation_fake_quant** – FakeQuantize type of activation, default is fake_quant. Avaliable items are fake_quant, lsq, pact.

- **weight_fake_quant** – FakeQuantize type of weight, default is fake_quant. Avaliable items are fake_quant, lsq, and pact.

- **activation_observer** – Observer type of activation, default is min_max. Avaliable items are min_max, fixed_scale, clip, percentile, clip_std, mse, kl.

- **weight_observer** – Observer type of weight, default is min_max. Avaliable items are min_max, fixed_scale, clip, percentile, clip_std, mse.

- **activation_qkwargs** – A dictionary containing activation Observer type, arguments of activation FakeQuantize, and arguments of activation Observer.

- **weight_qkwargs** – A dictionary containing weight Observer type, arguments of weight FakeQuantize, and arguments of weight Observer.

### Example of qconfig definition

- **RDK X3**:

```python 

default_qat_8bit_fake_quant_qconfig = get_default_qconfig(
        activation_observer="min_max",
        activation_qkwargs=None,
        weight_qkwargs={"qscheme": torch.per_channel_symmetric, "ch_axis": 0,},
    )

default_qat_out_8bit_fake_quant_qconfig = get_default_qconfig(
    activation_fake_quant=None,
    weight_fake_quant="fake_quant",
    activation_observer=None,
    weight_observer="min_max",
    activation_qkwargs=None,
    weight_qkwargs={"qscheme": torch.per_channel_symmetric, "ch_axis": 0,},
    )

default_calib_8bit_fake_quant_qconfig = get_default_qconfig(
    activation_fake_quant="fake_quant",
    weight_fake_quant="fake_quant",
    activation_observer="percentile",
    weight_observer="min_max",
    activation_qkwargs=None,
    weight_qkwargs={"qscheme": torch.per_channel_symmetric, "ch_axis": 0,},
    )

default_calib_out_8bit_fake_quant_qconfig = (
    default_qat_out_8bit_fake_quant_qconfig
    )

default_qat_8bit_lsq_quant_qconfig = get_default_qconfig(
    activation_fake_quant="lsq",
    weight_fake_quant="lsq",
    activation_observer="min_max",
    weight_observer="min_max",
    activation_qkwargs={"use_grad_scaling": True, "averaging_constant": 1.0,},
    weight_qkwargs={"qscheme": torch.per_channel_symmetric, "ch_axis": 0, "use_grad_scaling": True,"averaging_constant": 1.0,},
    )weight_observer="min_max",
        activation_qkwargs=None,
        weight_qkwargs={"qscheme": torch.per_channel_symmetric, "ch_axis": 0,},
        )

default_qat_8bit_weight_32bit_out_fake_quant_qconfig = get_default_qconfig(
    activation_fake_quant=None,
    weight_fake_quant="fake_quant",
    activation_observer=None,
    weight_observer="min_max",
    activation_qkwargs=None,
    weight_qkwargs={"qscheme": torch.per_channel_symmetric, "ch_axis": 0,},
    )

default_calib_8bit_fake_quant_qconfig = get_default_qconfig(
    activation_fake_quant="fake_quant",
    weight_fake_quant="fake_quant",
    activation_observer="percentile",
    weight_observer="min_max",
    activation_qkwargs=None,
    weight_qkwargs={"qscheme": torch.per_channel_symmetric, "ch_axis": 0,},
    )

default_calib_8bit_weight_32bit_out_fake_quant_qconfig = (
    default_qat_out_8bit_fake_quant_qconfig
    )

default_qat_8bit_weight_16bit_act_fake_quant_qconfig = get_default_qconfig(
    activation_fake_quant="fake_quant",
    weight_fake_quant="fake_quant",
    activation_observer="min_max",
    weight_observer="min_max",
    activation_qkwargs={"dtype": qint16,},
    weight_qkwargs={"qscheme": torch.per_channel_symmetric, "ch_axis": 0,},
)

default_calib_8bit_weight_16bit_act_fake_quant_qconfig = get_default_qconfig(
    activation_fake_quant="fake_quant",
    weight_fake_quant="fake_quant",
    activation_observer="percentile",
    weight_observer="min_max",
    activation_qkwargs={"dtype": qint16,},
    weight_qkwargs={"qscheme": torch.per_channel_symmetric, "ch_axis": 0,},
)class horizon_plugin_pytorch.quantization.FakeQuantize(observer: type = <class 'horizon_plugin_pytorch.quantization.observer.MovingAverageMinMaxObserver'>, saturate: bool = None, in_place: bool = False, compat_mask: bool = True, channel_len: int = 1, **observer_kwargs)

```

模拟训练期间的量化和反量化操作。

该模块的输出由以下公式计算得出：

- x_out = (clamp(round(x/scale + zero_point), quant_min, quant_max)-zero_point)*scale # noqa

- scale定义了用于量化的比例因子。

- zero_point指定浮点数中0所映射到的量化值

- quant_min指定允许的最小量化值。

- quant_max指定允许的最大量化值。

- fake_quant_enabled控制对张量应用伪量化的操作，注意统计信息仍然可以更新。

- observer_enabled控制对张量进行统计收集。

- dtype指定了使用伪量化进行模拟的量化dtype，允许的值为qint8和qint16。quant_min和quant_max的值应与dtype一致。

**Parameters**

- **observer** – 用于观察输入张量统计信息并计算scale和zero-point的模块。

- **saturate** – 是否将超出量化范围的梯度置为0。

- **in_place** – 是否使用就地伪量化。

- **compat_mask** – 当saturate=True时，是否将布尔掩码打包到位字段中。

- **channel_len** – 通道维度上的数据大小。

- **observer_kwargs** – 观察模块的参数。

```python
observer
```

用户提供的模块，用于收集输入张量的统计信息并计算scale和zero-point。

```python
extra_repr()
```

设置模块的额外表示。

要打印自定义的额外信息，您应该在自己的模块中重新实现此方法。可以接受单行和多行字符串。

``````python
forward(x)
```

定义每次调用时执行的计算。

所有子类都应该重写这个函数。

:::info 注解

尽管前向传播的步骤需要在这个函数中定义，但是应该之后调用模块实例，而不是直接调用这个函数，因为前者会处理注册的hooks的运行，而后者则会默默地忽略它们。
:::

```python
set_qparams(scale: Union[torch.Tensor, Sequence, float], zero_point: Optional[Union[torch.Tensor, Sequence, int]] = None)
```

设置量化参数，默认对称量化。

```python
classmethod with_args(**kwargs)
```

允许创建类工厂的包装器。

当需要使用相同的构造函数参数创建不同的实例时，这非常有用。可以与_callable_args连用。

示例：

```python
>>> # xdoctest: +SKIP("未定义的变量")
>>> Foo.with_args = classmethod(_with_args)
>>> foo_builder = Foo.with_args(a=3, b=4).with_args(answer=42)
>>> foo_instance1 = foo_builder()
>>> foo_instance2 = foo_builder()
>>> id(foo_instance1) == id(foo_instance2)
False
```

## QAT

```python
horizon_plugin_pytorch.quantization.convert(module, mapping=None, inplace=False, remove_qconfig=True, fast_mode=False)
```

转换模块。

通过调用目标模块类上的from_float方法，将输入模块中的子模块转换为不同的模块。
如果将remove_qconfig设置为True，则最后会删除qconfig。**Parameters**

- **module** – input module

- **mapping** – a dictionary that maps from source module type to target module type, can be overwritten to allow swapping user defined Modules

- **inplace** – carry out model transformations in-place, the original module is mutated

- **fast_mode** – whether to accelerate quantized model forward. If set True, quantized model cannot be compiled

```python
horizon_plugin_pytorch.quantization.convert_fx(graph_module: torch.fx.graph_module.GraphModule, inplace: bool = False, convert_custom_config_dict: Optional[Dict[str, Any]] = None, _remove_qconfig: bool = True, fast_mode: bool = False) → horizon_plugin_pytorch.quantization.fx.graph_module.QuantizedGraphModule
```

Convert a calibrated or trained model to a quantized model.

**Parameters**

- **graph_module** – A prepared and calibrated/trained model (GraphModule)

- **inplace** – Carry out model transformations in-place, the original module is mutated.

- **convert_custom_config_dict** –

dictionary for custom configurations for convert function:

```python
convert_custom_config_dict = {
    # We automativally preserve all attributes, this option is
    # just in case and not likely to be used.
    "preserved_attributes": ["preserved_attr"],
}
```

- **_remove_qconfig** – Option to remove the qconfig attributes in the model after convert. for internal use only.

- **fast_mode** – whether to accelerate quantized model forward. If set True, quantized model cannot be compiled.

**Returns**

A quantized model (GraphModule)

Example: convert fx example:

```python
# prepared_model: the model after prepare_fx/prepare_qat_fx and
# calibration/training
quantized_model = convert_fx(prepared_model)
``````python
horizon_plugin_pytorch.quantization.fuse_fx(model: torch.nn.modules.module.Module, fuse_custom_config_dict: Optional[Dict[str, Any]] = None) → horizon_plugin_pytorch.quantization.fx.graph_module.GraphModuleWithAttr
```

Fuse modules like conv+add+bn+relu etc.

Fusion rules are defined in horizon_plugin_pytorch.quantization.fx.fusion_pattern.py

**Parameters**

- **model** – a torch.nn.Module model

- **fuse_custom_config_dict** –

Dictionary for custom configurations for fuse_fx, e.g.

```python
fuse_custom_config_dict = {
    # We automativally preserve all attributes, this option is
    # just in case and not likely to be used.
    "preserved_attributes": ["preserved_attr"],
}
```

Example: fuse_fx example:

```python
from torch.quantization import fuse_fx
m = fuse_fx(m)
```

```python
horizon_plugin_pytorch.quantization.fuse_known_modules(mod_list, is_qat=False, additional_fuser_method_mapping=None)
```

Fuse modules.

Return a list of modules that fuses the operations specified in the input module list.

Fuses only the following sequence of modules: conv, bn; conv, bn, relu; conv, relu; conv, bn, add; conv, bn, add, relu; conv, add; conv, add, relu; linear, bn; linear, bn, relu; linear, relu; linear, bn, add; linear, bn, add, relu; linear, add; linear, add, relu. For these sequences, the first element in the output module list performs the fused operation. The rest of the elements are set to nn.Identity()

```python
horizon_plugin_pytorch.quantization.fuse_modules(model, modules_to_fuse, inplace=False, fuser_func=<function fuse_known_modules>, fuse_custom_config_dict=None)
```

Fuses a list of modules into a single module.

Fuses only the following sequence of modules: conv, bn; conv, bn, relu; conv, relu; conv, bn, add; conv, bn, add, relu; conv, add; conv, add, relu; linear, bn; linear, bn, relu; linear, relu; linear, bn, add; linear, bn, add, relu; linear, add; linear, add, relu. For these sequences, the first element in the output module list performs the fused operation. The rest of the elements are set to nn.Identity()**Parameters**

- **model** - Model containing the modules to be fused

- **modules_to_fuse** - list of list of module names to fuse. Can also be a list of strings if there is only a single list of modules to fuse.

- **inplace** - bool specifying if fusion happens in place on the model, by default a new model is returned

- **fuser_func** - Function that takes in a list of modules and outputs a list of fused modules of the same length. For example, fuser_func([convModule, BNModule]) returns the list [ConvBNModule, nn.Identity()]. Defaults to torch.ao.quantization.fuse_known_modules

- **fuse_custom_config_dict** - custom configuration for fusion

```python
# Example of fuse_custom_config_dict
fuse_custom_config_dict = {
    # Additional fuser_method mapping
    "additional_fuser_method_mapping": {
        (torch.nn.Conv2d, torch.nn.BatchNorm2d): fuse_conv_bn
    },
}
```

**Returns**

model with fused modules. A new copy is created if inplace=True.

Examples:

```python
>>> # xdoctest: +SKIP
>>> m = M().eval()
>>> # m is a module containing the sub-modules below
>>> modules_to_fuse = [ ['conv1', 'bn1', 'relu1'],
                      ['submodule.conv', 'submodule.relu']]
>>> fused_m = fuse_modules(
                m, modules_to_fuse)
>>> output = fused_m(input)

>>> m = M().eval()
>>> # Alternately provide a single list of modules to fuse
>>> modules_to_fuse = ['conv1', 'bn1', 'relu1']
>>> fused_m = fuse_modules(
                m, modules_to_fuse)
>>> output = fused_m(input)
```

```python
horizon_plugin_pytorch.quantization.prepare_qat(model: torch.nn.modules.module.Module, mapping: Optional[Dict[Type[torch.nn.modules.module.Module], Type[torch.nn.modules.module.Module]]] = None, inplace: bool = False, optimize_graph: bool = False, hybrid: bool = False, optimize_kwargs: Optional[Dict[str, Tuple]] = None)
```准备qat。

为量化感知训练准备一个模型的副本，并将其转换为量化版本。

量化配置应事先分配给.qconfig属性中的各个子模块。

**参数**

- **model** - 要就地修改的输入模型
- **mapping** - 将浮点模块映射到要替换的量化模块的字典。
- **inplace** - 在原地执行模型转换，原始模块被改变。
- **optimize_graph** - 是否对原始模型进行一些处理以达到特定目的。目前仅支持使用torch.fx来修复cat输入比例（仅在Bernoulli上使用）。
- **hybrid** - 是否生成混合模型，其中部分中间操作在浮点数中计算。现在对此功能有一些限制：1.混合模型不能通过check_model，并且不能编译。2.某些量化操作无法直接接受来自浮点操作的输入，用户需要手动插入QuantStub。
- **optimize_kwargs** - 优化图的字典，格式如下：

```Python
optimize_kwargs = {
    # 可选，指定要进行的优化类型。目前只支持“ uniff_inputs_scale”
    "opt_types": ("unify_inputs_scale",),

    # 可选，以限定名称开头的模块进行优化
    "module_prefixes": ("backbone.conv",),

    # 可选，将优化的模块类型
    "module_types": (horizon.nn.qat.conv2d,),

    # 可选，要优化的函数
    "functions": (torch.clamp,),

    # 可选，要优化的方法。目前仅支持FloatFunctional方法
    "methods": ("add",),
}
```

```Python

horizon_plugin_pytorch.quantization.prepare_qat_fx(model: Union[torch.nn.modules.module.Module, torch.fx.graph_module.GraphModule], qconfig_dict: Optional[Dict[str, Any]] = None, prepare_custom_config_dict: Optional[Dict[str, Any]] = None, optimize_graph: bool = False, hybrid: bool = False, hybrid_dict: Optional[Dict[str, List]] = None) → horizon_plugin_pytorch.quantization.fx.graph_module.ObservedGraphModule
```

为量化感知训练准备模型。**Parameters**

- **model** - torch.nn.Module model or GraphModule model (maybe from fuse_fx)

- **qconfig_dict** -

qconfig_dict is a dictionary with the following configurations:

```python

qconfig_dict = {
    # optional, global config
    "": qconfig,

    # optional, used for module types
    "module_type": [
        (torch.nn.Conv2d, qconfig),
        ...,
    ],

    # optional, used for module names
    "module_name": [
        ("foo.bar", qconfig)
        ...,
    ],
    # priority (in increasing order):
    #   global, module_type, module_name, module.qconfig
    # qconfig == None means quantization should be
    # skipped for anything matching the rule.
    # The qconfig of function or method is the same as the
    # qconfig of its parent module, if it needs to be set
    # separately, please wrap this function as a module.
}
```

- **prepare_custom_config_dict** -

customization configuration dictionary for quantization tool:

```python
prepare_custom_config_dict = {
    # We automativally preserve all attributes, this option is
    # just in case and not likely to be used.
    "preserved_attributes": ["preserved_attr"],
}
```

- **optimize_graph** - whether to do some process on origin model for special purpose. Currently only support using torch.fx to fix cat input scale(only used on Bernoulli)- **hybrid** - 在混合模式下准备模型。默认值为False，模型完全在BPU上运行。如果模型通过模型转换量化或包含一些CPU操作，则应该设置为True。在混合模式下，不受BPU支持的操作和用户指定的操作将在CPU上运行。如何设置qconfig：混合模式下的qconfig与非混合模式下的qconfig相同。对于BPU操作，我们应确保该操作的输入被量化，其前一个非量化操作的激活qconfig即使是一个CPU操作，也不应为None。如何指定CPU操作：在hybrid_dict中定义CPU module_name或module_type。

- **hybrid_dict** -

hybrid_dict是一个字典，用于定义用户指定的CPU操作：

```python
hybrid_dict = {
    # 可选，用于模块类型
    "module_type": [torch.nn.Conv2d, ...],

    # 可选，用于模块名称
    "module_name": ["foo.bar", ...],
}
# 优先级（从低到高）：module_type，module_name
# 要将函数或方法设置为CPU操作，请将其封装为一个模块。
```

**返回**

带有伪量化模块（由qconfig_dict配置）的GraphModule，准备进行量化感知训练

示例：prepare_qat_fx示例：

```python

import torch
from horizon_plugin_pytorch.quantization import get_default_qat_qconfig
from horizon_plugin_pytorch.quantization import prepare_qat_fx

qconfig = get_default_qat_qconfig()
def train_loop(model, train_data):
    model.train()
    for image, target in data_loader:
        ...

qconfig_dict = {"": qconfig}
prepared_model = prepare_qat_fx(float_model, qconfig_dict)
# 运行QAT训练
train_loop(prepared_model, train_loop)
```

torch.fx的扩展追踪器和包装器。

该文件定义了一个继承自torch.fx.Tracer的追踪器和一个扩展的包装器，允许包装用户定义的模块或方法，帮助用户通过torch.fx对自己的模块进行优化。

```python
horizon_plugin_pytorch.utils.fx_helper.wrap(skip_compile: bool = False)
```Extend torch.fx.warp.

This function can be:
- 1) called or used as a decorator on a string to register a builtin function as a “leaf function”
- 2) called or used as a decorator on a function to register this function as a “leaf function”
- 3) called or used as a decorator on subclass of torch.nn.Module to register this module as a “leaf module”, and register all user defined method in this class as “leaf method”
- 4) called or used as a decorator on a class method to register it as “leaf method”

**Parameters**

skip_compile – Whether the wrapped part should not be compiled.

**Returns**

The actual decorator.

**Return Type**

wrap_inner


## ONNX

```python
horizon_plugin_pytorch.utils.onnx_helper.export_to_onnx(model, args, f, export_params=True, verbose=False, training=<TrainingMode.EVAL: 0>, input_names=None, output_names=None, operator_export_type=<OperatorExportTypes.ONNX_FALLTHROUGH: 3>, opset_version=11, do_constant_folding=True, dynamic_axes=None, keep_initializers_as_inputs=None, custom_opsets=None)
```

Export a (float or qat)model into ONNX format.

**Parameters**

- **model** (torch.nn.Module/torch.jit.ScriptModule/ScriptFunction) – the model to be exported.

- **args** (tuple or torch.Tensor) –

    args can be structured either as:

    a. ONLY A TUPLE OF ARGUMENTS:

    ```python
        args = (x, y, z)
    ```

    The tuple should contain model inputs such that model(*args) is a valid invocation of the model. Any non-Tensor arguments will be hard-coded into the exported model; any Tensor arguments will become inputs of the exported model, in the order they occur in the tuple.

    b. A TENSOR:```python
args = torch.Tensor([1])
```

This is equivalent to a 1-ary tuple of that Tensor.

c. A TUPLE OF ARGUMENTS ENDING WITH A DICTIONARY OF NAMED ARGUMENTS:

```python
args = (x,
        {'y': input_y,
        'z': input_z})
```

All but the last element of the tuple will be passed as non-keyword arguments, and named arguments will be set from the last element. If a named argument is not present in the dictionary, it is assigned the default value, or None if a default value is not provided.

- **f** – a file-like object or a string containing a file name. A binary protocol buffer will be written to this file.

- **export_params** (bool, default True) – if True, all parameters will be exported.

- **verbose** (bool, default False) – if True, prints a description of the model being exported to stdout, doc_string will be added to graph. doc_string may contain mapping of module scope to node name in future torch onnx.

- **training** (enum, default TrainingMode.EVAL) –

    if model.training is False and in training mode if model.training is True.

    ``TrainingMode.EVAL``: export the model in inference mode.

    ``TrainingMode.PRESERVE``: export the model in inference mode.

    ``TrainingMode.TRAINING``: export the model in training mode. Disables optimizations which might interfere with training.

- **input_names** (list of str, default empty list) – names to assign to the input nodes of the graph, in order.

- **output_names** (list of str, default empty list) – names to assign to the output nodes of the graph, in order.

- **operator_export_type** (enum, default ONNX_FALLTHROUGH) –

    ``OperatorExportTypes.ONNX``: Export all ops as regular ONNX ops (in the default opset domain).

    ``OperatorExportTypes.ONNX_FALLTHROUGH``: Try to convert all ops to standard ONNX ops in the default opset domain.

    ``OperatorExportTypes.ONNX_ATEN``: All ATen ops (in the TorchScript namespace "aten") are exported as ATen ops.

    ``OperatorExportTypes.ONNX_ATEN_FALLBACK``: Try to export each ATen op (in the TorchScript namespace "aten") as a regular ONNX op. If we are unable to do so, fall back to exporting an ATen op.

- **opset_version** (int, default 11) – by default we export the model to the opset version of the onnx submodule.

- **do_constant_folding** (bool, default False) – Apply the constant-folding optimization. Constant-folding will replace some of the ops that have all constant inputs with pre-computed constant nodes.- **dynamic_axes** (dict<str, list(int)/dict<int, str>>, default empty dict) –

    By default the exported model will have the shapes of all input and output tensors set to exactly match those given in args (and example_outputs when that arg is required). To specify axes of tensors as dynamic (i.e. known only at run-time), set dynamic_axes to a dict with schema:

    ``KEY (str)``: an input or output name. Each name must also be provided in input_names or output_names.

    ``VALUE (dict or list)``: If a dict, keys are axis indices and values are axis names. If a list, each element is an axis index.

- **keep_initializers_as_inputs** (bool, default None) – If True, all the initializers (typically corresponding to parameters) in the exported graph will also be added as inputs to the graph. If False, then initializers are not added as inputs to the graph, and only the non-parameter inputs are added as inputs. This may allow for better optimizations (e.g. constant folding) by backends/runtimes.

- **custom_opsets** (dict<str, int>, default empty dict) –

    A dict with schema:

    ``KEY (str)``: opset domain name

    ``VALUE (int)``: opset version

    If a custom opset is referenced by model but not mentioned in this dictionary, the opset version is set to 1.


## TorchScript Model Save and Load

```python
horizon_plugin_pytorch.jit.load(f, map_location=None, _extra_files=None)
```

Load ScriptModule previously saved with horizon.jit.save.

In addition to loaded plugin version comparsion with current plugin version, this function is same as torch.jit.save.

**Parameters**

- **f** – a file-like object (has to implement read, readline, tell, and seek), or a string containing a file name

- **map_location** (string or torch.device) – A simplified version of map_location in torch.jit.save used to dynamically remap storages to an alternative set of devices.

- **_extra_files** (dictionary of filename to content) – The extra filenames given in the map would be loaded and their content would be stored in the provided map.

**Returns**

A ScriptModule object.

```python
horizon_plugin_pytorch.jit.save(m, f, _extra_files=None)
```

Save ScriptModule.

In addition to plugin version saved, this function is same as torch.jit.save.**Parameters**

- **m** - A ScriptModule to save.

- **f** - A file-like object (has to implement write and flush) or a string containing a file name.

- **_extra_files** - Map from filename to contents which will be stored as part of f.


## Horizon Operators

```python
horizon_plugin_pytorch.nn.functional.filter(*inputs: Union[Tuple[torch.Tensor], Tuple[horizon_plugin_pytorch.qtensor.QTensor]], threshold: float, idx_range: Optional[Tuple[int, int]] = None) → List[List[torch.Tensor]]
```

Filter.

The output order is different with bpu, because that the compiler do some optimization and slice input following complex rules, which is hard to be done by plugin.

All inputs are filtered along HW by the max value within a range in channel dim of the first input. Each NCHW input is splited, transposed and flattened to List[Tensor[H * W, C]] first. If input is QTensor, the output will be dequantized.

**Parameters**

- **inputs** - Data in NCHW format. Each input shold have the same size in N, H, W. The output will be selected according to the first input.

- **threshold** - Threshold, the lower bound of output.

- **idx_range** - The index range of values counted in compare of the first input. Defaults to None which means use all the values.

**Returns**

A list with same length of batch size, and each element contains:

- **max_value**: Flattened max value within idx_range in channel dim.

- **max_idx**: Flattened max value index in channel dim.

- **coord**: The original coordinates of the output data in the input data in the shape of [M, (h, w)].

(multi) data: Filtered data in the shape of [M, C].

**Return type**

Union[List[List[Tensor]], List[List[QTensor]]]

```python
horizon_plugin_pytorch.nn.functional.point_pillars_preprocess(points_list: List[torch.Tensor], pc_range: torch.Tensor, voxel_size: torch.Tensor, max_voxels: int, max_points_per_voxel: int, use_max: bool, norm_range: torch.Tensor, norm_dims: torch.Tensor) → Tuple[torch.Tensor, torch.Tensor]
```Preprocess PointPillars.

**Parameters**

- **points_list** - [(M1, ndim), (M2, ndim),...], List of PointCloud data.

- **pc_range** - (6,), indicate voxel range, format: [x_min, y_min, z_min, x_max, y_max, z_max]

- **voxel_size** - (3,), xyz, indicate voxel size.

- **max_voxels** - Indicate maximum voxels.

- **max_points_per_voxel** - Indicate maximum points contained in a voxel.

- **use_max** - Whether to use max_voxels, for deploy should be True.

- **norm_range** - Feature range, like [x_min, y_min, z_min, ..., x_max, y_max, z_max, ...].

- **norm_dims** - Dims to do normalize.

**Returns**

(features, coords), encoded feature and coordinates in (idx, z, y, x) format.

**Return Type**
(Tensor, Tensor)

```python
class horizon_plugin_pytorch.nn.BgrToYuv444(channel_reversal: bool = False)
```

Convert image color format from bgr to yuv444.

**Parameters**

- **channel_reversal** - Color channel order, set to True when used on RGB input. Defaults to False.

```python
forward(input: torch.Tensor)
```

Forward pass of BgrToYuv444.

```python
class horizon_plugin_pytorch.nn.Correlation(kernel_size: int = 1, max_displacement: int = 1, stride1: int = 1, stride2: int = 1, pad_size: int = 0, is_multiply: bool = True)
```

Perform multiplicative patch comparisons between two feature maps.

![qat_correlation](./image/expert/qat_correlation.png)**Parameters**

- **kernel_size** – kernel size for Correlation must be an odd number

- **max_displacement** – Max displacement of Correlation

- **stride1** – stride1 quantize data1 globally

- **stride2** – stride2 quantize data2 within neighborhood centered around data1

- **pad_size** – pad for Correlation

- **is_multiply** – operation type is either multiplication or subduction, only support True now

```python
forward(data1: Union[torch.Tensor, horizon_plugin_pytorch.qtensor.QTensor], data2: Union[torch.Tensor, horizon_plugin_pytorch.qtensor.QTensor]) → torch.Tensor
```

Forward for Horizon Correlation.

**Parameters**

- **data1** – shape of [N,C,H,W]

- **data2** – shape of [N,C,H,W]

**Returns**

output

**Return Type**

Tensor

```python
class horizon_plugin_pytorch.nn.DetectionPostProcess(score_threshold: int = 0, regression_scale: Optional[Tuple[float, float, float, float]] = None, background_class_idx: Optional[int] = None, size_threshold: Optional[float] = None, image_size: Optional[Tuple[int, int]] = None, pre_decode_top_n: Optional[int] = None, post_decode_top_n: Optional[int] = None, iou_threshold: Optional[float] = None, pre_nms_top_n: Optional[int] = None, post_nms_top_n: Optional[int] = None, nms_on_each_level: bool = False, mode: str = 'normal')
```

General post process for object detection models.

Compatible with YOLO, SSD, RetinaNet, Faster-RCNN (RPN & RCNN), etc. Note that this is a float OP, please use after DequantStubs.

**Parameters**

- **score_threshold** – Filter boxes whose score is lower than this. Defaults to 0.

- **regression_scale** – Scale to be multiplied to box regressions. Defaults to None.

- **background_class_idx** – Specify the class index to be ignored. Defaults to None.- **size_threshold** – 过滤高度或宽度小于此数值的框。默认为None。

- **image_size** – 将框裁剪到图像尺寸。默认为None。

- **pre_decode_top_n** – 在解码之前，按照目标检测概率（得分向量的第一个元素）获取前n个框。默认为None。

- **post_decode_top_n** – 在解码之后，按照得分获取前n个框。默认为None。

- **iou_threshold** – NMS的IoU阈值。默认为None。

- **pre_nms_top_n** – 在NMS之前，按照得分获取前n个框。默认为None。

- **post_nms_top_n** – 在NMS之后，按照得分获取前n个框。默认为None。

- **nms_on_each_level** – 是否在每个级别上进行独立的NMS。默认为False。

- **mode** – 仅支持“normal”和“yolo”。如果设置为“yolo”：1. 框将根据目标检测概率而不是分类得分进行过滤。2. 回归中的dx、dy将被视为绝对偏移量。3. 目标检测概率将与分类得分相乘。默认为“normal”。

```python
forward(boxes: List[torch.Tensor], scores: List[torch.Tensor], regressions: List[torch.Tensor], image_shapes: Optional[torch.Tensor] = None) → Tuple[Tuple[torch.Tensor], Tuple[torch.Tensor], Tuple[torch.Tensor]]
```

DetectionPostProcess的前向传递。

```python
class horizon_plugin_pytorch.nn.DetectionPostProcessV1(num_classes: int, box_filter_threshold: float, class_offsets: List[int], use_clippings: bool, image_size: Tuple[int, int], nms_threshold: float, pre_nms_top_k: int, post_nms_top_k: int, nms_padding_mode: Optional[str] = None, nms_margin: float = 0.0, use_stable_sort: Optional[bool] = None, bbox_min_hw: Tuple[float, float] = (0, 0))
```

用于目标检测模型的后处理。仅支持bernoulli2模型。

该操作在BPU上实现，因此预计比CPU实现更快。此操作需要输入缩放因子为1 / 2 ** 4，或者将应用重新缩放到输入数据。因此，您可以将之前操作（例如Conv2d）的输出尺度手动设置为1 / 2 ** 4，以避免重新缩放并获得最佳性能和准确性。

与DetectionPostProcess的主要区别：

1. 每个锚点只会生成一个预测框，但在DetectionPostProcess中，每个锚点会为每个类别生成一个框（共num_classes个框）。
2. NMS有一个margin参数，仅当box1.score - box2.score > margin时，box2才会被box1压制（DetectionPostProcess中，box1.score > box2.score）。
3. 可以为输出类别索引添加偏移量（使用class_offsets）。

**参数**

- **num_classes** – 类别数。

- **box_filter_threshold** – 通过最大得分过滤框的默认阈值。

- **class_offsets** – 要为每个分支输出类别索引添加的偏移量。

- **use_clippings** – 是否将框裁剪到图像尺寸。如果输入被填充，可以通过提供图像尺寸将框裁剪到真实内容。

- **image_size** – 固定的图像尺寸（h，w），如果输入具有不同的尺寸，则设置为None。- **nms_threshold** – IoU阈值用于nms。

- **nms_margin** – 只有在box1.score - box2.score > nms_margin时，才会抑制box2。

- **pre_nms_top_k** – nms之前每个图像中的最大边界框数量。

- **post_nms_top_k** – 每个图像中输出的最大边界框数量。

- **nms_padding_mode** – 将bbox填充以匹配输出的边界框数目到post_nms_top_k的方式，可以是None，“pad_zero”或“rollover”。

- **bbox_min_hw** – 所选边界框的最小高度和宽度。

```python
forward(data: List[torch.Tensor], anchors: List[torch.Tensor], image_sizes: Tuple[int, int] = None) → torch.Tensor
```

DetectionPostProcessV1的前向传递。

**参数**

- **data** – (N, (4 + num_classes) * anchor_num, H, W)

- **anchors** – (N, anchor_num * 4, H, W)

- **image_sizes** – 默认为None。

**返回**

（bbox (x1, y1, x2, y2), score, class_idx）的列表。

**返回类型**

List[Tuple[Tensor, Tensor, Tensor]]

```python
class horizon_plugin_pytorch.nn.PointPillarsScatter(output_shape=None)

forward(voxel_features: torch.Tensor, coords: torch.Tensor, output_shape: Optional[Union[torch.Tensor, list, tuple]] = None) → torch.Tensor
```

Horizon PointPillarsScatter的前向传递。

**参数**

- **voxel_features** – [M, …]，M之后的维度将被展平。

- **coords** – [M, (n, …, y, x)]，仅使用N、H和W上的索引。

- **output_shape** – 期望的输出形状。默认为None。**Returns**

The NCHW pseudo image.

**Return Type**

Tensor

```python
class horizon_plugin_pytorch.nn.RcnnPostProcess(image_size: Tuple[int, int] = (1024, 1024), nms_threshold: float = 0.3, box_filter_threshold: float = 0.1, num_classes: int = 1, post_nms_top_k: int = 100, delta_mean: List[float] = (0.0, 0.0, 0.0, 0.0), delta_std: List[float] = (1.0, 1.0, 1.0, 1.0))
```

Post Process of RCNN output.

Given bounding boxes and corresponding scores and deltas, decodes bounding boxes and performs NMS. In details, it consists of:

Argmax on multi-class scores

Filter out those belows the given threshold

Non-linear Transformation, convert box deltas to original image coordinates

Bin-sort remaining boxes on score

Apply class-aware NMS and return the firstnms_output_box_num of boxes

**Parameters**

- **image_size** – a int tuple of (h, w), for fixed image size

- **nms_threshold** – bounding boxes of IOU greater than nms_threshold will be suppressed

- **box_filter_threshold** – bounding boxes of scores less than box_filter_threshold will be discarded

- **num_classes** – total number of classes

- **post_nms_top_k** – number of bounding boxes after NMS in each image

- **delta_mean** – a float list of size 4

- **delta_std** – a float list of size 4

```python
forward(boxes: List[torch.Tensor], scores: torch.Tensor, deltas: torch.Tensor, image_sizes: Optional[torch.Tensor] = None)
```

Forward of RcnnPostProcess.

**Parameters**- **boxes** - list of box of shape [box_num, (x1, y1, x2, y2)]. can be Tensor(float), QTensor(float, int)

- **scores** - shape is [num_batch * num_box, num_classes + 1, 1, 1,], dtype is float32

- **deltas** - shape is [num_batch * num_box, (num_classes + 1) * 4, 1, 1,], dtype is float32

- **image_sizes** - shape is [num_batch, 2], dtype is int32, for dynamic image size, can be None. Defaults to None

**Returns**
Output data in format
[x1, y1, x2, y2, score, class_index], dtype is float32. If the output boxes number is less than post_nms_top_k, they are padded with -1.0.

**Return Type**
Tensor[num_batch, post_nms_top_k, 6]

Horizon plugin.

```python
horizon_plugin_pytorch.bgr2centered_gray(input: torch.Tensor) → torch.Tensor
```

Convert color space.

Convert images from BGR format to centered gray.

**Parameters**
- **input** - input image in BGR format of shape [N, 3, H, W], ranging 0~255

**Returns**
Centered gray image of shape [N, 1, H, W], ranging -128~127.

**Return Type**
Tensor

```python
horizon_plugin_pytorch.bgr2centered_yuv(input: torch.Tensor, swing: str = 'studio') → torch.Tensor
```

Convert color space.

Convert images from BGR format to centered YUV444 BT.601.

**Parameters**- **input** – 输入图像的BGR格式，范围在0~255之间

- **swing** – YUV Studio摆动的“studio”（Y: -112~107, U, V: -112~112）。YUV全摆动的“full”（Y, U, V: -128~127）。默认为“studio”。

**Returns**

居中的YUV图像

**返回类型**

Tensor

```python
horizon_plugin_pytorch.bgr2gray(input: torch.Tensor) → torch.Tensor
```

颜色空间转换。

将图像从BGR格式转换为灰度

**参数**

- **input** – 输入图像的BGR格式，形状为[N, 3, H, W]，范围在0~255之间

**返回**

形状为[N, 1, H, W]的灰度图像，范围在0~255之间

**返回类型**

Tensor

```python
horizon_plugin_pytorch.bgr2rgb(input: torch.Tensor) → torch.Tensor
```

颜色空间转换。

将图像从BGR格式转换为RGB

**参数**

- **input** – 形状为[N, 3, H, W]的BGR格式图像

**返回**

形状为[N, 3, H, W]的RGB格式图像

**返回类型**TensorQTensor

```python
horizon_plugin_pytorch.centered_yuv2rgb(input: horizon_plugin_pytorch.qtensor.QTensor, swing: str = 'studio', mean: Union[List[float], torch.Tensor] = (128.0,), std: Union[List[float], torch.Tensor] = (128.0,), q_scale: Union[float, torch.Tensor] = 0.0078125) → horizon_plugin_pytorch.qtensor.QTensor
```

转换颜色空间。

将图像从中心化的YUV444 BT.601格式转换为转换和量化的RGB。只在量化模型中使用此操作符。将其插入在QuantStub之后。将QuantStub的比例传递给q_scale参数，并在此后将QuantStub的比例设置为1。

**Parameters**

- **input**：以中心化的YUV444 BT.601格式表示的输入图像，由金字塔中心化，范围为-128。

- **swing**：YUV studio swing的“studio”（Y：-112~107，U，V：-112~112）。“full”表示完全振荡的YUV（Y，U，V：-128~127）。默认为“studio”。

- **mean**：RGB均值，是一个浮点数列表或torch.Tensor，可以是标量[float]或[ float, float, float]表示的每通道均值。

- **std**：RGB标准差，是一个浮点数列表或torch.Tensor，可以是标量[float]或[ float, float, float]表示的每通道标准差。

- **q_scale**：RGB量化比例。

**Returns**

转换和量化后的RGB颜色图像，dtype是qint8。

**Returns Type**

QTensor

```python
horizon_plugin_pytorch.rgb2bgr(input: torch.Tensor) → torch.Tensor
```

转换颜色空间。

将图像从RGB格式转换为BGR。

**Parameters**

- **input**：RGB格式的图像，形状为[N, 3, H, W]。

**Returns**

形状为[N, 3, H, W]的BGR格式图像。

**Returns Type**

Tensor```python
horizon_plugin_pytorch.rgb2centered_gray(input: torch.Tensor) → torch.Tensor
```

Convert color space.

Convert images from RGB format to centered gray

**Parameters**

- **input** – input image in RGB format of shape [N, 3, H, W], ranging 0~255

**Returns**

centered gray image of shape [N, 1, H, W], ranging -128~127

**Return type**

Tensor

```python
horizon_plugin_pytorch.rgb2centered_yuv(input: torch.Tensor, swing: str = 'studio') → torch.Tensor
```

Convert color space.

Convert images from RGB format to centered YUV444 BT.601

**Parameters**

- **input** – input image in RGB format, ranging 0~255

- **swing** – “studio” for YUV studio swing (Y: -112~107, U, V: -112~112). “full” for YUV full swing (Y, U, V: -128~127). default is “studio”

**Returns**

centered YUV image

**Return type**

Tensor

```python
horizon_plugin_pytorch.rgb2gray(input: torch.Tensor) → torch.Tensor
```

Convert color space.

Convert images from RGB format to gray**Parameters**

- **input** - input image in RGB format of shape [N, 3, H, W], ranging 0~255

**Returns**

gray image of shape [N, 1, H, W], ranging 0~255

**Return Type**

Tensor

```python
horizon_plugin_pytorch.rgb2yuv(input: torch.Tensor, swing: str = 'studio') → torch.Tensor
```

Convert color space.

Convert images from RGB format to YUV444 BT.601

**Parameters**

- **input** - input image in RGB format, ranging 0~255

- **swing** - “studio” for YUV studio swing (Y: 16~235, U, V: 16~240). “full” for YUV full swing (Y, U, V: 0~255). default is “studio”

**Returns**

YUV image

**Return Type**

Tensor

## Model compilation

```python
horizon_plugin_pytorch.quantization.check_model(module: Union[torch.jit._script.ScriptModule, torch.nn.modules.module.Module], example_inputs: tuple, march: Optional[str] = None, input_source: Union[Sequence[str], str] = 'ddr', advice: Optional[int] = None, check_quanti_param: bool = True)
```

Check if nn.Module or jit.ScriptModule can be compiled by HBDK.

Dump advices for improving performance on BPU.

**Parameters**

- **module** (nn.Module or jit.ScriptModule.) -

- **example_inputs** (A tuple of example inputs, in torch.tensor format.) – For jit.trace and shape inference.- **march** (指定bpu的目标march) - 有效的选项有bayes和bernoulli2。如果未提供，则使用horizon插件的全局march。

- **input_source** (指定输入特征的来源(ddr/resizer/pyramid)) -

- **advice** (如果模型的层变慢超过指定的时间（以微秒为单位），打印HBDK编译器提供的用于提高bpu上模型利用率的建议) -

- **check_quanti_param** (检查量化参数) -

**Returns**

标志 - 如果通过，则为0，否则不通过。

**Return type**

整数

```python
horizon_plugin_pytorch.quantization.compile_model(module: Union[torch.jit._script.ScriptModule, torch.nn.modules.module.Module], example_inputs: tuple, hbm: str, march: Optional[str] = None, name: Optional[str] = None, input_source: Union[Sequence[str], str] = 'ddr', input_layout: Optional[str] = None, output_layout: str = 'NCHW', opt: Union[str, int] = 'O2', balance_factor: int = 2, progressbar: bool = True, jobs: int = 16, debug: bool = True, extra_args: Optional[list] = None)
```

编译nn.Module或jit.ScriptModule。

**Parameters**

- **module** (nn.Module或jit.ScriptModule） -

- **example_inputs** （示例输入的元组，以torch.tensor格式） - 用于jit.trace和形状推断。

- **hbm** （指定hbdk-cc的输出路径） -

- **march** (指定bpu的目标march） - 有效的选项有bayes和bernoulli2。如果未提供，则使用horizon插件的全局march。

- **name** （模型的名称，记录在hbm中） - 可以通过运行时的hbdk-disas或hbrtGetModelNamesInHBM获得。

- **input_source** (指定输入特征的来源(ddr/resizer/pyramid)) -

- **input_layout** (指定所有模型输入的输入布局) - 可用的布局为NHWC、NCHW、BPU_RAW。

- **output_layout** (指定所有模型输入的输出布局) - 可用的布局为NHWC、NCHW、BPU_RAW。

- **opt** (指定优化选项) - 可用的选项为O0、O1、O2、O3、ddr、fast、balance。

- **balance_factor** (当优化选项为'balance'时指定平衡比例) -

- **progressbar** (显示编译进度以缓解焦虑) -

- **jobs** (指定在编译器优化期间启动的线程数) - 默认值为'16'。0表示使用所有可用的硬件并发性。

- **debug** (在hbm中启用调试信息) -- **extra_args**（指定在“hbdk-cc -h”中列出的额外参数。） - 格式为字符串列表：例如，['--ability-entry'，str(entry_value)，...]

**Returns**

flag - 如果通过，则为0，否则为否。

**Return Type**

int

```python
horizon_plugin_pytorch.quantization.export_hbir(module: Union[torch.jit._script.ScriptModule, torch.nn.modules.module.Module], example_inputs: tuple, hbir: str, march: Optional[str] = None)
```

将nn.Module或jit.ScriptModule导出为hbdk3.HBIR。

**Parameters**

- **module**（nn.Module或jit.ScriptModule。） -

- **example_inputs**（示例输入的元组，以torch.tensor格式。） - 用于jit.trace和形状推断。

- **hbir**（指定hbir的输出路径。） -

- **march**（指定导出hbir的march。） - 有效选项为bayes和bernoulli2。如果未提供，则使用horizon插件全局march。

**Returns**
**Return Type**

输入名称和输出名称

```python
horizon_plugin_pytorch.quantization.perf_model(module: Union[torch.jit._script.ScriptModule, torch.nn.modules.module.Module], example_inputs: tuple, march: Optional[str] = None, out_dir: str = '.', name: Optional[str] = None, hbm: Optional[str] = None, input_source: Union[Sequence[str], str] = 'ddr', input_layout: Optional[str] = None, output_layout: str = 'NCHW', opt: Union[str, int] = 'O3', balance_factor: int = 2, progressbar: bool = True, jobs: int = 16, layer_details: bool = False, extra_args: Optional[list] = None)
```

估算nn.Module或jit.ScriptModule的性能。

**Parameters**

- **module**（nn.Module或jit.ScriptModule。） -

- **example_inputs**（示例输入的元组，以torch.tensor格式。） - 用于jit.trace和形状推断。

- **march**（指定bpu目标march。） - 有效选项为bayes和bernoulli2。如果未提供，则使用horizon插件全局march。

- **out_dir**（指定保存性能结果的输出目录。） -

- **name**（模型的名称，记录在hbm中。） - 可以通过运行时的hbdk-disas或hbrtGetModelNamesInHBM获得。

- **hbm**（指定hbdk-cc的输出路径。） -- **input_source** (指定输入特征的来源(ddr/resizer/pyramid)) –

- **input_layout** (指定模型所有输入的输入布局。) – 可用的布局为NHWC，NCHW，BPU_RAW。

- **output_layout** (指定模型所有输出的输出布局。) – 可用的布局为NHWC，NCHW，BPU_RAW。

- **opt** (指定优化选项。) – 可用的选项有O0，O1，O2，O3，ddr，fast，balance。

- **balance_factor** (当优化选项为'balance'时，指定平衡比例。) –

- **progressbar** (显示编译进度以缓解焦虑。) –

- **jobs** (指定编译器优化期间启动的线程数。) – 默认为'16'。0表示使用所有可用的硬件并发。

- **layer_details** (显示层的性能详细信息。(仅供开发人员使用)) –

- **extra_args** (指定在"hbdk-cc -h"中列出的额外参数。) – 以字符串列表的格式: 例如 [’–ability-entry’, str(entry_value), …]

**返回**
**返回类型**

性能详细信息的json字典。或失败时的错误代码。

```python
horizon_plugin_pytorch.quantization.visualize_model(module: Union[torch.jit._script.ScriptModule, torch.nn.modules.module.Module], example_inputs: tuple, march: Optional[str] = None, save_path: Optional[str] = None, show: bool = True)
```

以HBDK的视角可视化nn.Module或jit.ScriptModule。

**参数**

- **module** (nn.Module或jit.ScriptModule。) –

- **example_inputs** (示例输入的元组，以torch.tensor格式。) – 用于jit.trace和形状推断。

- **march** (指定bpu的目标march。) – 有效选项为bayes和bernoulli2。如果未提供，则使用horizon plugin的全局march。

- **save_path** (指定保存绘图图像的路径。) –

- **show** (通过显示器显示绘制的图像。) – 确保X服务器的配置正确。

**返回**
**返回类型**

NonePlease translate the Chinese parts in the following content into English while keeping the original format and content: