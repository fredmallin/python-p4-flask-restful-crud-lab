#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

# ===== Flask App Setup =====
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False  # nicer JSON formatting

# ===== Database Migration Setup =====
migrate = Migrate(app, db)
db.init_app(app)

# ===== Flask-RESTful API Setup =====
api = Api(app)

# ===== Plants List Resource =====
class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
            is_in_stock=data.get('is_in_stock', True)  # default to True if not provided
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(jsonify(new_plant.to_dict()), 201)

# Register the Plants list resource
api.add_resource(Plants, '/plants')

# ===== Plant Single Resource =====
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first_or_404()
        return make_response(jsonify(plant.to_dict()), 200)

    def patch(self, id):
        plant = Plant.query.filter_by(id=id).first_or_404()
        data = request.get_json()

        # Update only fields provided in request
        if "name" in data:
            plant.name = data["name"]
        if "image" in data:
            plant.image = data["image"]
        if "price" in data:
            plant.price = data["price"]
        if "is_in_stock" in data:
            plant.is_in_stock = data["is_in_stock"]

        db.session.commit()
        return make_response(jsonify(plant.to_dict()), 200)

    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first_or_404()
        db.session.delete(plant)
        db.session.commit()
        return '', 204

# Register the single plant resource
api.add_resource(PlantByID, '/plants/<int:id>')

# ===== Run the App =====
if __name__ == '__main__':
    app.run(port=5555, debug=True)
