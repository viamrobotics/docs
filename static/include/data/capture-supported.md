{{< tabs >}}
{{% tab name="viam-server" %}}

<!-- prettier-ignore -->
| Type | Method |
| ---- | ------ |
| [Arm](/hardware/common-components/add-an-arm/) | `EndPosition`, `JointPositions`, `GetWorldPose`, `DoCommand` |
| [Audio out](/reference/apis/components/audio-out/) | `GetWorldPose` |
| [Base](/hardware/common-components/add-a-base/) | `GetWorldPose`, `DoCommand` |
| [Board](/hardware/common-components/add-a-board/) | `Analogs`, `Gpios`, `GetWorldPose`, `DoCommand` |
| [Button](/hardware/common-components/add-a-button/) | `GetWorldPose`, `DoCommand` |
| [Camera](/hardware/common-components/add-a-camera/) | `GetImages`, `ReadImage` (deprecated), `NextPointCloud`, `GetWorldPose`, `DoCommand` |
| [Encoder](/hardware/common-components/add-an-encoder/) | `TicksCount`, `GetWorldPose`, `DoCommand` |
| [Gantry](/hardware/common-components/add-a-gantry/) | `Lengths`, `Position`, `GetWorldPose`, `DoCommand` |
| [Generic](/hardware/common-components/add-a-generic/) | `GetWorldPose`, `DoCommand` |
| [Gripper](/hardware/common-components/add-a-gripper/) | `GetWorldPose`, `DoCommand` |
| [Input controller](/hardware/common-components/add-an-input-controller/) | `GetWorldPose`, `DoCommand` |
| [Motor](/hardware/common-components/add-a-motor/) | `Position`, `IsPowered`, `GetWorldPose`, `DoCommand` |
| [Movement sensor](/hardware/common-components/add-a-movement-sensor/) | `AngularVelocity`, `CompassHeading`, `LinearAcceleration`, `LinearVelocity`, `Orientation`, `Position`, `GetWorldPose`, `DoCommand` |
| [Power sensor](/hardware/common-components/add-a-power-sensor/) | `Voltage`, `Current`, `Power`, `GetWorldPose`, `DoCommand` |
| [Sensor](/hardware/common-components/add-a-sensor/) | `Readings`, `GetWorldPose`, `DoCommand` |
| [Servo](/hardware/common-components/add-a-servo/) | `Position`, `GetWorldPose`, `DoCommand` |
| [Switch](/hardware/common-components/add-a-switch/) | `GetWorldPose`, `DoCommand` |
| [Base remote control service](/reference/services/base-rc/) | `DoCommand` |
| [Discovery service](/reference/services/discovery/) | `DoCommand` |
| [Vision service](/vision/configure/) | `CaptureAllFromCamera`, `DoCommand` |
| [Motion service](/reference/services/motion/) | `DoCommand` |
| [Navigation service](/reference/services/navigation/) | `DoCommand` |
| Shell service | `DoCommand` |

`GetWorldPose` captures the component's position and orientation in the world reference frame using the [frame system](/motion-planning/frame-system/overview/). It is available for all component types. To use it, [configure a frame](/motion-planning/frame-system/overview/#configure-a-frame) for the component.

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

<!-- prettier-ignore -->
| Type | Method |
| ---- | ------ |
| [Movement Sensor](/hardware/common-components/add-a-movement-sensor/) | [`AngularVelocity`](/reference/apis/components/movement-sensor/#getangularvelocity), [`LinearAcceleration`](/reference/apis/components/movement-sensor/#getlinearacceleration), [`LinearVelocity`](/reference/apis/components/movement-sensor/#getlinearvelocity) |
| [Sensor](/hardware/common-components/add-a-sensor/) | [`GetReadings`](/reference/apis/components/sensor/#getreadings) |

{{% /tab %}}
{{< /tabs >}}
