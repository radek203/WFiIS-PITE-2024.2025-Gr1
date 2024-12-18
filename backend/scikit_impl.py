import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from surprise import Dataset, Reader
from surprise import SVD
from surprise import accuracy
import streamlit as st

from backend.utils import get_top_n_categories

class ScikitImpl:

    def __init__(self, debug=False):
        self.debug = debug
        # Read the ratings data
        ratings_df = pd.read_csv("data/ratings.csv")
        self.adjectives_df = pd.read_csv("data/adjectives.csv", header=None)
        if self.debug:
            # Display all columns in the output
            pd.set_option('display.max_columns', None)
            print(ratings_df)

        # Encode the userIds
        self.user_encoder = LabelEncoder()
        ratings_df['userId'] = self.user_encoder.fit_transform(ratings_df['userId'])

        # Process only ratings with multiple categories
        data_expanded = pd.DataFrame([
            {"userId": row.userId, "tag": self.remove_tag(row.tags), "rating": row.rating, "tags": self.remove_tag(row.tags)}
            for _, row in ratings_df.iterrows()
            if '|' in row.categoryId
        ])

        # Split the tags column into multiple columns based on the delimiter '|' - It is how the model can understand the tags
        mlb = MultiLabelBinarizer()
        data_expanded = data_expanded.join(pd.DataFrame(mlb.fit_transform(data_expanded.pop('tags').str.split('|')), columns=mlb.classes_, index=data_expanded.index))

        # Encode the tags
        self.tag_encoder = LabelEncoder()
        data_expanded['tag'] = self.tag_encoder.fit_transform(data_expanded['tag'])
        self.ratings_df = data_expanded

        # Model based on the SVD Singular Value Decomposition algorithm
        self.model_svd = SVD()

        # another model - worse RMSE
        # model_knn = KNNBasic()
        # model_knn.fit(trainset)

    def remove_tag(self, tags):
        filtered_list = [tag for tag in tags.split('|') if tag not in self.adjectives_df[0].tolist()]
        return '|'.join(filtered_list)

    def train(self):
        # 80% training, 20% testing - To learn the model and test it
        train_df, test_df = train_test_split(self.ratings_df, test_size=0.2)
        # Model must know the range of ratings in the dataset
        reader = Reader(rating_scale=(1, 10))

        # Load only the necessary columns from the training data
        data = Dataset.load_from_df(train_df[['userId', 'tag', 'rating']], reader)

        # Build the training set
        trainset = data.build_full_trainset()

        # Train the model
        self.model_svd.fit(trainset)

        if self.debug:
            # testset to test the model
            testset = [(row['userId'], row['tag'], row['rating']) for _, row in test_df.iterrows()]

            # Predict ratings for the testset
            predictions_test = self.model_svd.test(testset)

            # Calculate RMSE on the test set, the lower the value the better, for 1-10 rating scale, we want RMSE to be less than 1 (1 point of rating)
            accuracy.rmse(predictions_test)

    def get_top_n_ratings(self, user_id, n=3):
        top_categories = sorted(get_top_n_categories(3, user_id)['categoryId'].tolist())
        user_id = self.user_encoder.transform([user_id])[0]
        user_tags = self.ratings_df[(self.ratings_df['userId'] == user_id)]['tag'].unique()
        tags_count = 10 if self.debug else 100
        cat1 = st.session_state['image_generator'].get_random_tags(tags_count, int(top_categories[0])).iloc[0:tags_count, 0].tolist()
        cat2 = st.session_state['image_generator'].get_random_tags(tags_count, int(top_categories[1])).iloc[0:tags_count, 0].tolist()
        cat3 = st.session_state['image_generator'].get_random_tags(tags_count, int(top_categories[2])).iloc[0:tags_count, 0].tolist()

        # Generate all possible tags combinations
        all_tags = ['|'.join([cat1[i], cat2[j], cat3[k]]) for i in range(tags_count) for j in range(tags_count) for k in range(tags_count)]

        # Remove tags that the user has already rated
        user_tags = self.tag_encoder.inverse_transform(user_tags)
        tags_to_predict = list(set(all_tags) - set(user_tags))
        tags_to_predict = self.tag_encoder.fit_transform(tags_to_predict)

        # Generate user-tags pairs for prediction
        user_tag_pairs = [(user_id, tags_ids, 0) for tags_ids in tags_to_predict]

        # Predict ratings for all user-tags pairs
        predictions_cf = self.model_svd.test(user_tag_pairs)

        # Sort predictions by estimated rating in descending order
        top_n_recommendations = sorted(predictions_cf, key=lambda x: x.est, reverse=True)[:n]

        if self.debug:
            print("Top N ratings:", top_n_recommendations)

        # Decode the top tags and retrieve their predicted ratings
        top_tags = [self.tag_encoder.inverse_transform([pred.iid])[0] for pred in top_n_recommendations]
        predicted_ratings = [pred.est for pred in top_n_recommendations]

        return top_tags, predicted_ratings, top_categories
