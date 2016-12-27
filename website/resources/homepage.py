from flask import render_template, make_response
from flask_restful import Resource

from website.blog_management import image_cards


class Homepage(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}

    def get(self):
        cards = image_cards.get_image_cards()
        template = render_template('homepage.html', cards=cards)
        return make_response(template, 200, self.header)
