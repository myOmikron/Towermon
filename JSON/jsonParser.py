import json
from pathlib import Path

#JSON file öffnen und in Variable speichern
pokedexPath = Path('JSON/pokedex.json')
pokedex_dict = json.load(pokedexPath.open())

typePath = Path('JSON/typesystem.json')
type_dict = json.load(typePath.open())

#JSON File zu Python Dictionary Parsen
def parsePokemon (json_dict: dict):
    pokemon_dict = {}
    for entry in json_dict:
        key = entry["name"]
        value = {"id" : entry["id"], "name": entry["name"], "type": entry["type"]}
        pokemon_dict[key] = value
    return pokemon_dict


#Einzelnes Pokemon auslesen (für Konstruktor der pokemonTower Klasse!)
def getPokemonData (name:str):
    pokemon_dict = parsePokemon(pokedex_dict)
    return pokemon_dict[name]

def getTypeList():
    i = 0
    typeList = []
    for entry in type_dict:
        typeList.append(entry)
    return typeList

def getDamageFactor(attack: str, enemyType: str):
    return type_dict[attack][enemyType]
