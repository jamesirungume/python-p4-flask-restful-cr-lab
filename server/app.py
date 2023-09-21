#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        all_plants = [n.to_dict() for n in Plant.query.all()]
        response = make_response(jsonify(all_plants), 200)
        return response

    def post(self):  # Changed the method name to 'post'
        data = request.get_json()
        new_plant = Plant(name=data['name'], image=data['image'], price=data['price'])
        db.session.add(new_plant)
        db.session.commit()
        response = make_response(jsonify(new_plant.to_dict()), 201)
        return response

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):  # Changed the method name to 'get'
        plant = Plant.query.filter(Plant.id == id).first()
        if plant is None:
            return make_response(jsonify({"error": "Plant not found"}), 404)  # Handle plant not found
        plant_dict = plant.to_dict()
        response = make_response(jsonify(plant_dict), 200)
        return response

api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
