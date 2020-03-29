from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


def start_server():
    app.run(debug=True)


api.add_resource(HelloWorld, '/')
