"""Thin client for WeatherAPI.com."""

from __future__ import annotations

from dataclasses import dataclass

import requests

from farmflow import config


class WeatherError(RuntimeError):
    """Raised when weather data cannot be fetched or parsed."""


@dataclass(frozen=True)
class CurrentWeather:
    temperature_c: float
    humidity: float
    rainfall_mm: float


@dataclass(frozen=True)
class DayForecast:
    date: str
    rainfall_mm: float


def _get(endpoint: str, **params) -> dict:
    if not config.WEATHER_API_KEY:
        raise WeatherError("WEATHER_API_KEY is not set")
    try:
        response = requests.get(
            f"{config.WEATHER_API_BASE_URL}/{endpoint}",
            params={"key": config.WEATHER_API_KEY, **params},
            timeout=config.HTTP_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as exc:
        raise WeatherError(f"Weather request failed: {exc}") from exc


def get_current_weather(city: str) -> CurrentWeather:
    current = _get("current.json", q=city).get("current")
    if current is None:
        raise WeatherError("Unexpected response from weather API")
    return CurrentWeather(
        temperature_c=current["temp_c"],
        humidity=current["humidity"],
        rainfall_mm=current.get("precip_mm", 0),
    )


def get_forecast(city: str, days: int = 7) -> list[DayForecast]:
    forecast_days = _get("forecast.json", q=city, days=days)["forecast"]["forecastday"]
    return [
        DayForecast(date=d["date"], rainfall_mm=d["day"].get("totalprecip_mm", 0))
        for d in forecast_days
    ]
