Set individual properties in a machine {{< glossary_tooltip term_id="part" text="part" >}}'s configuration by path, without replacing the whole configuration as [`UpdateRobotPart`](#updaterobotpart) does.
Paths are dot-separated, such as `network.bind_address`.
In `components`, `services`, `jobs`, `remotes`, `triggers`, `modules`, `processes`, and `packages`, the second segment names the resource by name or ID, such as `components.my-camera.attributes.width_px`.
Changes apply in order, and each change succeeds or fails on its own; the result for each change reports whether it succeeded and, if not, the error.
You can send at most 100 changes per request.
If the part's own configuration sets a property, the change is made there.
If a fragment the part imports provides the property instead, the change is saved as a `$set` [fragment override](/fleet/reuse-configuration/#override-specific-settings) on the last import that provides it, since later fragments win when fragments merge.
A property that neither sets is added to the part's configuration.
Fragment overrides can't change `billing` or `access_policy`, so setting a property in either section that comes from a fragment returns an error.
Replacing a whole resource that comes from a fragment the part imports more than once returns an error; set the resource's fields instead.
