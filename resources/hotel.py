from multiprocessing import connection
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

# CRUD: Create, Read, Update, Delete
#       Post,   Get,  Put,   Delete -> Restful

def normalize_path_params(city=None, min_stars=0, max_stars=5, min_rate = 0, max_rate = 1000000, limit=50, offset=0, **data):

    if city:

        return {'min_stars': min_stars, 'max_stars': max_stars, 'min_rate': min_rate, 'max_rate': max_rate, 'city': city, 'limit': limit, 'offset':offset}

    return {'min_stars': min_stars, 'max_stars': max_stars, 'min_rate': min_rate, 'max_rate': max_rate, 'limit': limit, 'offset':offset}

path_params = reqparse.RequestParser()
path_params.add_argument('city', type=str)
path_params.add_argument('stars',type=float)
path_params.add_argument('min_stars',type=float)
path_params.add_argument('max_stars',type=float)
path_params.add_argument('min_rate',type=float)
path_params.add_argument('max_rate',type=float)
path_params.add_argument('limit',type=float)
path_params.add_argument('offset',type=float)

class Hoteis(Resource):

    def get(self):

        connection = sqlite3.connect('database.db')
        
        cursor = connection.cursor()
        
        data = path_params.parse_args()
        
        data_full = {key:data[key] for key in data if data[key] is not None}
        
        parameters = normalize_path_params(**data_full)
        
        if not parameters.get('city'):
            
            query = "SELECT * FROM hoteis \
                    WHERE (stars > ? and stars < ?) \
                    and (rate > ? and rate < ?)\
                    LIMIT ? OFFSET ?"

            tupl = tuple([parameters[key] for key in parameters.keys()])

            results = cursor.execute(query, tupl)

        else:
            
            query = "SELECT * FROM hoteis WHERE (stars > ?  AND stars < ?)\
                 AND (rate > ? and rate < ?)\
                 AND city = ? LIMIT ? OFFSET ?"
            
            
            tupl = tuple([parameters[key] for key in parameters])

            results = cursor.execute(query, tupl)
            

        hoteis = []

        for line in results:

            hoteis.append({
                            "id": line[0],
                            "name": line[1],
                            "stars": line[2],
                            "rate": line[3],
                            "city": line[4]
                           })

        return {'hoteis': hoteis}

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
