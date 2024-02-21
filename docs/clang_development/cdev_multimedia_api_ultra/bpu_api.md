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

**[Function Prototype]**

`bpu_module *sp_init_bpu_module(const char *model_file_name)`

**[Description]**

Open the algorithm model specified by `model_file_name` and initialize an inference task.

**[Parameters]**

- `model_file_name`: The algorithm model file, which needs to be converted by Horizon AI algorithm toolchain or trained to obtain a fixed-point model.

**[Return Type]**

AI algorithm inference task object.

## sp_bpu_start_predict

**[Function Prototype]**

`int32_t sp_bpu_start_predict(bpu_module *bpu_handle, char *addr)`

**[Description]**

Pass in the image data to complete AI algorithm inference and return the algorithm result.

**[Parameters]**

- `bpu_handle`: The algorithm inference task object.
- `addr`: Input image data.
```## sp_release_bpu_module  

**【Function Prototype】**  

`int32_t sp_release_bpu_module(bpu_module *bpu_handle)`

**【Description】**  
Release the BPU module and free the memory.

**【Parameters】**

- `bpu_handle`: The handle of the inference task object.

**【Return Type】** 

None.Turn off algorithm inference task.

**【Parameters】**

- `bpu_handle`: Algorithm inference task object

**【Return Type】**

Returns 0 on success, -1 on failure.