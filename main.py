from data_explorer import DataExplorer
from neo4j_for_search import Neo4jForSearch
from historgram_visualizer import HistorgramVisualizer
from word_cloud_visualizer import WordCloudVisualizer
import nltk

if __name__ == "__main__":
    nltk.download('stopwords')
    nltk.download('punkt')

    data_explorer = DataExplorer(Neo4jForSearch(
        "bolt://localhost:7687", "neo4j", "steven6409"))
    data_explorer.search_keyword('apple')
    data_explorer.visualize(HistorgramVisualizer())
    data_explorer.visualize(WordCloudVisualizer())
