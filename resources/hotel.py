from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

# CRUD: Create, Read, Update, Delete
#       Post,   Get,  Put,   Delete -> Restful

class Hoteis(Resource):

    def get(self):
        
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

    features = reqparse.RequestParser()
    features.add_argument('name', type=str, required=True, help="The field 'name' cannot be empty")
    features.add_argument('city', type=str)
    features.add_argument('stars', type=float, required=True, help="The field 'stars' cannot be empty")
    features.add_argument('rate', type=str)

    
    def get(self, id):
        
        hotel = HotelModel.find_hotel(id)

        if hotel is not None:
            
            return hotel.json()

        else: return {'message': f"Hotel '{id}' not found"}, 404 # Not Found

    @jwt_required()
    def post(self, id):

        if HotelModel.find_hotel(id):

            return {'Message': f"id '{id}' already exists."}, 400
        
        data = Hotel.features.parse_args()

        obj_hotel = HotelModel(id, **data)

        try:

            obj_hotel.save_hotel()
        
        except: 
            return {'message': 'An internal error ocurred while trying to save hotel.'}, 500 # internal server error
        
        return obj_hotel.json()

    @jwt_required()
    def put(self, id):
               
        data = Hotel.features.parse_args()

        found_hotel = HotelModel.find_hotel(id)

        if found_hotel is not None:
            
            found_hotel.update_hotel(**data)

            found_hotel.save_hotel()

            return found_hotel.json(), 200 # OK

        obj_hotel = HotelModel(id, **data)

        try:

            obj_hotel.save_hotel()
        
        except: 

            return {'message': 'An internal error ocurred while trying to save hotel.'}, 500 # internal server error
        
        
        return obj_hotel.json(), 201 # created
    
    @jwt_required()
    def delete(self, id):

        hotel = HotelModel.find_hotel(id)

        if hotel:


            try:

                hotel.delete_hotel()
            
            except: 

                return {'message': 'An internal error ocurred while trying to delete hotel.'}, 500 # internal server error
            
            return {'message': f"Hotel '{id}' deleted."}

        return {'message': f"Hotel '{id}' not found."}, 404 
