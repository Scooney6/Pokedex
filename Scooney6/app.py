import requests
from flask import Flask, render_template, url_for, request
from functools import lru_cache

app = Flask(__name__)


@lru_cache
def api_call(url):
    print("fetching")
    data = requests.get(url).json()
    return data


@app.route("/")
def index():
    return render_template("index.html", versions=[versiongroup["name"] for versiongroup in
                                                   api_call("https://pokeapi.co/api/v2/version-group/")["results"]])


@app.route("/version", methods=["GET"])
def version():
    data = api_call("https://pokeapi.co/api/v2/version-group/%s/" % (request.args.get('version')))
    generation = data['generation']['name']
    versions = [versions['name'] for versions in data['versions']]
    regions = [regions['name'] for regions in data['regions']]
    pokedexes = [pokedexes['name'] for pokedexes in data['pokedexes']]
    return render_template("version.html", version=request.args.get('version'), generation=generation,
                           versions=versions, regions=regions, pokedexes=pokedexes)


@app.route("/pokedex", methods=["GET"])
def pokedex():
    data = api_call("https://pokeapi.co/api/v2/pokedex/%s/" % (request.args.get('pokedex')))
    pokemon = [pokemons['pokemon_species']['name'] for pokemons in data['pokemon_entries']]
    return render_template("pokedex.html", pokemon=pokemon, pokedex=request.args.get('pokedex'))


if __name__ == '__main__':
    app.run()
