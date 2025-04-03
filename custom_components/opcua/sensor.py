"""Support for OPC UA sensors."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import OPCUAEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up OPC UA sensors from a config entry."""
    client = hass.data[DOMAIN][entry.entry_id]
    
    # Example: Add a sensor for a specific node
    # In a real implementation, you would get these from configuration
    sensors = [
        OPCUASensor(
            client,
            SensorEntityDescription(
                key="example_node",
                name="Example Node",
                native_unit_of_measurement="°C",
            ),
            "ns=2;i=1",  # Example node ID
        )
    ]
    
    async_add_entities(sensors, True)


class OPCUASensor(OPCUAEntity, SensorEntity):
    """Representation of an OPC UA sensor."""

    def __init__(
        self,
        client: Any,
        description: SensorEntityDescription,
        node_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(client, description)
        self._node_id = node_id

    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        try:
            self._attr_native_value = await self._client.read_value(
                self._node_id
            )
        except Exception as err:
            _LOGGER.error("Error updating sensor: %s", err)
            self._attr_available = False
