"""Configure tests for the OpenSky integration."""
from collections.abc import Awaitable, Callable
from unittest.mock import patch

import pytest
from python_opensky import StatesResponse

from homeassistant.components.opensky.const import CONF_ALTITUDE, DOMAIN
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_RADIUS
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from tests.common import MockConfigEntry

ComponentSetup = Callable[[MockConfigEntry], Awaitable[None]]


@pytest.fixture(name="config_entry")
def mock_config_entry() -> MockConfigEntry:
    """Create OpenSky entry in Home Assistant."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="OpenSky",
        data={
            CONF_LATITUDE: 0.0,
            CONF_LONGITUDE: 0.0,
        },
        options={
            CONF_RADIUS: 10.0,
            CONF_ALTITUDE: 0.0,
        },
    )


@pytest.fixture(name="setup_integration")
async def mock_setup_integration(
    hass: HomeAssistant,
) -> Callable[[MockConfigEntry], Awaitable[None]]:
    """Fixture for setting up the component."""

    async def func(mock_config_entry: MockConfigEntry) -> None:
        mock_config_entry.add_to_hass(hass)
        with patch(
            "python_opensky.OpenSky.get_states",
            return_value=StatesResponse(states=[], time=0),
        ):
            assert await async_setup_component(hass, DOMAIN, {})
            await hass.async_block_till_done()

    return func
