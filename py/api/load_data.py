from consts import JSON_NAME, JSON_DIR_PATH, Q_CODE_PATH
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
import json


def load_data() -> dict:
    """Loads the JSON file full of the main game data. Returns dict[str, dict[str, set | str]]"""
    data = defaultdict(lambda: {"developers": set(), "platforms": set(), "genres": set(), "releaseDate": ""})
    
    with open(JSON_DIR_PATH + JSON_NAME, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    
    for row in raw_data:
        game_title = row.get("title")
        if not game_title:
            continue  # skip rows without a title

        dev = row.get("developer")
        if dev:
            data[game_title]["developers"].add(dev)

        plat = row.get("platform")
        if plat:
            data[game_title]["platforms"].add(plat)

        genre = row.get("genre")
        if genre:
            data[game_title]["genres"].add(genre)

        rel = row.get("releaseDate")
        if rel:
            data[game_title]["releaseDate"] = rel

    return data


def get_data_json() -> None: 
    """Gets games data from Wikidata API and saves to standard json format"""
    # Initialize SPARQL endpoint
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    # SPARQL query: video games released between 2004–2010
    query = """
    SELECT ?game ?gameLabel ?developerLabel ?platformLabel ?genreLabel ?releaseDate
    WHERE {
      ?game wdt:P31 wd:Q7889;       # instance of video game
            wdt:P577 ?releaseDate.  # publication date
      FILTER(YEAR(?releaseDate) >= 2004 && YEAR(?releaseDate) <= 2010)
      OPTIONAL { ?game wdt:P178 ?developer. }  # developer
      OPTIONAL { ?game wdt:P400 ?platform. }   # platform
      OPTIONAL { ?game wdt:P136 ?genre. }      # genre
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    LIMIT 1000
    """

    sparql.setQuery(query)
    results = sparql.query().convert()

    # Process results into a simple JSON format 
    games = []

    for result in results["results"]["bindings"]:
        game = {
            "title": result.get("gameLabel", {}).get("value"),
            "developer": result.get("developerLabel", {}).get("value"),
            "platform": result.get("platformLabel", {}).get("value"),
            "genre": result.get("genreLabel", {}).get("value"),
            "releaseDate": result.get("releaseDate", {}).get("value")
        }
        games.append(game)

    # Save to JSON
    with open(JSON_DIR_PATH + JSON_NAME, "w", encoding="utf-8") as f:
        json.dump(games, f, indent=2, ensure_ascii=False)


