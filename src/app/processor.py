"""Processor module for dividend-based stock analysis.

This module enriches messages with dividend-related insights,
such as dividend yield classification or recent dividend trends.
"""

from typing import Any

from app.utils.setup_logger import setup_logger
from app.utils.types import validate_dict

# Initialize module-level logger
logger = setup_logger(__name__)


def process(payloads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Process a batch of dividend data messages.

    Adds classification labels based on dividend yield and flags for recent changes.

    Parameters
    ----------
    payloads : list[dict[str, Any]]
        List of incoming messages to process.

    Returns
    -------
    list[dict[str, Any]]
        Enriched messages with dividend metrics.

    """
    results: list[dict[str, Any]] = []

    for item in payloads:
        if not validate_dict(item, ["symbol", "dividend_yield"]):
            logger.warning("⚠️ Skipping message missing required fields: %s", item)
            continue

        try:
            yield_pct = float(item["dividend_yield"])
            if yield_pct >= 5.0:
                label = "high"
            elif yield_pct >= 2.0:
                label = "moderate"
            else:
                label = "low"

            item["dividend_classification"] = label
            logger.debug("📈 %s dividend yield: %.2f%% → %s", item["symbol"], yield_pct, label)

            results.append(item)

        except Exception as e:
            logger.exception(
                "❌ Failed to process dividend data for %s: %s", item.get("symbol", "unknown"), e
            )

    return results
