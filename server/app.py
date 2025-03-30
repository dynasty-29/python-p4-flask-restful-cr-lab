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
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])

    # ✅ Create Route: POST /plants
    def post(self):
        data = request.get_json()
        # Validate that required fields are present
        if "name" not in data or "image" not in data or "price" not in data:
            return jsonify({"error": "Missing required fields"}), 400
        new_plant = Plant(
            name=data["name"],
            image=data["image"],
            price=data["price"]
        )

        db.session.add(new_plant)
        db.session.commit()

        return jsonify(new_plant.to_dict()), 201

api.add_resource(Plants, '/plants')


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return jsonify({"error": "Plant not found"}), 404

        return jsonify(plant.to_dict())

api.add_resource(PlantByID, '/plants/<int:id>')


class Home(Resource):
    def get(self):
        return jsonify({"message": "Welcome to the Plants RESTful API"})

api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
