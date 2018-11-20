from flask import Blueprint

delete_blue = Blueprint('delete_view', __name__, static_folder='static', template_folder='templates', url_prefix='/delete' )

from .views import *