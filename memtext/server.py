from flask import Flask, request, abort
from utils import ServiceResponse

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
        res = ServiceResponse(success=True, data={'id' : 1, 'length' : 12, 'lang' : 'en', 'text' : 'Hello World!'})
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

    app.run(host=config.get("Settings", "host"), port = config.get("Settings", "port"), debug=config.get("Settings", "debug"))