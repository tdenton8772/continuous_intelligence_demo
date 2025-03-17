from flask import Blueprint, Response, make_response, Request, request, session, stream_with_context
from flask_session import Session
from flask import render_template, flash, redirect, url_for
from flask import send_from_directory
from application import application

mod = Blueprint('main', __name__, url_prefix='/')

@mod.route('/', methods=['GET', 'POST'])
def index():
    if "5000" in request.url:
        css = "./static/css/main.css"
        icon = "./static/images/favicon.ico"
    else:
        css = "./static/css/main.css"
        icon = "./static/images/favicon.ico"

    response = Response("")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0" # Proxies.
    response.headers['Access-Control-Allow-Origin'] = '*'

    response = make_response(render_template('index.html',
                                             title='Default',
                                             description="Default",
                                             css = css,
                                             icon = icon))
    return response