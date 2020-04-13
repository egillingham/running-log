import logging
from datetime import datetime
from flask import render_template, make_response, url_for, request, redirect
from flask_restful import Resource

from blog_management import hearts

LOGGER = logging.getLogger("running-log")


class HeartsGame(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}

    def get(self, group_name):
        try:
            group = hearts.Group(group_name)
        except Exception as e:
            LOGGER.error(e)
            template = render_template('404.html', error="Group {} not found".format(group_name))
            return make_response(template, 404, self.header)
        template = render_template("add_hearts_game.html", group_name=group_name, players=group.get_players(),
                                   group_url=url_for('heartsgame', group_name=group_name))
        return make_response(template, 200, self.header)

    def post(self, group_name):
        try:
            group = hearts.Group(group_name)
        except Exception as e:
            LOGGER.error(e)
            template = render_template('404.html', error="Group {} not found".format(group_name))
            return make_response(template, 404, self.header)
        try:
            if not group.is_valid_code(request.form.get("code")):
                raise Exception("Invalid group code")
            date = request.form.get("date")
            if not date:
                raise Exception("Please select a valid date")
            if request.form.get("player_1_score") is None or request.form.get("player_2_score") is None or \
                    request.form.get("player_3_score") is None or request.form.get("player_4_score") is None:
                raise Exception("Please include a score for every player")
            results = {request.form.get("player_1"): int(request.form.get("player_1_score")),
                       request.form.get("player_2"): int(request.form.get("player_2_score")),
                       request.form.get("player_3"): int(request.form.get("player_3_score")),
                       request.form.get("player_4"): int(request.form.get("player_4_score"))
                       }
            date = datetime.strptime(date, "%Y-%m-%d")
            notes = request.form.get("notes")
            group.add_game(date, results, notes)
            return redirect(url_for('heartsgroup', group_name=group_name))

        except Exception as e:
            msg = "Error adding game results: {}".format(e)
            LOGGER.error(msg)
            LOGGER.exception(e)
            template = render_template("add_hearts_game.html", group_name=group_name, players=group.get_players(),
                                       group_url=url_for('heartsgame', group_name=group_name), error=msg)
            return make_response(template, 400, self.header)


