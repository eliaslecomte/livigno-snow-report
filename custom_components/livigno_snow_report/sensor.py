"""Sensor platform for Livigno Snow Report."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfLength
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTRIBUTION,
    DOMAIN,
    SENSOR_ALPINE_SKIING,
    SENSOR_CROSS_COUNTRY,
    SENSOR_FRESH_SNOW,
    SENSOR_LAST_SNOWFALL_AMOUNT,
    SENSOR_LAST_SNOWFALL_DATE,
    SENSOR_SNOW_ALTITUDE,
    SENSOR_SNOW_VILLAGE,
    SENSOR_WINTER_TRAIL,
)
from .coordinator import LivignoSnowCoordinator, LivignoSnowData


@dataclass(frozen=True, kw_only=True)
class LivignoSensorEntityDescription(SensorEntityDescription):
    """Describes a Livigno sensor entity."""

    value_fn: Callable[[LivignoSnowData], Any]


SENSOR_DESCRIPTIONS: tuple[LivignoSensorEntityDescription, ...] = (
    LivignoSensorEntityDescription(
        key=SENSOR_SNOW_ALTITUDE,
        translation_key=SENSOR_SNOW_ALTITUDE,
        native_unit_of_measurement=UnitOfLength.CENTIMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:snowflake",
        value_fn=lambda data: data.snow_altitude,
    ),
    LivignoSensorEntityDescription(
        key=SENSOR_SNOW_VILLAGE,
        translation_key=SENSOR_SNOW_VILLAGE,
        native_unit_of_measurement=UnitOfLength.CENTIMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:snowflake",
        value_fn=lambda data: data.snow_village,
    ),
    LivignoSensorEntityDescription(
        key=SENSOR_LAST_SNOWFALL_DATE,
        translation_key=SENSOR_LAST_SNOWFALL_DATE,
        device_class=SensorDeviceClass.DATE,
        icon="mdi:calendar-snowflake",
        value_fn=lambda data: data.last_snowfall_date,
    ),
    LivignoSensorEntityDescription(
        key=SENSOR_LAST_SNOWFALL_AMOUNT,
        translation_key=SENSOR_LAST_SNOWFALL_AMOUNT,
        native_unit_of_measurement=UnitOfLength.CENTIMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:snowflake-alert",
        value_fn=lambda data: data.last_snowfall_amount,
    ),
    LivignoSensorEntityDescription(
        key=SENSOR_FRESH_SNOW,
        translation_key=SENSOR_FRESH_SNOW,
        native_unit_of_measurement=UnitOfLength.CENTIMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:snowflake-variant",
        value_fn=lambda data: data.fresh_snow,
    ),
    LivignoSensorEntityDescription(
        key=SENSOR_CROSS_COUNTRY,
        translation_key=SENSOR_CROSS_COUNTRY,
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:ski-cross-country",
        value_fn=lambda data: data.cross_country_skiing,
    ),
    LivignoSensorEntityDescription(
        key=SENSOR_ALPINE_SKIING,
        translation_key=SENSOR_ALPINE_SKIING,
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:ski",
        value_fn=lambda data: data.alpine_skiing,
    ),
    LivignoSensorEntityDescription(
        key=SENSOR_WINTER_TRAIL,
        translation_key=SENSOR_WINTER_TRAIL,
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:walk",
        value_fn=lambda data: data.winter_trail,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Livigno Snow Report sensors based on a config entry."""
    coordinator: LivignoSnowCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        LivignoSnowSensor(coordinator, description)
        for description in SENSOR_DESCRIPTIONS
    )


class LivignoSnowSensor(CoordinatorEntity[LivignoSnowCoordinator], SensorEntity):
    """Representation of a Livigno Snow sensor."""

    entity_description: LivignoSensorEntityDescription
    _attr_has_entity_name = True
    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: LivignoSnowCoordinator,
        description: LivignoSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, DOMAIN)},
            "name": "Livigno Snow Report",
            "manufacturer": "Livigno.eu",
            "model": "Snow Data",
            "entry_type": "service",
        }

    @property
    def native_value(self) -> float | date | None:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)
