#!/usr/bin/python3
"""Exports app_views"""
from flask import Blueprint
app_views = Blueprint('app_views', __name__)
from api.v1.views.states import *
from api.v1.views.index import *
