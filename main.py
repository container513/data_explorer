from data_explorer import DataExplorer
from full_text_search import FullTextSearch
from visualizer import Visualizer

if __name__ == "__main__":
    data_explorer = DataExplorer(FullTextSearch())
    data_explorer.search_keyword('apple')
    data_explorer.visualize('Word Cloud')