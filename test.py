from data_explorer import DataExplorer
from search.neo4j_for_search import Neo4jForSearch
from search.mongodb_for_search import MongoDBForSearch
from visualizer.historgram_visualizer import HistorgramVisualizer
from visualizer.word_cloud_visualizer import WordCloudVisualizer
import nltk

if __name__ == "__main__":
    nltk.download('stopwords')
    nltk.download('punkt')

    searchEngine = Neo4jForSearch(
        "bolt://localhost:7687", "neo4j", "steven6409","neo4j")
    data_explorer = DataExplorer(searchEngine)
    data_explorer.search_keyword('apple')
    # searchEngine.graph_visualize('apple')
    data_explorer.visualize(HistorgramVisualizer())
    data_explorer.visualize(WordCloudVisualizer())
    searchEngine.close()
