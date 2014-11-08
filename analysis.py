import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import re


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
        self.G = nx.Graph(season=self.season)
        for (player, coach, weight) in data.values:
            self.G.add_edge(player, coach, weight=weight)
        # self.G = nx.read_edgelist(fname, delimiter=",", nodetype=str, edgetype=float, data=(('weight', float),))

    def load_nodes(self, fname="data/players_rapm_id.csv"):
        data = pd.read_csv(fname)
        data = data[data['season'] == self.season]
        for node in self.G.nodes():
            try:
                self.G.node[node]['rapm_both'] = data[data['id'] == node]['rapm_both'].values[0]
            except:
                self.G.node[node]['rapm_both'] = data.median()

    def label_nodes(self):
        self.coach_nodes = [node for node in self.G.nodes() if re.search('c\Z' , node)]
        self.player_nodes = [node for node in self.G.nodes() if not re.search('c\Z' , node)]

    def viz_network(self):
        edge_width = [d['weight']*2 for (u, v, d) in self.G.edges(data=True)]
        node_pos = nx.spring_layout(self.G)

        f = plt.figure(figsize=(32, 20))
        ax = f.add_subplot(1, 1, 1)
        ax.set_title('NBA Player-Coach Relationships %s' % self.season)
        # nx.draw_spring(graph, ax=ax)
        # nx.draw_networkx_nodes(self.G, node_pos)
        # nx.draw_networkx_edges(self.G, node_pos, width=edge_width)
        nx.draw_networkx_nodes(self.G, pos=node_pos, nodelist=self.coach_nodes, node_color='black', alpha=1.0, label="coaches")
        nx.draw_networkx_nodes(self.G, pos=node_pos, nodelist=self.player_nodes, alpha=0.1, label="players")
        nx.draw_networkx_edges(self.G, pos=node_pos, width=edge_width, edge_color=edge_width)
        ax.legend()
        plt.show()

    def build_network(self):
        self.load_edges()
        self.load_nodes()
        self.label_nodes()


def main():
    nw = NBANetwork(season=2013)
    nw.build_network()
    nw.viz_network()
    return nw

if __name__ == "__main__":
    main()