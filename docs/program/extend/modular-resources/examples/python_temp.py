from typing import ClassVar, Mapping, Sequence

from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.components.base import Base

class MyBase(Base, Reconfigurable):
    """
    mybase implements a base that only supports SetPower (basic forward/back/turn controls.)

    It inherents from Base, and conforms to the ``Reconfigurable`` protocol, which signifies that this component can be reconfigured.
    It also specifies a function ``MyBase.new``, which confirms to the ``resource.types.ResourceCreator`` type required for all models.
    """

    """ Here is where we define our new model's colon-delimited-triplet (acme:demo:mybase) 
    acme = namespace, demo = resource type, mybase = model. """
    MODEL: ClassVar[Model] = Model(ModelFamily("acme"))
    my_arg: str 

    # Constructor
    @classmethod
    def newBase()