import pokepy
from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect

app = Flask(__name__)


@app.route("/")
def index():
    # TODO: manually request all pokedexes and display them
    # TODO: clicking on a pokedex pulls up the pokemon in that pokedex
    # TODO: add a search bar to search pokemon or pokedexes
    pk = pokepy.V2Client().get_pokedex(1)
    print(pk[0].pokemon_entries[0].pokemon_species.name)
    return redirect(url_for("pokedex", name="national"))


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
