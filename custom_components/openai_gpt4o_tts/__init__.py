import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .gpt4o import GPT4oClient
from .gpt4o_chat import GPT4oChatClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up GPT-4o integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Initialize and store both TTS and Chat clients
    tts_client = GPT4oClient(hass, entry)
    chat_client = GPT4oChatClient(hass, entry)

    hass.data[DOMAIN][entry.entry_id] = {
        "tts_client": tts_client,
        "chat_client": chat_client,
    }

    # Forward setup to platform(s) — like TTS
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload GPT-4o config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
