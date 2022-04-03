from sql_alchemy import database


class HotelModel(database.Model):
    
    __tablename__ = 'hoteis'

    id = database.Column(database.String(40), primary_key = True)
    name = database.Column(database.String(80))
    stars = database.Column(database.Float(precision=1))
    rate = database.Column(database.Float(precision=2))
    city = database.Column(database.String(40))


    def __init__(self, id, name, stars, rate, city) -> None:
        
        self.id = id
        self.name = name
        self.stars = stars
        self.rate = rate
        self.city = city


    def json(self):

        return {'id': self.id, 'name': self.name, 'stars': self.stars, 'rate': self.rate, 'city': self.city}


    @classmethod
    def find_hotel(cls, id):

        hotel = cls.query.filter_by(id = id).first()
        
        if hotel:
            return hotel
        
        return None


    def save_hotel(self):

        database.session.add(self)
        database.session.commit()


    def update_hotel(self, name, stars, rate, city):

        self.name = name
        self.stars = stars
        self.rate = rate
        self.city = city

    def delete_hotel(self):
        
        database.session.delete(self)
        database.session.commit()