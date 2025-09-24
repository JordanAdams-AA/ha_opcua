"""Support for OPC UA sensors."""
from __future__ import annotations

import logging
import voluptuous as vol
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    PLATFORM_SCHEMA,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback


from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_URL,
    CONF_NAME,
    CONF_UNIT_OF_MEASUREMENT,
)

from .const import (
    DOMAIN,
    CONF_NODEID,
    CONF_NODES,
    )

_LOGGER = logging.getLogger(__name__)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NODES): [
            {
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_NODEID): cv.string,
                vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
            }
        ]
    }
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up OPC UA sensors from a config entry."""
    client = hass.data[DOMAIN][entry.entry_id]
    
    sensors = []

    for node in ConfigEntry[CONF_NODES]:

        sensors.append(
            OPCUASensor(
                client,
                node[CONF_NAME],
                node[CONF_NODEID],
                node.get(CONF_UNIT_OF_MEASUREMENT),
                node.get(CONF_DEVICE_CLASS) 
            )
        )
    
    
    async_add_entities(sensors, True)


class OPCUASensor(RestoreEntity):
    """Representation of an OPC UA sensor."""

    def __init__(
        self,
        client: Any,
        name: str,
        node_id: str,
        unit_of_measurement,
        device_class,
    ) -> None:
        """Initialize the sensor."""
        self._name = name
        self._node_id = node_id
        self._unit_of_measurement = unit_of_measurement
        self._device_class = device_class
        self._value = None
        self._available = False
        self._unique_id = str(DOMAIN) + "-" + str(self._name)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._value

    @property
    def unique_id(self):
        """Return the unique_id of the sensor."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement
    
    @property
    def device_class(self) -> Optional[str]:
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    async def async_added_to_hass(self):
        """Get the value for the first time"""
        self.async_update()

    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        try:
            self._value = await self._client.read_value(
                self._node_id
            )
            
            self._available = True
        except Exception as err:
            _LOGGER.error("Error updating sensor: %s", err)
            self._available = False
            self._value = None
