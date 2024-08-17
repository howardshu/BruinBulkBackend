# app.py
from flask import Flask, jsonify
from scraper import get_dining_hall_links, get_menu_for_hall

app = Flask(__name__)


@app.route('/dining_halls', methods=['GET'])
def dining_halls():
    halls = get_dining_hall_links()
    return jsonify(halls)


@app.route('/menu/<hall_name>', methods=['GET'])
def menu(hall_name):
    dining_halls = get_dining_hall_links()
    hall_url = dining_halls.get(hall_name)
    if not hall_url:
        return jsonify({"error": "Dining hall not found"}), 404

    menu = get_menu_for_hall(hall_url)
    return jsonify(menu)


if __name__ == '__main__':
    app.run(debug=True)