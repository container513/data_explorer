from nltk.corpus import stopwords
from analyzer.text_analyzer import TextAnalyzer
from collections import defaultdict
from nltk.tokenize import word_tokenize
import string
from collections import Counter
import pandas as pd

class NltkAnalyzer(TextAnalyzer):
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.bigram_counts = Counter()
        self.bigram_field_name_counts = Counter()
        self.bigram_info = defaultdict(list)
        self.collection_keyword_counts = Counter()

    def analyze(self, collection_name, field_name, field_value, keyword):

        text = field_value
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text)
        tokens = [token for token in tokens if token.lower()
                  not in self.stop_words]
        for i in range(len(tokens) - 1):
            if tokens[i].lower() == keyword:
                # Include the word before the keyword
                if i > 0:
                    bigram_before = tokens[i - 1] + ' ' + tokens[i]
                    self.bigram_counts[bigram_before] += 1
                    self.bigram_field_name_counts[(
                        bigram_before, field_name)] += 1
                    self.collection_keyword_counts[collection_name] += 1
                # Include the word after the keyword
                bigram_after = tokens[i] + ' ' + tokens[i + 1]
                self.bigram_counts[bigram_after] += 1
                self.bigram_field_name_counts[(bigram_after, field_name)] += 1
                self.collection_keyword_counts[collection_name] += 1
        
    def analyze_for_graph(self, data, keyword):
        df = pd.DataFrame([], columns=["n1_label", "n1_properties","trigram", "r", "n2_labels", "n2_properties"])
        for i in range(0, len(data)):
            if keyword in str(data[i]["n1"]._properties):
                text = str(data[i]["n1"]._properties)
                text = text.translate(str.maketrans('', '', string.punctuation))
                tokens = word_tokenize(text)
                tokens = [token for token in tokens if token.lower()
                    not in self.stop_words]
                for j in range(len(tokens) - 1):
                    if tokens[j].lower() == keyword:
                        trigram = tokens[j - 1] + ' ' + tokens[j] + ' ' + tokens[j + 1]
                        print(trigram)
                        df = df.append({"n1_label": data[i]["n1"]._labels,"n1_properties": data[i]["n1"]._properties,"trigram": trigram, "r": data[i]["r"].type, "n2_label": data[i]["n2"]._labels, "n2_properties": data[i]["n2"]._properties}, ignore_index=True)
            else:
                pass
        return df