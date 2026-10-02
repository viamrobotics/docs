Each `change` carries a `changeType` (one of `TransformChangeType.ADDED`, `.UPDATED`, `.REMOVED`, or `.UNSPECIFIED`) and an `updatedFields` field mask:

- For `ADDED`, `updatedFields` is `undefined`; use the whole transform.
- For `UPDATED`, `updatedFields.paths` lists the field paths that changed, so you can apply a partial update instead of replacing the whole transform.
- For `REMOVED`, `updatedFields.paths` holds the transform's UUID path.
