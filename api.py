import model
from flask import Flask, request, jsonify

app = Flask(__name__)

# список всех фильмов
@app.route('/api/movies', methods = ['GET'])
def get_all_movies():
    movies = model.get_all_movies()
    return jsonify(movies)

# фильм по id
@app.route('/api/movies/<id>', methods = ['GET'])
def get_movie(id):
    movie = model.get_movie(id)
    return jsonify(movie)

# оценки (фильтруем по userId и movieId)
@app.route('/api/ratings', methods=['GET'])
def get_ratings():
    args = request.args
    ratings = model.get_ratings(args.to_dict())
    return jsonify(ratings)

# новая оценка
@app.route('/api/ratings', methods=['POST'])
def post_rating():
    rating = request.get_json(force=True)
    model.add_rating(rating)
    return '', 201

# теги (фильтруем по userId и movieId)
@app.route('/api/tags', methods=['GET'])
def get_tags():
    args = request.args
    tags = model.get_tags(args.to_dict())
    return jsonify(tags)

# новый тег
@app.route('/api/tags', methods=['POST'])
def post_tag():
    tag = request.get_json(force=True)
    model.add_tag(tag)
    return '', 201

if __name__ == '__main__':
    app.run(debug=True)