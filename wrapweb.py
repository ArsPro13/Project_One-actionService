from flask import Flask, render_template, request
import importlib
import ast
import os
import models
from initApp import app
from inspect import getmembers, isfunction


def toweb(f, url_site: str, parameters: dict):
    #app = Flask(__name__)

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
    toweb(func, url_site, parameters).run(host='0.0.0.0', port=5001)


def get_parameters(name_file: str) -> list:
    with open(name_file) as file:
        lines = [line.rstrip() for line in file]
    parameters = []
    for line in lines:
        first_space = line.find(" ")
        second_space = line.find(" ", first_space + 1)
        url = line[:first_space]
        name_func_file = line[first_space + 1: second_space]
        str_parameters = line[second_space + 1:]
        parameters.append([url, name_func_file, ast.literal_eval(str_parameters)])
    return parameters


def route_url(now_path: str):
    for root, dirs, files in os.walk(now_path):
        for dir in dirs:
            route_url(dir)
        for file in files:
            if file == '__init__.py':
                for url, name_func_file, parameters in get_parameters(file):
                    wrapweb(url, name_func_file, parameters)


route_url(os.getcwd())