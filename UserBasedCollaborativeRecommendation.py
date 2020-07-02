import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances


def find_n_neighbours(df, n):
    print(df.shape[0])
    if n > df.shape[0]:
        n = df.shape[0] - 1
    order = np.argsort(df.values, axis=1)[:, :n]
    df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
                                      .iloc[:n].index,
                                      index=['top{}'.format(i) for i in range(1, n + 1)]), axis=1)
    return df


def get_user_similar_movies(user1, user2, Rating_avg, movies):
    common_movies = Rating_avg[Rating_avg.userId == user1].merge(
        Rating_avg[Rating_avg.userId == user2],
        on="movieId",
        how="inner")

    return common_movies.merge(movies, on='movieId')


def User_item_score(user_index, restaurants, final, similar_users, restaurant_user, final_movie,
                    Mean, similarity_with_movie):
    print(final)
    movies_seen_by_user = final.columns[final[final.index == user_index].notna().any()].tolist()
    print(movies_seen_by_user)
    a = similar_users[similar_users.index == user_index].values
    similar_users_list = a.squeeze().tolist()
    print('similar users')
    print(similar_users_list)
    d = ','.join(restaurant_user[restaurant_user.index.isin(similar_users_list)].values)
    movie_seen_by_similar_users = d.split(',')
    restaurants_under_consideration = list(set(movie_seen_by_similar_users) - set(list(map(str, movies_seen_by_user))))
    print('movies seen by user')
    print(set(list(map(str, movies_seen_by_user))))
    print('movies seen by others')
    print(set(movie_seen_by_similar_users))
    print('finaly')
    print(restaurants_under_consideration)

    restaurants_under_consideration = list(map(int,  restaurants_under_consideration))
    score = []
    for item in restaurants_under_consideration:
        c = final_movie.loc[:, item]
        d = c[c.index.isin(similar_users_list)]
        f = d[d.notnull()]
        avg_user = Mean.loc[Mean['user_id'] == user_index, 'rating'].values[0]
        index = f.index.values.squeeze().tolist()
        corr = similarity_with_movie.loc[user_index, index]
        fin = pd.concat([f, corr], axis=1)
        fin.columns = ['adg_score', 'correlation']
        fin['score'] = fin.apply(lambda x: x['adg_score'] * x['correlation'], axis=1)
        nume = fin['score'].sum()
        deno = fin['correlation'].sum()
        final_score = avg_user + (nume / deno)
        score.append(final_score)
    data = pd.DataFrame({'restaurant_id': restaurants_under_consideration, 'score': score})
    top_recommendation = data.sort_values(by='score', ascending=False).head(15)
    Movie_Name = top_recommendation.merge(restaurants, how='inner', on='restaurant_id')
    Movie_Names = Movie_Name.name.values.tolist()
    return top_recommendation.values.tolist()


def get_collaborative_recommended_restaurants(user_index, restaurants, ratings):
    restaurants = pd.DataFrame.from_records([s.to_dict() for s in restaurants])
    # aflu ratingul mediu dat de fiecare user
    all_ratings = pd.DataFrame.from_records([s.to_dict() for s in ratings])
    mean_ratings = all_ratings.groupby(by="user_id", as_index=False)['rating'].mean()
    print(mean_ratings)
    all_ratings = pd.merge(all_ratings, mean_ratings,
                           on='user_id')  # concatenez acel rating mediu la lista cu ratingurile

    all_ratings['adg_rating'] = all_ratings['rating_x'] - all_ratings['rating_y']
    # calculez diferenta dintre rating si ratingul mediu

    final = pd.pivot_table(all_ratings, values='adg_rating', index='user_id', columns='restaurant_id')

    final = final.fillna(final.mean(axis=0))  # am Nan la filmele pe care userii nu le-au vazut

    final_user = final.apply(lambda row: row.fillna(row.mean()), axis=1)  # Replacing NaN by user Average

    # user similarity on replacing NAN by item(movie) avg
    cosine_sim = cosine_similarity(final)
    np.fill_diagonal(cosine_sim, 0)
    similarity_with_movie = pd.DataFrame(cosine_sim, index=final.index)
    similarity_with_movie.columns = final.index

    similar_30_users = find_n_neighbours(similarity_with_movie, 15)
    print('similar users')
    print(similar_30_users)

    Rating_avg = all_ratings.astype({"restaurant_id": str})
    restaurant_user = Rating_avg.groupby(by='user_id')['restaurant_id'].apply(lambda x: ','.join(x))
    print('rest')
    print(restaurant_user)

    current_user_id = int(user_index)
    predicted_restaurants = User_item_score(current_user_id, restaurants, final, similar_30_users,
                                       restaurant_user, final, mean_ratings, similarity_with_movie)

    for i in predicted_restaurants:
        print(i)
    return  predicted_restaurants
