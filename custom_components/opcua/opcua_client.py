"""OPC UA client implementation."""
from __future__ import annotations

import logging
from typing import Any

from asyncua import Client
from asyncua.ua import NodeId

_LOGGER = logging.getLogger(__name__)


class OPCUAClient:
    """OPC UA client implementation."""

    def __init__(
        self,
        url: str,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        """Initialize the OPC UA client."""
        self._url = url
        self._username = username
        self._password = password
        self._client: Client | None = None

    async def connect(self) -> None:
        """Connect to the OPC UA server."""
        self._client = Client(self._url)
        
        if self._username and self._password:
            self._client.set_user(self._username)
            self._client.set_password(self._password)
            
        await self._client.connect()

    async def disconnect(self) -> None:
        """Disconnect from the OPC UA server."""
        if self._client:
            await self._client.disconnect()
            self._client = None

    async def read_value(self, node_id: str) -> Any:
        """Read a value from a node."""
        if not self._client:
            raise ConnectionError("Not connected to OPC UA server")
            
        node = self._client.get_node(node_id)
        return await node.read_value()

    async def write_value(self, node_id: str, value: Any) -> None:
        """Write a value to a node."""
        if not self._client:
            raise ConnectionError("Not connected to OPC UA server")
            
        node = self._client.get_node(node_id)
        await node.write_value(value)

    async def browse_node(self, node_id: str) -> list[NodeId]:
        """Browse a node and return its children."""
        if not self._client:
            raise ConnectionError("Not connected to OPC UA server")
            
        node = self._client.get_node(node_id)
        return await node.get_children() 