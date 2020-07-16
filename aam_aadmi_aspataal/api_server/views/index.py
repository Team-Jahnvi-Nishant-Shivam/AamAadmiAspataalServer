from aam_aadmi_aspataal import api_server
from flask import Blueprint, jsonify

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def signup():
    return jsonify(
        {
        'status': 'ok',
        'message': 'Welcome to Aam Aadmi Aspataal'
        }
    )
