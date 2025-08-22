import re
import requests
import os
import json
from consts import Q_CODE_PATH, JSON_DIR_PATH, JSON_NAME
from collections import defaultdict

def q_code_clean(data: dict) -> dict:
    """The wikidata API sometimes doesn't return a english label and just gives the Q id code for it.
    This function tries to figure out what the q code refers to and replaces it in the data"""
    for game in data:
        for col in data[game]:
            # Handle sets (developers, platforms, genres)
            if isinstance(data[game][col], set):
                cleaned_set = set()
                for val in data[game][col]:
                    if is_qcode(val):
                        q_codes_lookup = load_q_codes() # inefficiently opens the q code file but will do for now
                        val = lookup_label(val, q_codes_lookup)
                    cleaned_set.add(val)
                data[game][col] = cleaned_set

            # Handle releaseDate (string)
            elif isinstance(data[game][col], str) and is_qcode(data[game][col]):
                data[game][col] = lookup_label(data[game][col], q_codes_lookup)
    return data

def lookup_label(qid: str, q_codes) -> str:
    """Looks for q_code in cached codes. if not found searches the API"""
    if qid in q_codes:
        return q_codes[qid]
    try:
        url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
        r = requests.get(url)
        
        entity = r.json()["entities"][qid]
        labels = entity.get("labels", {})

        if labels:
            label = next(iter(labels.values())).get("value", qid) # Looks for the first label
        else:
            label = qid

        q_codes[qid] = label
        # Saves the code to the json to cache and prevent using the API again
        with open(Q_CODE_PATH, "w") as f:
            json.dump(q_codes, f)

    except Exception as e:
        print(f"Error Occurred : {e}")

    return label

def load_q_codes():
    """Loads the q code cache from a file to prevent slow API calls"""
    if os.path.exists(Q_CODE_PATH):
        with open(Q_CODE_PATH, "r") as f:
            q_codes = json.load(f)
        return q_codes
    else:
        return defaultdict()

def is_qcode(value: str) -> bool:
    return bool(re.fullmatch(r"Q\d+", value))
