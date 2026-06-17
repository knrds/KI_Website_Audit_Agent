from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


def normalize_url(raw_url: str) -> str:
    """Return a URL with scheme so Playwright can open it later."""

    value = raw_url.strip()
    if not value:
        return value

    parsed = urlparse(value)
    if parsed.scheme:
        return value

    return f"https://{value}"


def safe_filename_from_url(url: str) -> str:
    """Create a compact filename stem from a URL."""

    parsed = urlparse(url)
    host = parsed.netloc or parsed.path or "website"
    stem = re.sub(r"[^a-zA-Z0-9_-]+", "_", host).strip("_").lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{stem or 'website'}_{timestamp}"


def ensure_directory(path: str | Path) -> Path:
    """Create a directory if needed and return it as Path."""

    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory
