import matplotlib.pyplot as plt
import pandas as pd
import sqlite3 as sql


class CoachValue(object):

    def __init__(self, name, dbname='data/network.sqlite'):
        self.coach = name
        self.size = (16, 10)
        self.db = dbname

    def load_data(self):
        query = '''
                SELECT pd.*
                FROM
                (SELECT p1.id, p1.season AS season_prior, p2.season AS season_current, p1.rapm_both AS rapm_prior, p2.rapm_both AS rapm_current, p2.rapm_both - p1.rapm_both AS rapm_delta
                FROM players_rapm_id AS p1
                JOIN players_rapm_id AS p2
                ON p1.id = p2.id AND p1.season = p2.season - 1) AS pd
                JOIN player_coach_tenures AS pct
                ON pd.id = pct.player_id AND pd.season_current = pct.season AND pct.coach_id = (SELECT id FROM coaches WHERE name = ?)
                ORDER BY id, season_prior
                '''
        with sql.connect(self.db) as con:
            cur = con.cursor()
            cur.execute(query, (self.coach, ))
            data = pd.DataFrame(cur.fetchall())
        data.columns = ['player', 'season_prior', "season_current", 'rapm_prior', 'rapm_current', 'rapm_delta']
        data['season_num'] = data.groupby(['player'])['season_current'].rank()
        return data

    def viz_agg_performance(self, data):
        fig = plt.figure(figsize=self.size)
        ax = fig.add_subplot(1, 1, 1)
        data[['season_num', 'rapm_delta']].groupby(['season_num']).mean().plot(y='rapm_delta', ax=ax, label="mean")
        data[['season_num', 'rapm_delta']].groupby(['season_num']).median().plot(y='rapm_delta', ax=ax, label="median")
        plt.suptitle(self.coach)
        plt.legend()
        plt.show()

    def viz_performance(self, data):
        fig = plt.figure(figsize=self.size)
        ax = fig.add_subplot(1, 1, 1)
        data.groupby('player').plot(x='season_num', y='rapm_prior', ax=ax)
        plt.show()

