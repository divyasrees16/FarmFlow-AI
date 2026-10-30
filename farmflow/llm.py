"""LLM-backed natural-language explanations (Groq, via the OpenAI-compatible API)."""

from __future__ import annotations

import logging
from functools import lru_cache

from openai import OpenAI

from farmflow import config

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _client() -> OpenAI:
    if not config.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set")
    return OpenAI(api_key=config.GROQ_API_KEY, base_url=config.GROQ_BASE_URL)


last_error: str = ""


def unavailable_message() -> str:
    """User-facing text for when an explanation could not be generated."""
    detail = f" ({last_error})" if last_error else ""
    return f"AI explanation is currently unavailable{detail}."


def _chat(system: str, prompt: str) -> str | None:
    """Send one chat completion. Returns None if the LLM is unavailable."""
    global last_error
    last_error = ""
    extra = {}
    if "gpt-oss" in config.GROQ_MODEL:
        # Reasoning models spend tokens "thinking"; keep that small so an answer fits.
        extra["extra_body"] = {"reasoning_effort": "low"}
    try:
        response = _client().chat.completions.create(
            model=config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1500,
            **extra,
        )
        choice = response.choices[0]
        content = (choice.message.content or "").strip()
        if not content:
            last_error = f"model returned no text (finish_reason={choice.finish_reason})"
            logger.error("LLM returned empty content: %s", last_error)
            return None
        return content
    except Exception as exc:  # network, auth, quota, bad model name...
        last_error = f"{type(exc).__name__}: {exc}"[:300]
        logger.exception("LLM request failed")
        return None


def irrigation_explanation(
    city: str, crop: str, temperature: float, humidity: float, rainfall: float, method: str
) -> str | None:
    prompt = (
        f"A farmer in {city} is growing {crop}. Today's weather: {temperature}°C, "
        f"humidity {humidity}%, rainfall {rainfall} mm. You suggested {method} as the "
        "irrigation method. Explain clearly in simple words (about 50 words):\n"
        "1. Why this method suits the current conditions.\n"
        "2. What happens if rainfall decreases tomorrow."
    )
    return _chat("You are an expert agricultural assistant.", prompt)


def crop_explanation(
    n: float,
    p: float,
    k: float,
    ph: float,
    temperature: float,
    humidity: float,
    rainfall: float,
    crops: list[str],
) -> str | None:
    prompt = (
        "A farmer has provided the following soil and weather data:\n"
        f"- Nitrogen: {n}\n- Phosphorous: {p}\n- Potassium: {k}\n- pH value: {ph}\n"
        f"- Temperature: {temperature}°C\n- Humidity: {humidity}%\n- Rainfall: {rainfall} mm\n\n"
        f"The recommended crops are: {', '.join(crops[:3])}.\n"
        "Explain in a simple paragraph why these crops are suitable for these conditions "
        "(avoid bullet points or repetition)."
    )
    return _chat("You are a helpful crop advisor.", prompt)


def disease_explanation(disease_name: str) -> str | None:
    prompt = (
        f"A plant disease has been detected: {disease_name}.\n"
        "Explain clearly and simply:\n"
        "1. Symptoms of this disease.\n"
        "2. Recommended treatment steps.\n"
        "3. Prevention methods for farmers.\n"
        "Use about 100 words in a friendly tone."
    )
    return _chat("You are an expert agricultural assistant.", prompt)