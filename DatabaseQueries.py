import pyodbc

def make_database_connection():
    db_name = 'foodzDB'
    connection = pyodbc.connect('Driver={SQL Server};'
                          'Server=localhost\SQLEXPRESS;'
                          'Database=' + db_name + ';'
                           'Trusted_Connection=yes;')
    return connection


def get_restaurants(connection):
    cursor = connection.cursor()
    restaurants = cursor.execute(
        'SELECT r.restaurant_id, r.name, r.price_category, a.street '
        'FROM foodzDB.dbo.restaurants r join foodzDB.dbo.address a on r.address_id = a.address_id ').fetchall()
    return restaurants

def get_reviews(connection, user_id):
    cursor = connection.cursor()
    reviews = cursor.execute('SELECT rating, restaurant_id FROM '
                             'foodzDB.dbo.review where user_id = ? ', user_id).fetchall()
    return reviews

def get_users_reviews(connection):
    cursor = connection.cursor()
    reviews = cursor.execute('SELECT avg(rating), restaurant_id, user_id FROM '
                             'foodzDB.dbo.review '
                             'group by user_id, restaurant_id').fetchall()
    return reviews

def get_keywords(connection, restaurant_id):
    cursor = connection.cursor()
    keywords = cursor.execute(""" select tag_name FROM foodzDB.dbo.tag_restaurant where restaurant_id = ? """,
                              restaurant_id).fetchall()
    return keywords


def get_local_types(connection, restaurant_id):
    cursor = connection.cursor()
    local_types = cursor.execute(""" select lt.local_type FROM foodzDB.dbo.local_types lt 
                 join foodzDB.dbo.local_restaurant lr on lr.local_type_id = lt.type_id where restaurant_id = ? """,
                                   restaurant_id).fetchall()
    return local_types

def get_kitchen_types(connection, restaurant_id):
    cursor = connection.cursor()
    kitchen_types = cursor.execute(""" select kt.kitchen_type FROM foodzDB.dbo.kitchen_types kt 
                 join foodzDB.dbo.kitchen_restaurant kr on kr.kitchen_id = kt.type_id where restaurant_id = ? """,
                                   restaurant_id).fetchall()
    return kitchen_types

def get_all_reviews(connection):
    cursor = connection.cursor()
    reviews = cursor.execute('SELECT rating, restaurant_id FROM '
                             'foodzDB.dbo.review ').fetchall()
    return reviews
