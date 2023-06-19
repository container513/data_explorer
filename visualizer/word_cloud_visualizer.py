from visualizer.visualizer import Visualizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class WordCloudVisualizer(Visualizer):
    def visualize(self, bigram_counts):
        wordcloud = WordCloud(
            width=800, height=400, background_color='white').generate_from_frequencies(bigram_counts)
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
