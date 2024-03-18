---
sidebar_position: 5
---
# BPU (Algorithm Inference Module) API

The `BPU` API provides the following interfaces:

| Function | Description |
| ---- | ----- |
| sp_init_bpu_module | **Initialize the algorithm inference module and create an inference task** |
| sp_bpu_start_predict | **Perform AI algorithm inference and get the inference result** |
| sp_release_bpu_module | **Close the inference task** |
| sp_init_bpu_tensors | **Allocate tensor memory** |
| sp_deinit_bpu_tensor | **Destroy tensor memory** |


## sp_init_bpu_module

**【Function Prototype】**

`bpu_module *sp_init_bpu_module(const char *model_file_name)`

**【Description】**

Open the algorithm model specified by `model_file_name` and initialize an algorithm inference task.

**【Parameters】**

- `model_file_name`: Algorithm model file, which needs to be converted by Horizon AI algorithm toolchain or trained fixed-point model.

**【Return Type】**

AI algorithm inference task object.

## sp_bpu_start_predict

**【Function Prototype】**

`int32_t sp_bpu_start_predict(bpu_module *bpu_handle, char *addr)`

**【Function Description】**

Passes in image data to complete AI algorithm inference and returns the algorithm result.

**【Parameters】**

- `bpu_handle`: Object for the AI inference task.
- `addr`: Input address of the image data.

**【Return Type】**

None.

## sp_init_bpu_tensors

**【Function Prototype】**

`int32_t sp_init_bpu_tensors(bpu_module *bpu_handle, hbDNNTensor *output_tensors)`

**【Function Description】**

Initializes and allocates memory for the passed-in `tensor`.

**【Parameters】**

- `bpu_handle`: Object for the AI inference task.
- `output_tensors`: Address of the `tensor`.

**【Return Type】**

None.

## sp_deinit_bpu_tensor 

**【函数原型】**  
`int32_t sp_deinit_bpu_tensor(hbDNNTensor *tensor, int32_t len)`

**【功能描述】**  
Release and reclaim memory for the input `tensor`.

**【参数】**
- `tensor`: Pointer to the `tensor`
- `len`: Length of the `tensor`

**【返回类型】**  
None.

## sp_release_bpu_module  

**【函数原型】**  
`int32_t sp_release_bpu_module(bpu_module *bpu_handle)`

**【功能描述】**  
Release the BPU module.

**【参数】**  
- `bpu_handle`: BPU module object

**【返回类型】**  
None.Turn off algorithm inference task.

**【Parameters】**

- `bpu_handle`: Algorithm inference task object.

**【Return Type】**

Return 0 if successful, -1 if failed.