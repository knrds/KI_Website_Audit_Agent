from __future__ import annotations

import re
import json
import time
from pathlib import Path
from urllib.parse import urlparse

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

STRONG_CTA_KEYWORDS = (
    "angebot anfragen",
    "termin buchen",
    "jetzt anrufen",
    "kostenlos beraten",
    "beratung vereinbaren",
    "rueckruf",
    "rückruf",
    "kontakt aufnehmen",
    "reserve",
    "book",
    "call now",
    "get quote",
)

BENEFIT_KEYWORDS = (
    "kostenlos",
    "schnell",
    "regional",
    "lokal",
    "zuverlaessig",
    "zuverlässig",
    "professionell",
    "erfahren",
    "individuell",
    "fair",
)

SERVICE_KEYWORDS = (
    "leistung",
    "leistungen",
    "service",
    "services",
    "angebot",
    "angebote",
    "beratung",
    "reparatur",
    "montage",
    "planung",
    "verkauf",
    "lieferung",
)

LOCAL_KEYWORDS = (
    "in der naehe",
    "in der nähe",
    "vor ort",
    "regional",
    "lokal",
    "umgebung",
    "region",
    "stadt",
    "landkreis",
)

TRUST_KEYWORDS = (
    "bewertung",
    "bewertungen",
    "rezension",
    "rezensionen",
    "kundenstimme",
    "kundenstimmen",
    "testimonial",
    "referenz",
    "referenzen",
    "meister",
    "zertifiziert",
    "garantie",
    "erfahrung",
    "seit ",
    "trusted",
)

OFFER_KEYWORDS = (
    "preis",
    "preise",
    "angebot",
    "kostenvoranschlag",
    "paket",
    "kostenlos",
    "rabatt",
    "aktion",
)

IMPRINT_KEYWORDS = ("impressum", "imprint", "legal notice")
PRIVACY_KEYWORDS = ("datenschutz", "privacy", "privacy policy")
CONTACT_KEYWORDS = ("kontakt", "contact", "telefon", "phone", "e-mail", "email")
EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_PATTERN = re.compile(r"(\+?\d[\d\s()./-]{6,}\d)")
ZIP_CITY_PATTERN = re.compile(r"\b\d{5}\s+[A-ZÄÖÜ][A-Za-zÄÖÜäöüß.-]+")
STREET_PATTERN = re.compile(
    r"\b[A-ZÄÖÜ][A-Za-zÄÖÜäöüß.-]+\s+(straße|strasse|weg|platz|allee|ring|gasse)\b",
    re.I,
)
OPENING_HOURS_PATTERN = re.compile(
    r"\b(mo|di|mi|do|fr|sa|so|montag|dienstag|mittwoch|donnerstag|freitag|samstag|sonntag)\b.*\d{1,2}[:.]\d{2}",
    re.I,
)
WORD_PATTERN = re.compile(r"\b[\wÄÖÜäöüß-]{3,}\b")


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
    signals.title_length = len(signals.page_title or "")
    signals.meta_description = _find_meta_description(soup)
    signals.meta_description_length = len(signals.meta_description or "")

    h1_tags = [_clean_text(tag.get_text(" ", strip=True)) for tag in soup.find_all("h1")]
    h1_values = [value for value in h1_tags if value]
    signals.h1 = h1_values[0] if h1_values else None
    signals.h1_count = len(h1_values)
    signals.h2_count = len([tag for tag in soup.find_all("h2") if _clean_text(tag.get_text(" ", strip=True))])

    page_text = soup.get_text(" ", strip=True)
    lowered_text = page_text.lower()
    signals.word_count = len(WORD_PATTERN.findall(page_text))

    link_texts = _collect_link_and_button_texts(soup)
    signals.call_to_action_texts = _find_matching_texts(link_texts, CTA_KEYWORDS, limit=6)
    signals.has_call_to_action = bool(signals.call_to_action_texts)
    signals.strong_call_to_action_texts = _find_matching_texts(link_texts, STRONG_CTA_KEYWORDS, limit=4)
    signals.has_strong_call_to_action = bool(signals.strong_call_to_action_texts)

    signals.has_imprint = _has_keyword_in_links_or_text(soup, lowered_text, IMPRINT_KEYWORDS)
    signals.has_privacy_policy = _has_keyword_in_links_or_text(soup, lowered_text, PRIVACY_KEYWORDS)

    signals.contact_signals = _find_contact_signals(soup, page_text, lowered_text)
    signals.has_contact_info = bool(signals.contact_signals)
    signals.has_address = _has_address(page_text)
    signals.has_opening_hours = _has_opening_hours(page_text, lowered_text)

    title_context = " ".join(value for value in (signals.page_title, signals.meta_description, signals.h1) if value)
    lowered_title_context = title_context.lower()
    signals.title_has_business_keyword = any(keyword in lowered_title_context for keyword in SERVICE_KEYWORDS)
    signals.title_has_local_keyword = any(keyword in lowered_title_context for keyword in LOCAL_KEYWORDS) or signals.has_address
    signals.meta_description_has_benefit = any(
        keyword in (signals.meta_description or "").lower() for keyword in BENEFIT_KEYWORDS
    )
    signals.meta_description_has_cta = any(
        keyword in (signals.meta_description or "").lower() for keyword in CTA_KEYWORDS
    )

    signals.local_seo_signals = _find_local_seo_signals(page_text, lowered_text)
    signals.has_local_seo_signals = bool(signals.local_seo_signals)
    signals.service_signals = _find_signal_matches(lowered_text, SERVICE_KEYWORDS, "Leistungsbegriff")
    signals.has_service_keywords = bool(signals.service_signals)
    signals.trust_signals = _find_signal_matches(lowered_text, TRUST_KEYWORDS, "Trust-Signal")
    signals.has_trust_signals = bool(signals.trust_signals)
    signals.has_reviews_or_testimonials = any(keyword in lowered_text for keyword in TRUST_KEYWORDS[:6])
    signals.has_offer_or_price_signal = any(keyword in lowered_text for keyword in OFFER_KEYWORDS)

    signals.has_viewport_meta = soup.find("meta", attrs={"name": re.compile(r"^viewport$", re.I)}) is not None
    signals.has_canonical = soup.find("link", attrs={"rel": re.compile(r"canonical", re.I)}) is not None
    signals.has_noindex = _has_noindex(soup)
    signals.has_open_graph = _has_open_graph(soup)
    signals.structured_data_types = _extract_structured_data_types(soup)
    signals.has_structured_data = bool(signals.structured_data_types)
    signals.has_local_business_schema = any("localbusiness" in value.lower() for value in signals.structured_data_types)

    signals.internal_link_count, signals.external_link_count = _count_links(soup, signals.final_url or signals.url)
    signals.image_count, signals.images_missing_alt = _count_images(soup)
    signals.seo_warnings = _build_seo_warnings(signals)


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


def _has_address(page_text: str) -> bool:
    return ZIP_CITY_PATTERN.search(page_text) is not None or STREET_PATTERN.search(page_text) is not None


def _has_opening_hours(page_text: str, lowered_text: str) -> bool:
    if OPENING_HOURS_PATTERN.search(page_text):
        return True
    return "oeffnungszeiten" in lowered_text or "öffnungszeiten" in lowered_text or "opening hours" in lowered_text


def _find_local_seo_signals(page_text: str, lowered_text: str) -> list[str]:
    signals: list[str] = []
    zip_city = ZIP_CITY_PATTERN.search(page_text)
    street = STREET_PATTERN.search(page_text)
    if zip_city:
        signals.append(f"PLZ/Ort gefunden: {zip_city.group(0)}")
    if street:
        signals.append(f"Adresse gefunden: {street.group(0)}")
    for keyword in LOCAL_KEYWORDS:
        if keyword in lowered_text:
            signals.append(f"Lokaler Begriff: {keyword}")
    return _deduplicate(signals)[:6]


def _find_signal_matches(lowered_text: str, keywords: tuple[str, ...], label: str) -> list[str]:
    matches = [f"{label}: {keyword}" for keyword in keywords if keyword in lowered_text]
    return _deduplicate(matches)[:6]


def _has_noindex(soup: BeautifulSoup) -> bool:
    robots_meta = soup.find("meta", attrs={"name": re.compile(r"^robots$", re.I)})
    content = _clean_text(robots_meta.get("content")) if robots_meta else None
    return bool(content and "noindex" in content.lower())


def _has_open_graph(soup: BeautifulSoup) -> bool:
    has_title = soup.find("meta", attrs={"property": re.compile(r"^og:title$", re.I)}) is not None
    has_description = soup.find("meta", attrs={"property": re.compile(r"^og:description$", re.I)}) is not None
    has_image = soup.find("meta", attrs={"property": re.compile(r"^og:image$", re.I)}) is not None
    return has_title and has_description and has_image


def _extract_structured_data_types(soup: BeautifulSoup) -> list[str]:
    types: list[str] = []

    for script in soup.find_all("script", attrs={"type": re.compile(r"ld\+json", re.I)}):
        raw = script.string or script.get_text()
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        types.extend(_collect_schema_types(data))

    for tag in soup.find_all(attrs={"itemtype": True}):
        itemtype = _clean_text(tag.get("itemtype"))
        if itemtype:
            types.append(itemtype.rsplit("/", 1)[-1])

    return _deduplicate([value for value in types if value])[:12]


def _collect_schema_types(value: object) -> list[str]:
    if isinstance(value, dict):
        result: list[str] = []
        schema_type = value.get("@type")
        if isinstance(schema_type, str):
            result.append(schema_type)
        elif isinstance(schema_type, list):
            result.extend(str(item) for item in schema_type)
        for item in value.values():
            result.extend(_collect_schema_types(item))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(_collect_schema_types(item))
        return result
    return []


def _count_links(soup: BeautifulSoup, base_url: str) -> tuple[int, int]:
    base_host = urlparse(base_url).netloc.lower()
    internal = 0
    external = 0

    for link in soup.find_all("a", href=True):
        href = str(link.get("href")).strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        parsed = urlparse(href)
        if not parsed.netloc or parsed.netloc.lower() == base_host:
            internal += 1
        else:
            external += 1

    return internal, external


def _count_images(soup: BeautifulSoup) -> tuple[int, int]:
    images = soup.find_all("img")
    missing_alt = 0
    for image in images:
        alt = _clean_text(image.get("alt"))
        if not alt:
            missing_alt += 1
    return len(images), missing_alt


def _build_seo_warnings(signals: WebsiteSignals) -> list[str]:
    warnings: list[str] = []

    if signals.has_noindex:
        warnings.append("Noindex-Meta-Tag gefunden: Seite kann aus Suchergebnissen ausgeschlossen sein.")
    if signals.title_length and not 30 <= signals.title_length <= 65:
        warnings.append(f"Title-Laenge kritisch: {signals.title_length} Zeichen.")
    if signals.meta_description_length and not 80 <= signals.meta_description_length <= 170:
        warnings.append(f"Meta-Description-Laenge schwach: {signals.meta_description_length} Zeichen.")
    if signals.word_count < 250:
        warnings.append(f"Sehr wenig sichtbarer Text: nur {signals.word_count} Woerter.")
    if signals.image_count and signals.images_missing_alt / signals.image_count > 0.4:
        warnings.append(f"Viele Bilder ohne Alt-Text: {signals.images_missing_alt} von {signals.image_count}.")
    if not signals.has_strong_call_to_action:
        warnings.append("Kein starker conversion-orientierter CTA erkannt.")
    if not signals.has_local_business_schema:
        warnings.append("Kein LocalBusiness Structured Data erkannt.")

    return warnings


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
