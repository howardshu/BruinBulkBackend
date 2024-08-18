# app.py
from flask import Flask, jsonify, json
import Constants
from scraper import get_dining_halls, get_menu_for_hall
import numpy as np

app = Flask(__name__)


@app.route('/dining_halls', methods=['GET'])
def dining_halls():
    halls = get_dining_halls()
    return jsonify(halls)

# ex. hall_name = 'Rieber'
@app.route('/menu/<hall_name>', methods=['GET'])
def menu(hall_name):
    dining_halls = get_dining_halls()
    hall_link = "/Menus/" + hall_name
    found = hall_link in dining_halls
    if not found:
        return jsonify({"error": "Dining hall not found"}), 404

    menu = get_menu_for_hall(Constants.LINK + hall_link)

    # NumPy arrays cannot be jsonified, so turn them into lists
    for key in menu:
        if isinstance(menu[key], np.ndarray):
            menu[key] = menu[key].tolist()

    return jsonify(menu)
    # return json.dumps(menu)


if __name__ == '__main__':
    app.run(debug=True)