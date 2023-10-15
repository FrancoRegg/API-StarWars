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
from models import db, User, Character, Planets, Starships, Favorite_Starships, Favorite_Character, Favorite_Planets
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


##### USER #####

##>GET USER<##
@app.route('/user', methods=['GET'])
def handle_hello():
    user = User.query.all()
    user_serialized = list(map(lambda x: x.serialize(), user))
    return jsonify(user_serialized), 200

##>GET USER+ID<##
@app.route('/user/<int:user_id>', methods=['GET'])
def get_userId(user_id):
    user = User.query.get(user_id)
    if user is None:
        return('Not found'), 400
    user_serialized = user.serialize()
    return jsonify(user_serialized), 200

##>POST A USER<##
@app.route('/user', methods=['POST'])
def create_user():
    body_user = request.get_json()
    new_user = User(email=body_user['email'], password=body_user['password'], is_active=body_user['is_active'] )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(body_user), 200

##>DELETE A USER<##
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'User not found'}), 400
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({'msg':'User successfully removed'}), 200


##### PLANETS #####


##>GET PLANETS<##
@app.route('/planets', methods=['GET'])
def get_planet():
    planets = Planets.query.all()
    planets_serialized = list(map(lambda x: x.serialize(), planets))
    return jsonify(planets_serialized),200

##>GET FAVORITE PLANETS<##
@app.route('/fav_planets', methods=['GET'])
def get_favPlanets():
    favPlanets = Favorite_Planets.query.all()
    favPlanets_serialized = list(map(lambda x: x.serialize(), favPlanets))
    return jsonify(favPlanets_serialized), 200

##>GET ALL FAVORITE PLANETS OF A USER+ID<##
@app.route('/fav_planets/<int:user>', methods=['GET'])
def get_favPlanets_user(user):
    favPlanets = Favorite_Planets.query.filter_by(user = user).all()
    favPlanets_serialized = list(map(lambda x:x.serialize(),favPlanets))
    return(favPlanets_serialized), 200

##>POST A PLANETS<##
@app.route('/planets', methods=['POST'])
def create_planet():
    body_planet = request.get_json()
    new_planet = Planets( name=body_planet['name'], rotation_period=body_planet['rotation_period'], orbital_period=body_planet['orbital_period'], climate=body_planet['climate'], terrain=body_planet['terrain'], surface_water=['surface_water'])
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(body_planet), 200

##>POST A FAVORITE PLANETS<## 
@app.route('/fav_planets', methods=['POST'])
def create_favplanets():
    body_favplanet = request.get_json()
    new_favplanets = Favorite_Planets(planets=body_favplanet["planets"], user=body_favplanet["user"])
    db.session.add(new_favplanets)
    db.session.commit()

    return jsonify(body_favplanet), 200

##>DELETE A PLANETS<##
@app.route('/planets/<int:planets_id>', methods=['DELETE'])
def delete_planet(planets_id):
    planet = Planets.query.get(planets_id)
    if planet is None:
        return jsonify({'msg': 'Planet not found'}), 400
    
    db.session.delete(planet)
    db.session.commit()

    return jsonify({'msg':'Planet with id {planets_id} successfully removed'}), 200

##>DELETE A FAVORITE PLANETS<##
@app.route('/fav_planets/<int:favplanets_id>', methods=['DELETE'])
def delete_favPlanets(fav_planets_id):
    fav_planets = Favorite_Planets.query.get(fav_planets_id)

    if fav_planets is None:
        return jsonify({'msg': 'Favorite planet not found'}), 404

    db.session.delete(fav_planets)
    db.session.commit()

    return jsonify({'msg': 'A favorite planet was successfully eliminated'}), 200


##### CHARACTER #####


##>GET CHARACTER<##
@app.route('/character', methods=['GET'])
def get_character():
    character = Character.query.all()
    character_serialized = list(map(lambda x: x.serialize(), character))
    return jsonify(character_serialized),200

##>GET FAVORITE CHARACTER<##
@app.route('/fav_character', methods=['GET'])
def get_favCharacter():
    favCharacter = Favorite_Character.query.all()
    favCharacter_serialized = list(map(lambda x: x.serialize(), favCharacter))
    return jsonify(favCharacter_serialized), 200

##>GET ALL FAVORITE CHARACTER OF A USER+ID<##
@app.route('/fav_character/<int:user>', methods=['GET'])
def get_favCharacter_user(user):
    favCharacter = Favorite_Character.query.filter_by(user = user).all()
    favCharacter_serialized = list(map(lambda x:x.serialize(),favCharacter))
    return(favCharacter_serialized), 200

##>POST A CHARACTER<##
@app.route('/character', methods=['POST'])
def create_character():
    body_character = request.get_json()
    new_character = Character(name=body_character['name'], height=body_character['height'], hair_color=body_character['hair_color'], skin_color=body_character['skin_color'], eye_color=body_character['eye_color'], mass=body_character['mass'], gender=body_character['gender'], homeworld=body_character['homeworld'])
    db.session.add(new_character)
    db.session.commit()

    return jsonify(body_character), 200

##>POST A FAVORITE CHARACTER<## 
@app.route('/fav_character', methods=['POST'])
def create_favcharacter():
    body_favcharacter = request.get_json()
    new_favcharacter = Favorite_Character(character=body_favcharacter["character"], user=body_favcharacter["user"])
    db.session.add(new_favcharacter)
    db.session.commit()

    return jsonify(body_favcharacter), 200

##>DELETE A CHARACTER<##
@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({'msg': 'Character not found'}), 400
    
    db.session.delete(character)
    db.session.commit()

    return jsonify({'msg':'Character successfully removed'}), 200

##>DELETE A FAVORITE CHARACTER<##
@app.route('/fav_character/<int:favcharacter_id>', methods=['DELETE'])
def delete_favCharacter(fav_character_id):
    fav_character = Favorite_Character.query.get(fav_character_id)

    if fav_character is None:
        return jsonify({'msg': 'Favorite character not found'}), 404

    db.session.delete(fav_character)
    db.session.commit()

    return jsonify({'msg': 'A favorite character was successfully eliminated'}), 200


##### STARSHIPS #####


##>GET STARSHIPS<##
@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starships.query.all()
    starships_serialized = list(map(lambda x: x.serialize(), starships))
    return jsonify(starships_serialized),200

##>GET FAVORITE STARSHIPS<##
@app.route('/fav_starships', methods=['GET'])
def get_favStarships():
    favStarships = Favorite_Starships.query.all()
    favStarships_serialized = list(map(lambda x: x.serialize(), favStarships))
    return jsonify(favStarships_serialized), 200

##>GET ALL FAVORITE STARSHIPS OF A USER+ID<##
@app.route('/fav_starships/<int:user>', methods=['GET'])
def get_favStarships_user(user):
    favStarships = Favorite_Starships.query.filter_by(user = user).all()
    favStarships_serialized = list(map(lambda x:x.serialize(),favStarships))
    return(favStarships_serialized), 200

##>POST A STARSHIPS<##
@app.route('/starships', methods=['POST'])
def create_starship():
    body_starships = request.get_json()
    new_starship = Starships(name=body_starships['name'], model=body_starships['model'], length=body_starships['length'], passengers=body_starships['passengers'], starship_class=body_starships['starship_class'], pilots=body_starships['pilots'])
    db.session.add(new_starship)
    db.session.commit()

    return jsonify(body_starships), 200

##>POST A FAVORITE STARSHIPS<## 
@app.route('/fav_starships', methods=['POST'])
def create_favstarships():
    body_favstarships = request.get_json()
    new_favstarships = Favorite_Starships(starships=body_favstarships["starships"], user=body_favstarships["user"])
    db.session.add(new_favstarships)
    db.session.commit()

    return jsonify(body_favstarships), 200

##>DELETE A STARSHIPS<##
@app.route('/starships/<int:starships_id>', methods=['DELETE'])
def delete_Starships(starships_id):
    starships = Starships.query.get(starships_id)
    if starships is None:
        return jsonify({'msg': 'Starships not found'}), 400
    
    db.session.delete(starships)
    db.session.commit()

    return jsonify({'msg':'Starships successfully removed'}), 200

##>DELETE A FAVORITE STARSHIPS<##
@app.route('/fav_starships/<int:favstarships_id>', methods=['DELETE'])
def delete_favStarships(fav_starships_id):
    fav_starships = Favorite_Starships.query.get(fav_starships_id)

    if fav_starships is None:
        return jsonify({'msg': 'Favorite starship not found'}), 404

    db.session.delete(fav_starships)
    db.session.commit()

    return jsonify({'msg': 'A favorite starship was successfully eliminated'}), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
