from search.full_text_search import FullTextSearch
from visualizer.historgram_visualizer import HistorgramVisualizer
from visualizer.visualizer import Visualizer
from visualizer.word_cloud_visualizer import WordCloudVisualizer


class DataExplorer():
    def __init__(self, full_text_search: FullTextSearch):
        self.full_text_search = None
        self.full_text_search = full_text_search
        self.data = None

    def search_keyword(self, keyword: str):
        self.data = self.full_text_search.search_keyword(keyword)

    def visualize(self, type: str):
        if type == 'histogram':
            visualizer = HistorgramVisualizer()
        elif type == 'wordcloud':
            visualizer = WordCloudVisualizer()
        visualizer.visualize(self.data)
