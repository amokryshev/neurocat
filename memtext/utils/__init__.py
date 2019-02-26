from __future__ import absolute_import
import json


class ResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ServiceResponse):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

class ServiceResponse:
    def __init__(self, success = False, data = {}, error = {'code' : 0, 'message' : 'Not initialized!'}):
        self.success = success
        if success:
            self.data = data
        else:
            self.error = error

    def to_json(self): return json.dumps(self, cls=ResponseEncoder)


