import json
import falcon
from falcon.util.uri import parse_query_string
from werkzeug.http import parse_options_header
from werkzeug.formparser import parse_form_data
from cStringIO import StringIO

def generate_formdata(req, resp, params):
    form = dict()
    files = dict()
    if req.method == 'GET':
        di = parse_query_string(req.query_string)
        form = dict(di)
        params['form'], params['files'] = dict(form), dict(files)
    else:
        if 'json' in req.get_header('content-type', None):
            #if the method type is post "form" variable below can contain 
            #only either the post body or the quer parameter at once, modify 
            #umcomment the below commented line to store query parameters in "form"
            form = json.load(req.stream)
            #form = dict(parse_query_string(req.query_string))
            params['form'], params['files'] = dict(form), dict(files)
        else:
            mimetype, options = parse_options_header(req.get_header('content-type'))
            data = req.stream.read()
            environ = {'wsgi.input':StringIO(data),
                       'CONTENT_LENGTH': str(len(data)),
                       'CONTENT_TYPE': req.get_header('content-type'),
                       'REQUEST_METHOD': 'POST'}
            stream, tempform, tempfiles = parse_form_data(environ)
            for item in tempform:
                form[item] = tempform[item]
            di = parse_query_string(req.query_string)
            for item in di:
                form[item] = di[item]
            for item in tempfiles:
                files[item] = tempfiles[item]
            params['form'], params['files'] = dict(form), dict(files)
    #print form
    #print params
    return True
