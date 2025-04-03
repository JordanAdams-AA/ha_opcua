"""OPC UA entity implementation."""
from __future__ import annotations

from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .opcua_client import OPCUAClient


class OPCUAEntity(CoordinatorEntity):
    """Base class for OPC UA entities."""

    def __init__(
        self,
        client: OPCUAClient,
        description: EntityDescription,
    ) -> None:
        """Initialize the entity."""
        super().__init__(None)  # type: ignore[arg-type]
        self._client = client
        self.entity_description = description
        self._attr_name = description.name
        self._attr_unique_id = f"{client._url}-{description.key}"
        self._attr_available = True 