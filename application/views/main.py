from flask import Blueprint, Response, make_response, Request, request, session, stream_with_context
from flask_session import Session
from flask import render_template, flash, redirect, url_for
from flask import send_from_directory
from application import application
import os

mod = Blueprint('v1', __name__, url_prefix='/')

@mod.route('/')
def main():
    return {}