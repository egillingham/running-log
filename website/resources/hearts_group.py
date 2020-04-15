import logging
from flask import render_template, make_response, url_for
from flask_restful import Resource

from blog_management import hearts

LOGGER = logging.getLogger("running-log")


class HeartsGroup(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}

    def get(self, group_name):
        try:
            group = hearts.Group(group_name)
        except Exception as e:
            LOGGER.error(e)
            template = render_template('404.html', error="Group {} not found".format(group_name))
            return make_response(template, 404, self.header)
        group.calculate_scoreboard()
        group.calculate_point_breakdown_day()

        template = render_template('hearts_group.html', group_name=group.name,
                                   scoreboard=group.get_scoreboard(),
                                   player_1=group.get_players()[0],
                                   player_2=group.get_players()[1],
                                   player_3=group.get_players()[2],
                                   player_4=group.get_players()[3],
                                   results=group.point_breakdown_day,
                                   addurl=url_for('heartsgame', group_name=group_name)
                                   )
        return make_response(template, 200, self.header)
