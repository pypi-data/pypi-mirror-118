#!/usr/bin/python3

#     Copyright 2021. FastyBird s.r.o.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""
Entities cache to prevent database overloading
"""

# Library dependencies
import uuid
from abc import ABC
from typing import Dict
from modules_metadata.triggers_module import TriggerConditionOperator
from modules_metadata.types import SwitchPayload


class TriggerItem:
    """
    Trigger entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __trigger_id: uuid.UUID
    __enabled: bool

    __device_property_conditions: Dict[str, "DevicePropertyConditionItem"] = {}
    __channel_property_conditions: Dict[str, "ChannelPropertyConditionItem"] = {}

    __device_property_actions: Dict[str, "DevicePropertyActionItem"] = {}
    __channel_property_actions: Dict[str, "ChannelPropertyActionItem"] = {}

    # -----------------------------------------------------------------------------

    def __init__(self, trigger_id: uuid.UUID, enabled: bool) -> None:
        self.__trigger_id = trigger_id
        self.__enabled = enabled

        self.__device_property_actions = {}
        self.__channel_property_actions = {}

        self.__device_property_conditions = {}
        self.__channel_property_conditions = {}

    # -----------------------------------------------------------------------------

    @property
    def trigger_id(self) -> uuid.UUID:
        """Trigger identifier"""
        return self.__trigger_id

    # -----------------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """Flag informing if trigger is enabled"""
        return self.__enabled

    # -----------------------------------------------------------------------------

    @property
    def actions(
        self,
    ) -> Dict[str, "DevicePropertyConditionItem" or "ChannelPropertyConditionItem"]:
        """All trigger actions"""
        return {
            **self.__device_property_actions,
            **self.__channel_property_actions,
        }

    # -----------------------------------------------------------------------------

    @property
    def conditions(
        self,
    ) -> Dict[str, "DevicePropertyConditionItem" or "ChannelPropertyConditionItem"]:
        """All trigger conditions"""
        return {
            **self.__device_property_conditions,
            **self.__channel_property_conditions,
        }

    # -----------------------------------------------------------------------------

    def add_condition(
        self,
        condition_id: str,
        condition: "DevicePropertyConditionItem" or "ChannelPropertyConditionItem",
    ) -> None:
        """Assign condition to trigger"""
        if isinstance(condition, DevicePropertyConditionItem):
            self.__device_property_conditions[condition_id] = condition

        elif isinstance(condition, ChannelPropertyConditionItem):
            self.__channel_property_conditions[condition_id] = condition

    # -----------------------------------------------------------------------------

    def add_action(
        self,
        action_id: str,
        action: "DevicePropertyActionItem" or "ChannelPropertyActionItem",
    ) -> None:
        """Assign action to trigger"""
        if isinstance(action, DevicePropertyActionItem):
            self.__device_property_actions[action_id] = action

        elif isinstance(action, ChannelPropertyActionItem):
            self.__channel_property_actions[action_id] = action


class PropertyConditionItem(ABC):
    """
    Base property condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __condition_id: uuid.UUID
    __enabled: bool

    __operator: TriggerConditionOperator
    __operand: str

    __device: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        enabled: bool,
        operator: TriggerConditionOperator,
        operand: str,
        device: uuid.UUID,
    ) -> None:
        self.__condition_id = condition_id
        self.__enabled = enabled

        self.__operator = operator
        self.__operand = operand

        self.__device = device

    # -----------------------------------------------------------------------------

    @property
    def device(self) -> uuid.UUID:
        """Device identifier"""
        return self.__device

    # -----------------------------------------------------------------------------

    @property
    def condition_id(self) -> uuid.UUID:
        """Condition identifier"""
        return self.__condition_id

    # -----------------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """Flag informing if condition is enabled"""
        return self.__enabled

    # -----------------------------------------------------------------------------

    @property
    def operator(self) -> TriggerConditionOperator:
        """Condition operator"""
        return self.__operator

    # -----------------------------------------------------------------------------

    @property
    def operand(self) -> str:
        """Condition operand"""
        return self.__operand

    # -----------------------------------------------------------------------------

    def validate(
        self,
        previous_value: str or None,
        actual_value: str
    ) -> bool:
        """Property value validation"""
        if previous_value is not None and previous_value == actual_value:
            return False

        if self.__operator == TriggerConditionOperator.EQUAL:
            return self.operand == actual_value

        if self.__operator == TriggerConditionOperator.ABOVE:
            return self.operand < actual_value

        if self.__operator == TriggerConditionOperator.BELOW:
            return self.operand > actual_value

        return False


class DevicePropertyConditionItem(PropertyConditionItem):
    """
    Device property condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __device_property: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        enabled: bool,
        operator: TriggerConditionOperator,
        operand: str,
        device_property: uuid.UUID,
        device: uuid.UUID,
    ) -> None:
        super().__init__(condition_id, enabled, operator, operand, device)

        self.__device_property = device_property

    # -----------------------------------------------------------------------------

    @property
    def device_property(self) -> uuid.UUID:
        """Device property identifier"""
        return self.__device_property


class ChannelPropertyConditionItem(PropertyConditionItem):
    """
    Channel property condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __channel_property: uuid.UUID
    __channel: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        enabled: bool,
        operator: TriggerConditionOperator,
        operand: str,
        channel_property: uuid.UUID,
        channel: uuid.UUID,
        device: uuid.UUID,
    ) -> None:
        super().__init__(condition_id, enabled, operator, operand, device)

        self.__channel_property = channel_property
        self.__channel = channel

    # -----------------------------------------------------------------------------

    @property
    def channel(self) -> uuid.UUID:
        """Channel identifier"""
        return self.__channel

    # -----------------------------------------------------------------------------

    @property
    def channel_property(self) -> uuid.UUID:
        """Channel property identifier"""
        return self.__channel_property


class PropertyActionItem(ABC):
    """
    Base property action entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __action_id: uuid.UUID
    __enabled: bool

    __value: str

    __device: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(self, action_id: uuid.UUID, enabled: bool, value: str, device: uuid.UUID) -> None:
        self.__action_id = action_id
        self.__enabled = enabled

        self.__value = value

        self.__device = device

    # -----------------------------------------------------------------------------

    @property
    def device(self) -> uuid.UUID:
        """Device identifier"""
        return self.__device

    # -----------------------------------------------------------------------------

    @property
    def action_id(self) -> uuid.UUID:
        """Action identifier"""
        return self.__action_id

    # -----------------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """Flag informing if action is enabled"""
        return self.__enabled

    # -----------------------------------------------------------------------------

    @property
    def value(self) -> str:
        """Action property value to be set"""
        return self.__value

    # -----------------------------------------------------------------------------

    def validate(
        self,
        actual_value: str
    ) -> bool:
        """Property value validation"""
        if self.__value == SwitchPayload(SwitchPayload.TOGGLE).value:
            return False

        return self.__value == actual_value


class DevicePropertyActionItem(PropertyActionItem):
    """
    Device property action entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __device_property: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        action_id: uuid.UUID,
        enabled: bool,
        value: str,
        device_property: uuid.UUID,
        device: uuid.UUID,
    ) -> None:
        super().__init__(action_id, enabled, value, device)

        self.__device_property = device_property

    # -----------------------------------------------------------------------------

    @property
    def device_property(self) -> uuid.UUID:
        """Device property identifier"""
        return self.__device_property


class ChannelPropertyActionItem(PropertyActionItem):
    """
    Channel property action entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __channel_property: uuid.UUID
    __channel: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        action_id: uuid.UUID,
        enabled: bool,
        value: str,
        channel_property: uuid.UUID,
        channel: uuid.UUID,
        device: uuid.UUID,
    ) -> None:
        super().__init__(action_id, enabled, value, device)

        self.__channel_property = channel_property
        self.__channel = channel

    # -----------------------------------------------------------------------------

    @property
    def channel(self) -> uuid.UUID:
        """Channel identifier"""
        return self.__channel

    # -----------------------------------------------------------------------------

    @property
    def channel_property(self) -> uuid.UUID:
        """Channel property identifier"""
        return self.__channel_property
