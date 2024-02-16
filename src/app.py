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
from models import db, User, Character, Planet, Vehicle, Favorites
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

# EndPoint USER
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]
    return jsonify(serialized_users), 200

# EndPoints CHARACTER

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    serialized_characters = [character.serialize() for character in characters]
    return jsonify(serialized_characters), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(character.serialize()), 200

@app.route('/characters', methods=['POST'])
def add_character():
    body = request.get_json()
    character = Character(
        id = body['id'],
        name = body['name'],
        birth_year = body['birth_year'],
        gender = body['gender'],
        height = body['height'],
        weight = body['weight'],
        eye_color = body['eye_color'],
        hair_color = body['hair_color'],
        planet_id = body['planet_id'],
    )
    db.session.add(character)
    db.session.commit()
    return jsonify({"message": "Character created successfully", "character": character.serialize()}), 200

@app.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    body = request.get_json()
    character = Character.query.get(character_id)

    if character:
        character.name = body['name'],
        character.birth_year = body['birth_year'],
        character.gender = body['gender'],
        character.height = body['height'],
        character.weight = body['weight'],
        character.eye_color = body['eye_color'],
        character.hair_color = body['hair_color'],
        character.planet_id = body['planet_id'],

        db.session.commit()
        return jsonify({"message": "Character updated successfully", "character": character.serialize()}), 200
    else:
        return jsonify({"error": "Character not found"}), 404

@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)

    if character:
        db.session.delete(character)
        db.session.commit()
        return jsonify({"message": "Character deleted successfully"}), 200
    else:
        return jsonify({"error": "Character not found"}), 404


# EndPoints PLANET

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify(serialized_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/planets', methods=['POST'])
def add_planet():
    body = request.get_json()
    planet = Planet(
        id = body['id'],
        name = body['name'],
        diameter = body['diameter'],
        climate = body['climate'],
        terrain = body['terrain'],
        surface_water = body['surface_water'],
        population = body['population'],
        orbital_period = body['orbital_period'],
        rotation_period = body['rotation_period'],
        gravity = body['gravity'],
    )

    db.session.add(planet)
    db.session.commit()
    return jsonify({"message": "Planet created successfully", "planet": planet.serialize()}), 200

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    body = request.get_json()
    planet = Planet.query.get(planet_id)

    if planet:
        planet.id = body['id'],
        planet.name = body['name'],
        planet.diameter = body['diameter'],
        planet.climate = body['climate'],
        planet.terrain = body['terrain'],
        planet.surface_water = body['surface_water'],
        planet.population = body['population'],
        planet.orbital_period = body['orbital_period'],
        planet.rotation_period = body['rotation_period'],
        planet.gravity = body['gravity'],

        db.session.commit()
        return jsonify({"message": "Planet updated successfully", "planet": planet.serialize()}), 200
    else:
        return jsonify({"error": "Planet not found"}), 404

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"message": "Planet deleted successfully"}), 200
    else:
        return jsonify({"error": "Planet not found"}), 404



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

