from flask import Flask, render_template, request
import importlib
import os
from inspect import getmembers, isfunction


def toweb(f, url_site: str, parameters: dict):
    app = Flask(__name__)

    @app.route('/' + url_site, methods=['GET', 'POST'])
    def myfunc():
        about = f.__doc__
        a = f.__annotations__
        if 'return' in a:
            a.pop('return')

        if request.form:
            res = f(**request.form)
        else:
            res = None

        return render_template('func.html', about=about, a=a, res=res)

    return app


def wrapweb(url_site: str, name_file: str, parameters: dict):
    module = importlib.import_module(name_file[:-3])
    func = getmembers(module, isfunction)[0][1]
    toweb(func, url_site, parameters).run(host='0.0.0.0', port="5001")


def get_parameters(name_file: str) -> (str, str, dict):
    '''
    тут должна быть функция, которая получает параметры на основе файла __init__.py
    '''
    return 'title', 'function.py', {}


def route_url(now_path: str):
    for root, dirs, files in os.walk(now_path):
        for dir in dirs:
            route_url(dir)
        for file in files:
            if file == '__init__.py':
                wrapweb(*get_parameters(file))


route_url(os.getcwd())