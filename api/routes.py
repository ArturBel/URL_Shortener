from flask import Blueprint, request, render_template, redirect, flash
from api.models import Urls
from api.extensions import db, limiter
from api.config import HOST, PORT
import random
import string
import validators
from datetime import datetime


shorten_bp = Blueprint('shortener', __name__, template_folder='templates', static_folder='static')
redirecter = Blueprint('redirecter', __name__, template_folder='templates', static_folder='static')


# index page
@shorten_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', original_url='', short_url=None)
    elif request.method == 'POST':
        # getting original url from user and checking if it is valid
        original_url = request.form.get('long_url')
        if not validators.url(original_url):
            flash('Error: Invalid URL')
            return render_template('index.html', original_url='', short_url=None)

        # shortening original url via random chars and making sure each short url is unique
        while True:
            short_url = ''.join(random.choice(string.ascii_letters) for i in range(6))
            if not Urls.query.filter_by(short_url=short_url).first():
                break
        
        # saving them to database
        new_url = Urls(
            original_url=original_url,
            short_url = short_url
        )
        db.session.add(new_url)
        db.session.commit()

        # rendering template with all required arguments
        context = {
            'original_url': original_url,
            'short_url': short_url,
            'host': HOST,
            'port': PORT
        }

        return render_template('index.html', **context)


# redirect page
@redirecter.route('/<short_url>', methods=['GET'])
def short_redirect(short_url: str):
    # finding url in the database, and raising 404 status error if it does not exist
    url = Urls.query.filter_by(short_url=short_url).first_or_404()

    # updating count and time of last access
    url.count += 1
    url.last_access = datetime.now()
    db.session.commit()

    # redirecting user to original url
    return redirect(f'{url.original_url}')