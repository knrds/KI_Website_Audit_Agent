from __future__ import annotations

import re
import time
from pathlib import Path

from bs4 import BeautifulSoup
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from models import WebsiteSignals
from utils import ensure_directory, normalize_url, safe_filename_from_url


BASE_DIR = Path(__file__).resolve().parent
SCREENSHOT_DIR = BASE_DIR / "outputs" / "screenshots"
REQUEST_TIMEOUT_MS = 15_000

CTA_KEYWORDS = (
    "angebot",
    "anfrage",
    "anrufen",
    "beratung",
    "bestellen",
    "buchen",
    "jetzt",
    "kontakt",
    "reservieren",
    "termin",
    "call",
    "contact",
    "quote",
)

IMPRINT_KEYWORDS = ("impressum", "imprint", "legal notice")
PRIVACY_KEYWORDS = ("datenschutz", "privacy", "privacy policy")
CONTACT_KEYWORDS = ("kontakt", "contact", "telefon", "phone", "e-mail", "email")
EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_PATTERN = re.compile(r"(\+?\d[\d\s()./-]{6,}\d)")


def run_audit(raw_url: str) -> WebsiteSignals:
    """Load one website, extract basic signals and store a screenshot."""

    url = normalize_url(raw_url)
    signals = WebsiteSignals(url=url)
    start = time.perf_counter()

    try:
        with sync_playwright() as playwright:
            browser = None
            context = None
            try:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(
                    ignore_https_errors=True,
                    locale="de-DE",
                    viewport={"width": 1440, "height": 1000},
                )
                page = context.new_page()
                response = page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=REQUEST_TIMEOUT_MS,
                )

                try:
                    page.wait_for_load_state("networkidle", timeout=5_000)
                except PlaywrightTimeoutError:
                    signals.notes.append("Networkidle wurde nicht erreicht; DOM wurde trotzdem analysiert.")

                signals.load_time_ms = int((time.perf_counter() - start) * 1000)
                signals.final_url = page.url
                signals.reachable = response is not None and response.ok
                signals.status_code = response.status if response else None

                html = page.content()
                _fill_html_signals(signals, html)
                signals.screenshot_path = _save_screenshot(page, signals.final_url or url)
            finally:
                if context:
                    context.close()
                if browser:
                    browser.close()

    except PlaywrightTimeoutError:
        signals.load_time_ms = int((time.perf_counter() - start) * 1000)
        signals.notes.append(f"Timeout nach {REQUEST_TIMEOUT_MS // 1000} Sekunden.")
    except PlaywrightError as exc:
        signals.load_time_ms = int((time.perf_counter() - start) * 1000)
        signals.notes.append(_friendly_playwright_error(str(exc)))

    return signals


def _fill_html_signals(signals: WebsiteSignals, html: str) -> None:
    soup = BeautifulSoup(html, "html.parser")

    signals.page_title = _clean_text(soup.title.string if soup.title else None)
    signals.meta_description = _find_meta_description(soup)

    h1_tags = [_clean_text(tag.get_text(" ", strip=True)) for tag in soup.find_all("h1")]
    h1_values = [value for value in h1_tags if value]
    signals.h1 = h1_values[0] if h1_values else None
    signals.h1_count = len(h1_values)

    page_text = soup.get_text(" ", strip=True)
    lowered_text = page_text.lower()

    link_texts = _collect_link_and_button_texts(soup)
    signals.call_to_action_texts = _find_matching_texts(link_texts, CTA_KEYWORDS, limit=6)
    signals.has_call_to_action = bool(signals.call_to_action_texts)

    signals.has_imprint = _has_keyword_in_links_or_text(soup, lowered_text, IMPRINT_KEYWORDS)
    signals.has_privacy_policy = _has_keyword_in_links_or_text(soup, lowered_text, PRIVACY_KEYWORDS)

    signals.contact_signals = _find_contact_signals(soup, page_text, lowered_text)
    signals.has_contact_info = bool(signals.contact_signals)


def _find_meta_description(soup: BeautifulSoup) -> str | None:
    description = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    if not description:
        description = soup.find("meta", attrs={"property": re.compile(r"^og:description$", re.I)})

    content = description.get("content") if description else None
    return _clean_text(content)


def _collect_link_and_button_texts(soup: BeautifulSoup) -> list[str]:
    candidates: list[str] = []
    for tag in soup.find_all(["a", "button"]):
        text = _clean_text(tag.get_text(" ", strip=True))
        aria_label = _clean_text(tag.get("aria-label"))
        title = _clean_text(tag.get("title"))
        for value in (text, aria_label, title):
            if value and value not in candidates:
                candidates.append(value)
    return candidates


def _find_matching_texts(values: list[str], keywords: tuple[str, ...], limit: int) -> list[str]:
    matches: list[str] = []
    for value in values:
        lowered = value.lower()
        if any(keyword in lowered for keyword in keywords):
            matches.append(value)
        if len(matches) >= limit:
            break
    return matches


def _has_keyword_in_links_or_text(
    soup: BeautifulSoup,
    lowered_text: str,
    keywords: tuple[str, ...],
) -> bool:
    for link in soup.find_all("a"):
        link_text = _clean_text(link.get_text(" ", strip=True)) or ""
        href = _clean_text(link.get("href")) or ""
        combined = f"{link_text} {href}".lower()
        if any(keyword in combined for keyword in keywords):
            return True

    return any(keyword in lowered_text for keyword in keywords)


def _find_contact_signals(soup: BeautifulSoup, page_text: str, lowered_text: str) -> list[str]:
    signals: list[str] = []

    email = EMAIL_PATTERN.search(page_text)
    if email:
        signals.append(f"E-Mail gefunden: {email.group(0)}")

    phone = PHONE_PATTERN.search(page_text)
    if phone:
        signals.append(f"Telefonnummer gefunden: {phone.group(0).strip()}")

    if soup.find("a", href=re.compile(r"^mailto:", re.I)):
        signals.append("Mailto-Link gefunden")

    if soup.find("a", href=re.compile(r"^tel:", re.I)):
        signals.append("Telefon-Link gefunden")

    if any(keyword in lowered_text for keyword in CONTACT_KEYWORDS):
        signals.append("Kontaktbereich oder Kontaktbegriff gefunden")

    return _deduplicate(signals)


def _save_screenshot(page, url: str) -> str:
    screenshot_dir = ensure_directory(SCREENSHOT_DIR)
    path = screenshot_dir / f"{safe_filename_from_url(url)}.png"
    page.screenshot(path=str(path), full_page=True)
    return str(path)


def _clean_text(value: object) -> str | None:
    if value is None:
        return None

    cleaned = re.sub(r"\s+", " ", str(value)).strip()
    return cleaned or None


def _deduplicate(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def _friendly_playwright_error(message: str) -> str:
    if "Executable doesn't exist" in message or "playwright install" in message.lower():
        return "Playwright-Browser fehlt. Bitte ausfuehren: playwright install chromium"

    first_line = message.splitlines()[0] if message else "Unbekannter Playwright-Fehler."
    return f"Playwright-Fehler: {first_line}"
