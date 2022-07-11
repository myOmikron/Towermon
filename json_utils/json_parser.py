import json
from pathlib import Path

# JSON file öffnen und in Variable speichern
from typing import List, Dict

pokedex_path = Path('data/pokedex.json')
pokedex_dict = json.load(pokedex_path.open())

type_path = Path('data/typesystem.json')
type_dict = json.load(type_path.open())


# JSON File zu Python Dictionary Parsen
def parse_pokemon(json_dict: dict) -> Dict:
    pokemon_dict = {}
    for entry in json_dict:
        key = entry["name"]
        value = {"id": entry["id"], "name": entry["name"], "type": entry["type"]}
        pokemon_dict[key] = value
    return pokemon_dict


# Einzelnes Pokemon auslesen (für Konstruktor der pokemonTower Klasse!)
def get_pokemon_data(name: str):
    pokemon_dict = parse_pokemon(pokedex_dict)
    return pokemon_dict[name]


def get_type_list() -> List[dict]:
    type_list = []
    for entry in type_dict:
        type_list.append(entry)
    return type_list


def get_pokemon_list() -> List[dict]:
    list = []
    for entry in pokedex_dict:
        list.append(entry['name'])
    print(list)
    return list


def get_damage_factor(attack: str, enemy_type: str) -> float:
    return type_dict[attack][enemy_type]
