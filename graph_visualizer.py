import os
import pandas as pd
import webbrowser
from pyvis.network import Network
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from neo4j import GraphDatabase

class GraphVisualizer():
    def __init__(self, uri, user, password, database):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), database=database)
        self.data = []
        self.stop_words = set(stopwords.words('english'))
    def graph_visualize(self, df):
        
        # Initialize a pyvis network object
        net = Network()

        for _, row in df.iterrows():
            net.add_node(f"{row['trigram']}", label=f"{row['n1_label']}", title=f"{row['trigram']}", color='red')
            net.add_node(f"{(row['n2_label'], row['n2_properties'])}", label=f"{row['n2_label']}", title=f"{row['n2_properties']}")
            net.add_edge(f"{row['trigram']}", f"{(row['n2_label'], row['n2_properties'])}", label=f"{row['r']}")
        # Set layout and save the graph
        net.show('graph.html')
        webbrowser.open('file://' + os.path.realpath('graph.html'))

if __name__ == '__main__':
    client = GraphVisualizer("bolt://localhost:7687", "neo4j", "Ian173859", "yelp")
    client.graph_visualize("apple")
    client.close()
