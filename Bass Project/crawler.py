import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin, parse_qs, urlparse
from time import sleep

BASE_URL = "https://bassmasterfantasy.com"
LIST_URL = f"{BASE_URL}/TournamentResultsList.aspx"

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0"
})


def get_tournament_links():

    html = session.get(LIST_URL).text
    soup = BeautifulSoup(html, "html.parser")

    tournaments = []

    for a in soup.select("table.rosterResults a"):

        href = a.get("href")

        if href and "TournamentDetails.aspx" in href:

            tournaments.append({
                "tournament_name": a.get_text(strip=True),
                "url": urljoin(BASE_URL, href)
            })

    return tournaments


def parse_tournament(url):

    print("Scraping:", url)

    r = session.get(url)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    tournament_name = soup.select_one(
        "#cphContent_cphContent_lblTournamentName"
    )

    tournament_name = (
        tournament_name.get_text(strip=True)
        if tournament_name
        else None
    )

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    period_id = params.get("periodId", [None])[0]
    year = params.get("year", [None])[0]

    table = soup.select_one(
        "#cphContent_cphContent_divTournamentResults table.rosterResults"
    )

    rows = table.select("tr")[1:]

    results = []

    for row in rows:

        cols = row.find_all("td")

        if len(cols) < 8:
            continue

        player_link = row.select_one(
            'a[href*="AnglerPastResults.aspx"]'
        )

        player_id = None

        if player_link:

            href = player_link.get("href")

            player_id = parse_qs(
                urlparse(href).query
            ).get(
                "playerId",
                [None]
            )[0]

            angler = player_link.get_text(
                strip=True
            )

        else:
            angler = None

        results.append({
            "tournament_name": tournament_name,
            "year": year,
            "period_id": period_id,
            "place": cols[0].get_text(strip=True),
            "angler": angler,
            "player_id": player_id,
            "fish": cols[2].get_text(strip=True),
            "weight_oz": cols[3].get_text(strip=True),
            "big_bag": cols[4].get_text(strip=True),
            "big_bass": cols[5].get_text(strip=True),
            "leader_bonus": cols[6].get_text(strip=True),
            "fantasy_points": cols[7].get_text(strip=True),
            "tournament_url": url
        })

    return results


def main():

    tournaments = get_tournament_links()

    print(f"{len(tournaments)} tournaments found")

    all_results = []

    for tournament in tournaments:

        try:

            all_results.extend(
                parse_tournament(
                    tournament["url"]
                )
            )

            sleep(1)

        except Exception as e:

            print(
                f"Failed: {tournament['url']}"
            )

            print(e)

    df = pd.DataFrame(all_results)

    df["place"] = pd.to_numeric(
        df["place"],
        errors="coerce"
    )

    df["fish"] = pd.to_numeric(
        df["fish"],
        errors="coerce"
    )

    df["weight_oz"] = pd.to_numeric(
        df["weight_oz"],
        errors="coerce"
    )

    df["fantasy_points"] = pd.to_numeric(
        df["fantasy_points"],
        errors="coerce"
    )

    df.to_csv(
        "bassmaster_fantasy_results.csv",
        index=False
    )

    print(df.head())
    print(df.shape)


if __name__ == "__main__":
    main()