import os
from app.mod_auth.models import Mongo
import requests
from flask import Blueprint, request, jsonify, Response, render_template

mod = Blueprint('pages', __name__)