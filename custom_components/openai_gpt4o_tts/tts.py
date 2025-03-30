import logging
import re

from homeassistant.components.tts import (
    ATTR_AUDIO_OUTPUT,
    ATTR_VOICE,
    TextToSpeechEntity,
    TtsAudioType,
    Voice,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, OPENAI_TTS_VOICES
from .gpt4o import GPT4oClient, GPT4oChatClient

_LOGGER = logging.getLogger(__name__)


def should_use_web_search(text: str, options: dict) -> bool:
    if options.get("use_web_search", False):
        return True

    search_keywords = ["weather", "news", "today", "score", "price", "update", "current", "latest"]
    question_words = ["what", "who", "how", "where", "why", "when"]

    lower_text = text.strip().lower()
    if any(lower_text.startswith(word) for word in question_words):
        return True
    if any(word in lower_text for word in search_keywords):
        return True

    return False


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    """Set up GPT-4o TTS with optional web search from a config entry."""
    client = hass.data[DOMAIN][config_entry.entry_id]
    chat_client = GPT4oChatClient(hass, config_entry)
    async_add_entities([OpenAIGPT4oTTSProvider(config_entry, client, chat_client)])


class OpenAIGPT4oTTSProvider(TextToSpeechEntity):
    """GPT-4o TTS provider with optional web search."""

    def __init__(self, config_entry: ConfigEntry, client: GPT4oClient, chat_client: GPT4oChatClient) -> None:
        self._config_entry = config_entry
        self._client = client
        self._chat_client = chat_client
        self._name = "OpenAI GPT-4o Mini TTS"
        self._attr_unique_id = f"{config_entry.entry_id}-tts"

    @property
    def name(self) -> str:
        return self._name

    @property
    def default_language(self) -> str:
        return "en"

    @property
    def supported_languages(self) -> list[str]:
        return ["en"]

    @property
    def default_options(self) -> dict:
        return {ATTR_AUDIO_OUTPUT: "mp3"}

    @property
    def supported_options(self) -> list[str]:
        return [ATTR_VOICE, "instructions", ATTR_AUDIO_OUTPUT, "use_web_search"]

    async def async_get_tts_audio(
        self, message: str, language: str, options: dict | None = None
    ) -> TtsAudioType:
        if options is None:
            options = {}

        if should_use_web_search(message, options):
            _LOGGER.debug("Routing message through GPT-4o chat + web search flow")
            response = await self._chat_client.get_web_enhanced_response(message)
            if not response:
                _LOGGER.warning("Chat + web search failed, falling back to raw TTS")
                return await self._client.get_tts_audio(message, options)
            return await self._client.get_tts_audio(response, options)

        return await self._client.get_tts_audio(message, options)

    def async_get_supported_voices(self, language: str) -> list[Voice] | None:
        return [Voice(vid, vid.capitalize()) for vid in OPENAI_TTS_VOICES]

    @property
    def extra_state_attributes(self) -> dict:
        return {"provider": self._name}
