import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scrape_all import scrape_amazon, scrape_flipkart

def search_af(s):
    amazon_df = scrape_amazon(s)
    flipkart_df = scrape_flipkart(s)

    # Price comparison
    amazon_avg_price = amazon_df['Price'].mean()
    flipkart_avg_price = flipkart_df['Price'].mean()

    print(f"Average Price on Amazon: {amazon_avg_price}")
    print(f"Average Price on Flipkart: {flipkart_avg_price}")

    # Rating comparison
    amazon_avg_rating = amazon_df['Rating'].mean()
    flipkart_avg_rating = flipkart_df['Rating'].mean()

    print(f"Average Rating on Amazon: {amazon_avg_rating}")
    print(f"Average Rating on Flipkart: {flipkart_avg_rating}")

    # Visualize data
    plt.figure(figsize=(12, 6))

    # Price distribution comparison
    plt.subplot(1, 2, 1)
    sns.histplot(amazon_df['Price'], bins=20, color='blue', label='Amazon', kde=True)
    sns.histplot(flipkart_df['Price'], bins=20, color='orange', label='Flipkart', kde=True)
    plt.title('Price Distribution Comparison')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)

    # Rating distribution comparison
    plt.subplot(1, 2, 2)
    sns.histplot(amazon_df['Rating'], bins=5, color='blue', label='Amazon', kde=True)
    sns.histplot(flipkart_df['Rating'], bins=5, color='orange', label='Flipkart', kde=True)
    plt.title('Rating Distribution Comparison')
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    t = input("What do you want to compare: ")
    search_af(t)
