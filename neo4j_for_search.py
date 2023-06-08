from text_analyzer import TextAnalyzer
from neo4j import GraphDatabase
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import json
import time
import re
import os


class Neo4jForSearch(TextAnalyzer):
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.data = []

    def close(self):
        self.driver.close()

    def deleteAll(self):
        with self.driver.session() as session:
            session.run('''
                MATCH (n)
                DETACH DELETE n
            ''')

    def loadYelpToNeo4j(self, json_file, limit=10000):
        dataList = []
        with open(json_file, encoding='utf-8-sig') as f:
            for line in f:
                data = json.loads(line)
                dataList.append(data)
                if len(dataList) >= limit:
                    break
        label = os.path.splitext(json_file)[0].split('_')[-1]
        with self.driver.session() as session:
            for data in dataList:
                param = ", ".join([f'n.{k} = "' + v.replace('"', "'") + '"' for k, v in data.items() if type(v) in [
                    str]])
                session.run('''
                    CREATE (n:''' + label.capitalize() + ''')
                    SET ''' + param + '''
                ''')

    def search_keyword(self, keyword):
        start_time = time.time()
        with self.driver.session() as session:
            result1 = session.run('''
                MATCH (n)
                WHERE any(prop in keys(n) WHERE n[prop] CONTAINS $keyword)
                RETURN n, labels(n)
            ''', keyword=keyword)
            result2 = session.run('''
                MATCH ()-[r]-()
                WHERE any(prop in keys(r) WHERE r[prop] CONTAINS $keyword)
                RETURN r
            ''', keyword=keyword)
            print("Query time in Neo4j: %s seconds" %
                  (time.time() - start_time))
            print('Search result:')
            data_list = []
            for record in result1:
                label_name = ", ".join(record['labels(n)'])
                for k, v in record['n'].items():
                    sentences = re.split(r'(?<=[.!?])\s+', v)
                    result = []
                    for sentence in sentences:
                        if re.search(r"\bapple\b", sentence, re.IGNORECASE):
                            cleaned_sentence = re.sub(r'[^\w\s]', '', sentence)
                            result.append(cleaned_sentence)
                            self.data.append(cleaned_sentence)
                            data_list.append(
                                [label_name, k, v, v.lower().count(keyword.lower())])
            df = pd.DataFrame(data_list, columns=[
                              'label', 'property', 'value', 'frequency'])
            return df


if __name__ == "__main__":
    client = Neo4jForSearch("bolt://localhost:7687", "neo4j", "steven6409")
    # client.deleteAll()
    # client.loadYelpToNeo4j("yelp_academic_dataset_user.json")
    client.search_keyword("apple")
    client.visualize("Word Cloud")
    client.close()
