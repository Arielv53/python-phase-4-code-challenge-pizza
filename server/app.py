#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods=['GET'])
def restaurants():
    if request.method == 'GET':
        rsrnts = Restaurant.query.all()
        result = [rsrnt.to_dict() for rsrnt in rsrnts]
        return jsonify(result), 200
    
@app.route("/restaurants/<int:id>", methods=['GET', 'DELETE'])
def restaurants_by_id(id):
    rsrnts = Restaurant.query.filter(Restaurant.id == id).first()

    if not rsrnts:
        return jsonify({"error": "Restaurant not found"}), 404
    
    if request.method == 'GET':
        # Manually construct the response JSON
        restaurant_pizzas = []
        for rp in rsrnts.rest_pizzas:
            pizza = {
                "id": rp.pizza.id,
                "ingredients": rp.pizza.ingredients,
                "name": rp.pizza.name
            }
            restaurant_pizza = {
                "id": rp.id,
                "pizza_id": rp.pizza_id,
                "price": rp.price,
                "restaurant_id": rp.restaurant_id,
                "pizza": pizza
            }
            restaurant_pizzas.append(restaurant_pizza)

        response = {
            "id": rsrnts.id,
            "name": rsrnts.name,
            "address": rsrnts.address,
            "restaurant_pizzas": restaurant_pizzas
        }
        return jsonify(response), 200
    
    elif request.method == 'DELETE':
        db.session.delete(rsrnts)
        db.session.commit()
        return {}, 204
    
@app.route("/pizzas", methods=['GET'])
def pizzas():
    if request.method == 'GET':
        pizzas = Pizza.query.all()
        result = [pizza.to_dict() for pizza in pizzas]
        return jsonify(result), 200
    
@app.route("/restaurant_pizzas", methods=['POST'])
def rest_pizzas():
    data = request.get_json()

    if not data or 'price' not in data or 'pizza_id' not in data or 'restaurant_id' not in data:
        return jsonify({"errors": ["validation errors"]}), 400
    
    price = data.get('price')

    if price < 1 or price > 30:
        return jsonify({"errors": ["validation errors"]}), 400
    
    try:
        new_rp = RestaurantPizza(
            price=data.get('price'),
            pizza_id=data.get('pizza_id'),
            restaurant_id=data.get('restaurant_id')
        )
        db.session.add(new_rp)
        db.session.commit()
        return jsonify(new_rp.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)
