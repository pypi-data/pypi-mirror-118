"""Python wrapper aorund the CheckWX API"""

from json.decoder import JSONDecodeError
from aiohttp import ClientSession
from requests.exceptions import HTTPError
from checkwxapi.const import API_KEY_HEADER, BASE_URL, METAR_ENDPOINT, STATION_ENDPOINT, STATS_ENDPOINT, TAF_ENDPOINT
import json
import logging
from typing import Dict, Text

_LOGGER = logging.getLogger(__name__)


class CheckWXAPI:
    """CheckWX API client"""
    def __init__(
        self,
        api_key: str,
        httpClient: ClientSession = None
    ):
        """Initialize the client"""
        if not self._is_valid_api_key(api_key):
            raise InvalidApiKeyError("Your API Key must be a valid string")

        self._api_key = api_key
        self._httpClient = httpClient if not None else ClientSession()

    async def _async_fetch_data(self, url: str, rawDict: bool=False):
        """Makes a request to the CheckWX API"""
        headers = {f"{API_KEY_HEADER}": f"{self.api_key}"}
        async with self._httpClient.get(url, headers=headers) as response:
            try:
              response.raise_for_status()
              
              return await response.json()['data'] if not rawDict else await response.json()
            except HTTPError as e:
                raise ApiError(e)
            except JSONDecodeError as e:
                raise InvalidResponsePayload(e.msg)

    async def async_get_station_info(self, icao_codes: str, decoded: bool=True) -> Dict:
        """Get information for one or several stations"""
        if not self._is_valid_icao_code(icao_codes):
            raise InvalidICAOCodeError("Your ICAO codes must be a string")

        url = f"{BASE_URL}{STATION_ENDPOINT}/{icao_codes}"

        data = await _async_fetch_data(url)

    async def async_get_metar(self, icao_codes: str, decoded: bool=True) -> Dict:
        """Get decoded METAR for one or several stations"""
        if not self._is_valid_icao_code(icao_codes):
            raise InvalidICAOCodeError("Your ICAO codes must be a string")

        url = f"{BASE_URL}{METAR_ENDPOINT}/{icao_codes}"
        if decoded:
            url += "/decoded"
            
        data = await _async_fetch_data(url)

    async def async_get_taf(self, icao_codes: str, decoded: bool=True) -> Dict:
        """Get decoded TAF for one or several stations"""
        if not self._is_valid_icao_code(icao_codes):
            raise InvalidICAOCodeError("Your ICAO codes must be a string")

        url = f"{BASE_URL}{TAF_ENDPOINT}/{icao_codes}"
        if decoded:
            url += "/decoded"
            
        data = await _async_fetch_data(url)

    async def async_get_stats(self) -> Dict:
        """Get stats for the user account"""

        url = f"{BASE_URL}{STATS_ENDPOINT}"
            
        data = await _async_fetch_data(url, False)

    @staticmethod
    def _is_valid_api_key(self, api_key: str) -> bool:
        """Validates the API Key"""
        try:
            assert isinstance(api_key, str)
            assert len(api_key) == 26
        except AssertionError:
            return False
        
        return True

    @staticmethod
    def _is_valid_icao_code(self, icao_code: str) -> bool:
        """Validates the station ICAO code"""
        try:
            assert isinstance(icao_code, str)
        except AssertionError:
            return False
        
        return True

class ApiError(Exception):
    """The request to CheckWXAPi failed with an error"""

    def __init__(self, message: str):
        """Initialize error"""
        super.__init__(message)

class InvalidICAOCodeError(Exception):
    """Used to signal that the ICAO code is invalid"""

    def __init__(self, message: str):
        """Initialize error"""
        super.__init__(message)

class InvalidApiKeyError(Exception):
    """The API Key is not valid"""

    def __init__(self, message: str):
        """Initialize error"""
        super.__init__(message)

class InvalidResponsePayload(Exception):
    """The data received from CheckWXAPi is not valid"""

    def __init__(self, message: str):
        """Initialize error"""
        super.__init__(message)

