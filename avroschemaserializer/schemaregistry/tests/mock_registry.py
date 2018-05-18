import re
import json
import http.server
from threading import Thread

from avroschemaserializer.schemaregistry.tests import data_gen

from avroschemaserializer.schemaregistry.serializers import Util


class ReqHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def do_GET(self):
        self.server._run_routes(self)

    def do_POST(self):
        self.server._run_routes(self)

    def log_message(self, format, *args):
        pass


class MockServer(http.server.HTTPServer, object):

    def __init__(self, *args, **kwargs):
        super(MockServer, self).__init__(*args, **kwargs)
        self.counts = { }
        self.schema_cache = { }
        self.all_routes = {
            'GET' : [
                (r"/schemas/ids/(\d+)", 'get_schema_by_id'),
                (r"/subjects/(\w+-\w+)/versions/latest", 'get_latest')
            ],
            'POST' : [
                (r"/subjects/(\w+-\w+)/versions", 'register'),
                (r"/subjects/(\w+-\w+)", 'get_version')
            ]
        }
        self.schema = data_gen.load_schema_file('basic_schema.avsc')

    def _send_response(self, resp, status, body):
        resp.send_response(status)
        resp.send_header("Content-Type", "application/json")
        resp.end_headers()
        resp.wfile.write(json.dumps(body).encode('utf-8'))

    def _create_error(self, msg, status=400, err_code=1):
        return (status, {
            "error_code" : err_code,
            "message" : msg
        })

    def _run_routes(self, req):
        self.add_count((req.command, req.path))
        routes = self.all_routes.get(req.command, [])
        for r in routes:
            m = re.match(r[0], req.path)
            if m:
                func = getattr(self, r[1])
                status, body = func(req, m.groups())
                ret = self._send_response(req, status, body)
                return ret

        # here means we got a bad req
        status, body = self._create_error("bad path specified")
        self._send_response(req, status, body)

    def get_schema_by_id(self, req, groups):
        result = {
            "schema" : self.schema
        }
        return (200, result)

    def _get_identity_schema(self, avro_schema):
        return json.dumps(avro_schema.to_json())

    def _get_schema_from_body(self, req):
        length = req.headers['content-length']
        data = req.rfile.read(int(length))
        data = json.loads(data.decode('utf-8'))
        schema = data.get("schema", None)

        if not schema:
            return None
        try:
            avro_schema = Util.parse_schema_from_string(schema)
            return self._get_identity_schema(avro_schema)
        except:
            return None

    def register(self, req, groups):
        schema_id = 1
        return (200, {'id' : schema_id })

    def get_version(self, req, groups):
        avro_schema = self._get_schema_from_body(req)

        if not avro_schema:
            return self._create_error("Invalid avro schema", 422, 42201)
        subject = groups[0]
        version = 1
        if version == -1:
            return self._create_error("Not found", 404)
        schema_id = 1

        result = {
            "schema" : avro_schema,
            "subject" : subject,
            "id" : schema_id,
            "version" : version
        }
        return (200, result)

    def get_latest(self, req, groups):
        subject = groups[0]
        result = {
            "schema" : self.schema,
            "subject" : subject,
            "id" : 1,
            "version" : 1
        }
        return (200, result)

    def add_count(self, path):
        if path not in self.counts:
            self.counts[path] = 0
        self.counts[path] += 1


class ServerThread(Thread):

    def __init__(self, port):
        Thread.__init__(self)
        self.server = None
        self.port = port

    def run(self):
        self.server = MockServer(('127.0.0.1', self.port), ReqHandler)
        self.server.serve_forever()

    def shutdown(self):
        if self.server:
            self.server.shutdown()
            self.server.socket.close()


if __name__ == '__main__':
    s = ServerThread(9001)
    s.start()
