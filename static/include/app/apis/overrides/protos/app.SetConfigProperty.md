Set individual properties in a machine {{< glossary_tooltip term_id="part" text="part" >}}'s configuration by path, without replacing the whole configuration as [`UpdateRobotPart`](#updaterobotpart) does.

Paths are dot-separated, such as `network.bind_address`.
In `components`, `services`, `jobs`, `remotes`, `triggers`, `modules`, and `packages`, the second segment names the resource by name or ID, such as `components.my-camera.attributes.width_px`.
Set `processes` as a whole section.

**Where a change is saved:**

- If the property is in a resource or section that the part's own configuration defines, the change is made there. A property that isn't set yet is added.
- If the resource comes from a fragment the part imports, the change is saved through that fragment, even if the fragment doesn't set that property yet:
  - If the fragment sets the property with a [fragment variable](/fleet/reuse-configuration/#customize-fragments-with-variables) that no other property uses, the change sets the variable's value on the part's fragment import.
  - Otherwise, including when other properties share the variable, the change is saved as a `$set` [fragment override](/fleet/reuse-configuration/#override-specific-settings) for the last fragment that provides the resource, since later fragments win when fragments merge.

**Limits and errors:**

- Changes apply in order, and each change succeeds or fails on its own. The result for each change reports whether it succeeded and, if not, the error.
- You can send at most 100 changes per request.
- Fragment overrides can't change `billing` or `access_policy`, so setting a property in either section that comes from a fragment returns an error.
- Replacing a whole resource that comes from a fragment the part imports more than once returns an error. Set the resource's fields instead.
