Each `TransformChange` carries a `ChangeType` (one of `pb.TransformChangeType_TRANSFORM_CHANGE_TYPE_ADDED`, `_UPDATED`, `_REMOVED`, or `_UNSPECIFIED`) and an `UpdatedFields []string`:

- For an added transform, `UpdatedFields` is empty; use the whole transform.
- For an updated transform, `UpdatedFields` lists the field paths that changed, so you can apply a partial update instead of replacing the whole transform.
- For a removed transform, `UpdatedFields` holds the transform's UUID path.

`StreamTransformChanges` returns a `*TransformChangeStream`, not a channel: call `Next()` repeatedly until it returns `io.EOF`, as shown above.
