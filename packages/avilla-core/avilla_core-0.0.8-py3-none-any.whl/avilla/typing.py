from typing import (TYPE_CHECKING, AsyncContextManager, Callable, Literal,
                    TypeVar, Union)

if TYPE_CHECKING:
    from avilla.builtins.profile import GroupProfile
    from avilla.entity import Entity, EntityPtr
    from avilla.execution import Execution
    from avilla.group import Group, GroupPtr
    from avilla.profile import BaseProfile
    from avilla.protocol import BaseProtocol
    from avilla.provider import Provider
    from avilla.relationship import Relationship


T_Protocol = TypeVar("T_Protocol", bound="BaseProtocol")
T_Config = TypeVar("T_Config")
T_GroupProfile = TypeVar("T_GroupProfile", bound="GroupProfile", covariant=True)
T_Profile = TypeVar("T_Profile", bound="BaseProfile", covariant=True)
T_Result = TypeVar("T_Result")
T_Target = TypeVar("T_Target", "Entity", "Group", "EntityPtr", "GroupPtr", str, Literal[None])
T_Provider = TypeVar("T_Provider", bound="Provider")
T_Receive = TypeVar("T_Receive")
T_Value = TypeVar("T_Value")
T_Origin = TypeVar("T_Origin")
T_Ctx = TypeVar("T_Ctx", bound="Union[Entity, Group]")


# Service: may need to be remade
T_Connection = TypeVar("T_Connection")

T_ExecMW = Callable[["Relationship[T_Ctx]", "Execution"], AsyncContextManager[None]]
U_Target = Union["Entity", "Group", "GroupPtr", "EntityPtr", str, Literal[None]]
