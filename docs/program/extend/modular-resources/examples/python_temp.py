from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional

from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.components.base import Base
from viam.components.motor import Motor

class MyBase(Base, Reconfigurable):
    """
    mybase implements a base that only supports SetPower (basic forward/back/turn controls.)

    It inherents from Base, and conforms to the ``Reconfigurable`` protocol, which signifies that this component can be reconfigured.
    It also specifies a function ``MyBase.new``, which confirms to the ``resource.types.ResourceCreator`` type required for all models.
    """

    """ Here is where we define our new model's colon-delimited-triplet (acme:demo:mybase) 
    acme = namespace, demo = resource type, mybase = model. """
    MODEL: ClassVar[Model] = Model(ModelFamily("acme"))

    left: str # Left motor name
    right: str # Right motor name

    # Constructor
    @classmethod
    def newBase(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        base := cls(MyBase(config.name))
        base.left = config.attributes.fields["motorL"].string_value
        base.right = config.attributes.fields["motorR"].string_value
        return base

    # Validates JSON Configuration
    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        left_motor = config.attributes.fields["motorL"].string_value
        if left_motor == "":
            raise Exception("A motorL attribute is required for a MyBase component.")
        right_motor = [config.attributes.fields["motorR"].string_value]
        if right_motor == [""]:
            raise Exception("A motorR attribute is required for a MyBase component.")
        return [left_motor, right_motor]

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.left = config.attributes.fields["motorL"].string_value
        self.right = config.attributes.fields["motorR"].string_value

    # Implement the methods the Viam RDK defines for the base API (rdk:component:base)

    # move_straight: unimplemented
    async def move_straight(self, distance: int, velocity: float, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        pass

    # spin: unimplemented
    async def spin(self, angle: float, velocity: float, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        pass

    # set_velocity: unimplemented
    async def set_velocity( self, linear: Vector3, angular: Vector3, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        pass

    # set_power: sets the linear and angular velocity of the left and right motors on the base
    set_power(self, linear: Vector3, angular: Vector3, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None,
    ):

    # stop: stops the base from moving by stopping both motors
    async def stop(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):

    # is_moving: checks if the base is moving
    async def is_moving(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None) -> bool:
        