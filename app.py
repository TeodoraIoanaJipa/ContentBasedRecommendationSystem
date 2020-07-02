from flask import Flask, jsonify, abort, make_response
from flask import request
from RestaurantRecommendation import make_recommendations_for_user
from RestaurantRecommendation import make_collaborative_recommendations_for_user

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)


@app.route('/recommendation/api/v1.0/restaurants/<int:user_id>', methods=['GET'])
def get_restaurants(user_id):
    recommended_restaurants = make_recommendations_for_user(user_id)
    return jsonify({'restaurant_ids': recommended_restaurants})


@app.route('/recommendation/api/restaurant-collaborative/<int:user_id>', methods=['GET'])
def get_collaborative_recomendation(user_id):
    recommended_restaurants = make_collaborative_recommendations_for_user(user_id)
    return jsonify({'restaurant_ids': recommended_restaurants})



if __name__ == '__main__':
    app.run(debug=True)
