class Review:
    def __init__(self, rating, restaurant_id, user_id = None):
        self.rating = rating
        self.restaurant_id = restaurant_id
        self.user_id = user_id

    def __repr__(self):  # to string
        var = " UserId " + str(self.user_id) + " Restaurant_id " + str(self.restaurant_id) + \
              " Rating " + str(self.rating)

        return var

    def __eq__(self, other):
        return self.rating == other.rating and self.restaurant_id == other.restaurant_id \
               and self.user_id == other.user_id

    def to_dict(self):
        return {
            'restaurant_id': self.restaurant_id,
            'rating': self.rating,
            'user_id': self.user_id
        }
