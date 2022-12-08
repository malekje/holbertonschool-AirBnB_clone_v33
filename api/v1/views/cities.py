#!/usr/bin/python3
""" 
api
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage
from models.city import City



@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['GET'])
def retrieve_cities(state_id):
    """ request every city obj in state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['GET'])
def view_city(city_id):
    """ request city within its id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@ app_views.route('/cities/<city_id>',
                  strict_slashes=False,
                  methods=['DELETE'])
def del_city(city_id):
    """ delete city fully"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@ app_views.route('/states/<state_id>/cities',
                  strict_slashes=False,
                  methods=['POST'])
def touch_city(state_id):
    """ create city """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    try:
        body = request.get_json()

        if body is None:
            abort(400, description="Not a JSON")
        elif body.get('name') is None:
            abort(400, description='Missing name')
        else:
            obj = City(**body)
            obj.state_id = state.id
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    except ValueError:
        abort(400, desciption="Not a JSON")


@ app_views.route('/cities/<city_id>', methods=["PUT"])
def update_city(city_id):
    """ update city"""
    found = storage.get(City, city_id)
    if not found:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        else:
            invalid = ['id', 'created_at', 'updated_at']
            for key, value in req.items():
                if key not in invalid:
                    setattr(found, key, value)
            storage.save()
            return jsonify(found.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")