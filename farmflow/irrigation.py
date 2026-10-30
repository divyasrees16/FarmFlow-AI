"""Rule-based irrigation logic (pure functions, no I/O)."""

from __future__ import annotations

from collections.abc import Callable, Sequence

from farmflow.weather import DayForecast

FLOOD = "Flood Irrigation"
DRIP = "Drip Irrigation"
SPRINKLER = "Sprinkler Irrigation"
FURROW = "Furrow Irrigation"


def _rice(humidity: float, rainfall: float) -> str:
    if rainfall > 100:
        return FLOOD
    if rainfall > 50 and humidity > 60:
        return DRIP
    return SPRINKLER


def _wheat(humidity: float, rainfall: float) -> str:
    if rainfall < 30:
        return SPRINKLER
    if rainfall <= 70:
        return DRIP
    return FLOOD


def _sugarcane(humidity: float, rainfall: float) -> str:
    if rainfall > 120:
        return FURROW
    if rainfall > 60:
        return DRIP
    return SPRINKLER


def _maize(humidity: float, rainfall: float) -> str:
    if humidity > 65 and rainfall > 80:
        return FLOOD
    if humidity > 50:
        return DRIP
    return SPRINKLER


def _cotton(humidity: float, rainfall: float) -> str:
    return DRIP if humidity < 40 or rainfall < 30 else SPRINKLER


def _millets(humidity: float, rainfall: float) -> str:
    return DRIP if rainfall < 40 else SPRINKLER


def _groundnut(humidity: float, rainfall: float) -> str:
    return DRIP if rainfall < 50 and humidity < 50 else SPRINKLER


_RULES: dict[str, Callable[[float, float], str]] = {
    "rice": _rice,
    "wheat": _wheat,
    "sugarcane": _sugarcane,
    "maize": _maize,
    "cotton": _cotton,
    "millets": _millets,
    "groundnut": _groundnut,
}


def recommend_method(crop: str, humidity: float, rainfall: float) -> str:
    """Pick an irrigation method for a crop given current humidity (%) and rainfall (mm)."""
    rule = _RULES.get(crop.lower())
    return rule(humidity, rainfall) if rule else SPRINKLER


def rain_alerts(forecast: Sequence[DayForecast]) -> list[str]:
    """Per-day alerts for very heavy or very low forecast rainfall."""
    alerts = []
    for day in forecast:
        if day.rainfall_mm > 50:
            alerts.append(f"📅 {day.date}: ⚠️ Heavy rain expected – avoid irrigation.")
        elif day.rainfall_mm < 1:
            alerts.append(f"📅 {day.date}: 💧 Low rain – consider increasing irrigation.")
    return alerts


def weekly_advisory(forecast: Sequence[DayForecast]) -> tuple[str, str]:
    """Return (level, message) for the week; level is 'low', 'high' or 'moderate'."""
    avg = sum(d.rainfall_mm for d in forecast) / len(forecast)
    if avg < 5:
        return "low", "📢 Low rainfall expected this week. Increase irrigation frequency or use drip system."
    if avg > 40:
        return "high", "📢 Heavy rainfall expected. Avoid overwatering. Ensure field drainage."
    return "moderate", "✅ Weather conditions are moderate. Continue usual irrigation practice."