from flask import Blueprint

index_blue = Blueprint('index_view',__name__)

from .views import *