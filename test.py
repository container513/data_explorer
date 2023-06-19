from data_explorer import DataExplorer
from search.neo4j_for_search import Neo4jForSearch
from search.mongodb_for_search import MongoDBForSearch
from search.mysql_for_search import MysqlForSearch
import nltk

if __name__ == "__main__":
    nltk.download('stopwords')
    nltk.download('punkt')

    searchEngine = Neo4jForSearch(
        "bolt://localhost:7687", "user", "password","db_name")
    # searchEngine = MongoDBForSearch("mongodb://localhost:27017/", "db_name")
    # searchEngine = MysqlForSearch('localhost', 'user', 'password', 'db_name')
    data_explorer = DataExplorer(searchEngine)
    data_explorer.search_keyword('apple')
    data_explorer.visualize('histogram')
    data_explorer.visualize('wordcloud')
    searchEngine.close()
