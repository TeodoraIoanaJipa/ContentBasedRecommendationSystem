class Restaurant:
    def __init__(self, restaurant_id, name, price_category= None, street= None, kitchen_types= None, local_types= None, keywords= None):
        self.restaurant_id = restaurant_id
        self.name = name
        self.price_category = price_category
        self.street = street
        self.kitchen_types = kitchen_types
        self.local_types = local_types
        self.keywords = keywords

    def __repr__(self):  # to string
        if self.street:
            var = str(self.restaurant_id) + ", " + self.name + ", " \
                  + str(self.kitchen_types) + ", " + self.price_category + \
                  " " + self.street + " keywords : " + str(self.keywords)
        else:
            var = str(self.restaurant_id) + ", " + self.name
        return var

    def to_dict(self):
        return {
            'restaurant_id': self.restaurant_id,
            'name': self.name,
        }
