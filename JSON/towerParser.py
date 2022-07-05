import json

#JSON file öffnen und in Variable speichern
with open('pokedex.json', 'r') as file:
    json_dict = json.load(file)

#JSON File zu Python Dictionary Parsen
def parsePokemon (json_dict: dict):
    pokemon_dict = {}
    for entry in json_dict:
        key = entry["name"]
        value = {"id" : entry["id"], "name": entry["name"], "type": entry["type"]}
        pokemon_dict[key] = value
    return pokemon_dict

pokemon_dict = parsePokemon(json_dict)

#Einzelnes Pokemon auslesen (für Konstruktor der pokemonTower Klasse!)
def getPokemonData (name:str):
    return pokemon_dict[name]
