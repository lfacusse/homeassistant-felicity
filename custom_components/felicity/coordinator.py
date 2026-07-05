"""DataUpdateCoordinator for Felicity Solar."""

from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import FelicityAPI

_LOGGER = logging.getLogger(__name__)


class FelicityCoordinator(DataUpdateCoordinator):
    """Coordinator."""

    def __init__(self, hass, entry):
        super().__init__(
            hass,
            _LOGGER,
            name="Felicity Solar",
            update_interval=timedelta(seconds=30),
        )

        self.api = FelicityAPI(
            username=entry.data["username"],
            password=entry.data["password"],
        )

    async def _async_update_data(self):

        try:
            await self.api.login()

            devices = await self.api.get_devices()

            inverter = devices[1]["deviceSn"]

            data = await self.api.get_latest_data(inverter)

            return data

        except Exception as err:
            raise UpdateFailed(str(err))