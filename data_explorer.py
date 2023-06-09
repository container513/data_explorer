from full_text_search import FullTextSearch
from visualizer import Visualizer


class DataExplorer():
    def __init__(self, full_text_search: FullTextSearch):
        self.full_text_search = None
        self.full_text_search = full_text_search
        self.data = None

    def search_keyword(self, keyword: str):
        self.data = self.full_text_search.search_keyword(keyword)

    def visualize(self, visualizer: Visualizer):
        visualizer.visualize(self.data)
