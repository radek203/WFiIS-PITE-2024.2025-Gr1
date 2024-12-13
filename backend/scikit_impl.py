import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from surprise import Dataset, Reader
from surprise import SVD
from surprise import accuracy


class ScikitImpl:

    def __init__(self, debug=False):
        self.debug = debug
        # Read the ratings data
        ratings_df = pd.read_csv("data/ratings.csv")
        if self.debug:
            # Display all columns in the output
            pd.set_option('display.max_columns', None)
            print(ratings_df)

        # Encode the userId and categoryId columns
        self.user_encoder = LabelEncoder()
        self.category_encoder = LabelEncoder()
        ratings_df['userId'] = self.user_encoder.fit_transform(ratings_df['userId'])
        # ratings_df['categoryId'] = self.category_encoder.fit_transform(ratings_df['categoryId'])
        data_expanded = pd.DataFrame([
            {"userId": row.userId, "tag": tag, "rating": row.rating}
            for _, row in ratings_df.iterrows()
            for tag in row.tags.split('|')
        ])

        # Encode the tags
        self.tag_encoder = LabelEncoder()
        data_expanded['tag'] = self.tag_encoder.fit_transform(data_expanded['tag'])
        self.ratings_df = data_expanded
        # Split the tags column into multiple columns based on the delimiter '|' - It is how the model can understand the tags
        # mlb = MultiLabelBinarizer()
        # self.ratings_df = ratings_df.join(pd.DataFrame(mlb.fit_transform(ratings_df.pop('tags').str.split('|')), columns=mlb.classes_, index=ratings_df.index))
        # Model based on the SVD Singular Value Decomposition algorithm
        self.model_svd = SVD()

    # This function doesn't contain final implementation of choosing categories/tags!
    def get_tags_train_data_set(self):
        # Group data by userId and tag to calculate mean ratings
        data_grouped = self.ratings_df.groupby(['userId', 'tag'], as_index=False).agg(
            rating=('rating', 'mean')
        )
        return data_grouped


    def train(self):
        ratings_tags_df = self.get_tags_train_data_set()
        # 80% training, 20% testing - To learn the model and test it
        # train_df, test_df = train_test_split(self.ratings_df, test_size=0.2)
        train_df, test_df = train_test_split(ratings_tags_df, test_size=0.2)
        # Model must know the range of ratings in the dataset
        reader = Reader(rating_scale=(1, 10))

        # Load only the necessary columns from the training data
        data = Dataset.load_from_df(train_df[['userId', 'tag', 'rating']], reader)

        # Build the training set
        trainset = data.build_full_trainset()

        # Train the model
        self.model_svd.fit(trainset)

        # another model - worse RMSE
        # model_knn = KNNBasic()
        # model_knn.fit(trainset)

        if self.debug:
            # testset to test the model
            testset = [(row['userId'], row['tag'], row['rating']) for _, row in test_df.iterrows()]

            # Predict ratings for the testset
            predictions_test = self.model_svd.test(testset)

            # Calculate RMSE on the test set, the lower the value the better, for 1-10 rating scale, we want RMSE to be less than 1 (1 point of rating)
            accuracy.rmse(predictions_test)


    def get_top_n_ratings(self, user_id, n=10):
        user_id_encoded = self.user_encoder.transform([user_id])[0]

        # Get all unique tags
        all_tags = self.ratings_df['tag'].unique()

        # Generate user-tag pairs for prediction
        user_tag_pairs = [(user_id_encoded, tag_id, 0) for tag_id in all_tags]

        # Predict ratings for all user-tag pairs
        predictions_cf = self.model_svd.test(user_tag_pairs)

        # Sort predictions by estimated rating in descending order
        top_n_recommendations = sorted(predictions_cf, key=lambda x: x.est, reverse=True)[:n]

        if self.debug:
            print("Top N ratings:", top_n_recommendations)

        # Decode the top tags and retrieve their predicted ratings
        top_tags_ids = [self.tag_encoder.inverse_transform([pred.iid])[0] for pred in top_n_recommendations]
        predicted_ratings = [pred.est for pred in top_n_recommendations]

        return top_tags_ids, predicted_ratings
