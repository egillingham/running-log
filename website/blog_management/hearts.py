from datetime import datetime
from pymysql import connect, cursors
from flask import url_for

from utilities.creds import mysql_creds
from utilities.mysql_query import Query


class Groups(object):

    def __init__(self):
        self.conn = connect(host=mysql_creds['host'], port=mysql_creds['port'], user=mysql_creds['user'],
                            passwd=mysql_creds['password'], db='hearts', cursorclass=cursors.DictCursor)

        self.groups = self._get_groups()

    def _get_groups(self):
        groups_q = Query(self.conn, table='groups')
        groups = groups_q.select(["name", "id"])
        return groups

    def get_group_info(self):
        group_info = []
        for group in self.groups:
            url = url_for('heartsgroup', group_name=group.get("name"))
            games_q = Query(self.conn, table='games')
            games = games_q.select_count_star("games_played", where="group_id = {}".format(group.get("id")))
            group_info.append({"name": group.get("name"), "url": url, "games_played": games.get("games_played")})
        return group_info

    def get_weekly_games_played(self):
        query = Query(self.conn, 'games')
        select_query = '''SELECT WEEK(date, 1) as year_week, YEAR(min(date)) as year, count(*) as games_played
        FROM games GROUP BY WEEK(date, 1);
        '''
        data = query.select_query(select_query)
        num_games_played = []
        # convert week and year to week date
        for week in data:
            date = datetime.strptime('{}-W{}-1'.format(week['year'], week['year_week']), "%Y-W%W-%w")
            num_games_played.append({'games_played': week['games_played'], 'date': date.strftime("%Y-%m-%d")})
        return num_games_played

    def losses_by_player(self, username):
        query = Query(self.conn, 'games')
        return query.select(['date', "1 as count"], where='loser = "{}"'.format(username))


class Group(object):

    def __init__(self, name: str):
        self.conn = connect(host=mysql_creds['host'], port=mysql_creds['port'], user=mysql_creds['user'],
                            passwd=mysql_creds['password'], db='hearts', cursorclass=cursors.DictCursor)
        self.name = name
        self._id = None
        self._code = None
        self.set_group_info()
        self.group_where = "group_id = {}".format(self._id)
        self._players = None

        self.leader = None
        self.leader_count = 0
        self.loser = None
        self.loser_count = 0
        self.point_breakdown_day = {}

    def set_group_info(self):
        groups_q = Query(self.conn, table='groups')
        groups = groups_q.select(["id", "code"], where="name = '{}'".format(self.name))
        if not groups or len(groups) != 1:
            raise Exception("Group {} does not exist".format(groups))
        self._id = int(groups[0].get("id"))
        self._code = groups[0].get("code")

    def is_valid_code(self, code: str) -> bool:
        return code == self._code

    def get_scoreboard(self) -> dict:
        return {"leader_name": self.leader, "leader_count": self.leader_count,
                "loser_name": self.loser, "loser_count": self.loser_count}

    def get_players(self) -> list:
        if not self._players:
            players_q = Query(self.conn, table='players')
            players = players_q.select(["username"], where=self.group_where)
            self._players = [player.get("username") for player in players]
        if len(self._players) != 4:
            raise Exception("Group does not have enough players")
        return self._players

    def calculate_scoreboard(self):
        games_q = Query(self.conn, table='games')
        games = games_q.select(["date", "winner", "loser"], where=self.group_where)
        if not games:
            return
        leaderboard = {}
        loserboard = {}
        for game in games:
            leaderboard[game.get("winner")] = leaderboard.get(game.get("winner"), 0) + 1
            loserboard[game.get("loser")] = loserboard.get(game.get("loser"), 0) + 1
        self.leader = max(leaderboard, key=lambda key: leaderboard[key])
        self.loser = max(loserboard, key=lambda key: loserboard[key])
        self.leader_count = leaderboard.get(self.leader)
        self.loser_count = loserboard.get(self.loser)

    def calculate_point_breakdown_day(self):
        games_players_q = Query(self.conn, table='games_players')
        games_players = games_players_q.select(["date", "username", "points"], where=self.group_where)

        for games_player in games_players:
            date_str = games_player.get("date").strftime("%B %d, %Y")
            date_details = self.point_breakdown_day.get(date_str, {})
            date_details[games_player.get("username")] = games_player.get("points")
            self.point_breakdown_day[date_str] = date_details

    def add_game(self, date: datetime, player_results: dict, notes: str = None):
        game_winner = min(player_results, key=lambda key: player_results[key])
        game_loser = max(player_results, key=lambda key: player_results[key])
        self._add_game_result(date, game_winner, game_loser, notes)
        self._add_player_result(date, player_results)

    def _add_player_result(self, date: datetime, player_results: dict):
        data = []
        for player, points in player_results.items():
            data.append({"date": date, "group_id": self._id, "username": player, "points": points})
        games_players_q = Query(self.conn, table='games_players')
        games_players_q.insert_update(data)

    def _add_game_result(self, date: datetime, winner: str, loser: str, notes: str = None):
        games_q = Query(self.conn, table='games')
        game = {"date": date, "group_id": self._id, "winner": winner, "loser": loser}
        if notes:
            game["notes"] = notes
        games_q.insert_update([game])
