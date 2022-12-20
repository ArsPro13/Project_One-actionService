from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import importlib
import ast
import os
# import models
# from initApp import app
from inspect import getmembers, isfunction
from werkzeug.utils import secure_filename
from flask import send_file
import jinja2


class MyForm(FlaskForm):
    def __init__(self, input_dict: dict, submit_label: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_forms: list = [FileField(validators=[FileRequired()]) for _ in range(input_dict['files'])]
        self.text_forms: list = [StringField('name', validators=[DataRequired()]) for _ in range(input_dict['text'])]
        self.submit = SubmitField(submit_label)


def toweb(function, url_site: str, parameters: dict):
    app = Flask(__name__, template_folder='__wrapweb__')
    app.config['UPLOAD_FOLDER'] = os.getcwd() + '/__wrapweb__/'
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    @app.route('/download')
    def download_file(path):
        return send_file(path)

    if ('account' not in parameters.keys() or not parameters['account']) and (
            'history' not in parameters.keys() or not parameters['history']):
        @app.route('/' + url_site + '/', methods=['GET', 'POST'])
        def myfunc():
            result = None
            try:
                button = 'Получить результат'
                if 'button' in parameters.keys():
                    button = parameters['button']
                form = MyForm(parameters['input'], button)
            except NameError:
                print('Не хватает параметров входных данных')
            if form.validate_on_submit():
                annotations = function.__annotations__
                types = list(annotations.values())
                args: list = []
                for i in range(parameters['input']['forms']):
                    args.append(types[i](form.text_forms[i].data))
                for i in range(parameters['input']['text']):
                    file = form.file_forms[i].data
                    filename = secure_filename(file.filename)
                    args.append(app.config['UPLOAD_FOLDER'] + filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                result = function(*args)

            return render_template('index.html', parameters=parameters, url=url_site, form=form, result=result)

    return app


def wrapweb(url_site: str, name_file: str, parameters: dict):
    module = importlib.import_module(name_file[:-3])
    func = getmembers(module, isfunction)[0][1]
    toweb(func, url_site, parameters).run(host='0.0.0.0', port=5001, debug=True)


def get_parameters(name_file: str) -> list:
    try:
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
    except SyntaxError:
        print('Неверно заданы параметры')


def route_url(now_path: str):
    for root, dirs, files in os.walk(now_path):
        for dir in dirs:
            route_url(dir)
        for file in files:
            if file == '__init__.py':
                for url, name_func_file, parameters in get_parameters(file):
                    wrapweb(url, name_func_file, parameters)


route_url(os.getcwd())