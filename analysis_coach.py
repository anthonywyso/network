import matplotlib.pyplot as plt
import pandas as pd
import sqlite3 as sql
import numpy as np
from scipy.stats import ks_2samp, ttest_ind
from collections import defaultdict


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


class CoachFirstYear(object):

    def __init__(self, dbname='data/network.sqlite'):
        self.default_size = (16, 10)
        self.db = dbname

    def load_data(self):
        query = '''
                SELECT pri.*, pct.coach_id, pct.player_coach_tenure_pct,
                1.0 * rapm_off * pct.player_coach_tenure_pct AS rapm_off_impact,
                1.0 * rapm_def * pct.player_coach_tenure_pct AS rapm_def_impact,
                1.0 * rapm_both * pct.player_coach_tenure_pct AS rapm_both_impact
                FROM players_rapm_id AS pri
                JOIN player_coach_tenures AS pct,
                (SELECT player_id, MIN(season) AS season_rookie
                FROM players_seasonlog_totals AS pst
                GROUP BY player_id
                HAVING season_rookie >= 1991) AS rp
                ON pri.id = pct.player_id AND pri.id = rp.player_id AND pri.season = pct.season AND pri.season = rp.season_rookie
                '''
        with sql.connect(self.db) as con:
            cur = con.cursor()
            cur.execute(query)
        data = pd.DataFrame(cur.fetchall())
        data.columns = ['player_id','name','rapm_off','rapm_def','rapm_both','season','poss','coach_id','player_coach_tenure_pct', 'rapm_off_impact', 'rapm_def_impact', 'rapm_both_impact']
        return data

    def display_hist(self, data, metric="rapm_both"):
        fig = plt.figure(figsize=self.default_size)
        ax = fig.add_subplot(1, 1, 1)
        data[metric].hist(ax=ax, label="population", normed=True)
        plt.legend()
        plt.show()

    def display_hist_all(self, data, data_population, metric="rapm_both"):
        eligibility = data.groupby(['coach_id']).count()['player_id'].median()
        eligible = data.groupby(['coach_id']).count()['player_id'] > eligibility
        eligible = eligible.reset_index()
        coaches_eligible = eligible[eligible['player_id'] == True]

        fig = plt.figure(figsize=self.default_size)
        for i, coach in enumerate(coaches_eligible['coach_id']):
            ax = fig.add_subplot(9, 9, i+1)
            ax.set_title(coach)
            data_population[metric].hist(ax=ax, label="population", alpha=.50, normed=True, grid=False, ylabelsize=0)
            data[data['coach_id'] == coach][metric].hist(ax=ax, label=coach, alpha=.40, normed=True, grid=False, ylabelsize=0)
        # plt.legend()
        plt.tight_layout()
        plt.show()

    def ks(self, data, data_population, metric="rapm_both"):
        coaches_ks = defaultdict(list)
        for coach in data['coach_id']:
            d, p = ks_2samp(data[data['coach_id'] == coach][metric], data_population[metric])
            coaches_ks[coach] = [d, p]

        coaches_score = pd.DataFrame.from_dict(coaches_ks, orient='index').reset_index()
        coaches_score.columns = ['coach_id', 'd', 'p']

        players_coached = data.groupby(['coach_id']).count()['player_id'].reset_index()
        crit_vals = 1.36 * np.sqrt((players_coached['player_id'] + data.shape[0]) / (players_coached['player_id'] * data.shape[0]))
        coaches_crit = pd.concat([players_coached, pd.DataFrame(crit_vals)], axis=1)
        coaches_crit.columns = ['coach_id', 'player_count', 'crit']

        ks_grid = coaches_crit.merge(coaches_score, on=['coach_id'])
        return ks_grid

    def t(self, data, data_population, metric="rapm_both"):
        coaches_t = defaultdict(list)
        for coach in data['coach_id']:
            t, p = ttest_ind(data[data['coach_id'] == coach][metric], data_population[metric])
            coaches_t[coach] = [t, p]

        coaches_score = pd.DataFrame.from_dict(coaches_t, orient='index').reset_index()
        coaches_score.columns = ['coach_id', 't', 'p']

        players_coached = data.groupby(['coach_id']).count()['player_id'].reset_index()
        players_coached.columns = ['coach_id', 'player_count']

        t_grid = players_coached.merge(coaches_score, on=['coach_id'])
        return t_grid

    def display_coach(self, data, coach, metric="rapm_both", cols=[]):
        """
        INPUT: DataFrame, str, str, list
        OUTPUT: DataFrame
        Displays players and their metrics under a particular coach
        """
        return data[data['coach_id'] == coach].sort([metric])[cols]


class CoachMultiYear(CoachFirstYear):

    def load_data(self, dbname2="players_soph_performances", y_delta=1):
        """
        INPUT: str, int
        OUTPUT: DataFrame
        Loads data from specified db and year delta; returns dataframe of player performances
        """
        # TODO protect against db injection attacks
        query = " ".join(["SELECT y1.*, y2.rapm_both AS rapm_both_y2, y2.rapm_both - y1.rapm_both AS rapm_both_delta FROM players_rookie_performances AS y1 JOIN", dbname2, "AS y2 ON y1.id = y2.id AND y1.season = y2.season -", str(y_delta), "AND y1.coach_id = y2.coach_id"])
        query_population = " ".join(["SELECT y1.*, y2.rapm_both AS rapm_both_y2, y2.rapm_both - y1.rapm_both AS rapm_both_delta FROM players_rookie_performances AS y1 JOIN", dbname2, "AS y2 ON y1.id = y2.id AND y1.season = y2.season -", str(y_delta)])
        with sql.connect(self.db) as con:
            cur = con.cursor()
            cur.execute(query)
            data = pd.DataFrame(cur.fetchall())
            cur.execute(query_population)
            data_population = pd.DataFrame(cur.fetchall())
        data.columns = ['player_id','name','rapm_off','rapm_def','rapm_both','season','poss','coach_id','player_coach_tenure_pct', 'rapm_off_impact', 'rapm_def_impact', 'rapm_both_impact', 'rapm_both_y2', 'rapm_both_delta']
        data_population.columns = ['player_id','name','rapm_off','rapm_def','rapm_both','season','poss','coach_id','player_coach_tenure_pct', 'rapm_off_impact', 'rapm_def_impact', 'rapm_both_impact', 'rapm_both_y2', 'rapm_both_delta']
        return data, data_population