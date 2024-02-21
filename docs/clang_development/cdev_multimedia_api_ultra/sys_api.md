---
sidebar_position: 6
---
# SYS (Module Binding) API

The `SYS` API provides the following interfaces:

| Function | Description |
| ---- | ----- |
| sp_module_bind | **Bind data source and target module** |
| sp_module_unbind | **Unbind modules** |

### sp_module_bind

**[Function Prototype]**

```int32_t sp_module_bind(void *src, int32_t src_type, void *dst, int32_t dst_type)```

**[Description]**

This interface allows for internal binding of the output and input of the `VIO`, `ENCODER`, `DECODER`, and `DISPLAY` modules. After the binding, the data from these two modules will flow internally automatically without the need for user operations. For example, after binding `VIO` and `DISPLAY`, the data from an open MIPI camera will be displayed directly on the screen without the need to call the `sp_vio_get_frame` interface to obtain the data and then call the `sp_display_set_image` interface of `DISPLAY` to display it.

The supported module bindings are as follows:

| Source Module | Target Module |
| ---- | ----- |
| VIO | ENCODER |
| VIO | DISPLAY |
| DECODER | ENCODER |
| DECODER | DISPLAY |

**[Parameters]**

- `src`: Pointer to the object of the data source module (obtained by calling the initialization interface of each module)
- `src_type`: Type of the source data module, supports `SP_MTYPE_VIO` and `SP_MTYPE_DECODER`
- `dst`: Pointer to the object of the target module (obtained by calling the initialization interface of each module)
- `dst_type`: Type of the target data module, supports `SP_MTYPE_ENCODER` and `SP_MTYPE_DISPLAY`

**[Return Type]**

Returns 0 if successful, otherwise returns another value.

### sp_module_unbind

**[Function Prototype]**

```int32_t sp_module_unbind(void *src, int32_t src_type, void *dst, int32_t dst_type)```

**[Description]**

This function unbinds the two modules.This interface completes the unbinding of two already bound modules. The unbinding process needs to be completed before the module exits.

**【Parameters】**

- `src`: Pointer to the object of the data source module (obtained by calling the initialization interface of each module).
- `src_type`: The type of the source data module, which supports `SP_MTYPE_VIO` and `SP_MTYPE_DECODER`.
- `dst`: Pointer to the object of the target module (obtained by calling the initialization interface of each module).
- `dst_type`: The type of the target data module, which supports `SP_MTYPE_ENCODER` and `SP_MTYPE_DISPLAY`.

**【Return Type】**

Successful: returns 0; unsuccessful: returns other values.