Set individual properties in a machine {{< glossary_tooltip term_id="part" text="part" >}}'s configuration by path, without replacing the whole configuration as [`UpdateRobotPart`](#updaterobotpart) does.

Paths are dot-separated, such as `network.bind_address`.
In `components`, `services`, `jobs`, `remotes`, `triggers`, `modules`, and `packages`, the second segment names the resource by name or ID, such as `components.my-camera.attributes.width_px`.
In `fragments` and `fragment_mods`, the second segment is the fragment ID, such as `fragments.<fragment-id>.version`.
If the part imports the same fragment more than once, name one import in `fragments` as `<fragment-id>@<prefix>`. Without a prefix, the path names the import that has no prefix, and returns an error if every import has one. A fragment mod applies to every import of its fragment, so `fragment_mods` paths can't name a prefix.
Fragment imports and fragment mods are always set in the part's own configuration, even if a fragment the part imports also imports that fragment.

**Where a change is saved:**

- If the property is in a resource or section that the part's own configuration defines, the change is made there. A property that isn't set yet is added.
- If the resource comes from a fragment the part imports, the change is saved through that fragment, even if the fragment doesn't set that property yet:
  - If the fragment sets the property with a [fragment variable](/fleet/reuse-configuration/#customize-fragments-with-variables) that no other property uses, the change sets the variable's value on the part's fragment import.
  - Otherwise, including when other properties share the variable, the change is saved as a `$set` [fragment override](/fleet/reuse-configuration/#override-specific-settings) for the last fragment that provides the resource.

**Limits and errors:**

- Changes apply in order, and each change succeeds or fails on its own. The result for each change reports whether it succeeded and, if not, the error.
- You can send at most 100 changes per request.
- Replacing a whole resource that comes from a fragment the part imports more than once returns an error. Set the resource's fields instead.
- If `fragment_mods` has more than one entry for the same fragment ID, setting a path inside one of them returns an error. Set the whole `fragment_mods` list instead.
