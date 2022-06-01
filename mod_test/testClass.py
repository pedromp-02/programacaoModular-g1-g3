from flask import jsonify
from flask_restful import Resource

class Test(Resource):
    def get(self):
        return jsonify({'aa': 'bb'})