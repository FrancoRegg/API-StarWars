"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planets, Starships
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

##### GET User #####

@app.route('/user', methods=['GET'])
def handle_hello():
    user = User.query.all()
    user_serialized = list(map(lambda x: x.serialize(), user))
    return jsonify(user_serialized), 200

##### GET User + ID #####
@app.route('/user/<int:user_id>', methods=['GET'])
def get_userId(user_id):
    user = User.query.get(user_id)
    if user == None:
        return('Not found'), 400
    user_serialized = user.serialize()
    return jsonify(user_serialized), 200

##### GET Planets #####
@app.route('/planets', methods=['GET'])
def get_planet():
    planets = Planets.query.all()
    planets_serialized = list(map(lambda x: x.serialize(), planets))
    return jsonify(planets_serialized),200

###### GET Planets + ID #####
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planetsId(planets_id):
    planets = Planets.query.get(planets_id)
    if planets == None:
        return('Not found'), 400
    planets_serialized = planets.serialize()
    return jsonify(planets_serialized)

##### GET Character #####
@app.route('/character', methods=['GET'])
def get_character():
    character = Character.query.all()
    character_serialized = list(map(lambda x: x.serialize(), character))
    return jsonify(character_serialized),200

###### GET Character + ID #####
@app.route('/character/<int:character_id>', methods=['GET'])
def get_characterId(character_id):
    character = Character.query.get(character_id)
    if character == None:
        return('Not found'), 400
    character_serialized = character.serialize()
    return jsonify(character_serialized)

##### GET Starships #####
@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starships.query.all()
    starships_serialized = list(map(lambda x: x.serialize(), starships))
    return jsonify(starships_serialized),200

###### GET Starships + ID #####
@app.route('/starships/<int:starships_id>', methods=['GET'])
def get_starshipsId(starships_id):
    starships = Starships.query.get(starships_id)
    if starships == None:
        return('Not found'), 400
    starships_serialized = starships.serialize()
    return jsonify(starships_serialized)




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
