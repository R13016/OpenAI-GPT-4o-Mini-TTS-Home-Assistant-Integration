# 🗣️ OpenAI GPT-4o Mini TTS for Home Assistant

This custom integration brings high-quality text-to-speech (TTS) to Home Assistant using [OpenAI's GPT-4o TTS API](https://platform.openai.com/docs/guides/text-to-speech), with optional web search support for real-time information like weather, news, and more.

---

## ✨ Features

- 🎤 High-quality speech generation using `gpt-4o-mini-tts`
- 🌐 Optional dynamic web search via GPT-4o's `web_search` tool
- 🎛️ Customizable voice, tone, affect, pronunciation, pauses, and emotion
- 🔁 Supports multiple OpenAI voices
- 🧠 Automatically detects when web search is useful (e.g. “What’s the weather?”)
- 📦 Fully integrated with Home Assistant's TTS platform

---

## 🔧 Installation

1. **Copy the repository folder** to:  
   `config/custom_components/openai_gpt4o_tts/`

2. **Restart Home Assistant**

3. **Add the integration** via **Settings > Devices & Services > Add Integration**  
   Search for **OpenAI GPT-4o Mini TTS**.

---

## 🛠 Configuration Options

During setup or in the options panel, you can define:

| Field | Description |
|-------|-------------|
| `API Key` | Your OpenAI API key |
| `Voice` | One of the supported OpenAI TTS voices |
| `Affect / Personality` | Style or persona of the voice |
| `Tone` | Voice tone (e.g., friendly, formal) |
| `Pronunciation` | Dictates speech clarity and pacing |
| `Pause Strategy` | Controls pauses for natural delivery |
| `Emotion` | Expressiveness and warmth |
| `Use Web Search` | Enable real-time responses via GPT-4o + web |

You can adjust these in **Settings > Devices & Services > OpenAI GPT-4o Mini TTS > Configure**.

---

## 🗣️ Using the TTS Service

Service:  
```yaml
service: tts.openai_gpt4o_tts_say
