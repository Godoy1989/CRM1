"""Connector class to interact with e-Distribución API."""
import aiohttp
import asyncio
import json
import logging
from datetime import datetime, timedelta
from dateutil.tz import tzutc

UTC = tzutc()

_LOGGER = logging.getLogger(__name__)

class EdsConnector:
    """Class to manage the e-Distribución API connection."""

    def __init__(self, user, password):
        """Initialize the connector."""
        self.username = user
        self.password = password
        self.session = None
        self._token = None
        self._identities = {}

    async def async_login(self):
        """Log in to the e-Distribución API."""
        if not self.session:
            self.session = aiohttp.ClientSession()

        try:
            login_url = "https://zonaprivada.edistribucion.com/areaprivada/s/login"
            async with self.session.get(login_url) as response:
                if response.status != 200:
                    raise Exception("Failed to load login page")

            # Simulate login process (replace with actual logic)
            self._token = "example_token"
            _LOGGER.info("Login successful")
        except Exception as e:
            _LOGGER.error("Error during login: %s", e)
            raise

    async def get_cups_list(self):
        """Retrieve the list of CUPS."""
        if not self._token:
            await self.async_login()

        try:
            headers = {"Authorization": f"Bearer {self._token}"}
            url = "https://api.edistribucion.com/getCupsList"
            async with self.session.post(url, headers=headers, json={"account_id": self._identities.get("account_id")}) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    _LOGGER.error("Failed to fetch CUPS list: %s", await response.text())
                    return []
        except Exception as e:
            _LOGGER.error("Error fetching CUPS list: %s", e)
            return []

    async def get_cycle_list(self, cups_id):
        """Retrieve the list of cycles for a specific CUPS."""
        if not self._token:
            await self.async_login()

        try:
            headers = {"Authorization": f"Bearer {self._token}"}
            url = f"https://api.edistribucion.com/getCycleList/{cups_id}"
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    _LOGGER.error("Failed to fetch cycle list: %s", await response.text())
                    return {}
        except Exception as e:
            _LOGGER.error("Error fetching cycle list: %s", e)
            return {}

    async def get_custom_curve(self, cups_id, start_date, end_date):
        """Retrieve custom energy curve for a specific CUPS."""
        if not self._token:
            await self.async_login()

        try:
            headers = {"Authorization": f"Bearer {self._token}"}
            url = "https://api.edistribucion.com/getCustomCurve"
            data = {
                "cups_id": cups_id,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            }
            async with self.session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    _LOGGER.error("Failed to fetch custom curve: %s", await response.text())
                    return {}
        except Exception as e:
            _LOGGER.error("Error fetching custom curve: %s", e)
            return {}

    async def close_session(self):
        """Close the session."""
        if self.session:
            await self.session.close()
            _LOGGER.debug("Session closed")