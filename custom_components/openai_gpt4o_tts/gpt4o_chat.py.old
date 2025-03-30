import logging
import requests

_LOGGER = logging.getLogger(__name__)

class GPT4oChatClient:
    """Handles /v1/chat/completions with web search tool enabled."""

    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry
        self._api_key = entry.data["api_key"]
        self._model = "gpt-4o"  # not the mini-tts version

    async def get_web_enhanced_response(self, prompt: str) -> str | None:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self._model,
            "messages": [{"role": "user", "content": prompt}],
            "tools": [{"type": "web_search"}],
            "tool_choice": "auto"
        }

        def do_request():
            try:
                resp = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                resp.raise_for_status()
                data = resp.json()
                message = data.get("choices", [{}])[0].get("message", {})
                content = message.get("content")
                if not content:
                    _LOGGER.warning("No content returned from chat response")
                return content
            except Exception as e:
                _LOGGER.error("Failed to get web-enhanced chat response: %s", e)
                return None

        return await self.hass.async_add_executor_job(do_request)
