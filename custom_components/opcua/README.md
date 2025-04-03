# OPC UA Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

This integration allows you to connect to OPC UA servers and monitor their data in Home Assistant.

## Features

- Connect to OPC UA servers
- Monitor OPC UA nodes as sensors
- Support for authentication
- Multi-language support (English, Norwegian, Swedish, German)

## Installation

### HACS Installation
1. Open HACS
2. Go to Integrations
3. Click the three dots in the top right
4. Select "Custom repositories"
5. Add this repository
6. Click "Add"
7. Find "OPC UA" in the list
8. Click "Install"

### Manual Installation
1. Copy the `opcua` folder to your `custom_components` directory in your Home Assistant configuration.
2. Restart Home Assistant.
3. Go to Settings -> Devices & Services -> Add Integration
4. Search for "OPC UA" and click on it
5. Enter your OPC UA server details:
   - Server URL (required)
   - Username (optional)
   - Password (optional)
   - Name (optional)

## Configuration

### Server URL
The URL should be in the format: `opc.tcp://hostname:port`

### Authentication
If your OPC UA server requires authentication, you can provide a username and password.

### Node Configuration
After adding the integration, you can configure which nodes to monitor by adding them as sensors in your `configuration.yaml`:

```yaml
sensor:
  - platform: opcua
    server: "opcua_server_name"
    nodes:
      - name: "Temperature"
        node_id: "ns=2;i=1"
        unit_of_measurement: "°C"
```

## Supported Languages

- English
- Norwegian
- Swedish
- German

## Troubleshooting

If you encounter connection issues:
1. Verify that the server URL is correct
2. Check if the server is accessible from your Home Assistant instance
3. Verify authentication credentials if required
4. Check the Home Assistant logs for detailed error messages

## Development

To contribute to this integration:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- [asyncua](https://github.com/FreeOpcUa/opcua-asyncio) - The OPC UA client library used in this integration
- [Home Assistant](https://www.home-assistant.io/) - The home automation platform
- [HACS](https://hacs.xyz/) - Home Assistant Community Store
