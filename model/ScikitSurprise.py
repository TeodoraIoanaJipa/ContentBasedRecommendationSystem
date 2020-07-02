#Collaborative filtering
#I think it suits better for my needs
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from RestaurantRecommendation import make_recommendations_for_user

# data = pd.read_csv("C://Users//teote//PycharmProjects//FoodzRecommendaionSystem//movie_dataset.csv")
data = make_recommendations_for_user(2)

# data.__delattr__('rating').value_counts().plot(kind='bar')
# plt.show()