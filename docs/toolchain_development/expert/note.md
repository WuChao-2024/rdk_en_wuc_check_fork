# Appendix

## Eager Mode

Similar to PyTorch official recommendation, we suggest users to use fx quantization mode as the first choice. horizon_plugin_pytorch currently supports quantization with eager mode.
The overall process of eager mode follows the quantization interface and concept from PyTorch officially, therefore, it is recommended to first read the relevant part about eager mode in [**PyTorch official documentation**](https://pytorch.org/docs/stable/quantization.html#quantization).

### Difference with fx mode

When using eager mode in horizon_plugin_pytorch, the main differences compared with fx mode are:

- Eager mode only supports module-based operators. You need to manually replace the functional operators in the floating-point model with Module-based operators in PyTorch or proprietary operators defined in horizon_plugin_pytorch, including but not limited to:

| Floating-point operators | Replaced operators |
|--------------------------|--------------------|
| torch.nn.functional.relu | torch.nn.ReLU() |
| a + b <br/> torch.add | horizon.nn.quantized.FloatFunctional().add |
| Tensor.exp | horizon.nn.Exp() |
| torch.nn.functional.interpolate | horizon.nn.Interpolate() |

- You need to manually define the operators to be fused and explicitly call the fusion function, and specify to use `fuser_func` provided in horizon_plugin_pytorch. The example is shown below:

```python
import torch
from torch import nn
import horizon_plugin_pytorch as horizon


class ConvBNReLU(nn.Sequential):
    def __init__(self, in_channels, out_channels, kernel_size):
        super(ConvBNReLU, self).__init__(
            nn.Conv2d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size
            ),
            nn.BatchNorm2d(num_features=out_channels),
            nn.ReLU()
        )

    # Specify the operators that can be fused
    def fuse_model(self):
        torch.quantization.fuse_modules(
            self,
            ['0', '1', '2'],
            inplace=True,
```# Specify the fuse function provided by horizon_plugin_pytorch in the horizon_plugin_pytorch package
fuser_func=horizon.quantization.fuse_known_modules,
)

float_model = ConvBNReLU(1, 1, 1)
# Need to explicitly call the fuse function
float_model.fuse_model()

print(float_model)
# ConvBNReLU(
#   (0): ConvReLU2d(
#     (0): Conv2d(1, 1, kernel_size=(1, 1), stride=(1, 1))
#     (1): ReLU()
#   )
#   (1): Identity()
#   (2): Identity()
# )
```

### Usage Flow

The overall flow of quantization-aware training in Eager mode is shown in the following figure:

![qat](./image/expert/qat.svg)

#### Build Float Model

When building a float model in Eager mode, there are a few things to note:

1. Insert quantization and dequantization nodes in the network. Generally, a quantization node should be inserted at the beginning of the float model, and a dequantization node should be inserted at the end. When the float model is converted to a QAT model for quantization-aware training, the inserted quantization node will quantize the input;

2. Replace some float-type function-form operators with operators inherited from Module in PyTorch or some proprietary operators provided by the Plugin;

3. Define the fusion function for float operators to fuse eligible operators.

```python
import torch
import torch.optim as optim
import horizon_plugin_pytorch as horizon
import os
from torch import nn
from torchvision import datasets, transforms
from torch.quantization import DeQuantStub
from horizon_plugin_pytorch.quantization import QuantStub

class ConvBNReLU(nn.Sequential):
    def __init__(self, in_channels, out_channels, kernel_size):
        super(ConvBNReLU, self).__init__(
            nn.Conv2d(
            in_channels=in_channels,
```in_channels = in_channels,
            out_channels = out_channels,
            kernel_size = kernel_size
            ),
            nn.BatchNorm2d(num_features=out_channels),
            nn.ReLU()
        )

    # Specify the floating point operators that can be fused
    def fuse_model(self):
        torch.quantization.fuse_modules(
            self,
            ['0', '1', '2'],
            inplace=True,
            fuser_func=horizon.quantization.fuse_known_modules,
        )

class ClassiFier(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(ClassiFier, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, 1)

    def forward(self, data):
        return self.conv(data)

# Build the floating point model
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv0 = ConvBNReLU(1, 10, 5)
        self.max_pool = nn.MaxPool2d(kernel_size=2)
        self.conv1 = ConvBNReLU(10, 20, 5)
        self.avg_pool = nn.AvgPool2d(kernel_size=8)
        self.classifier = ClassiFier(20, 10)
        # To adapt to the BPU, when getting input from the camera, the scale of the QuantStub must be set to 1/128 explicitly.
        self.quant = QuantStub(scale=1/128)
        self.dequant = DeQuantStub()

    def forward(self, x):
        # Insert quantization node to quantize the input
        x = self.quant(x)
        x = self.conv0(x)
        x = self.max_pool(x)
        x = self.conv1(x)
        x = self.avg_pool(x)
        x = self.classifier(x)
        # Insert dequantization node to dequantize the output
        x = self.dequant(x)
        return x

    # Define the fusion function```python
def fuse_model(self):
    from horizon_plugin_pytorch import quantization

    for m in self.modules():
        if type(m) == ConvBNReLU:
            m.fuse_model()
```

#### Float Model Pretraining {#float-model-pretrain}

```python
train_batch_size = 16
test_batch_size = 16
epoch_num = 1
neval_batches = 1
model_file = 'model.pt'

class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self, name, fmt=":f"):
        self.name = name
        self.fmt = fmt
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

    def __str__(self):
        fmtstr = "{name} {val" + self.fmt + "} ({avg" + self.fmt + "})"
        return fmtstr.format(**self.__dict__)

criterion = nn.CrossEntropyLoss()

def accuracy(output, target, topk=(1,)):
    """Computes the accuracy over the k top predictions for the specified
    values of k
    """
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)
```        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res


def get_train_data_loader():
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST(
            'mnist_data',
            train=True,
            download=True,
            transform=transforms.Compose(
                [transforms.ToTensor(),
                 transforms.Normalize((0.5,), (0.5,))]
            )
        ),
        batch_size=train_batch_size,
        shuffle=True,
    )
    return train_loader

def get_test_data_loader():
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST(
            'mnist_data',
            train=False,
            download=True,
            transform=transforms.Compose(
                [transforms.ToTensor(),
                 transforms.Normalize((0.5,), (0.5,))]
            )
        ),
        batch_size=test_batch_size,
        shuffle=True,
    )
    return train_loader

data_loader = get_train_data_loader()
test_loader = get_test_data_loader()

def train(model, device, optimizer, epoch):
    global min_loss
    model.train()for batch_idx, (data, target) in enumerate(data_loader):
    # Move the data to the device
    data = data.to(device)
    target = target.to(device)

    # Forward pass
    output = model(data)
    output = output.view(-1, 10)

    # Calculate loss
    loss = criterion(output, target)

    # Zero the gradients
    optimizer.zero_grad()

    # Backward pass
    loss.backward()

    # Update weights
    optimizer.step()

    if batch_idx % 100 == 0:
        # Print training progress
        print('Train Epoch: {} batch {} \t Loss: {:.6f}'.format(epoch, batch_idx, loss.item()))


def evaluate(model, device, neval_batches):
    model.eval()

    # Initialize accuracy meters
    top1 = AverageMeter("Acc@1", ":6.2f")
    top5 = AverageMeter("Acc@5", ":6.2f")

    tested_batches = 0

    with torch.no_grad():
        for batch_idx, (data, target) in enumerate(test_loader):
            tested_batches += 1

            # Move the data to the device
            data = data.to(device)
            target = target.to(device)

            # Forward pass
            output = model(data)
            output = output.view(-1, 10)

            # Calculate loss
            loss = criterion(output, target)

            # Calculate accuracy
            acc1, acc5 = accuracy(output, target, topk=(1, 5))

            # Update accuracy meters
            top1.update(acc1[0], data.size(0))
            top5.update(acc5[0], data.size(0))

            if tested_batches >= neval_batches:
                return top1, top5

    return top1, top5


def train_float_model(device):
    # Create model
    model = Net().to(device)

    # Create optimizer
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.1)

    for nepoch in range(epoch_num):
        # Train the model
        train(model, device, optimizer, nepoch)

        # Evaluate the model
        top1, top5 = evaluate(model, device, neval_batches)

        # Print evaluation accuracy
        print("float training Epoch %d :float evaluation accuracy on %d images, %2.2f" % (nepoch, neval_batches * test_batch_size, top1.avg))

    # Save the trained model
    torch.save(model.state_dict(), model_file)

# Start training the model using GPU
train_float_model(torch.device('cuda'))If you want to perform quantization training on an existing floating-point model, you can first load the floating-point model and then proceed with the subsequent steps of fusion operators and quantization training. If you want to perform quantization training right after floating-point training, you don't need to load the model intentionally, just proceed with the subsequent steps.

```python
def load_model():
    model = Net()
    state_dict = torch.load(model_file)
    model.load_state_dict(state_dict)
    model.to('cpu')
    return model

qat_model = load_model()
```

#### Set BPU architecture {#set-bpu}

```python
# Set march to BERNOULLI2 for **RDK X3** and BAYES for **RDK Ultra**.
horizon.march.set_march(horizon.march.March.BAYES)
```

#### Operator fusion {#op-fuse}

```python
qat_model.fuse_model()
```

#### Convert floating-point model to quantized model {#float-to-quantized}

```python
def load_and_prepare_qat_model(device):
    # Load pre-trained floating-point model
    global qat_model
    qat_model = qat_model.to(device)
    top1, top5 = evaluate(qat_model, device, neval_batches)
    print(
        "float evaluation accuracy on %d images, \
        %2.2f" % (neval_batches * test_batch_size, top1.avg)
    )
    # Set the quantization parameters for quantizing the weights and outputs of operators
    qat_model.qconfig = horizon.quantization.get_default_qat_qconfig()
    # Turn off quantization for the output layer to improve accuracy
    qat_model.classifier.qconfig = \
        horizon.quantization.get_default_qat_out_qconfig()
    # Convert the floating-point model to quantized model
    horizon.quantization.prepare_qat(qat_model, inplace=True)
    print(
        "After preparation for QAT, note fake-quantization modules \n",
        qat_model.conv0,
    )
    qat_model = qat_model.to(device)
```load_and_prepare_qat_model(torch.device('cuda'))
```python
def quantization_training(device):
    # Quantization training for the quantized model
    optimizer = optim.SGD(qat_model.parameters(), lr=0.0001)
    for nepoch in range(1):
        train(qat_model, device, optimizer, nepoch)
        # Evaluate the quantized model for one epoch
        top1, top5 = evaluate(qat_model, device, neval_batches)
        print(
            "QAT Epoch %d :float evaluation accuracy on %d images, %2.2f"
            % (nepoch, neval_batches * test_batch_size, top1.avg)
        )

quantization_training(torch.device('cuda'))
```

#### Convert Quantized Model to Fixed-point Model

```python
quantized_model = horizon.quantization.convert(
    qat_model.eval(), inplace=False
)
```

#### Check and Compile the Fixed-point Prediction Model

```python
def compile_quantized_model(device):
    example_input = torch.ones(size=(neval_batches, 1, 28, 28), device=device)
    traced_model = torch.jit.trace(quantized_model, example_input)
    top1, top5 = evaluate(traced_model, device, neval_batches)
    print(
        "Traced : int evaluation accuracy on %d images, %2.2f"
        % (neval_batches * test_batch_size, top1.avg)
    )

    # Check if the model can be compiled using hbdk. hbdk is a tool for compiling fixed-point models.
    horizon.quantization.check_model(quantized_model, example_input, advice=1)
    hbdk_dir = "hbdk_model"
    if not os.path.exists(hbdk_dir):
        os.mkdir(hbdk_dir)

    # Compile the model, and the model.hbm in the hbdk_model directory is the compiled on-board model.
    horizon.quantization.compile_model(traced_model, [example_input], opt=2, hbm=hbdk_dir + "/model.hbm"
)
# Static performance analysis of the model
horizon.quantization.perf_model(
    traced_model,
    [example_input],
    opt=2,
    input_source=["pyramid"],
    layer_details=True,
    out_dir=hbdk_dir,
)
horizon.quantization.visualize_model(
    traced_model,
    [example_input],
    save_path=hbdk_dir + "/model.svg",
    show=False,
)

compile_quantized_model(torch.device('cuda'))
```



## Supported General Operators

### Overall Explanation

1. Unless otherwise specified, the inputs and outputs of Bernoulli2 architecture-constrained operators are all 4-dimensional.
2. In eager mode, some operators need to be manually replaced, while fx mode does not need to replace operators manually.
3. By default, the supported operators do not perform operator fusion. For operators that can be fused (such as (conv, bn), relu), refer to the [**Operator Fusion**](./advanced_content.md#op_fusion) section.
4. In the inference phase, transparent operators (such as Identity, Dropout) will be optimized out during deployment.

### torch function class


| Operator   | Eager mode equivalent operator | Bernoulli2 | Input | Output | Bayes | Output | Other constraints |
|------------|-------------------------------|-----------------|------------|-----------|-------------|----------|-----------------|
|            |                               |   Input         |	 Output |	Other constraints|   Input     |	Output  | Other constraints |
|torch.abs   |                               | Not supported  |        |          |qint8, qint16 | Same as input |                 |
|torch.acos  |horizon.nn.Acos	             | Not supported  |        |          |qint8, qint16	|qint8, qint16|	Implementation using a lookup table, with accuracy risks|
|torch.acosh |	horizon.nn.Acosh             |	Not supported  |       |           |Refer to torch.acos|           |                  |
|torch.add    | torch.nn.quantized.FloatFunctional or horizon.nn.quantized.FloatFunctional  |	qint8, qint16| qint8, qint16| in_channel<=2048, not supported for operands as constants |qint8, qint16|qint8, qint16| Supports broadcasting except for N dimensions, only one input can be broadcasted, call add_scalar if one of the operands is a scalar|
|torch.argmax|		            |Refer to torch.max     |	    |   		|Refer to torch.max	|           |	|
|torch.argmin|		            |Refer to torch.max		|	    |           |Refer to torch.max	|           |	|
|torch.asin	| horizon.nn.Asin	|   Not supported          |       |           | Refer to torch.acos|  | |
|torch.asinh	|horizon.nn.Asinh	|Not supported| | |Refer to torch.acos| | |
|torch.atan|	horizon.nn.Atan|	Not supported| | |Refer to torch.acos| | |
|torch.atanh|	horizon.nn.Atanh|	Not supported| | |Refer to torch.acos| | |
| torch.cat | torch.nn.quantized.FloatFunctional or horizon.nn.quantized.FloatFunctional | qint8, qint16 | qint8, qint16 |  |qint8, qint16 | qint8, qint16 | input shape: [N, C, H, W], N<=4096, HWC<=65536, 2<=input number<=1024 |
| torch.ceil | horizon.nn.Ceil | Not supported |  | | qint8, qint16 | Same as input |Do not exceed the level of 1e6 for int8 input and the level of 1e8 for int16 input. || Function                | Replaced by            | Input Types                    | Output Types       | Other Constraints                                                                                                                                                                                                                                                        |
|-------------------------|-----------------------|--------------------------------|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| torch.nn.functional.grid_sample             |                        | 不支持                            | 不支持                      | 不支持                                                                                                                                                                                                                                                                   |
| torch.nn.functional.interpolate              |                         | qint8                            | qint8               | 支持 nearest 和 billinear 插值模式。1/256<缩放比例<=256。                                                                                                                                    |
| torch.nn.functional.pad                                   |                         | 不支持                            | 不支持                      | 不支持 reflect 模式                                                                                                                                                                                                                                               |
| torch.nn.functional.relu                                 | torch.nn.ReLU        | qint8                          | qint8               | Conv2d+BN+ReLU 这种模式会自动 fuse                                                                                                                                                                                                                 |
| torch.nn.functional.relu6(fused)                  | torch.nn.ReLU6      |                                      |                             |                                                                                                                                                                                                                                                                                     |

### torch.nn Module 类

|    算子    | eager 模式替换算子  |	Bernoulli2   |       |           |    Bayes    |          |                 |
|------------|--------------------|-----------------|-------|-----------|-------------|----------|-----------------|
|            |                    |    输入         |	输出 |	 其它限制|	   输入     |	输出   |	其它限制      |
|torch.nn.AdaptiveAvgPool2d | |不支持 |不支持 |不支持 |qint8 |同输入 |使用 AvgPool2d 非等价拼凑，有精度问题 |
|torch.nn.AvgPool2d | |qint8 |同输入 |1<=kernel<=7，1<=stride<=185 | | |1<=kernel, stride, padding<=256; |
|torch.nn.BatchNorm2d | | | |BatchNorm2d 在 QAT 阶段被吸收，不体现在预测模型中。由于编译器限制，独立使用的 BatchNorm2d 底层调用 BpuConvolution 实现 |qint8 |qint8 |BatchNorm2d 在 QAT 阶段被吸收，因此，不体现在模型中。独立使用限制参考 Conv2d |
|torch.nn.BatchNorm3d | | | |BatchNorm3d 在 QAT 阶段被吸收，不体现在预测模型中。由于编译器限制，独立使用的 BatchNorm3d 底层调用 BpuConvolution 实现 |qint8 |qint8 |BatchNorm3d 在 QAT 阶段被吸收，因此，不体现在模型中。独立使用限制参考 Conv2d |
|torch.nn.ChannelShuffle | |qint8 |同输入 | |qint8, qint16 |同输入 |shuffle_index 中的数值不能重复 |
|torch.nn.ConstantPad2d | |参考 torch.nn.ZeroPad2d |参考 torch.nn.ZeroPad2d | |参考 torch.nn.ZeroPad2d |参考 torch.nn.ZeroPad2d | |
|torch.nn.Conv2d | |qint8 |qint8，qint32 | |input: qint8, qint16； weight: qint8； bias: qint32 |qint8, qint16,qint32 |out_channel<=8192，作为模型输出时，out_channel <= 16384. 输入 channel<=8192, kernel<32, dilation<=16, 当 dilation!=1 时，stride 只能 为 1. 支持 sumin, 带 sumin 的 conv 只支持 stride 为 (1, 1) 或 (2, 2). weight_shape: [N, C, H, W], N, C<=8192, H, W<=31, 作为模型输出 C<=16384, weight_size < 65535. padding<=256 qint16 输入时累加和不能超过 int32 范围 |
|torch.nn.Conv3d | |不支持 |不支持 |不支持 |input: qint8, weight: qint8， bias: qint32 |qint8 |input: [N, C, D, H, W] int8, N<=128; H, W, D, C<=65536; weight: [C_o, C_i, D, H, W] int8, N, C<=65536, D, H<=9, W<=8191; bias: int32; output: [N, C, D, H, W] int8, int16, int32; stride: [D, H, W], D, H, W 等于 1 或 2, 并且 D, H, W 相同; padding: [D, H, W], D<=kernel_d/2, H<=kernel_h/2, W<=kernel_w/2(kernel_w 指 weight W 维大小) group, dilation: 暂不支持 |
|torch.nn.ConvTranspose2d | |qint8 |qint8 |2<=kernel<= 14.channel<=2048. padding H*W=[0, (kernel_h-1)/2] * [0, (kernel_w-1)/2] 2<=stride<=4, dilation=(1, 1) |qint8 |qint8 |输入 shape: [N, C, H, W], 1<=N<=128, 1<=channel<=2048; weight_shape: [N, C, H, W], 1<=N, C<=2048, 2<=H, W<=14, weight_size<=65535; kernel>=stride, 1<=stride<=14, 1<=out_channel<=2048, in_channel<=2048 pad<=kernel/stride, 0<=out_pad<=1; bias 类型为 int32; 支持 sumin, sumin 输入类型为 int8; 0<=output_padding<=1; 支持 group, 要求 weight_n 和 输入 channel 均能被 group 整除; dilation=1 |
|torch.nn.Dropout | |qint8, qint16，qint32 |同输入 | |qint8, qint16，qint32 |同输入 | |
|torch.nn.Dropout2d | |qint8, qint16，qint32 |同输入 | |qint8, qint16，qint32 |同输入 | |
|torch.nn.ELU | |不支持 |不支持 |不支持 |参考 torch.acos |参考 torch.acos | |
|torch.nn.GELU | |参考 torch.exp |参考 torch.exp |参考 torch.exp |参考 torch.acos |参考 torch.acos | |
|torch.nn.GLU | |不支持 |不支持 | |参考 torch.acos |参考 torch.acos | |
|torch.nn.HardSigmoid | |不支持 |不支持 |不支持 |参考 torch.acos |参考 torch.acos | |
|torch.nn.Identity | |qint8, qint16，qint32 |同输入 | |qint8, qint16，qint32 |同输入 | |
|torch.nn.Layernorm | |不支持 |不支持 |不支持 |qint8 |qint8, qint16 |底层使用多次查表拼凑，精度风险较高。可通过 rsqrt_kwargs 属性来控制内部 rsqrt 查表的参数，若遇到 convert 精度降低的问题可以尝试 layernorm_op.rsqrt_kwargs = {“auto_divide_strategy”: “curvature”}. H * W <= 16384, normalized_shape H * W < 16384 |
|torch.nn.LeakyReLU | |不支持 |不支持 |不支持 |参考 torch.acos |参考 torch.acos | |
|torch.nn.Linear | |不支持 |不支持 |不支持 |input: qint8； weight:qint8； bias: qint32 |qint8 |in_features <= 8192, out_features <= 8192. |
|torch.nn.LSTMCell | |不支持 |不支持 |不支持 |qint8, qint16 |qint8, qint16 |输入是 2 维 |
|torch.nn.MaxPool2d | |qint8 |同输入 |1<=kernel<=64, 1<=stride<=256, padding>=0 |qint8 |同输入 |input_shape: [N, C, H, W], 1<=H, W, C<=8192;1<=kernel, stride<=256; 0<=padding<=255; |
|torch.nn.MultiheadAttention | |不支持 |不支持 |不支持 |qint8,qint16 |qint8,qint16 |不支持 add_bias_kv、add_zero_attn 和 q k v embed_dim 不一致的情况，支持输入输出 int8/int16，底层查表算子与 mask 量化可能带来精度风险 |
|torch.nn.PixelShuffle | |qint8, qint16 |同输入 | |qint8,qint16 |同输入 | |
|torch.nn.PixelUnshuffle | |qint8, qint16 |同输入 | |qint8,qint16 |同输入 | |
|torch.nn.PReLU | |不支持 |不支持 |不支持 |参考 torch.acos |参考 torch.acos | |
|torch.nn.ReLU | |qint8 |同输入 | |qint8,qint16 |同输入 | |
|torch.nn.ReLU6 | |qint8 |同输入 | |qint8,qint16 |同输入 | |
|torch.nn.ReplicationPad2d | |参考 torch.nn.ZeroPad2d |参考 torch.nn.ZeroPad2d |参考 torch.nn.ZeroPad2d |参考 torch.nn.ZeroPad2d |参考 torch.nn.ZeroPad2d | |
|torch.nn.Sigmoid | |参考 torch.exp |参考 torch.exp |参考 torch.exp |参考 torch.acos |参考 torch.acos | |
|torch.nn.SiLU | |参考 torch.exp |参考 torch.exp |参考 torch.exp |参考 torch.acos |参考 torch.acos | |
|torch.nn.Softmax | |不支持 |不支持 |不支持 |qint8 |qint8, qint16 |使用多次查表、求和等算子拼凑，精度风险较高 |
|torch.nn.Softplus | |不支持 |不支持 |不支持 |参考 torch.acos |参考 torch.acos | |
|torch.nn.SyncBatchNorm | |qint8 |qint8 |使用 torch.nn.Conv2d 拼凑 |qint8 |qint8 |使用 torch.nn.Conv2d 拼凑 |
|torch.nn.Tanh | |参考 torch.exp |参考 torch.exp |参考 torch.exp |参考 torch.acos |参考 torch.acos |参考 torch.acos |
|torch.nn.Upsample | |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |
|torch.nn.UpsamplingBilinear2d | |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |
|torch.nn.UpsamplingNearest2d | |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |参考 torch.nn.functional.interpolate |
|torch.nn.ZeroPad2d | |qint8 |同输入 | |qint8, qint16 |同输入 | |

### torch.quantization Module 类

|    算子    | eager 模式替换算子  |	Bernoulli2   |       |           |    Bayes    |          |                 |
|------------|--------------------|-----------------|-------|-----------|-------------|----------|-----------------|
|            |                    |    输入         |	输出 |	 其它限制|	   输入     |	输出   |	其它限制      |
|torch.quantization.DeQuantStub | |qint8,qint16,qint32 |float32 |典型使用场景：网络模型分段的场景，需要把数据 从 BPU 传输到 CPU，在 CPU 上进行反量化，方便 CPU 上处理 |qint8,qint16,qint32 |float32 |典型使用场景：网络模型分段的场景，需要把数据 从 BPU 传输到 CPU，在 CPU 上进行反量化，方便 CPU 上处理 |
|    Operator    | Eager mode replacement |    Input   |    Output   |   Other Constraints  |    Input   |   Output   |   Other Constraints  |
|----------------|-----------------------|------------|-------------|----------------------|------------|------------|----------------------|
|torch.Tensor.__getitem__ |                      |qint8, qint16, qint32 | Same as input |                     |            |            |                      |
|torch.Tensor.transpose |                       |Not supported         |Not supported   |Not supported        |qint8, qint16, qint32 |Tensor.dtype |Not supported for N-dimensional transpose |
|torch.Tensor.argmax |                           |Refer to torch.max |Refer to torch.max |Refer to torch.max |Refer to torch.max |Refer to torch.max |Refer to torch.max |
|torch.Tensor.argmin |                           |Refer to torch.max |Refer to torch.max |Refer to torch.max |Refer to torch.max |Refer to torch.max |Refer to torch.max |
|torch.Tensor.clamp |                             |Not supported         |Not supported   |Not supported       |qint8, qint16 |Tensor.dtype |dim <= 10, 1 <= each_dim_size < 65536 |
|torch.Tensor.clip |                               |Not supported         |Not supported   |Not supported       |Refer to torch.Tensor.clip |Refer to torch.Tensor.clip |Refer to torch.Tensor.clip |
|torch.Tensor.eq |                                 |Not supported         |Not supported   |Not supported       |Refer to torch.eq |Refer to torch.eq |Refer to torch.eq |
|torch.Tensor.expand |                            |Not supported         |Not supported   |Not supported       |qint8, qint16 |Tensor.dtype | |
|torch.Tensor.ge |                                 |Not supported         |Not supported   |Not supported       |Refer to torch.eq |Refer to torch.eq |Refer to torch.eq |
|torch.Tensor.greater |                           |Not supported         |Not supported  |Not supported        |Refer to torch.eq |Refer to torch.eq |Refer to torch.eq |
|torch.Tensor.greater_equal |                      |Not supported         |Not supported  |Not supported        |Refer to torch.eq |Refer to torch.eq |Refer to torch.eq |
|torch.Tensor.gt |                                 |Not supported         |Not supported  |Not supported        |Refer to torch.eq |Refer to torch.eq |Refer to torch.eq |
|torch.Tensor.le |                                 |Not supported         |Not supported  |Not supported        |Refer to torch.eq |Refer to torch.eq |Refer to torch.eq |
|torch.Tensor.less |                               |Not supported         |Not supported  |Not supported        |Refer to torch.eq |Refer to torch.eq |Refer to torch.eq |
|torch.Tensor.less_equal |                          |Not supported         |Not supported  |Not supported        |Refer to torch.eq |Refer to torch.eq |Refer to torch.eq |
|torch.Tensor.max |                                |Not supported         |Not supported  |Not supported        |Refer to torch.max |Refer to torch.max |Refer to torch.max |
|torch.Tensor.min |                                |Not supported         |Not supported  |Not supported        |Refer to torch.max |              |                      |
|torch.Tensor.repeat |                             |Not supported         |Not supported  |Not supported        |qint8, qint16 |Tensor.dtype | |
|torch.Tensor.reshape |                            |Not supported         |Not supported  |Not supported        |                 |Tensor.dtype | |
|torch.Tensor.tile |                               |Not supported         |Not supported  |Not supported        |qint8, qint16 |Tensor.dtype | |


### torchvision class

|    Operator    | Eager mode replacement |    Input   |    Output   |   Other Constraints  |    Input   |   Output   |   Other Constraints  |
|----------------|-----------------------|------------|-------------|----------------------|------------|------------|----------------------|
|torchvision.models.detection.rpn.AnchorGenerator |  horizon.nn.AnchorGenerator |qint8, qint16, qint32, float32 |float32 |Supports cases where Tensor.shape can be determined offline |qint8, qint16, qint32, float32 |float32 |Supports input int8/int16/int32/float32, output float32 |
|torchvision.ops.MultiScaleRoIAlign |	horizon.nn.MultiScaleRoIAlign |Refer to torchvision.ops.RoIAlign |Refer to torchvision.ops.RoIAlign |Refer to torchvision.ops.RoIAlign |Refer to torchvision.ops.RoIAlign |Refer to torchvision.ops.RoIAlign |Refer to torchvision.ops.RoIAlign |
|torchvision.ops.RoIAlign | |qint8 |qint8 | |qint8 |qint8 |1<=feature number<=5; bbox supports List[Tensor] format with shape:[1, box_num, 4], where the last dimension of bbox represents: [left, top, right, bottom] |