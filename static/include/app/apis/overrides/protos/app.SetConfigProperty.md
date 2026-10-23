Set individual properties in a machine {{< glossary_tooltip term_id="part" text="part" >}}'s configuration by path, without replacing the whole configuration as [`UpdateRobotPart`](#updaterobotpart) does.
Paths are dot-separated, such as `network.bind_address`.
In `components`, `services`, `jobs`, `remotes`, `triggers`, `modules`, `processes`, and `packages`, the second segment names the resource by name or ID, such as `components.my-camera.attributes.width_px`.
Changes apply in order, and each change succeeds or fails on its own; the result for each change reports whether it succeeded and, if not, the error.
You can send at most 100 changes per request.
If the part imports a fragment, you can only set properties that the part's own configuration already sets; setting a property that may come from the fragment returns an error.
