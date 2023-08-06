# @Date: 2021/9/3
# @Author: Hugh
# @Email: 609799548@qq.com

__all__ = ['request']

import os
import sys
import importlib

from flask import Flask, request

app = Flask(__name__, static_folder=None)

METHOD = 'method'
URL = 'url'
RESPONSE = 'response'


def get_dict_value(dic, key):
    try:
        return dic[key]
    except KeyError:
        raise ValueError('expose must has %s!' % key)


def mock_func(route, filename):
    method = route.get(METHOD, 'GET').upper()
    url = get_dict_value(route, URL)
    response = get_dict_value(route, RESPONSE)
    view_func = response if callable(response) else lambda: response
    methods = method if isinstance(method, (list, tuple)) else [method]
    app.add_url_rule(url, view_func=view_func, methods=methods, endpoint='%s.%s' % (filename, view_func.__name__))


def run(work_dir, port=5000):
    for filename in os.listdir(work_dir):
        if filename.endswith('.py'):
            m = importlib.import_module(filename[:-3])
            mock_func(getattr(m, 'expose'), filename)
    collection_routes()
    app.run(host='0.0.0.0', port=int(port))


def collection_routes():
    res = {}
    for route in app.url_map.iter_rules():
        res[route.rule] = '、'.join([method for method in route.methods if method not in ('HEAD', 'OPTIONS')])
    app.add_url_rule('/', view_func=lambda: res)


def main():
    msg = 'Usage: mock create project/interface <name>\nmock run port 5000'
    argv = sys.argv[1:]
    work_dir = os.getcwd()
    sys.path.insert(0, work_dir)
    if not argv:
        run(work_dir)
    elif len(argv) == 3:
        if argv[0] == 'create':
            if argv[1] == 'project':
                os.mkdir(os.path.join(work_dir, argv[2]))
                create_template(os.path.join(work_dir, argv[2], 'sample.py'))
            elif argv[1] == 'interface':
                create_template(os.path.join(work_dir, '%s.py' % argv[2]))
        elif argv[0] == 'run':
            if argv[1] == 'port':
                port = argv[2]
                run(work_dir, port)
        return
    print(msg)


def create_template(filepath):
    if os.path.exists(filepath):
        print('%s existing.' % filepath)
    else:
        s = '''\
"""
request has attrs: args、method、json ...
define a dict called expose:
    expose must have url、response
    expose response can be a dictionary or a callable object
"""
from quick_mock import request

expose = {
    'method': 'GET',
    'url': '/sample',
    'response': {
        'status': 200
    }
}'''
        with open(os.path.join(filepath), 'w', encoding='utf8') as f:
            f.write(s)


if __name__ == '__main__':
    main()
