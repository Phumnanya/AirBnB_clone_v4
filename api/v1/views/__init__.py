#!/usr/bin/python3
"""Exports app_views"""
from flask import Blueprint
app_views = Blueprint('views', __name__)
from api.v1.views.states import *
from api.v1.views.index import *
from api.v1.views.users import *
