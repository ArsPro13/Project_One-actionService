from flask import Flask, render_template, request
import importlib
import ast
import os
import asyncio
from functools import wraps
from inspect import getmembers, isfunction
from werkzeug.utils import secure_filename
from flask import send_from_directory


CURRENT_PATH = os.getcwd()
UPPER_PATH = os.path.dirname(os.getcwd())
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


def exception_handler(func):
  def wrapper(*args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_code = getattr(e, "code", 500)
  # Renaming the function name:
  wrapper.__name__ = func.__name__
  return wrapper


def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        return f(*args, **kwds)
    return wrapper


def toweb(function, url_site: str, parameters: dict):
    UPLOAD_FOLDER = f"{UPPER_PATH}/__wrapweb__/{url_site}_tmp_files"
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    @app.route('/download/<path:filename>')
    @my_decorator
    def downloading(filename):
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

    print(url_site)

    @app.route(f'/{url_site}', methods=['GET', 'POST'])
    @my_decorator
    def myfunc():
        result = None
        if request.method == 'POST':
            annotations = function.__annotations__
            types = list(annotations.values())
            args: list = []
            for i in range(parameters['input']['files']):
                file = request.files[f'file{i}']
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                args.append(f"{UPLOAD_FOLDER}/{filename}")
            for i in range(parameters['input']['text']):
                form = request.form.get(f'text{i}')
                args.append(types[i](form))
            result = function(*args)
            if result.__class__ == 'tuple':
                result = list(result)
            else:
                result = [result]
        return render_template('index.html', parameters=parameters, url=url_site, result=result, l=len(parameters['output']))


def wrapweb(url_site: str, name_file: str, parameters: dict):
    module = importlib.import_module(name_file[:-3])
    func = getmembers(module, isfunction)[0][1]
    toweb(func, url_site, parameters)


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
            if file == '__init__.py':
                file_path = f"{root}/{file}"
                for url, name_func_file, parameters in get_parameters(file_path):
                    wrapweb(url, name_func_file, parameters)


if __name__ == '__main__':
    route_url(UPPER_PATH)
    app.run(debug=True)
