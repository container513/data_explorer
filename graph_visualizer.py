import os
import pandas as pd
import webbrowser
from pyvis.network import Network
class GraphVisualizer():
    def graph_visualize(self, keyword):
        # Create a session to run Cypher statements in
        session = self.driver.session()
        # Write a Cypher statement
        query = "MATCH (n1)-[r]->(n2) RETURN (n1), (r), (n2)"
        # Run a Cypher statement
        result = session.run(query)
        data = []
        # Extract the data from the result
        for record in result:
            data.append(record)
        # Create a DataFrame from the data
        df = pd.DataFrame([], columns=["n1_label", "n1_properties", "r", "n2_labels", "n2_properties"])

        for i in range(0, len(data)):
            if keyword in str(data[i]["r"].type) or keyword in str(data[i]["n1"]._properties):
                df = df.append({"n1_label": data[i]["n1"]._labels,"n1_properties": data[i]["n1"]._properties, "r": data[i]["r"].type, "n2_label": data[i]["n2"]._labels, "n2_properties": data[i]["n2"]._properties}, ignore_index=True)
            else:
                pass
        # Initialize a pyvis network object
        net = Network()

        # Add nodes and edges
        for _, row in df.iterrows():
            net.add_node(f"{(row['n1_label'], row['n1_properties'])}", label=f"{row['n1_label']}", title=f"{row['n1_properties']}")
            net.add_node(f"{(row['n2_label'], row['n2_properties'])}", label=f"{row['n2_label']}", title=f"{row['n2_properties']}")
            net.add_edge(f"{(row['n1_label'], row['n1_properties'])}", f"{(row['n2_label'], row['n2_properties'])}", label=f"{row['r']}")

        # Set layout and save the graph
        net.show('graph.html')
        webbrowser.open('file://' + os.path.realpath('graph.html'))