from text_analyzer import TextAnalyzer
from neo4j import GraphDatabase
from nltk_analyzer import NltkAnalyzer
import json
import time
import os


class Neo4jForSearch(TextAnalyzer):
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.data = []
        self.analyzer = NltkAnalyzer()

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
            data_list = []
            result2
            for record in result1:
                label_name = ", ".join(record['labels(n)'])
                for k, v in record['n'].items():
                    self.analyzer.analyze(label_name, k, v, keyword)
        print(f"label: {label_name}")
        print("Most common bigrams:")
        for (bigram, field_name), count in self.analyzer.bigram_field_name_counts.most_common():
            print((bigram, field_name, count))

        print("\nBigram info:")
        for bigram, _ in self.analyzer.bigram_info.items():
            print(f"{bigram}:")

        return self.analyzer.bigram_counts


if __name__ == "__main__":
    client = Neo4jForSearch("bolt://localhost:7687", "neo4j", "steven6409")
    # client.deleteAll()
    # client.loadYelpToNeo4j("yelp_academic_dataset_user.json")
    client.search_keyword("apple")
    client.visualize("Word Cloud")
    client.close()
