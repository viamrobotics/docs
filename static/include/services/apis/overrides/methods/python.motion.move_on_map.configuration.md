<!-- preserve-formatting -->

The configuration you want to set across this machine for this motion service. This parameter and each of its fields are optional.

- `obstacle_detectors` [(Iterable[ObstacleDetector])](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.ObstacleDetector): The names of each [vision service](/operate/reference/services/vision/) and [camera](/operate/reference/components/camera/) resource pair you want to use for transient obstacle avoidance.
- `position_polling_frequency_hz` [(float)](https://docs.python.org/3/library/functions.html#float): The frequency in hz to poll the position of the machine.
- `obstacle_polling_frequency_hz` [(float)](https://docs.python.org/3/library/functions.html#float): The frequency in hz to poll the vision service for new obstacles.
- `plan_deviation_m` [(float)](https://docs.python.org/3/library/functions.html#float): The distance in meters that the machine can deviate from the motion plan. By default this is set to 2.6 m which is an appropriate value for outdoor usage. When you use the `MoveOnMap()` method from the **CONTROL** tab, the default is overwritten to 0.5 m for testing.
- `linear_m_per_sec` [(float)](https://docs.python.org/3/library/functions.html#float): Linear velocity this machine should target when moving.
- `angular_degs_per_sec` [(float)](https://docs.python.org/3/library/functions.html#float): Angular velocity this machine should target when turning.
