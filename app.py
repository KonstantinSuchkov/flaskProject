# from time import time
#
# from flask import Flask, request, g, session
#
# count = 0
# app = Flask(__name__)
# app.secret_key = b'amelia'
#
# """
# Домашнее задание.
# 3. Создайте базовый index view для обработки посещений на корень сайта.
# """
#
#
# # Вариант 1
# @app.route('/')
# def index():
#     global count
#     count += 1
#     return f'Посещений на данный момент - {count}'
#
#
# @app.route('/delete')
# def delete_index():
#     global count
#     count = 0
#     return f'Счетчик обнулен'
#
#
# # Вариант 2 - с помощью session
# @app.route('/root/')
# def index_2():
#     if 'count' in session:
#         session['count'] = session.get('count') + 1
#     else:
#         session['count'] = 1
#     return "Посещений на данный момент: {}".format(session.get('count'))
#
#
# @app.route('/root-delete/')
# def delete_index_2():
#     session.pop('root', None)
#     return 'Счетчик обнулен'
#
#
# @app.route('/<name>/')
# def hello_name(name: str):
#     return f'Hello, {name}'
#
#
# @app.route('/root/user/')
# def read_user():
#     name = request.args.get('name')
#     surname = request.args.get("surname")
#     return f"User {name or '[no name]'} {surname or '[no surname]'}"
#
#
# @app.route("/status/", methods=["GET", "POST"])
# def custom_status_code():
#     if request.method == "GET":
#         return """\
#         To get response with custom status code
#         send request using POST method
#         and pass `code` in JSON body / FormData
#         """
#     print("raw bytes data:", request.data)
#     if request.form and "code" in request.form:
#         return "code from form", request.form["code"]
#     if request.json and "code" in request.json:
#         return "code from json", request.json["code"]
#
#     return "", 204
#
#
# @app.before_request
# def process_before_request():
#     """
#     Sets start_time to `g` object
#     """
#     g.start_time = time()
#
#
# @app.after_request
# def process_after_request(response):
#     """
#     adds process time in headers
#     """
#     if hasattr(g, "start_time"):
#         response.headers["process-time"] = time() - g.start_time
#     return response
