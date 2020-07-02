import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances
#
#
# def find_n_neighbours(df, n):
#     order = np.argsort(df.values, axis=1)[:, :n]
#     df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
#                                       .iloc[:n].index,
#                                       index=['top{}'.format(i) for i in range(1, n + 1)]), axis=1)
#     return df
#
#
# def get_user_similar_movies(user1, user2):
#     common_movies = Rating_avg[Rating_avg.userId == user1].merge(
#         Rating_avg[Rating_avg.userId == user2],
#         on="movieId",
#         how="inner")
#
#     return common_movies.merge(movies, on='movieId')
#
# def User_item_score(user_index):
#     movies_seen_by_user = final.columns[final[final.index==user_index].notna().any()].tolist()
#     print(movies_seen_by_user)
#     a = similar_30_users[similar_30_users.index==user_index].values
#     similar_users_list = a.squeeze().tolist()
#     d = Movie_user[Movie_user.index.isin(similar_users_list)]
#     l = ','.join(d.values)
#     Movie_seen_by_similar_users = l.split(',')
#     Movies_under_consideration = list(set(Movie_seen_by_similar_users)-set(list(map(str, movies_seen_by_user))))
#     Movies_under_consideration = list(map(int, Movies_under_consideration))
#     score = []
#     for item in Movies_under_consideration:
#         c = final_movie.loc[:,item]
#         d = c[c.index.isin(similar_users_list)]
#         f = d[d.notnull()]
#         avg_user = Mean.loc[Mean['userId'] == user_index,'rating'].values[0]
#         index = f.index.values.squeeze().tolist()
#         corr = similarity_with_movie.loc[user_index,index]
#         fin = pd.concat([f, corr], axis=1)
#         fin.columns = ['adg_score','correlation']
#         fin['score']=fin.apply(lambda x:x['adg_score'] * x['correlation'],axis=1)
#         nume = fin['score'].sum()
#         deno = fin['correlation'].sum()
#         final_score = avg_user + (nume/deno)
#         score.append(final_score)
#     data = pd.DataFrame({'movieId':Movies_under_consideration,'score':score})
#     top_5_recommendation = data.sort_values(by='score',ascending=False).head(5)
#     Movie_Name = top_5_recommendation.merge(movies, how='inner', on='movieId')
#     Movie_Names = Movie_Name.title.values.tolist()
#     return Movie_Names
#
#
# movies = pd.read_csv("movies.csv", encoding="Latin1")
# Ratings = pd.read_csv("ratings.csv")
#
# #aflu ratingul mediu dat de fiecare user
# Mean = Ratings.groupby(by="userId", as_index=False)['rating'].mean()
#
# Rating_avg = pd.merge(Ratings, Mean, on='userId')
# # concatenez acel rating mediu la toate ratingurile
# print(Rating_avg.head(10))
# Rating_avg['adg_rating'] = Rating_avg['rating_x'] - Rating_avg['rating_y']
# # calculez diferenta dintre rating si ratingul mediu
# print(Rating_avg.head())
#
# final = pd.pivot_table(Rating_avg, values='adg_rating', index='userId', columns='movieId')
# print('final')
# print(final.head(10))
# # am Nan la filmele pe care userii nu le-au vazut
# # Replacing NaN by Movie Average
# final_movie = final.fillna(final.mean(axis=0))
#
# # Replacing NaN by user Average
# final_user = final.apply(lambda row: row.fillna(row.mean()), axis=1)
# print(final_movie.head(10))
#
# # user similarity on replacing NAN by user avg
#
# # b = cosine_similarity(final_user)
# # np.fill_diagonal(b, 0)
# # similarity_with_user = pd.DataFrame(b, index=final_user.index)
# # similarity_with_user.columns = final_user.index
# # similarity_with_user.head()
#
# # user similarity on replacing NAN by item(movie) avg
# cosine = cosine_similarity(final_movie)
# np.fill_diagonal(cosine, 0)
# print(cosine)
# similarity_with_movie = pd.DataFrame(cosine, index=final_movie.index)
# similarity_with_movie.columns = final_movie.index
# print(similarity_with_movie.head())
#
# # top 30 neighbours for each user
# # sim_user_30_u = find_n_neighbours(similarity_with_user, 30)
# # sim_user_30_u.head()
# similar_30_users = find_n_neighbours(similarity_with_movie,30)
# print(similar_30_users)
# a = get_user_similar_movies(370,86309)
# a = a.loc[ : , ['rating_x_x','rating_x_y','title']]
# # print(a)
#
# # score = User_item_score(320,7371)
# # print("score (u,i) is",score)
# Rating_avg = Rating_avg.astype({"movieId": str})
# Movie_user = Rating_avg.groupby(by = 'userId')['movieId'].apply(lambda x:','.join(x))
#
# current_user_id = int(input("Enter the user id to whom you want to recommend : "))
# predicted_movies = User_item_score(current_user_id)
#
# for i in predicted_movies:
#     print(i)
from UserBasedCollaborativeRecommendation import get_collaborative_recommended_restaurants
