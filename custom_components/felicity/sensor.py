from homeassistant.components.sensor import SensorEntity

from .api import FelicityApi


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):

    api = FelicityApi(
        entry.data["username"],
        entry.data["password"],
        entry.data["device_sn"],
    )

    await api.login()

    async_add_entities(
        [
            FelicityBatterySensor(api),
            FelicityPVSensor(api),
        ],
        True,
    )


class FelicityBatterySensor(SensorEntity):

    _attr_name = "Felicity Battery SOC"
    _attr_unique_id = "felicity_soc"

    def __init__(self, api):
        self.api = api
        self._attr_native_unit_of_measurement = "%"

    async def async_update(self):

        data = await self.api.get_latest()

        latest = data["data"]["dataList"][0]

        self._attr_native_value = float(latest["emsSoc"])


class FelicityPVSensor(SensorEntity):

    _attr_name = "Felicity PV Power"
    _attr_unique_id = "felicity_pv"

    def __init__(self, api):
        self.api = api
        self._attr_native_unit_of_measurement = "W"

    async def async_update(self):

        data = await self.api.get_latest()

        latest = data["data"]["dataList"][0]

        self._attr_native_value = float(latest["pvPower"])