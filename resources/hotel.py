from flask_restful import Resource

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
