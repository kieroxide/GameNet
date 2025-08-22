from consts import JSON_DIR_PATH, JSON_NAME, FINAL_DATA_JSON
from api.load_data import get_data_json, load_data
from api.q_codes import q_code_clean
from graph import convert_game_data_to_graph
import os
import json

def main():
    if not os.path.exists(JSON_DIR_PATH + JSON_NAME):
        get_data_json() # calls API

    data = load_data() # gets from json that API provided
    data = q_code_clean(data) # transforms dict's Q codes to real labels
    data = convert_game_data_to_graph(data) # converts to graphable data
    with open(FINAL_DATA_JSON, "w") as f:
        json.dump(data, f, indent=2)

main()