"""Helper class to manage e-Distribución data."""
import asyncio
from datetime import datetime, timedelta
import logging
from aiopvpc import PVPCData

_LOGGER = logging.getLogger(__name__)

class EdsHelper:
    """Class to manage the e-Distribución API connection."""

    def __init__(self, user, password, cups=None, short_interval=None, long_interval=None):
        """Initialize the helper."""
        from .connector import EdsConnector
        self._eds = EdsConnector(user, password)
        self._short_interval = short_interval or timedelta(minutes=30)
        self._long_interval = long_interval or timedelta(hours=1)
        self._cups_id = cups
        self._attributes = {}
        self._pvpc_handler = PVPCData(tariff="2.0TD", local_timezone=str(tzlocal.get_localzone()))

    async def async_login(self):
        """Log in to the e-Distribución API."""
        await self._eds.async_login()

    async def async_set_cups(self, candidate=None):
        """Set the selected CUPS."""
        await self._eds.async_login()
        all_cups = await self._eds.get_cups_list()
        _LOGGER.debug("CUPS: %s", all_cups)
        for c in all_cups:
            if candidate is None or c.get('CUPS', None) == candidate:
                self._cups_id = c.get('CUPS_Id', None)
                self._attributes['cups'] = c.get('CUPS', None)
                self._attributes['power_limit_p1'] = c.get('Power', None)
                self._attributes['power_limit_p2'] = c.get('Power', None)
                break

    async def async_update_data(self):
        """Fetch new data from the API."""
        if not self._cups_id:
            await self.async_set_cups()

        # Update cycles
        self._attributes['cycles'] = await self._eds.get_cycle_list(self._cups_id)

        # Update energy
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        self._attributes['energy'] = await self._eds.get_custom_curve(self._cups_id, start_date, end_date)

        # Update PVPC prices
        pvpc_data = await self._pvpc_handler.async_download_prices_for_range(
            start_date=start_date,
            end_date=end_date
        )
        self._attributes['pvpc_prices'] = pvpc_data

    @property
    def attributes(self):
        """Return the attributes."""
        return self._attributes