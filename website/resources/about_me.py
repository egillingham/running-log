from flask_restful import Resource, request
from flask import render_template, make_response

from blog_management import image_cards


class Hello(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}

    def get(self):
        cards = image_cards.get_image_cards()
        template = render_template('about_me.html', cards=cards)
        return make_response(template, 200, self.header)
