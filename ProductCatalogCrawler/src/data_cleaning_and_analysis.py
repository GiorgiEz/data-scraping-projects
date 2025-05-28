import pandas as pd


class DataCleaningAndAnalysis:
    def __init__(self):
        self.data_df = pd.read_csv('../datasets/products.csv')
        self.fieldnames = ['asin', 'title', 'link', 'image', 'rating', 'review_count', 'price', 'delivery']

    def clean_whitespace(self):
        # Apply stripping and whitespace normalization to all string fields
        for col in self.data_df.columns:
            if self.data_df[col].dtype == 'object':
                self.data_df[col] = self.data_df[col].astype(str).apply(
                    lambda x: ' '.join(x.split())
                )

    def remove_currency_sign(self):
        self.data_df['price'] = self.data_df['price'].str.replace('$', '')

    def clean_rating(self):
        # Replace 'N/A' or similar non-numeric values with NaN
        self.data_df['rating'] = self.data_df['rating'].replace('N/A', pd.NA)

        # Extract the numeric part and convert to float
        self.data_df['rating'] = self.data_df['rating'].str.extract(r'(\d+(\.\d+)?)')[0].astype(float)

    def analyze_data(self):
        # Convert price to numeric for analysis
        self.data_df['price'] = pd.to_numeric(self.data_df['price'], errors='coerce')

        print("==== Basic Statistics ====")
        print(self.data_df[['price', 'rating']].describe())
        print()

        print("==== Highest Priced Item ====")
        max_price_item = self.data_df.loc[self.data_df['price'].idxmax()]
        print(max_price_item[['title', 'price']])
        print()

        print("==== Lowest Priced Item ====")
        min_price_item = self.data_df.loc[self.data_df['price'].idxmin()]
        print(min_price_item[['title', 'price']])
        print()

        print("==== Average Rating and Price ====")
        print(f"Average Rating: {self.data_df['rating'].mean():.2f}")
        print(f"Average Price: ${self.data_df['price'].mean():.2f}")
        print()

        print("==== Price Distribution (Histogram Buckets) ====")
        print(pd.cut(self.data_df['price'], bins=5).value_counts().sort_index())
        print()

    def main(self):
        self.clean_whitespace()
        self.remove_currency_sign()
        self.clean_rating()
        self.data_df.to_csv('../datasets/cleaned_products.csv', index=False)
        self.analyze_data()
