
def normalize_path_params(city=None, min_stars=0, max_stars=5, min_rate = 0, max_rate = 1000000, limit=50, offset=0, **data):

    if city:

        return {'min_stars': min_stars, 'max_stars': max_stars, 'min_rate': min_rate, 'max_rate': max_rate, 'city': city, 'limit': limit, 'offset':offset}

    return {'min_stars': min_stars, 'max_stars': max_stars, 'min_rate': min_rate, 'max_rate': max_rate, 'limit': limit, 'offset':offset}

query_without_city = "SELECT * FROM hoteis \
                    WHERE (stars > ? and stars < ?) \
                    and (rate > ? and rate < ?)\
                    LIMIT ? OFFSET ?"


query_with_city = "SELECT * FROM hoteis WHERE (stars > ?  AND stars < ?)\
                 AND (rate > ? and rate < ?)\
                 AND city = ? LIMIT ? OFFSET ?"