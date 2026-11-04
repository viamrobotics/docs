Set individual properties in a machine {{< glossary_tooltip term_id="part" text="part" >}}'s configuration by path, without replacing the whole configuration as [`UpdateRobotPart`](#updaterobotpart) does.

Paths are dot-separated, such as `network.bind_address`.
In `components`, `services`, `jobs`, `remotes`, `triggers`, `modules`, and `packages`, the second segment names the resource by name or ID, such as `components.my-camera.attributes.width_px`.
Set `processes` as a whole section.

Where a change is saved depends on whether the part or a fragment it imports provides the resource.
For how changes interact with fragment variables and overrides, and which changes to fragment resources return an error, see [Change fragment values through the API](/fleet/reuse-configuration/#change-fragment-values-through-the-api).

- Changes apply in order, and each change succeeds or fails on its own. The result for each change reports whether it succeeded and, if not, the error.
- You can send at most 100 changes per request.
