from flask import Blueprint
app_views = Blueprint('views', __name__)
from api.v1.views.states import *
from api.v1.views.index import *
