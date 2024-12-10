<!-- prettier-ignore -->
| Method Name | Description | `viam-micro-server` Support |
| ----------- | ----------- | --------------------------- |
| [`MoveStraight`](/dev/reference/apis/components/base/#movestraight) | Move the base in a straight line across the given distance (mm) at the given velocity (mm/sec). | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`Spin`](/dev/reference/apis/components/base/#spin) | Turn the base in place, rotating it to the given angle (degrees) at the given angular velocity (degrees/sec). | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`SetPower`](/dev/reference/apis/components/base/#setpower) | Set the linear and angular power of the base, represented as a percentage of max power for each direction in the range of [-1.0 to 1.0]. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`SetVelocity`](/dev/reference/apis/components/base/#setvelocity) | Set the linear velocity (mm/sec) and angular velocity (degrees/sec) of the base. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`GetProperties`](/dev/reference/apis/components/base/#getproperties) | Get the width and turning radius of the {{< glossary_tooltip term_id="model" text="model" >}} of base in meters. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`IsMoving`](/dev/reference/apis/components/base/#ismoving) | Returns whether the base is actively moving (or attempting to move) under its own power. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`Stop`](/dev/reference/apis/components/base/#stop) | Stop the base from moving immediately. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetGeometries`](/dev/reference/apis/components/base/#getgeometries) | Get all the geometries associated with the base in its current configuration, in the frame of the base. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`Reconfigure`](/dev/reference/apis/components/base/#reconfigure) | Reconfigure this resource. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`DoCommand`](/dev/reference/apis/components/base/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetResourceName`](/dev/reference/apis/components/base/#getresourcename) | Get the `ResourceName` for this base with the given name. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`Close`](/dev/reference/apis/components/base/#close) | Safely shut down the resource and prevent further use. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
