---
sidebar_position: 5
---
# BPU (Algorithm Inference Module) API

The `BPU` API provides the following interfaces:

| Function | Description |
| ---- | ----- |
| sp_init_bpu_module | **Initialize the algorithm inference module object and create an inference task** |
| sp_bpu_start_predict | **Perform AI algorithm inference and obtain the inference result** |
| sp_release_bpu_module | **Close the inference task of the algorithm** |
| sp_init_bpu_tensors | **Allocate tensor memory** |
| sp_deinit_bpu_tensor | **Destroy tensor memory** |

## sp_init_bpu_module

**【Function Prototype】**

`bpu_module *sp_init_bpu_module(const char *model_file_name)`

**【Description】**

Open the algorithm model specified by `model_file_name` and initialize an inference task.

**【Parameters】**

- `model_file_name`: The algorithm model file, which needs to be converted by Horizon AI algorithm toolchain or trained to obtain a fixed-point model.

**【Return Type】**

AI algorithm inference task object.

## sp_bpu_start_predict

**【Function Prototype】**

`int32_t sp_bpu_start_predict(bpu_module *bpu_handle, char *addr)`

**【Function Description】**

Inputs image data to complete AI algorithm inference and returns the algorithm results.

**【Parameters】**

- `bpu_handle`: Object of the algorithm inference task
- `addr`: Input for image data

**【Return Type】**

None.


## sp_init_bpu_tensors

**【Function Prototype】**

`int32_t sp_init_bpu_tensors(bpu_module *bpu_handle, hbDNNTensor *output_tensors)`

**【Function Description】**

Initializes and allocates memory for the input `tensor`.

**【Parameters】**

- `bpu_handle`: Object of the algorithm inference task
- `output_tensors`: Address of the `tensor`

**【Return Type】**

None.


## sp_deinit_bpu_tensor

**【Function Prototype】**

`int32_t sp_deinit_bpu_tensor(hbDNNTensor *tensor, int32_t len)`

**【Function Description】**

Releases and recycles memory for the input `tensor`.

**【Parameters】**

- `tensor`: Pointer to the `tensor` to be released
- `len`: Length or size of the `tensor` (apparent inconsistency with parameter name)

**【Return Type】**

None.


## sp_release_bpu_module

**【Function Prototype】**

`int32_t sp_release_bpu_module(bpu_module *bpu_handle)`

**【Function Description】**

Closes the algorithm inference task.

**【Parameters】**

- `bpu_handle`: Object of the algorithm inference task

**【Return Type】**

Returns 0 on success, -1 on failure.
