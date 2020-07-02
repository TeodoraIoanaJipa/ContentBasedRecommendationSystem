import pandas as pd

def get_popular_restaurants(restaurants_data, ratings_data):
    print('sunt in get popular restaurants')
    restaurants_dataframe = pd.DataFrame.from_records([s.to_dict() for s in restaurants_data])

    ratings_dataframe = pd.DataFrame.from_records([s.to_dict() for s in ratings_data])

    restaurant_final_data = pd.merge(ratings_dataframe,restaurants_dataframe, on='restaurant_id')
    restaurant_final = restaurant_final_data.groupby('restaurant_id')['rating'].mean().sort_values(ascending=False).to_frame()
    restaurant_final = restaurant_final.loc[:,'rating']
    return restaurant_final