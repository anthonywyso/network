import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import re
import sqlite3 as sql


class NBANetwork(object):

    def __init__(self, season=2014):
        self.season = season
        self.G = None
        self.coach_nodes = None
        self.player_nodes = None

    def load_edges(self, fname='data/player_coach_edges.csv'):
        data = pd.read_csv(fname)
        data = data[data['season'] == self.season]
        data.pop('season')
        self.G = nx.DiGraph(season=self.season)
        for (player, coach, weight) in data.values:
            self.G.add_edge(player, coach, weight=weight)

    def load_nodes(self, fname="data/players_rapm_id.csv"):
        data = pd.read_csv(fname)
        data = data[data['season'] == self.season]
        for node in self.G.nodes():
            try:
                self.G.node[node]['rapm_both'] = data[data['id'] == node]['rapm_both'].values[0]
            except:
                self.G.node[node]['rapm_both'] = data.median()['rapm_both']

    def label_nodes(self):
        self.coach_nodes = [node for node in self.G.nodes() if re.search('c\Z', node)]
        self.player_nodes = [node for node in self.G.nodes() if not re.search('c\Z', node)]

    def weigh_edges(self):
        for player, coach, val in self.G.edges(data=True):
            self.G[player][coach]['weight_rapm'] = self.G.node[player]['rapm_both'] * val['weight']

    def viz_network(self):
        edge_width = [d['weight']*2 for (u, v, d) in self.G.edges(data=True)]
        node_pos = nx.spring_layout(self.G, k=.001, scale=5)

        f = plt.figure(figsize=(32, 20))
        ax = f.add_subplot(1, 1, 1)
        ax.set_title('NBA Player-Coach Relationships %s' % self.season)
        nx.draw_networkx_nodes(self.G, pos=node_pos, nodelist=self.coach_nodes, node_color='black', alpha=1.0, label="coaches")
        nx.draw_networkx_nodes(self.G, pos=node_pos, nodelist=self.player_nodes, alpha=0.1, label="players")
        nx.draw_networkx_edges(self.G, pos=node_pos, width=edge_width, edge_color=edge_width)
        ax.legend()
        plt.show()

    def build_network(self):
        self.load_edges()
        self.load_nodes()
        self.label_nodes()
        self.weigh_edges()


class NBAPlayerNetwork(object):

    def __init__(self, season=2014):
        self.season = season
        self.G = None
        self.coach_nodes = None
        self.player_nodes = None

    def load_edges(self, dbname='data/network.sqlite'):
        query = '''
                SELECT *
                FROM player_player_tenures
                WHERE season >= 2000
                '''
        with sql.connect(dbname) as con:
            data = pd.read_sql(query, con)
        data.pop('season')
        data.pop('team_id')
        self.G = nx.DiGraph(season=self.season)
        for (player, coach, weight) in data.values:
            self.G.add_edge(player, coach, weight=weight)

    def viz_network(self):
        edge_width = [d['weight']*2 for (u, v, d) in self.G.edges(data=True)]
        node_pos = nx.spring_layout(self.G, k=.001, scale=5)

        f = plt.figure(figsize=(32, 20))
        ax = f.add_subplot(1, 1, 1)
        ax.set_title('NBA Player-Player Relationships (as of %s)' % self.season)
        nx.draw_networkx_nodes(self.G, pos=node_pos, node_color='black', alpha=1.0)
        # nx.draw_networkx_nodes(self.G, pos=node_pos, nodelist=self.coach_nodes, node_color='black', alpha=1.0, label="coaches")
        # nx.draw_networkx_nodes(self.G, pos=node_pos, nodelist=self.player_nodes, alpha=0.1, label="players")
        nx.draw_networkx_edges(self.G, pos=node_pos, width=edge_width, edge_color=edge_width)
        plt.show()


def main():
    nw = NBANetwork(season=2013)
    nw.build_network()
    nw.viz_network()
    return nw

if __name__ == "__main__":
    main()