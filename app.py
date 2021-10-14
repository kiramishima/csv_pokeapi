import json
import math
from flask import Flask, jsonify, request, render_template
import pandas as pd

app = Flask(__name__)

# Load CSV
app.data = pd.read_csv("./data/pokemon.csv", header=0, sep='\t',
                   names=['id', 'name', 'type_1', 'type_2', 'total', 'hp', 'atk', 'def', 'sp_atk', 'sp_def', 'speed',
                          'generation', 'legendary'])

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/api/v1/pokemon')
def all():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    resp = pagination(app.data, page, per_page)
    return jsonify(resp)

def pagination(df, start_page = 1, per_page = 15):
    pagesize = per_page
    page = start_page - 1
    max_pages = math.ceil(df.shape[0] / pagesize)
    return {
        'total_records': df.shape[0],
        'current_page': page + 1,
        'max_pages': max_pages,
        'per_page': pagesize,
        'data': json.loads(df.iloc[page * pagesize: (page + 1) * pagesize].to_json(orient='records', force_ascii=False))
    }


@app.route('/api/v1/pokemon/<poke_id>', methods=['GET'])
def find(poke_id):
    print("poke -> {}".format(poke_id))
    pfind = app.data[(app.data['id'] == poke_id) | (app.data['name'] == poke_id)]
    dtjson = json.loads(pfind.to_json(orient='records', force_ascii=False))
    resp = {'status': True, 'data': dtjson}
    return jsonify(resp)


@app.route('/api/v1/pokemon', methods=['POST'])
def create_pokemon():
    form = request.form
    print(form)
    pokemon = {"id": form.get('id'), "name": form.get('name'), "type_1": form.get('type_1'),
               "type_2": form.get('type_2'), "total": form.get('total'), "hp": form.get('hp'), "atk": form.get('atk'),
               "def": form.get('def'),
               "sp_atk": form.get('sp_atk'), "sp_def": form.get('sp_def'), "speed": form.get('speed'),
               "generation": form.get('generation'), "legendary": form.get('legendary')}
    print(pokemon)
    new_row = pd.Series(pokemon)
    app.data = app.data.append(new_row, ignore_index=True)
    resp = {'status': True, 'data': pokemon}
    return jsonify(resp)

@app.route('/api/v1/pokemon/<poke_id>', methods=['POST'])
def update_pokemon(poke_id):
    form = request.form
    # build response
    pokemon = {"id": form.get('id'), "name": form.get('name'), "type_1": form.get('type_1'),
               "type_2": form.get('type_2'), "total": form.get('total'), "hp": form.get('hp'), "atk": form.get('atk'),
               "def": form.get('def'),
               "sp_atk": form.get('sp_atk'), "sp_def": form.get('sp_def'), "speed": form.get('speed'),
               "generation": form.get('generation'), "legendary": form.get('legendary')}

    pfind = app.data.loc[(app.data['id'] == poke_id) | (app.data['name'] == poke_id)]
    pfind = app.data.loc[pfind.index, :]
    pfind.id = form.get('id')
    pfind.name = form.get('name')
    pfind.type_1 = form.get('type_1')
    pfind.type_2 = form.get('type_2')
    pfind.total = form.get('total')
    pfind.hp = form.get('hp')
    pfind.atk = form.get('atk')
    pfind['def'] = form.get('def')
    pfind.sp_atk = form.get('sp_atk')
    pfind.sp_def = form.get('sp_def')
    pfind.speed = form.get('speed')
    pfind.generation = form.get('generation')
    pfind.legendary = form.get('legendary')
    # print(pfind)
    app.data.update(pfind)

    resp = {'status': True, 'message': 'Pokemon has been updated', 'data': pokemon}
    return jsonify(resp)


@app.route('/api/v1/pokemon/<poke_id>', methods=['DELETE'])
def delete_pokemon(poke_id):
    # find the target
    pfind = app.data.loc[(app.data['id'] == poke_id) | (app.data['name'] == poke_id)]
    # process to delete
    app.data.drop(index=pfind.index, inplace=True)
    resp = {'status': True, 'message': 'Pokemon has been deleted'}
    return jsonify(resp)

if __name__ == '__main__':
    app.run()
