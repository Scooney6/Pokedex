import pokepy
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
    # TODO: clicking on a pokedex pulls up the pokemon in that pokedex
    # TODO: add a search bar to search pokemon or pokedexes
    # pk = pokepy.V2Client().get_pokedex(1)
    # print(pk[0].pokemon_entries[0].pokemon_species.name)
    # return redirect(url_for("pokedex", name="national"))


@app.route("/version", methods=["GET"])
def version():
    data = api_call("https://pokeapi.co/api/v2/version-group/%s/" % (request.args.get('version')))
    generation = data['generation']['name']
    versions = [versions['name'] for versions in data['versions']]
    regions = [regions['name'] for regions in data['regions']]
    pokedexes = [pokedexes['name'] for pokedexes in data['pokedexes']]
    print(data)
    return render_template("version.html", version=request.args.get('version'), generation=generation, versions=versions, regions=regions, pokedexes=pokedexes)


@app.route("/pokedex", methods=["POST", "GET"])
def pokedex():
    pokedex = pokepy.V2Client().get_pokedex(request.args.get('name'))
    pokeobjs = pokedex[0].pokemon_entries
    pokemon = []
    i = 0
    for pokemons in pokeobjs:
        pokemon.append(pokeobjs[i].pokemon_species.name)
        i = i + 1
    return render_template("pokedex.html", pokemon=pokemon, pokedex=pokedex[0].name)


if __name__ == '__main__':
    app.run()
