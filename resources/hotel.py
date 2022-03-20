from flask_restful import Resource, reqparse
from models.hotel import HotelModel

# CRUD: Create, Read, Update, Delete
#       Post,   Get,  Put,   Delete -> Restful

hoteis = [{'id': 'alpha',
            'name': 'Alpha Hotel',
            'stars': 4.3,
            'rate': 420.34,
            'city': 'Campinas'
},

{'id': 'beta',
            'name': 'Beta Hotel',
            'stars': 4.2,
            'rate': 422.34,
            'city': 'Santa Catarina'
},

{'id': 'gamma',
            'name': 'Gamma Hotel',
            'stars': 3.9,
            'rate': 429.4,
            'city':'São Paulo'
}]

class Hoteis(Resource):

    def get(self):
        
        return {'hoteis': hoteis}



class Hotel(Resource):

    features = reqparse.RequestParser()
    features.add_argument('name')
    features.add_argument('city')
    features.add_argument('stars')
    features.add_argument('rate')

    def find_hotel(id):

        for hotel in hoteis:

            if hotel['id'] == id:

                return hotel

        return None 
    
    def get(self, id):
        
        hotel = Hotel.find_hotel(id)

        if hotel is not None:
            
            return hotel

        else: return {'message': f'Hotel {id} not found'}, 404 # Not Found


    def post(self, id):

        data = Hotel.features.parse_args()

        obj_hotel = HotelModel(id, **data)

        new_hotel = obj_hotel.json()

        hoteis.append(new_hotel)

        return new_hotel, 200 # OK


    def put(self, id):
               
        data = Hotel.features.parse_args()

        obj_hotel = HotelModel(id, **data)

        new_hotel = obj_hotel.json()

        hotel = Hotel.find_hotel(id)

        if hotel is not None:
            
            hotel.update(new_hotel)
            
            return new_hotel, 200 # OK

        hoteis.append(new_hotel)

        return new_hotel, 201 # created

    def delete(self, id):

        global hoteis

        hoteis = [hotel for hotel in hoteis if hotel['id']!= id]

        return {'message': f'Hotel {id} deleted.'}, 200 # OK
