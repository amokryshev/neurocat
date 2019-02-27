from flask import Flask, request, abort
from utils import ServiceResponse
import pandas as pd
from langdetect import detect

import configparser
config = configparser.ConfigParser()
config.read('settings')


app = Flask(__name__)

@app.route('/memtext', methods=['GET'])
def memtext():
    langs_allowed = ('en', 'ru')
    maxlen = request.args.get('maxlen', type=int)
    lang = request.args.get('lang', type=str)
    if maxlen != None and langs_allowed.count(lang) == 1:
        mem = mems[mems.lang == lang][mems.length <= maxlen].sample(n=1)
        res = ServiceResponse(success=True, data={'length' : int(mem.length.iloc[0]), 'lang' : mem.lang.iloc[0], 'text' : mem.quote.iloc[0]})
        return res.to_json()
    else:
        abort(400)

@app.errorhandler(400)
def not_found(error):
    return ServiceResponse(error = {'code': 400, 'message': 'Bad Request!'}).to_json(), 400

@app.errorhandler(404)
def not_found(error):
    return ServiceResponse(error = {'code' : 404, 'message' : 'Not Found!'}).to_json(), 404

@app.errorhandler(405)
def not_found(error):
    return ServiceResponse(error = {'code': 405, 'message': 'Method Not Allowed!'}).to_json(), 405

if __name__ == '__main__':

    mems = pd.read_csv(config.get("Settings", "mems"), sep='\t', header=0, skip_blank_lines=True, engine="python", encoding='utf8', error_bad_lines=False)
    mems['length'] = mems.apply(lambda row: len(row.quote), axis=1)
    mems['lang'] = mems.apply(lambda row: detect(row.quote), axis=1)
    app.run(host=config.get("Settings", "host"), port = config.get("Settings", "port"), debug=config.get("Settings", "debug"))