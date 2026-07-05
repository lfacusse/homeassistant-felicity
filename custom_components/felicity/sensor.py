"""Felicity sensors."""

import logging

from homeassistant.components.sensor import SensorEntity

from .api import FelicityApi

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Felicity sensors."""

    _LOGGER.warning("######## FELICITY SENSOR.PY LOADED ########")

    api = FelicityApi(
        entry.data["username"],
        entry.data["password"],
        entry.data["device_sn"],
    )

    async_add_entities(
        [
            FelicityBatterySensor(api),
            FelicityPVSensor(api),
            FelicityBatteryPowerSensor(api),
            FelicityGridPowerSensor(api),
            FelicityHouseLoadSensor(api),
        ],
        update_before_add=True,
    )


class FelicityBatterySensor(SensorEntity):
    """Battery SOC sensor."""

    def __init__(self, api):
        self.api = api
        self._attr_name = "Felicity Battery SOC"
        self._attr_unique_id = "felicity_battery_soc"
        self._attr_native_unit_of_measurement = "%"
        self._attr_should_poll = True
        self._value = None

    @property
    def native_value(self):
        return self._value

    async def async_update(self):
        """Update battery state."""

        try:
            _LOGGER.warning("Battery: starting update")

            data = await self.api.get_latest()

            _LOGGER.warning("Battery JSON: %s", data)

            latest = data["data"]["dataList"][0]

            _LOGGER.warning("LATEST JSON = %s", latest)

            self._value = float(latest["emsSoc"])

            _LOGGER.warning("Battery state = %s", self._value)

            

        except Exception:
            _LOGGER.exception("Battery update failed")
            raise

class FelicityGridPowerSensor(SensorEntity):
    """Grid Power sensor."""

    def __init__(self, api):
        self.api = api
        self._attr_name = "Felicity Grid Power"
        self._attr_unique_id = "felicity_grid_power"
        self._attr_native_unit_of_measurement = "W"
        self._attr_should_poll = True
        self._value = None

    @property
    def native_value(self):
        return self._value

    async def async_update(self):
        """Update grid power."""

        try:
            data = await self.api.get_latest()
            latest = data["data"]["dataList"][0]
            self._value = float(latest["meterPower"])
        except Exception:
            _LOGGER.exception("Grid Power update failed")
            raise

class FelicityHouseLoadSensor(SensorEntity):
    """House Load sensor."""

    def __init__(self, api):
        self.api = api
        self._attr_name = "Felicity House Load"
        self._attr_unique_id = "felicity_house_load"
        self._attr_native_unit_of_measurement = "W"
        self._attr_should_poll = True
        self._value = None

    @property
    def native_value(self):
        return self._value

    async def async_update(self):
        """Update house load."""

        try:
            data = await self.api.get_latest()
            latest = data["data"]["dataList"][0]
            self._value = float(latest["ctPower"])
        except Exception:
            _LOGGER.exception("House Load update failed")
            raise

class FelicityPVSensor(SensorEntity):
    """PV Power sensor."""

    def __init__(self, api):
        self.api = api
        self._attr_name = "Felicity PV Power"
        self._attr_unique_id = "felicity_pv_power"
        self._attr_native_unit_of_measurement = "W"
        self._attr_should_poll = True
        self._value = None

    @property
    def native_value(self):
        return self._value

    async def async_update(self):
        """Update PV state."""

        try:
            _LOGGER.warning("PV: starting update")

            data = await self.api.get_latest()

            latest = data["data"]["dataList"][0]

            _LOGGER.warning("LATEST JSON = %s", latest)

            self._value = float(latest["pvPower"])

            _LOGGER.warning("PV state = %s", self._value)

            

        except Exception:
            _LOGGER.exception("PV update failed")
            raise


class FelicityBatteryPowerSensor(SensorEntity):
    """Battery Power sensor."""

    def __init__(self, api):
        self.api = api
        self._attr_name = "Felicity Battery Power"
        self._attr_unique_id = "felicity_battery_power"
        self._attr_native_unit_of_measurement = "W"
        self._attr_should_poll = True
        self._value = None

    @property
    def native_value(self):
        return self._value

    async def async_update(self):
        """Update battery power."""

        try:
            _LOGGER.warning("Battery Power: starting update")

            data = await self.api.get_latest()

            latest = data["data"]["dataList"][0]

            self._value = -float(latest["emsPower"])

            _LOGGER.warning("Battery Power = %s", self._value)

        except Exception:
            _LOGGER.exception("Battery Power update failed")
            raise            