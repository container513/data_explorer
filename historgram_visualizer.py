from visualizer import Visualizer
import matplotlib.pyplot as plt


class HistorgramVisualizer(Visualizer):
    def visualize(self, bigram_counts):
        # Select top N bigrams
        top_bigrams = bigram_counts.most_common(10)

        # Prepare data for visualization
        bigrams = [bigram for bigram, _ in top_bigrams]
        counts = [count for _, count in top_bigrams]

        # bar chart
        plt.figure(figsize=(10, 6))
        plt.barh(bigrams, counts, color='skyblue')
        plt.gca().invert_yaxis()  # invert the y-axis to show the highest count on top
        plt.xlabel('Count')
        plt.ylabel('Bigram')
        plt.title('Top Bigrams')
        plt.show()
