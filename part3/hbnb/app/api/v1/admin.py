#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from hbnb.app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('admin', description='Admin operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/users/')
class AdminUserCreate(Resource):
    @api.response(201, 'User created successfully')
    @api.response(400, 'Invalid input data or email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        # Logic to create a new user
        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'password': new_user.password
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data or email already in use')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        # Ensure email uniqueness
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        # Logic to update user details
        try:
            user = facade.get_user(user_id)
            user.update(data)
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'password': user.password
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.response(201, 'Amenity created successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Logic to create a new amenity
        try:
            new_amenity = facade.create_amenity(request.json)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
                }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    api.response(200, 'Amenity details retrieved successfully')
    api.response(400, 'Invalid input data')
    api.response(403, 'Admin privileges required')
    api.response(404, 'Amenity not found')
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Logic to update an amenity
        if not request.json.get('name'):
            return {'error': 'Amenity name is required'}, 400

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        facade.update_amenity(amenity_id, request.json)
        return {
            'message': 'Amenity updated successfully'
        }, 200

@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Logic to update the place
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.update_place(place_id, request.json)
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
