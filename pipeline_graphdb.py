import pandas as pd
import sqlite3 as sql
from py2neo import Graph, Node, Relationship

import config


class NeoPipeline(object):

    def __init__(self):
        self.graph_path = config.GRAPH_DB['graph_path']
        self.graph = Graph(self.graph_path)
        self.sql_path = "data/network.sqlite"

    def nodes_from_sql(self, query, label, unique="id"):
        """
        INPUT: str, str, str
        OUTPUT: None
        Imports node data from sql query into neo4j
        """
        # Extract data from sql db.
        with sql.connect(self.sql_path) as con:
            nodes = pd.read_sql(sql=query, con=con, index_col=None)
        nodes_dict = nodes.to_dict(outtype="records")

        # Create nodes in graph.
        self.graph.schema.create_uniqueness_constraint(label, unique)
        for node in nodes_dict:
            n = Node.cast(label, node)
            self.graph.create(n)

    def relationships_from_sql(self, query, nodes, label, properties):
        """
        INPUT: str, list(dict), str, dict
        OUTPUT: None
        Imports relationship data from sql query into neo4j
        """
        with sql.connect(self.sql_path) as con:
            rels = pd.read_sql(sql=query, con=con, index_col=None)
        rels_dict = rels.to_dict(outtype="records")

        for rel in rels_dict:
            r = Relationship.cast(self.graph.find_one(nodes[0]["label"], nodes[0]["property"], rel[nodes[0]["sql_col"]]),
                                  label,
                                  self.graph.find_one(nodes[1]["label"], nodes[1]["property"], rel[nodes[1]["sql_col"]]),
                                  properties)
            self.graph.create(r)

    def build_network(self):
        query_players = '''
                        SELECT player_name AS name, player_id AS id, player_pos AS pos
                        FROM individuals_subset
                        GROUP BY player_id
                        '''
        self.nodes_from_sql(query_players, "Players", unique="id")
        query_coaches = '''
                        SELECT coach_name AS name, coach_id AS id
                        FROM individuals_subset
                        GROUP BY coach_id
                        '''
        self.nodes_from_sql(query_coaches, "Coaches", unique="id")

        query_play_coach = '''
                            SELECT *
                            FROM individuals_subset
                            '''
        play_coach = [{'label': "Coach", 'property': "id", 'sql_col': "coach_id"}, {'label': "Player", 'property': "id", 'sql_col': "player_id"}]
        self.relationships_from_sql(query_play_coach, nodes=play_coach, label_rel="COACHED", properties={"league": "NBA"})