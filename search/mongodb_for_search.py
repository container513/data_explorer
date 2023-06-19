from analyzer.nltk_analyzer import NltkAnalyzer
from search.full_text_search import FullTextSearch
from pymongo import MongoClient


class MongoDBForSearch(FullTextSearch):
    def __init__(self, mongodb_url, db_name):
        self.client = MongoClient(mongodb_url)
        self.db = self.client[db_name]
        self.analyzer = NltkAnalyzer()

    def search_keyword(self, keyword, sample_size=10000):
        collections = self.db.list_collection_names()

        for collection_name in collections:
            collection = self.db[collection_name]
            cursor = collection.aggregate([
                {"$sample": {"size": sample_size}}
            ])

            for document in cursor:
                for field_name, field_value in document.items():
                    if isinstance(field_value, str):
                        self.analyzer.analyze(collection_name, field_name, field_value, keyword)
        print(f"Collection: {collection_name}")
        print("Most common bigrams:")
        for (bigram, field_name), count in self.analyzer.bigram_field_name_counts.most_common():
            print((bigram, field_name, count))

        # print("\nBigram info:")
        # for bigram, _ in self.analyzer.bigram_info.items():
        #     print(f"{bigram}:")
        return self.analyzer.bigram_counts
    
    def close(self):
        self.client.close()

if __name__=="__main__":
    mongodb_url = "mongodb://localhost:27017/"
    db_name = "hw6"
    mongodb_for_search = MongoDBForSearch(mongodb_url, db_name)
    mongodb_for_search.search_keyword("r11922")