from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_similar_restaurants(restaurants, restaurant_features, restaurant_liked_by_user):
    cv = CountVectorizer()
    count_words_matrix = cv.fit_transform(restaurant_features)

    cosine_sim = cosine_similarity(count_words_matrix)
    restaurant_index = get_restaurant_index_from_restaurant_id(restaurants, restaurant_liked_by_user)
                                                                                                                        # gasim similaritatile dintre restaurantul apreciat si toate celelalte mergand pe linia corespunzatoare acestuia
    similar_scores = list(enumerate(cosine_sim[restaurant_index]))                                                      # accessing the row corresponding to given movie to find
    sorted_similar_restaurants = sorted(similar_scores, key=lambda x: x[1], reverse=True)                               # all the similarity scores for that movie and then enumerating over it#sortam restaurantele dupa scorul de similaritate aflat pe coloana a doua

    counter = 20 * len(sorted_similar_restaurants) / 100
    similar_restaurant_ids = []

    i = 0
    for element in sorted_similar_restaurants:
        similar_restaurant_ids.append(get_restaurant_id_from_index(element[0], restaurants))
        i = i + 1
        if i > counter:
            break
    return similar_restaurant_ids


def get_restaurant_name_from_index(rest_index, restaurants):
    for i in range(len(restaurants)):
        if i == rest_index:
            return restaurants[i].name
    return "none"


def get_restaurant_id_from_index(rest_index, restaurants):
    for i in range(len(restaurants)):
        if i == rest_index:
            return restaurants[i].restaurant_id
    return -1


def get_restaurant_index_from_restaurant_id(restaurants, r_id):
    for i in range(len(restaurants)):
        if restaurants[i].restaurant_id == r_id:
            return i
    return -1


def get_index_from_title(title, dataframe):
    return dataframe[dataframe.title == title]["index"].values[0]
