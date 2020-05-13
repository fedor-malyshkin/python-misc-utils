# -*- coding: UTF-8 -*-

from flask import Flask
from flask import request
from flask.json import jsonify
from flask_cors import CORS

from english.speak.storage import builder

# from flask_restx import Api

app = Flask(__name__)
CORS(app)
# api = Api(app, version='0.1', title='English study API',
#           description='Tiny API for english studying with a '
#                       'set of grammar rules, phrasal verbs and IELTS themes',
#           )

gt = builder.json_file("data/grammar.json")
mt = builder.flat_file("data/murphy.list")
pv = builder.flat_file_pairs("data/phrasal_verbs.list")
tp = builder.flat_file("data/topics.list")
gv = builder.flat_file("data/general_vocabulary.list")


@app.route('/topic')
def topic():
    return jsonify(tp.get_exact_part(1))


@app.route('/phrasal_verbs')
def phrasal_verbs():
    count = int(request.args.get('count', '5'))
    return jsonify(pv.get_exact_part(count))


@app.route('/grammar')
def grammar():
    count = int(request.args.get('count', '4'))
    return jsonify(gt.get_exact_part(count))


@app.route('/murphy')
def murphy():
    count = int(request.args.get('count', '4'))
    return jsonify(mt.get_exact_part(count))


@app.route('/vocabulary/<string:topic_value>')
def vocabulary(topic_value):
    vocab = builder.flat_file("data/vocabulary/{0}.list".format(topic_value))
    return jsonify(vocab.get_exact_part(7))


@app.route('/general_vocabulary')
def general_vocabulary():
    count = int(request.args.get('count', '5 '))
    return jsonify(gv.get_exact_part(count))
