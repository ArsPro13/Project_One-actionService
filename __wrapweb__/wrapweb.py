from flask import Flask, render_template, request
import importlib
import ast
import os
import asyncio
# import models
# from initApp import app
from inspect import getmembers, isfunction
from werkzeug.utils import secure_filename
from flask import send_from_directory


CURRENT_PATH = os.getcwd()
UPPER_PATH = os.path.dirname(os.getcwd())


def toweb(function, url_site: str, parameters: dict):
    app = Flask(__name__)
    UPLOAD_FOLDER = f"{UPPER_PATH}/__wrapweb__/{url_site}_tmp_files"
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    @app.route('/download/<path:filename>')
    def downloading(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

    if ('account' not in parameters.keys() or not parameters['account']) and (
            'history' not in parameters.keys() or not parameters['history']):
        @app.route(f'/{url_site}', methods=['GET', 'POST'])
        def myfunc():
            result = None
            if request.method == 'POST':
                annotations = function.__annotations__
                types = list(annotations.values())
                args: list = []
                for i in range(parameters['input']['files']):
                    file = request.files[f'file{i}']
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    args.append(f"{app.config['UPLOAD_FOLDER']}/{filename}")
                for i in range(parameters['input']['text']):
                    form = request.form.get(f'text{i}')
                    args.append(types[i](form))
                result = function(*args)
                if result.__class__ == 'tuple':
                    result = list(result)
                else:
                    result = [result]
            return render_template('index.html', parameters=parameters, url=url_site, result=result, l=len(parameters['output']))

    return app


def wrapweb(url_site: str, name_file: str, parameters: dict):
    module = importlib.import_module(name_file[:-3])
    func = getmembers(module, isfunction)[0][1]
    toweb(func, url_site, parameters).run(host='0.0.0.0', port=5001, debug=True)


def get_parameters(path_file: str) -> list:
    try:
        with open(path_file) as file:
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
    except SyntaxError:
        print('Неверно заданы параметры')


def route_url(now_path: str):
    for root, dirs, files in os.walk(now_path):
        for dir in dirs:
            route_url(dir)
        for file in files:
            if '__init__' in file:
                file_path = f"{root}/{file}"
                for url, name_func_file, parameters in get_parameters(file_path):
                    wrapweb(url, name_func_file, parameters)


route_url(UPPER_PATH)