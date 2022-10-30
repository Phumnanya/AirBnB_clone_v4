#!/usr/bin/python3
"""starts a simple flask web app"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
import uuid

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/1-hbnb/')
def hbnb():
    """lists all cities in alphabetical order"""
    States = storage.all(State).values()
    Amenities = storage.all(Amenity).values()
    Places = storage.all(Place).values()
    return render_template("1-hbnb.html",
                           States=States,
                           Amenities=Amenities,
                           Places=Places,
                           cache_id=uuid.uuid4())


@app.teardown_appcontext
def tear_Down(exception):
    """closes a db session or reload file storage"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
