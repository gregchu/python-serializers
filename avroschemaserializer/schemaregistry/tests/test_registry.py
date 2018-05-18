# from bottle import route, response
# import setup_test_path
# import data_gen
# import json
# from patched_bottle_daemon import *
#
# schema_cache = {}
# schema = data_gen.load_schema_file('basic_schema.avsc')
#
# def _send_response(resp, status, body):
#     resp.status = status
#     resp.content_type = "application/json"
#     return json.dumps(body).encode('utf-8')
#
# @route('/subjects/<subject>/versions/latest', method='GET')
# def get_latest(subject):
#     result = {
#         "schema" : schema,
#         "subject" : subject,
#         "id" : 1,
#         "version" : 1
#     }
#     resp = _send_response(response, 200, result)
#     return resp
#
# @route('/schemas/ids/<id>', method='GET')
# def get_schema_by_id(id):
#     result = {
#         "schema": schema
#     }
#     resp = _send_response(response, 200, result)
#     return resp
#
# @route('/subjects/<schema>/versions', method='POST')
# def register(schema):
#     schema_id = 1
#     resp = _send_response(response, 200, {'id' : schema_id })
#     return resp
#
# @route('/subjects/<subject>', method='POST')
# def get_version(subject):
#     result = {
#         "schema" : schema,
#         "subject" : subject,
#         "id" : 1,
#         "version" : 1
#     }
#     resp = _send_response(response, 200, result)
#     return resp
#
# class Server():
#
# def start(self):
# bottle_daemon_run(cmd='Start')
#
# def stop(self, cmd):
# testargs = [cmd]
# with patch.object(sys, 'argv', testargs):
# bottle_daemon_run(cmd='Stop')
#
#
#
