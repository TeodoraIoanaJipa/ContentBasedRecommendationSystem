from DatabaseQueries import *
from UserBasedCollaborativeRecommendation import get_collaborative_recommended_restaurants
from model.Restaurants import Restaurant
from model.Review import Review
from ContentBasedRecommendation import get_similar_restaurants
from PopularityBasedRecommendation import get_popular_restaurants
from collections import Counter
import numpy


def clean_ratings_for_each_restaurant(users_reviews):
    ratings = []
    if len(users_reviews) > 0:
        rest_id = users_reviews[0].restaurant_id
        sum = 0
        count = 0
        for index in range(len(users_reviews)):
            if users_reviews[index].restaurant_id != rest_id:
                ratings.append(Review(sum / count, rest_id))
                count = 1
                sum = users_reviews[index].rating
                rest_id = users_reviews[index].restaurant_id
            else:
                sum += users_reviews[index].rating
                count += 1
        ratings.append(Review(sum / count, rest_id))
    return ratings


def show_list(list):
    for r in list:
        print(r)
    print("\n")


def get_reviews_from_database(conn, user_id):
    reviews_list = []
    reviews = get_reviews(conn, user_id)

    for row in reviews:
        new_restaurant = Review(row[0], row[1], None)
        reviews_list.append(new_restaurant)

    reviews_list.sort(key=lambda x: x.restaurant_id)

    return reviews_list

def get_restaurants_names_and_ids(conn):
    restaurants_list = []
    restaurants = get_restaurants(conn)
    for row in restaurants:
        new_restaurant = Restaurant(row[0], row[1])
        restaurants_list.append(new_restaurant)
    return restaurants_list

def get_restaurants_keywords_kitchentypes_localtypes(conn):
    restaurants_list = []
    restaurants = get_restaurants(conn)
    for row in restaurants:
        keywords = get_keywords(conn, row[0])
        kitchen_types = get_kitchen_types(conn, row[0])
        local_types = get_local_types(conn, row[0])
        my_keywords = []
        my_kitchen_types = []
        my_local_types = []
        for key in keywords:
            my_keywords.append(key[0])
        for kitchen_type in kitchen_types:
            my_kitchen_types.append(kitchen_type[0])
        for type in local_types:
            my_local_types.append(type[0])
        new_restaurant = Restaurant(row[0], row[1], row[2], row[3], my_kitchen_types, my_local_types,
                                    my_keywords)
        restaurants_list.append(new_restaurant)
    return restaurants_list


def combine_features(restaurant):
    return restaurant.street + " " + restaurant.price_category + " " + ' '.join(restaurant.kitchen_types) + " " + \
           ' '.join(restaurant.local_types) + " " + ' '.join(restaurant.keywords)


def clean_data(df):
    data = []
    for elem in df:
        data.append(combine_features(elem).replace('\n', ' ').replace('\r', ' '))
    return data




def get_content_based_recommendations(reviews, restaurants, rests):
    # print('cleaned data ')
    # show_list(rests)
    # print("\n")
    restaurants_recommendation_full_list = []
    for review in reviews:
        recommended_restaurants = get_similar_restaurants(restaurants, rests, review.restaurant_id)
        restaurants_recommendation_full_list.append(recommended_restaurants)

    my_list = list(numpy.concatenate(restaurants_recommendation_full_list))
    print(my_list)
    restaurants_frequencies = Counter(my_list)
    print(Counter(my_list))
    final_restaurants_ids = []
    for key, value in Counter(my_list).most_common(8):
        final_restaurants_ids.append(key)
    print(final_restaurants_ids)
    return final_restaurants_ids


def get_popularity_based_recommendations(restaurants, rests):
    connection = make_database_connection()
    reviews = get_all_reviews(connection)
    reviews_list = []
    for row in reviews:
        new_restaurant = Review(row[0], row[1], None)
        reviews_list.append(new_restaurant)
    return get_popular_restaurants(restaurants, reviews_list)


def add_not_recommended_restaurants(parsed_list, restaurants):
    for restaurant in restaurants:
        if restaurant.restaurant_id not in parsed_list:
            parsed_list.append(restaurant.restaurant_id)
    return parsed_list


def make_collaborative_recommendations_for_user(user_id):
    connection = make_database_connection()
    reviews = get_users_reviews(connection)
    restaurants = get_restaurants_names_and_ids(connection)
    reviews_list = []
    for row in reviews:
        new_review = Review(row[0], row[1], row[2])
        reviews_list.append(new_review)
    reviews_list.sort(key=lambda x: (x.user_id, x.restaurant_id))
    restaurants_recommendation = get_collaborative_recommended_restaurants(user_id, restaurants, reviews_list)
    list = add_not_recommended_restaurants(restaurants_recommendation, restaurants)
    print(list)
    return numpy.array(list).tolist()

def make_recommendations_for_user(user_id):
    connection = make_database_connection()

    restaurants = get_restaurants_keywords_kitchentypes_localtypes(connection)
    reviews = get_reviews_from_database(connection, user_id)
    reviews = clean_ratings_for_each_restaurant(reviews)

    highest_reviews = [review for review in reviews if review.rating >= 4]
    show_list(highest_reviews)

    rests = clean_data(restaurants)
    print(rests)

    list_of_rests = []
    print("length reviews ", len(highest_reviews));
    if len(reviews) >= 5:
        list_of_rests = get_content_based_recommendations(highest_reviews, restaurants, rests)
        parsed_list = list_of_rests
    else:  # new user who does not have any reviews.. give him popular restaurants then
        list_of_rests = get_popularity_based_recommendations(restaurants, rests)
        parsed_list = []
        print(list_of_rests)
        for i, j in list_of_rests.iteritems():
            parsed_list.append(int(i))

    list = add_not_recommended_restaurants(parsed_list, restaurants)
    print(list)
    return numpy.array(list).tolist()
