from flask import Flask, request, send_file
from flask_restful import Resource, Api, abort
import os
import json

app = Flask(__name__)
api = Api(app)

# url = request.base_url
# print(url)

pokemon_data = {}
pokemon_index = {}
pokemon_directory = os.listdir('json')
for item in pokemon_directory:
    with open('json/' + item , 'r') as file:
        data = file.read()
    pokemon = json.loads(data)
    pokemon['image'] = 'pics/' + format(pokemon['number'], '03d') + '.png'
    pokemon_data[pokemon['name']] = pokemon
    pokemon_index[pokemon['number']] = pokemon['name']


def check_pokemon_exists(pokemon):
    if pokemon not in pokemon_data and pokemon not in pokemon_index:
        abort(404, message="Pokemon {} doesn't exist".format(pokemon))


class PokemonAll(Resource):
    def get(self):
        return pokemon_data

class Pokemon(Resource):
    def get(self, poke_ident): 
        if poke_ident.isnumeric():
            poke_num = int(poke_ident)
            check_pokemon_exists(poke_num)
            return pokemon_data[pokemon_index[poke_num]]
        poke_ident = poke_ident.capitalize()
        check_pokemon_exists(poke_ident)
        return pokemon_data[poke_ident]

class PokeImage(Resource):
    def get(self, poke_ident):
        if poke_ident.isnumeric():
            poke_num = int(poke_ident)
            check_pokemon_exists(poke_num)
            cur_poke = pokemon_data[pokemon_index[poke_num]]
            return send_file(cur_poke['image'], mimetype='image/png')
        poke_ident = poke_ident.capitalize()
        check_pokemon_exists(poke_ident)
        cur_poke = pokemon_data[poke_ident]
        return send_file(cur_poke['image'], mimetype='image/png')

api.add_resource(PokemonAll, '/pokemon')
api.add_resource(Pokemon, '/pokemon/<string:poke_ident>')
api.add_resource(PokeImage, '/pokeimage/<string:poke_ident>')

if __name__ == '__main__':
    app.run(debug=True) 

    