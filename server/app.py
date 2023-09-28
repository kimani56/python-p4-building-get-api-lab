#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route("/")
def index():
    return '<h1>Bakery GET API</h1>'

@app.route("/bakeries")
def get_bakeries():
    bakeries = Bakery.query.all()
    bakery_list = []
    for bakery in bakeries:
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at,
            'baked_goods': [{
                'id': baked_good.id,
                'name': baked_good.name,
                'price': baked_good.price
            } for baked_good in bakery.baked_goods]
        }
        bakery_list.append(bakery_data)
    return jsonify(bakery_list)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        bakery_dict = {
            "id" : bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at,

        }

        response = make_response(
        jsonify(bakery_dict), 
        200)
        response.headers["Content-Type"] = 'application/json'
    
    return response

@app.route('/baked_goods/by_price')

def baked_goods_by_price():
    baked_goods_prices = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = []

    for baked_good_price in baked_goods_prices:
        baked_goods_by_price_dict = {
            "id" : baked_good_price.id,
            "name": baked_good_price.name,
            "price": baked_good_price.price,
            "created_at": baked_good_price.created_at
        }
        baked_goods_list.append(baked_goods_by_price_dict)

    response = make_response(jsonify(baked_goods_list), 200)
    response.headers["Content-Type"] = 'application/json'
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    
    if most_expensive is not None:
        most_expensive_dict = {
            "id": most_expensive.id,
            "name": most_expensive.name,
            "price": most_expensive.price,
            "created_at": most_expensive.created_at
        }

    response = make_response(jsonify(most_expensive_dict), 200)
    response.headers["Content-Type"] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
