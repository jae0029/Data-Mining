from __future__ import annotations

import logging
import re
from pathlib import Path
from time import sleep
from urllib.parse import parse_qs, urljoin, urlparse
from bassmaster_master_map import (
    TOURNAMENT_INVENTORY,
    match_tournament_metadata,
)

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "https://bassmasterfantasy.com"
LIST_URL = f"{BASE_URL}/TournamentResultsList.aspx"

OUTPUT_DIR = Path("bassmaster_output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RESULTS_FILE = OUTPUT_DIR / "bassmaster_complete_participant_records.csv"
AUDIT_FILE = OUTPUT_DIR / "bassmaster_scrape_audit.csv"

REQUEST_TIMEOUT = (10, 30)
REQUEST_DELAY_SECONDS = 1.0

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    )
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            OUTPUT_DIR / "bassmaster_scraper.log",
            encoding="utf-8"
        ),
    ],
)

logger = logging.getLogger(__name__)

# Comprehensive Master Data Layer (2012-2026) to clean titles and map variables
# This systematically corrects fantasy shorthand names to precise historical specs
TOURNAMENT_MASTER_MAP = {
    # 2026 SEASON MAP
    ("2026", "1"): {"clean_name": "Progressive Bassmaster Elite at Lake Guntersville", "location": "Scottsboro, AL", "dates": "Feb 5–8, 2026", "ffs_status": "No"},
    ("2026", "2"): {"clean_name": "Progressive Bassmaster Elite at Lake Martin", "location": "Alexander City, AL", "dates": "Feb 12–15, 2026", "ffs_status": "Yes (Restricted)"},
    ("2026", "3"): {"clean_name": "Bass Pro Shops Bassmaster Classic", "location": "Tennessee River (Knoxville, TN)", "dates": "Mar 13–15, 2026", "ffs_status": "Yes (Restricted)"},
    ("2026", "4"): {"clean_name": "Progressive Bassmaster Elite at Tennessee-Tombigbee Waterway", "location": "Columbus, MS", "dates": "Mar 26–29, 2026", "ffs_status": "No"},
    ("2026", "5"): {"clean_name": "Progressive Bassmaster Elite at Arkansas River", "location": "Muskogee, OK", "dates": "Apr 16–19, 2026", "ffs_status": "Yes (Restricted)"},
    ("2026", "6"): {"clean_name": "Progressive Bassmaster Elite at Lake Murray", "location": "Columbia, SC", "dates": "May 7–10, 2026", "ffs_status": "Yes (Restricted)"},
    ("2026", "7"): {"clean_name": "Progressive Bassmaster Elite at Santee Cooper Lakes", "location": "Clarendon County, SC", "dates": "May 14–17, 2026", "ffs_status": "No"},
    ("2026", "8"): {"clean_name": "Progressive Bassmaster Elite at Pasquotank River/Albemarle Sound", "location": "Elizabeth City, NC", "dates": "Jun 11–14, 2026", "ffs_status": "Yes (Restricted)"},
    ("2026", "9"): {"clean_name": "Progressive Bassmaster Elite at Lake Champlain", "location": "Plattsburgh, NY", "dates": "Aug 13–16, 2026", "ffs_status": "No"},
    ("2026", "10"): {"clean_name": "Progressive Bassmaster Elite at St. Lawrence River", "location": "Clayton, NY", "dates": "Aug 27–30, 2026", "ffs_status": "Yes (Restricted)"},

    # 2025 SEASON MAP
    ("2025", "1"): {"clean_name": "Bassmaster Elite at St. Johns River", "location": "Palatka, FL", "dates": "Feb 20–23, 2025", "ffs_status": "Yes (Restricted)"},
    ("2025", "2"): {"clean_name": "Bassmaster Elite at Lake Okeechobee", "location": "Okeechobee, FL", "dates": "Feb 27–Mar 2, 2025", "ffs_status": "Yes (Restricted)"},
    ("2025", "3"): {"clean_name": "Bass Pro Shops Bassmaster Classic", "location": "Lake Ray Roberts (Fort Worth, TX)", "dates": "Mar 21–23, 2025", "ffs_status": "Yes (Restricted)"},
    ("2025", "4"): {"clean_name": "Bassmaster Elite at Pasquotank River", "location": "Elizabeth City, NC", "dates": "Apr 10–13, 2025", "ffs_status": "Yes (Restricted)"},
    ("2025", "5"): {"clean_name": "Bassmaster Elite at Lake Hartwell", "location": "Anderson, SC", "dates": "Apr 24–27, 2025", "ffs_status": "Yes (Restricted)"},
    ("2025", "6"): {"clean_name": "Bassmaster Elite at Lake Fork", "location": "Yantis, TX", "dates": "May 8–11, 2025", "ffs_status": "Yes (Restricted)"},
    ("2025", "7"): {"clean_name": "Bassmaster Elite at Sabine River", "location": "Orange, TX", "dates": "May 15–18, 2025", "ffs_status": "Yes (Restricted)"},
    ("2025", "8"): {"clean_name": "Bassmaster Elite at Lake Tenkiller", "location": "Cookson, OK", "dates": "Jun 12–15, 2025", "ffs_status": "Yes (Restricted)"},
    ("2025", "9"): {"clean_name": "Bassmaster Elite at Lake St. Clair", "location": "Macomb County, MI", "dates": "Aug 7–10, 2025", "ffs_status": "Yes (Restricted)"},
    ("2025", "10"): {"clean_name": "Bassmaster Elite at Mississippi River", "location": "La Crosse, WI", "dates": "Aug 21–24, 2025", "ffs_status": "Yes (Restricted)"},

    # 2024 SEASON MAP
    ("2024", "1"): {"clean_name": "Bassmaster Elite at Toledo Bend Reservoir", "location": "Many, LA", "dates": "Feb 22–25, 2024", "ffs_status": "Yes (Unrestricted)"},
    ("2024", "2"): {"clean_name": "Bassmaster Elite at Lake Fork", "location": "Yantis, TX", "dates": "Feb 29–Mar 3, 2024", "ffs_status": "Yes (Unrestricted)"},
    ("2024", "3"): {"clean_name": "Bass Pro Shops Bassmaster Classic", "location": "Grand Lake o' the Cherokees (Tulsa, OK)", "dates": "Mar 22–24, 2024", "ffs_status": "Yes (Unrestricted)"},
    ("2024", "4"): {"clean_name": "Bassmaster Elite at Harris Chain of Lakes", "location": "Leesburg, FL", "dates": "Apr 11–14, 2024", "ffs_status": "Yes (Unrestricted)"},
    ("2024", "5"): {"clean_name": "Bassmaster Elite at St. Johns River", "location": "Palatka, FL", "dates": "Apr 18–21, 2024", "ffs_status": "Yes (Unrestricted)"},
    ("2024", "6"): {"clean_name": "Bassmaster Elite at Lake Murray", "location": "Prosperity, SC", "dates": "May 9–12, 2024", "ffs_status": "Yes (Unrestricted)"},
    ("2024", "7"): {"clean_name": "Bassmaster Elite at Wheeler Lake", "location": "Decatur, AL", "dates": "Jun 13–16, 2024", "ffs_status": "Yes (Unrestricted)"},
    ("2024", "8"): {"clean_name": "Bassmaster Elite at Smith Lake", "location": "Cullman, AL", "dates": "Jun 27–30, 2024", "ffs_status": "Yes (Unrestricted)"},
    ("2024", "9"): {"clean_name": "Bassmaster Elite at Lake Champlain", "location": "Plattsburgh, NY", "dates": "Aug 8–11, 2024", "ffs_status": "Yes (Unrestricted)"},
    ("2024", "10"): {"clean_name": "Bassmaster Elite at St. Lawrence River", "location": "Waddington, NY", "dates": "Aug 15–18, 2024", "ffs_status": "Yes (Unrestricted)"},

    # 2023 SEASON MAP
    ("2023", "1"): {"clean_name": "Bassmaster Elite at Lake Okeechobee", "location": "Okeechobee, FL", "dates": "Feb 16–19, 2023", "ffs_status": "Yes (Unrestricted)"},
    ("2023", "2"): {"clean_name": "Bassmaster Elite at Lake Seminole", "location": "Bainbridge, GA", "dates": "Feb 23–26, 2023", "ffs_status": "Yes (Unrestricted)"},
    ("2023", "3"): {"clean_name": "Academy Sports + Outdoors Bassmaster Classic", "location": "Tennessee River (Knoxville, TN)", "dates": "Mar 24–26, 2023", "ffs_status": "Yes (Unrestricted)"},
    ("2023", "4"): {"clean_name": "Bassmaster Elite at Lake Murray", "location": "Columbia, SC", "dates": "Apr 20–23, 2023", "ffs_status": "Yes (Unrestricted)"},
    ("2023", "5"): {"clean_name": "Bassmaster Elite at Santee Cooper Lakes", "location": "Clarendon County, SC", "dates": "Apr 27–30, 2023", "ffs_status": "Yes (Unrestricted)"},
    ("2023", "6"): {"clean_name": "Bassmaster Elite at Lay Lake", "location": "Shelby County, AL", "dates": "May 11–14, 2023", "ffs_status": "Yes (Unrestricted)"},
    ("2023", "7"): {"clean_name": "Bassmaster Elite at Sabine River", "location": "Orange, TX", "dates": "Jun 1–4, 2023", "ffs_status": "Yes (Unrestricted)"},
    ("2023", "8"): {"clean_name": "Bassmaster Elite at Lake St. Clair", "location": "Macomb County, MI", "dates": "Jul 27–30, 2023", "ffs_status": "Yes (Unrestricted)"},
    ("2023", "9"): {"clean_name": "Bassmaster Elite at Lake Champlain", "location": "Plattsburgh, NY", "dates": "Aug 17–20, 2023", "ffs_status": "Yes (Unrestricted)"},
    ("2023", "10"): {"clean_name": "Bassmaster Elite at St. Lawrence River", "location": "Clayton, NY", "dates": "Aug 24–27, 2023", "ffs_status": "Yes (Unrestricted)"},

    # 2022 SEASON MAP
    ("2022", "1"): {"clean_name": "Bassmaster Elite at St. Johns River", "location": "Palatka, FL", "dates": "Feb 10–13, 2022", "ffs_status": "Yes (Unrestricted)"},
    ("2022", "2"): {"clean_name": "Bassmaster Elite at Harris Chain of Lakes", "location": "Leesburg, FL", "dates": "Feb 17–20, 2022", "ffs_status": "Yes (Unrestricted)"},
    ("2022", "3"): {"clean_name": "Academy Sports + Outdoors Bassmaster Classic", "location": "Lake Hartwell (Greenville, SC)", "dates": "Mar 4–6, 2022", "ffs_status": "Yes (Unrestricted)"},
    ("2022", "4"): {"clean_name": "Bassmaster Elite at Santee Cooper Lakes", "location": "Clarendon County, SC", "dates": "Mar 17–21, 2022", "ffs_status": "Yes (Unrestricted)"},
    ("2022", "5"): {"clean_name": "Bassmaster Elite at Chickamauga Lake", "location": "Dayton, TN", "dates": "Apr 7–10, 2022", "ffs_status": "Yes (Unrestricted)"},
    ("2022", "6"): {"clean_name": "Bassmaster Elite at Lake Fork", "location": "Quitman, TX", "dates": "May 19–22, 2022", "ffs_status": "Yes (Unrestricted)"},
    ("2022", "7"): {"clean_name": "Bassmaster Elite at Pickwick Lake", "location": "Counce, TN", "dates": "Jun 2–5, 2022", "ffs_status": "Yes (Unrestricted)"},
    ("2022", "8"): {"clean_name": "Bassmaster Elite at St. Lawrence River", "location": "Clayton, NY", "dates": "Jul 14–17, 2022", "ffs_status": "Yes (Unrestricted)"},
    ("2022", "9"): {"clean_name": "Bassmaster Elite at Lake Oahe", "location": "Mobridge, SD", "dates": "Aug 18–21, 2022", "ffs_status": "Yes (Unrestricted)"},
    ("2022", "10"): {"clean_name": "Bassmaster Elite at Mississippi River", "location": "La Crosse, WI", "dates": "Aug 26–29, 2022", "ffs_status": "Yes (Unrestricted)"},

    # 2020 SEASON MAP (Pandemic Schedule Revision Slots)
    ("2020", "1"): {"clean_name": "Bassmaster Elite at Lake Eufaula", "location": "Eufaula, AL", "dates": "Jun 10–13, 2020", "ffs_status": "Yes (Unrestricted)"},
    ("2020", "2"): {"clean_name": "Bassmaster Elite at Mississippi River", "location": "La Crosse, WI", "dates": "Jul 30–Aug 2, 2020", "ffs_status": "Yes (Unrestricted)"},
    ("2020", "3"): {"clean_name": "Bassmaster Elite at Lake St. Clair", "location": "Macomb County, MI", "dates": "Aug 20–23, 2020", "ffs_status": "Yes (Unrestricted)"},
    ("2020", "4"): {"clean_name": "Bassmaster Elite at Lake Champlain", "location": "Plattsburgh, NY", "dates": "Aug 27–30, 2020", "ffs_status": "Yes (Unrestricted)"},("2020", "5"): {"clean_name": "Bassmaster Elite at Lake Guntersville", "location": "Scottsboro, AL", "dates": "Sep 30–Oct 3, 2020", "ffs_status": "Yes (Unrestricted)"},
    ("2020", "6"): {"clean_name": "Bassmaster Elite at Santee Cooper Lakes", "location": "Manning, SC", "dates": "Oct 16–19, 2020", "ffs_status": "Yes (Unrestricted)"},
    ("2020", "7"): {"clean_name": "Bassmaster Elite at Chickamauga Lake", "location": "Dayton, TN", "dates": "Oct 22–25, 2020", "ffs_status": "Yes (Unrestricted)"},
    ("2020", "8"): {"clean_name": "Toyota Bassmaster Texas Fest at Lake Fork", "location": "Quitman, TX", "dates": "Nov 5–8, 2020", "ffs_status": "Yes (Unrestricted)"},
    ("2020", "9"): {"clean_name": "St. Croix Bassmaster Elite at St. Lawrence River", "location": "Waddington, NY", "dates": "July 23–26, 2020", "ffs_status": "Yes (Unrestricted)"},

    # 2019 SEASON MAP
    ("2019", "1"): {"clean_name": "Bassmaster Elite at St. Johns River", "location": "Palatka, FL", "dates": "Feb 7–10, 2019", "ffs_status": "Yes (Unrestricted)"},
    ("2019", "2"): {"clean_name": "Bassmaster Elite at Lake Lanier", "location": "Gwinnett, GA", "dates": "Mar 14–17, 2019", "ffs_status": "Yes (Unrestricted)"},
    ("2019", "3"): {"clean_name": "Bassmaster Elite at Lake Hartwell", "location": "Anderson, SC", "dates": "Apr 6–9, 2019", "ffs_status": "Yes (Unrestricted)"},
    ("2019", "4"): {"clean_name": "Bassmaster Elite at Winyah Bay", "location": "Georgetown, SC", "dates": "Apr 11–14, 2019", "ffs_status": "Yes (Unrestricted)"},
    ("2019", "5"): {"clean_name": "Toyota Bassmaster Texas Fest at Lake Fork", "location": "Quitman, TX", "dates": "May 2–5, 2019", "ffs_status": "Yes (Unrestricted)"},
    ("2019", "6"): {"clean_name": "Bassmaster Elite at Lake Guntersville", "location": "Scottsboro, AL", "dates": "Jun 21–24, 2019", "ffs_status": "Yes (Unrestricted)"},
    ("2019", "7"): {"clean_name": "Bassmaster Elite at St. Lawrence River", "location": "Waddington, NY", "dates": "Aug 15–18, 2019", "ffs_status": "Yes (Unrestricted)"},
    ("2019", "8"): {"clean_name": "Bassmaster Elite at Lake Champlain", "location": "Plattsburgh, NY", "dates": "Aug 22–25, 2019", "ffs_status": "Yes (Unrestricted)"},
    
    # 2012-2018 CONDENSED BASELINE ARCHIVE MATCH KEYS
    ("2018", "1"): {"clean_name": "Bassmaster Elite at Lake Martin", "location": "Alexander City, AL", "dates": "Feb 8–11, 2018", "ffs_status": "Yes (Unrestricted)"},
    ("2018", "2"): {"clean_name": "GEICO Bassmaster Classic", "location": "Lake Hartwell (Greenville, SC)", "dates": "Mar 16–18, 2018", "ffs_status": "Yes (Unrestricted)"},
    ("2018", "3"): {"clean_name": "Bassmaster Elite at Pickwick Lake", "location": "Florence, AL", "dates": "Apr 19–21, 2018", "ffs_status": "Yes (Unrestricted)"},
    ("2017", "1"): {"clean_name": "Bassmaster Elite at Lake Cherokee", "location": "Jefferson City, TN", "dates": "Feb 9–12, 2017", "ffs_status": "Yes (Unrestricted)"},
    ("2016", "1"): {"clean_name": "GEICO Bassmaster Classic", "location": "Grand Lake O' the Cherokees, OK", "dates": "Mar 4–6, 2016", "ffs_status": "Yes (Unrestricted)"},
    ("2015", "1"): {"clean_name": "Bassmaster Classic", "location": "Lake Hartwell, SC", "dates": "Feb 20–22, 2015", "ffs_status": "Yes (Unrestricted)"},
    ("2014", "1"): {"clean_name": "Bassmaster Classic", "location": "Lake Guntersville (Birmingham, AL)", "dates": "Feb 21–23, 2014", "ffs_status": "No FFS Existed"},
    ("2013", "1"): {"clean_name": "Bassmaster Classic", "location": "Grand Lake o' the Cherokees, OK", "dates": "Feb 22–24, 2013", "ffs_status": "No FFS Existed"},
    ("2012", "1"): {"clean_name": "Bassmaster Classic", "location": "Red River (Shreveport, LA)", "dates": "Feb 24–26, 2012", "ffs_status": "No FFS Existed"}
    }
    
    # ============================================================
# HTTP SESSION WITH RETRIES
# ============================================================

def create_session() -> requests.Session:
    """Create a reusable HTTP session with retry handling."""

    session = requests.Session()
    session.headers.update(HEADERS)

    retry_strategy = Retry(
        total=4,
        connect=4,
        read=2,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


session = create_session()


# ============================================================
# GENERAL HELPERS
# ============================================================

def clean_text(value) -> str | None:
    """Normalize scraped text while preserving meaningful values."""

    if value is None:
        return None

    text = re.sub(r"\s+", " ", str(value)).strip()

    if text in {"", "-", "—", "–", "N/A", "n/a"}:
        return None

    return text


def to_number(value):
    """
    Convert numeric strings to numbers.

    Handles comma-separated values and common blank markers.
    Returns None for values that cannot be parsed.
    """

    value = clean_text(value)

    if value is None:
        return None

    value = value.replace(",", "")

    match = re.fullmatch(r"-?\d+(?:\.\d+)?", value)

    if not match:
        return None

    number = float(value)

    return int(number) if number.is_integer() else number


def get_query_parameters(url: str) -> tuple[str | None, str | None]:
    """Extract year and tournament period ID from a tournament URL."""

    params = parse_qs(urlparse(url).query)

    year = params.get("year", [None])[0]
    period_id = params.get("periodId", [None])[0]

    return year, period_id


def get_tournament_metadata(year, period_id, soup):
    title_element = soup.select_one(
        "#cphContent_cphContent_lblTournamentName"
    )

    scraped_title = (
        title_element.get_text(" ", strip=True)
        if title_element
        else None
    )

    matched = match_tournament_metadata(
        year=year,
        scraped_title=scraped_title,
        period_id=period_id,
        legacy_map=TOURNAMENT_MASTER_MAP,
    )

    return {
        "Event_Name": matched["clean_name"],
        "Location": matched["location"],
        "Tournament_Dates": matched["dates"],
        "Allowed_FFS": matched["ffs_status"],
        "Metadata_Source": matched["metadata_source"],
        "Metadata_Match_Score": matched["metadata_match_score"],
        "Metadata_Needs_Review": matched["metadata_needs_review"],
    }


# ============================================================
# DISCOVER TOURNAMENT LINKS
# ============================================================

def get_tournament_links() -> list[dict]:
    """Find and deduplicate tournament result pages."""

    logger.info("Downloading tournament index: %s", LIST_URL)

    response = session.get(
        LIST_URL,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    tournaments = {}
    links = soup.select('a[href*="TournamentDetails.aspx"]')

    # Do not rely on a single CSS table class.
    for link in links:
        href = link.get("href")

        if not href:
            continue

        url = urljoin(BASE_URL, href)
        year, period_id = get_query_parameters(url)

        # These parameters are needed to identify the event.
        if not year or not period_id:
            logger.warning("Skipping unidentifiable tournament URL: %s", url)
            continue

        # Canonicalize the URL to prevent duplicate downloads caused
        # by equivalent query-string parameter ordering.
        canonical_url = (
            f"{BASE_URL}/TournamentDetails.aspx"
            f"?periodId={period_id}&year={year}"
        )

        tournaments[canonical_url] = {
            "raw_name": clean_text(link.get_text(" ", strip=True)),
            "url": canonical_url,
            "year": year,
            "period_id": period_id,
        }

    tournament_list = sorted(
        tournaments.values(),
        key=lambda item: (
            int(item["year"]),
            int(item["period_id"]),
        ),
    )

    logger.info(
        "Identified %d unique tournament pages.",
        len(tournament_list),
    )

    return tournament_list


# ============================================================
# PARSE ONE TOURNAMENT
# ============================================================

def parse_tournament(tournament: dict) -> tuple[list[dict], dict]:
    """
    Scrape one tournament.

    Returns:
        records: participant result dictionaries
        audit: status and diagnostics for this tournament
    """

    url = tournament["url"]
    year = tournament["year"]
    period_id = tournament["period_id"]

    audit = {
        "Season_Year": year,
        "Tournament_ID": period_id,
        "Source_URL": url,
        "Status": "started",
        "Rows_Parsed": 0,
        "Error": None,
    }

    logger.info("Processing tournament: %s", url)

    try:
        response = session.get(
            url,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        metadata = get_tournament_metadata(
            year,
            period_id,
            soup,
        )

        # Prefer the original results-table selector. Use a fallback
        # if the website changes its surrounding container.
        table = soup.select_one(
            "#cphContent_cphContent_divTournamentResults "
            "table.rosterResults"
        )

        if table is None:
            table = soup.select_one("table.rosterResults")

        if table is None:
            audit["Status"] = "no_results_table"
            audit["Error"] = "Could not locate results table."
            logger.warning("No results table found: %s", url)
            return [], audit

        records = []

        for row in table.select("tr"):
            # Header rows can contain either th or td elements.
            if row.find("th"):
                continue

            cells = row.find_all("td", recursive=False)

            # Expected layout:
            # Place, Angler, Fish, Weight, Big Bag, Big Bass,
            # Leader Bonus, Fantasy Points.
            if len(cells) < 8:
                continue

            player_link = row.select_one(
                'a[href*="AnglerPastResults.aspx"]'
            )

            if player_link:
                angler_name = clean_text(
                    player_link.get_text(" ", strip=True)
                )

                player_url = urljoin(
                    BASE_URL,
                    player_link.get("href", ""),
                )

                player_params = parse_qs(
                    urlparse(player_url).query
                )

                player_id = player_params.get(
                    "playerId", [None]
                )[0]
            else:
                angler_name = clean_text(
                    cells[1].get_text(" ", strip=True)
                )
                player_id = None

            # Ignore table rows that do not contain a participant.
            if not angler_name:
                continue

            record = {
                "Season_Year": year,
                "Tournament_ID": period_id,
                "Event_Name": metadata["Event_Name"],
                "Location": metadata["Location"],
                "Tournament_Dates": metadata["Tournament_Dates"],
                "Allowed_FFS": metadata["Allowed_FFS"],
                "Metadata_Source": metadata["Metadata_Source"],
                "Place": clean_text(
                    cells[0].get_text(" ", strip=True)
                ),
                "Angler_Name": angler_name,
                "Player_ID": player_id,
                "Fish_Caught": clean_text(
                    cells[2].get_text(" ", strip=True)
                ),
                "Weight_Oz": clean_text(
                    cells[3].get_text(" ", strip=True)
                ),
                "Big_Bag_Points": clean_text(
                    cells[4].get_text(" ", strip=True)
                ),
                "Big_Bass_Points": clean_text(
                    cells[5].get_text(" ", strip=True)
                ),
                "Leader_Bonus": clean_text(
                    cells[6].get_text(" ", strip=True)
                ),
                "Fantasy_Points": clean_text(
                    cells[7].get_text(" ", strip=True)
                ),
                "Source_URL": url,
            }

            records.append(record)

        audit["Rows_Parsed"] = len(records)

        if records:
            audit["Status"] = "success"
        else:
            audit["Status"] = "empty_results"
            audit["Error"] = (
                "Table found, but no participant rows were parsed."
            )

        return records, audit

    except requests.RequestException as exc:
        audit["Status"] = "request_error"
        audit["Error"] = str(exc)

        logger.exception("Request failed: %s", url)

        return [], audit

    except Exception as exc:
        audit["Status"] = "parse_error"
        audit["Error"] = str(exc)

        logger.exception("Parsing failed: %s", url)

        return [], audit


# ============================================================
# CLEAN AND VALIDATE DATA
# ============================================================

def clean_results(df: pd.DataFrame) -> pd.DataFrame:
    """Apply consistent types and create analysis-friendly columns."""

    numeric_columns = [
        "Season_Year",
        "Tournament_ID",
        "Place",
        "Fish_Caught",
        "Weight_Oz",
        "Big_Bag_Points",
        "Big_Bass_Points",
        "Leader_Bonus",
        "Fantasy_Points",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column].map(to_number),
                errors="coerce",
            )

    # Preserve the original raw ounce measurement.
    df["Weight_Lbs_Calculated"] = df["Weight_Oz"] / 16.0

    # Integer pounds and remaining ounces are easier to interpret.
    valid_weight = (
        df["Weight_Oz"].notna()
        & (df["Weight_Oz"] >= 0)
    )

    df["Weight_Lbs"] = pd.Series(
        pd.NA, index=df.index, dtype="Int64"
    )

    df["Weight_Oz_Remainder"] = pd.Series(
        pd.NA, index=df.index, dtype="Int64"
    )

    total_ounces = df.loc[valid_weight, "Weight_Oz"]

    df.loc[valid_weight, "Weight_Lbs"] = (
        total_ounces // 16
    ).astype("int64")

    df.loc[valid_weight, "Weight_Oz_Remainder"] = (
        total_ounces % 16
    ).astype("int64")

    # Detect duplicated participant-event records without deleting
    # them automatically. Repeated places can be legitimate ties.
    duplicate_keys = [
        "Season_Year",
        "Tournament_ID",
        "Player_ID",
        "Angler_Name",
    ]

    df["Potential_Duplicate"] = df.duplicated(
        subset=duplicate_keys,
        keep=False,
    )

    # Flag metadata that needs manual verification.
    df["Metadata_Needs_Review"] = (
        df["Metadata_Source"] != "master_map"
    ) | df["Location"].eq("Unknown Location") | (
        df["Allowed_FFS"].eq("Unknown")
    )

    # A stable, reproducible order for analysis.
    df = df.sort_values(
        [
            "Season_Year",
            "Tournament_ID",
            "Place",
            "Angler_Name",
        ],
        na_position="last",
    ).reset_index(drop=True)

    return df


# ============================================================
# MAIN WORKFLOW
# ============================================================

def main():
    tournaments = get_tournament_links()

    if not tournaments:
        logger.error(
            "No tournament links found. Check the website structure."
        )
        return

    all_results = []
    audit_records = []

    for index, tournament in enumerate(tournaments, start=1):
        logger.info(
            "Tournament %d of %d",
            index,
            len(tournaments),
        )

        records, audit = parse_tournament(tournament)

        all_results.extend(records)
        audit_records.append(audit)

        # Pause between pages to reduce unnecessary server load.
        if index < len(tournaments):
            sleep(REQUEST_DELAY_SECONDS)

    # Always save the audit, even if no participant records were found.
    audit_df = pd.DataFrame(audit_records)
    audit_df.to_csv(AUDIT_FILE, index=False)

    logger.info("Scrape audit saved to %s", AUDIT_FILE)

    if not all_results:
        logger.error(
            "No participant records collected. "
            "Review the audit and log files."
        )
        return

    df = pd.DataFrame(all_results)
    df = clean_results(df)

    df.to_csv(
        RESULTS_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    successful = (
        audit_df["Status"] == "success"
    ).sum()

    failed = len(audit_df) - successful

    logger.info("Processing complete.")
    logger.info("Participant records: %s", len(df))
    logger.info("Successful tournament pages: %s", successful)
    logger.info("Other tournament outcomes: %s", failed)
    logger.info("Output file: %s", RESULTS_FILE)
    logger.info("Dataset shape: %s", df.shape)

    preview_columns = [
        "Season_Year",
        "Event_Name",
        "Allowed_FFS",
        "Angler_Name",
        "Place",
        "Weight_Oz",
        "Fantasy_Points",
    ]

    print("\nParticipant results preview:")
    print(df[preview_columns].head(10).to_string(index=False))

    print("\nRecords by season:")
    print(df.groupby("Season_Year").size().to_string())

    print(f"\nTotal records: {len(df):,}")
    print(f"Dataset dimensions: {df.shape}")
    print(f"Results: {RESULTS_FILE.resolve()}")
    print(f"Audit: {AUDIT_FILE.resolve()}")


if __name__ == "__main__":
    main()

