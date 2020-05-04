# -*- coding: UTF-8 -*-

from flask import Flask
from flask import request
from flask.json import jsonify

from english.speak.storage import builder

app = Flask(__name__)

gt = builder.json_file("data/grammar.json")
mt = builder.flat_file("data/murphy.list")
pv = builder.flat_file_pairs("data/phrasal_verbs.list")
tp = builder.flat_file("data/topics.list")


@app.route('/topic')
def topic():
    return jsonify(tp.get_exact_part(1))


@app.route('/phrasal_verbs')
def phrasal_verbs():
    count = int(request.args.get('count', '10'))
    return jsonify(pv.get_exact_part(1))


@app.route('/grammar')
def grammar():
    return jsonify(gt.get_exact_part(1))


@app.route('/murphy')
def murphy():
    return jsonify(mt.get_exact_part(1))


@app.route('/vocabulary/<string:topic_value>')
def vocabulary(topic_value):
    vocab = builder.flat_file("data/vocabulary/{0}.list".format(topic_value))
    return jsonify(vocab.get_all())
