Each `change` carries a `change_type` (one of `TRANSFORM_CHANGE_TYPE_ADDED`, `TRANSFORM_CHANGE_TYPE_UPDATED`, `TRANSFORM_CHANGE_TYPE_REMOVED`, or `TRANSFORM_CHANGE_TYPE_UNSPECIFIED` from `viam.proto.service.worldstatestore`) and an `updated_fields` field mask:

- For `TRANSFORM_CHANGE_TYPE_ADDED`, `updated_fields` is empty; use the whole transform.
- For `TRANSFORM_CHANGE_TYPE_UPDATED`, `updated_fields.paths` lists the field paths that changed, so you can apply a partial update instead of replacing the whole transform.
- For `TRANSFORM_CHANGE_TYPE_REMOVED`, `updated_fields.paths` holds the transform's UUID path.
