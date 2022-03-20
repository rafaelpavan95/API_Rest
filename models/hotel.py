class HotelModel():

    def __init__(self, id, name, stars, rate, city) -> None:
        
        self.id = id
        self.name = name
        self.stars = stars
        self.rate = rate
        self.city = city

    def json(self):

        return {'id': self.id, 'name': self.name, 'stars': self.stars, 'rate': self.rate, 'city': self.city}
