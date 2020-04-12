from pymysql import connect, cursors

from utilities.creds import mysql_creds
from utilities.mysql_query import Query


class Group(object):

    def __init__(self, name: str):
        self.conn = connect(host=mysql_creds['host'], port=mysql_creds['port'], user=mysql_creds['user'],
                            passwd=mysql_creds['password'], db='hearts', cursorclass=cursors.DictCursor)
        self.name = name
        self._id = self.get_group_id()
        self.group_where = "group_id = {}".format(self._id)
        self._players = None

        self.leader = None
        self.leader_count = 0
        self.loser = None
        self.loser_count = 0
        self.point_breakdown_day = {}

    def get_group_id(self) -> int:
        groups_q = Query(self.conn, table='groups')
        groups = groups_q.select(["id", "name"], where="name = '{}'".format(self.name))
        if not groups or len(groups) != 1:
            raise Exception("Group {} does not exist".format(groups))
        return int(groups[0].get("id"))

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
