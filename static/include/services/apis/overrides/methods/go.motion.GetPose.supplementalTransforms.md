<!-- retain-formatting -->
An optional list of `LinkInFrame`s.
  A `LinkInFrame` represents an additional frame which is added to the machine's frame system.
  It consists of:

  - a `PoseInFrame`: Provides the relationship between the frame being added and another frame.
  - `Geometry`: An optional `Geometry` can be added to the frame being added.
    When `supplementalTransforms` are provided, a frame system is created within the context of the `GetPose` function.
    This new frame system builds off the machine's frame system and incorporates the `LinkInFrame`s provided.
    If the result of adding the `LinkInFrame`s results in a disconnected frame system, an error is thrown.