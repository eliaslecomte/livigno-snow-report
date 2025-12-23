# Livigno Snow Report

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/eliaslecomte/livigno-snow-report.svg)](https://github.com/eliaslecomte/livigno-snow-report/releases)

A Home Assistant custom integration that fetches snow conditions and ski piste status for Livigno, Italy.

## Features

- **Snow conditions**: Monitor snow depth at altitude and in the village
- **Snowfall tracking**: Last snowfall date and amount, fresh snow height
- **Piste status**: Open kilometers for alpine skiing, cross-country skiing, and winter trails
- **Live webcam**: 360° panoramic webcam image of Livigno

## Sensors

| Sensor | Unit | Description |
|--------|------|-------------|
| Snow in altitude | cm | Snow depth at mountain altitude |
| Snow in village | cm | Snow depth in Livigno village |
| Last snowfall date | date | Date of most recent snowfall |
| Last snowfall amount | cm | Amount of snow from last snowfall |
| Fresh snow | cm | Fresh snow height |
| Cross-country skiing | km | Open cross-country ski trails |
| Alpine skiing | km | Open alpine ski pistes |
| Winter trail | km | Open winter walking trails |

## Image Entity

| Entity | Description |
|--------|-------------|
| 360° Panorama webcam | Live panoramic webcam image of Livigno |

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots menu in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/eliaslecomte/livigno-snow-report` with category "Integration"
6. Click "Add"
7. Search for "Livigno Snow Report" and install it
8. Restart Home Assistant
9. Go to Settings > Devices & Services > Add Integration
10. Search for "Livigno Snow Report"

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/eliaslecomte/livigno-snow-report/releases)
2. Extract and copy `custom_components/livigno_snow_report` to your `config/custom_components/` directory
3. Restart Home Assistant
4. Go to Settings > Devices & Services > Add Integration
5. Search for "Livigno Snow Report"

## Configuration

No configuration is required. The integration fetches data from [livigno.eu](https://www.livigno.eu/en/snow-data) every 30 minutes.

## Data Source

All data is scraped from the official Livigno tourism website: https://www.livigno.eu/en/snow-data

## License

MIT License - see [LICENSE](LICENSE) for details.
