import neo
import elastic
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/neo4j/<int:query_id>')
def neo4j(query_id):
    return jsonify(neo.execute_query(query_id))


@app.route('/elastic/<int:query_id>')
def es(query_id):
    return jsonify(elastic.execute_query(query_id))
